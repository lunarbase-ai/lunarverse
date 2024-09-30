import json
import re
import pandas as pd
import matplotlib.pyplot as plt
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from langchain.schema import AgentAction, AgentFinish
from langchain.callbacks.base import BaseCallbackHandler
from typing import List, Union
from .casual_inference_methods import dowhy_causal_inference, dowhy_falsify_dag
from .casual_inference_methods import run_causalpy_ancova, run_casualpy_syntheticcontrol
from .casual_inference_methods import run_casualpy_differenceindifferences, run_casualpy_regressiondiscontinuity 
from .casual_inference_methods import run_causalpy_iv 


class LoggingCallback(BaseCallbackHandler):
    def __init__(self):
        self.log = []

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.log.append(f"--- LLM started ---\n")

    def on_llm_end(self, response, **kwargs):
        return

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.log.append(f"\t> Tool started with input:\n\t\t {input_str}\n")

    def on_tool_end(self, output, **kwargs):
        self.log.append(f"\t> Tool ended with output:\n\t\t {output}\n")

    def on_agent_action(self, action, **kwargs):
        self.log.append(f"\t> Agent action: {action.tool} with input: {action.tool_input}\n")

    def on_agent_finish(self, finish, **kwargs):
        self.log.append(f"\t> Agent finished with output: {finish.return_values['output']}\n")

class CausalInferenceAgentLLM:
    def __init__(self, client, data, bg_knowledge):
        self.llm = client
        self.background_knowledge = bg_knowledge
        self.data = data
        self.dci_res = []
        self.cpy_res = []
        self.tools = [
            Tool(
                name="run_dowhy",
                func=self._dowhy_causal_inference,
                description="""
                Runs DoWhy causal inference and refutations on the data using the current DAG.
                Inputs should be a comma-separated list of:
                    use_current_dag: Whether to use the current DAG as the background knowledge (1 or 0). Might be usefull for comparisons.
                    treatment: The name of the treatment variable.
                    outcome: The name of the outcome variable.
                    effect_modifiers (can be left empty): The effect modifiers for the causal effect [var1,var2,...].
                    target_units (can be left empty): The target units for the causal effect (“ate”, “att”, or “atc”).
                    method (can be left empty): The method to use for estimating the causal effect. Available methods from DoWhy:
                        - 'backdoor.linear_regression'
                            method_params={}
                        - 'backdoor.distance_matching'
                            method_params={'distance_metric':"minkowski", 'p':2}
                        - 'backdoor.propensity_score_stratification'
                            method_params={}
                        - 'backdoor.propensity_score_matching'
                            method_params={}
                        - 'backdoor.propensity_score_weighting'
                            method_params={"weighting_scheme":"ips_weight" or "ips_normalized_weight" or "ips_stabilized_weight"}
                        - 'iv.instrumental_variable'
                            method_params = {'iv_instrument_name': 'Z0'}
                        - 'iv.regression_discontinuity'
                            method_params = { 'rd_variable_name':'Z1',
                                            'rd_threshold_value':0.5,
                                            'rd_bandwidth': 0.15}
                    method_params (could be left empty): The parameters for the chosen method.
                
                Examples: 
                1,treatment_var,outcome_var,[],,backdoor.linear_regression,{}
                0,treatment_var,outcome_var,[eff_var_name],ate,backdoor.distance_matching,{'distance_metric':"minkowski", 'p':2}

                This tool will:
                1. Perform causal inference using DoWhy
                2. Run standard refutation tests
                3. Return the causal effect estimate and refutation results
                """
            ),
            Tool(
                name="dowhy_falsify_DAG",
                func=self._dowhy_falsify_dag,
                description="""
                Uses DoWhy to falsify the current DAG and suggest potential changes.
                No input is required. Use carefully, it is computationally expensive.

                This tool will:
                1. Attempt to falsify the current DAG using DoWhy's methods
                2. Suggest potential changes to improve the DAG based on the falsification results
                3. Return a list of suggested changes and their justifications
                """
            ),
            Tool(
                name="run_ancova",
                func=self._cp_ancova,
                description="""
                This is appropriate when you have a single pre and post intervention measurement
                and have a treament and a control group.
                Input:
                    -   postreatment variable name: the name of the variable after the treatment (post)
                    -   pretreatment variable name: the name of the variable before the treatment (pre)
                    -   group variable name: the name of the variable that distinguishes between groups
                Examples:
                outcome,pre_treatment_outcome,is_treated
                x0,x1,group
                """
            ),
            Tool(
                name="run_synthetic_control",
                func=self._cp_synth_control,
                description="""
                This is appropriate when you have multiple units, one of which is treated.
                You build a synthetic control as a weighted combination of the untreated units.
                Input:
                    -   variable which we want to estimate the causal impact of
                    -   covariates that will be used for the weighted combination [x1,x2,x3...]
                    -   intercept value
                    -   treatment_time: The time when treatment occured, should be in reference to the data index
                Examples:
                UK,[Belgium,Spain,France,Germany,Italy],0,2016 June 24
                Infection,[date,country,num_vacc],2,1800
                
                """
            ),
            Tool(
                name="run_difference_in_differences",
                func=self._cp_diff_in_diff,
                description="""
                This is appropriate when you have pre and post intervention measurement(s)
                and have a treament and a control group.
                Input:
                    -   outcome variable name: resulting measurment variable
                    -   variable that determines if treatment was applied to the entry or not (True or False)
                    -   time variable name
                    -   group variale name: variable that distinguishes between treatment and control group
                Examples:
                glucose_level,on_diet,date,group
                score,attended_summer_classes,day_of_year,is_control
                """
            ),
            Tool(
                name="run_regression_discontinuity",
                func=self._cp_reg_disc,
                description="""
                Regression discontinuity designs are used when treatment is applied to units according to a
                cutoff on a running variable, which is typically not time. By looking for the presence of
                a discontinuity at the precise point of the treatment cutoff then we can make causal claims
                about the potential impact of the treatment.
                Input:
                    -   outcome variable name: resulting measurment variable
                    -   running_variable_name: the variable name for the running variable of interest
                    -   treatment_variable_name: variable that determines if treatment was applied to the entry or not (True or False)
                    -   treatment_threshold: The running variable threshold is the point that separates units into treatment and control groups. Units just above this threshold receive the treatment, while those just below do not.
                    -   bandwidth (infinity as default): the range of data around the threshold (cutoff) that is included in the analysis.
                    -   use_splines (false as default): approximate using splines instead of a line
                    -   num_for_spline (6 as default): How many points to use for the splines
                    -   epsilon (0.001 as default):  A small scalar value which determines how far above and below the treatment threshold to evaluate the causal impact
                Examples:
                mortality,age,is_treated,21,,False,,
                mortality,age,attended_treatment,18,,True,6,0.01
                """
            ),
            Tool(
                name="run_intrumental_variable",
                func=self._cp_iv,
                description="""
                Instrumental Variable regression is an appropriate technique when you wish to estimate the treatment
                effect of some variable on another, but are concerned that the treatment variable is endogenous in the
                system of interest i.e. correlated with the errors. In this case an “instrument” variable can be used in
                a regression context to disentangle treatment effect due to the threat of confounding due to endogeneity.
                The idea is to recover the unbiased treatment effect of X by invoking 
                Z, our instrument, which is assumed to be correlated with Y only through its influence on X. (Z->X->Y)
                Input:
                    -   Outcome variable name
                    -   Treatment variable name
                    -   Instrument variable name
                Examples:
                y,x,z
                diabetes,glucose,diet
                """
            ),
            Tool(
                name="Error",
                func=self._error,
                description="Returns the error message if the input is not valid. Do not run this!"
            )
        ]
            
    def _dowhy_causal_inference(self, input_str:str):
        try:
            params, method_params = input_str.split('{')
            bk, treatment_var, outcome_var, effect_vars, target_units, method, _ = params.split(',')
            method_params = method_params.replace('}', '')
            effect_vars = effect_vars.replace('[', '').replace(']', '').split(',')
            if target_units == '':
                target_units = None
            if method == '':
                method = 'backdoor.linear_regression'
            if method_params == '':
                method_params = None
            else:
                method_params = json.loads("{" + method_params + "}")
            if(bk == '0'):
                graph = None
            else:
                graph = self.background_knowledge
            dci = dowhy_causal_inference(self.data, treatment_var, outcome_var, graph, effect_vars, target_units, method, method_params)
            self.dci_res.append(dci)
            return dci
        except Exception as e:
            return f"Error while running DoWhy: {e}"
    def _dowhy_falsify_dag(self, _):
        dfalsify = dowhy_falsify_dag(self.background_knowledge, self.data)
        self.dci_res.append(f"Falsify DAG results: \n{dfalsify}")
        return dfalsify
    def _cp_ancova(self, input_str):
        try:
            post,pre,group = input_str.split(',')
        except Exception as e:
            return f"Error while parsing the input {e}"
        try:
            ancova_res = run_causalpy_ancova(self.data, post, pre, group)
            complete_res = ancova_res['result']
            summary = ancova_res['summary']
            fig, _ = complete_res.plot()
            plt.title = "Ancova - " + post + " vs " + pre + " by " + group
            # add title
            fig.suptitle(plt.title, fontsize=16)
            plt.savefig("ANCOVA_plot.png")
            plt.close()
            self.cpy_res.append(f"ANCOVA results: \n\t{summary}\n")
            return f"ANCOVA results: \n\t{summary}"
        except Exception as e:
            return f"Error while running ANCOVA: {e}"
    def _cp_synth_control(self, input_str: str):
        try:
            actual,cov_str,intercept,tretment_time = input_str.split(',')
            covariates = cov_str.strip('[]').split(',')
        except Exception as e:
            return f"Error while parsing the input {e}"
        try:
            synth_res = run_casualpy_syntheticcontrol(
                self.data,
                actual,
                intercept,
                tretment_time,
                covariates)
            complete_res = synth_res['result']
            summary = synth_res['summary']
            _, _ = complete_res.plot()
            plt.savefig("SYNTH_plot.png")
            plt.close()
            self.cpy_res.append(f"Synthetic control results: \n\t{summary}\n")
            return f"Synthetic control results: \n\t{summary}"
        except Exception as e:
            return f"Error while running Synthetic control: {e}"
    def _cp_diff_in_diff(self, input_str: str):
        try:
            outcome, treatment, time, group = input_str.split(',')
        except Exception as e:
            return f"Error while parsing the input {e}"
        try:
            diff_res = run_casualpy_differenceindifferences(
                self.data,
                outcome,
                treatment,
                time,
                group
                )
            complete_res = diff_res['result']
            summary = diff_res['summary']
            fig, _ = complete_res.plot()
            plt.title = "Diff in Diffs - " + outcome + " on " + treatment + " by " + group
            # add title
            fig.suptitle(plt.title, fontsize=16)
            plt.savefig("DID_plot.png")
            plt.close()
            self.cpy_res.append(f"Diff in diffs results: \n\t{summary}\n")
            return f"Diff in diffs results: \n\t{summary}"
        except Exception as e:
            return f"Error while running Diff in diffs: {e}"
    def _cp_reg_disc(self, input_str: str):
        try:
            outcome, runn, treatment, threshold, bandwidth, splines, num_splines, epsilon = input_str.split(',')
            ## parse the input
            if bandwidth == '':
                bandwidth = None
            else:
                bandwidth = float(bandwidth)
            if splines == '':
                splines = False
            else:
                splines = bool(splines)
            if num_splines == '':
                num_splines = 6
            else:
                num_splines = int(num_splines)
            if epsilon == '':
                epsilon = 0.001
            else:
                epsilon = float(epsilon)
                
        except Exception as e:
            return f"Error while parsing the input {e}"
        
        try:
            reg_res = run_casualpy_regressiondiscontinuity(
                self.data,
                outcome,
                runn,
                treatment,
                threshold,
                bandwidth,
                splines,
                num_splines,
                epsilon
                )
            complete_res = reg_res['result']
            summary = reg_res['summary']
            fig, _ = complete_res.plot()
            plt.title = "Regression Discontinuity - " + outcome + " with " + runn + " on " + treatment
            # add title
            fig.suptitle(plt.title, fontsize=16)
            plt.savefig("RegDisc_plot.png")
            plt.close()
            self.cpy_res.append(f"Regression Discontinuity results: \n\t{summary}\n")
            return f"Regression Discontinuity results: \n\t{summary}"
        except Exception as e:
            return f"Error while running Regression Discontinuity: {e}"
    def _cp_iv(self, input_str: str):
        try:
            outcome, treatment, instrument = input_str.split(',')
        except Exception as e:
            return f"Error while parsing the input {e}"
        try:
            iv_res = run_causalpy_iv(
                self.data,
                outcome,
                treatment,
                instrument
                )
            complete_res = iv_res['result']
            summary = iv_res['summary']
            fig, _ = complete_res.plot()
            plt.title = "Instrumental Variables - " + outcome + " with " + treatment + " and " + instrument
            # add title
            fig.suptitle(plt.title, fontsize=16)
            plt.savefig("IV_plot.png")
            plt.close()
            self.cpy_res.append(f"Instrumental Variables results: \n\t{summary}\n")
            return f"Instrumental Variables results: \n\t{summary}"
        except Exception as e:
            return f"Error while running Instrumental Variables: {e}"
    def _error(self, input_error: str) -> str:
        return "Parsing error - No Action was taken (no tool) \n\t\t" + input_error
    class CustomPromptTemplate(StringPromptTemplate):
        template: str
        tools: List[Tool]
        data: pd.DataFrame
        background_knowledge: dict
        
        def format(self, **kwargs) -> str:
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            kwargs["agent_scratchpad"] = thoughts
            kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
            kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
            kwargs["data_columns"] = ", ".join(self.data.columns)
            kwargs["data_shape"] = str(self.data.shape)
            kwargs["data_head"] = str(self.data.head())
            kwargs["background_knowledge"] = str(self.background_knowledge['links'])
            return self.template.format(**kwargs)

    class CustomOutputParser(AgentOutputParser):
        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                    log=llm_output,
                )
                
            regex = r"Action: (\w+)\nAction Input: (.*)"
            match = re.search(regex, llm_output, re.DOTALL)
            if not match:
                if "final answer" in llm_output:
                    return AgentFinish(
                        return_values={"output": llm_output.split("final answer")[-1].strip()},
                        log=llm_output,
                    )
                return AgentAction(tool="Error", tool_input=llm_output, log=llm_output)
            action = match.group(1)
            action_input = match.group(2)
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

    def create_agent(self):
        prompt = self.CustomPromptTemplate(
            template="""
                - Answer the following question as best you can. You only have access to the following tools:

                {tools}
                
                - The context is:
                
                {context}
                
                - Some information about the dataset:

                Columns: {data_columns}
                Shape: {data_shape}
                Head: {data_head}
                
                - Graph: 
                The causal relationships between the nodes with weights, where:
                weight = -1 : There is no direct relationship from Source to Target
                weight = 1 : There is a direct relationship from Source to Target
                no link for A to B: There was no background to support a causal relationship between the two nodes, but latent variables may exist.
                
                This is the causal graph links:
                {background_knowledge}
                
                - Use the following format:

                Question: the input question you must answer
                Thought: you should always think about what to do
                Action: the action to take, should be one of {tool_names}
                Action Input: the input to the action (if none, input None (e.g. Action Input: None))
                Observation: the result of the action
                ... (this Thought/Action/Action Input/Observation can repeat N times)
                Thought: I now know the final answer
                Final Answer: the final answer to the original input question with all the information needed.
                
                Begin!
                
                Question: {input}
                Thought: To answer this question, I need to run some causal discovery methods.
                I will run one of the tools to find some insights about the dataset.
                {agent_scratchpad}""",
            tools=self.tools,
            data=self.data,
            background_knowledge=self.background_knowledge,
            input_variables=["input", "context", "intermediate_steps"]
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        tool_names = [tool.name for tool in self.tools]
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=self.CustomOutputParser(),
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools, verbose=True, max_iterations=25, max_execution_time=5000, early_stopping_method='generate')

    def determine_causal_inference(self, context: str) -> dict:
        agent = self.create_agent()
        input_question = f"""
            Can you run DoWhy and CausalPy to test for causality given the context and give an interpretation of the results?
            
            Make sure to run the tools with the best methods and parameters while giving a step-by-step reasoning.
            After the results are analyzed, please make sure to re run the tests with different parameters if needed.
            
            Output the results with some insights on causality of the variables and the effects and give an interpretation
            alongside possible enhancements to create a better model. 
            
            Be exhaustive and thorough in you analysis and interpretation of the results.
            
            If some needed parameters are not given, please infer them, such as treatment and outcome.
        """

        callback = LoggingCallback()
            
        out = agent.run(input=input_question, context=context, callbacks=[callback])
        
        return {
            "agent_output": out,
            "dowhy": self.dci_res,
            "causalpy": self.cpy_res,
            "full_log": "".join(callback.log)
        }
