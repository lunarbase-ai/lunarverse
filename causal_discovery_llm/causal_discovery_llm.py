import json
import networkx as nx
import re
import pandas as pd
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from langchain.schema import AgentAction, AgentFinish
from langchain.callbacks.base import BaseCallbackHandler
from scipy import stats
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tsa.stattools import adfuller
from typing import List, Union
from .casual_discovery_methods import pc_algorithm, fci_algorithm
from .casual_discovery_methods import lingam_algorithm, granger_algorithm, grasp_algorithm
from .casual_discovery_methods import pnl_algorithm, gin_algorithm, ges_algorithm

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

class CausalDiscoveryAgentLLM:
    def __init__(self, client, data, bg_knowledge):
        self.llm = client
        self.background_knowledge = bg_knowledge
        self.data = data
        self.tools = [
            Tool(
                name="Run_PC_Algorithm",
                func=self._pc_algorithm,
                description="""
                Runs the PC algorithm to discover causal relations between variables in the data.
                The only optional input needed is the value of the alpha (default to 0.05).
                
                Inputs:
                    use_current_dag: Whether to use the current DAG as the background knowledge (1 or 0). Might be usefull for comparisons.
                    alpha: The significance level of the test.
                
                Examples:
                1,0.05
                0,0.05
                
                When it can be useful: 
                - For both tabular and time series data, of both continuous and discrete types.
                - When you assume no latent confounders and no cyclic causal relationships.
                - For relatively small to medium-sized datasets with many variables.
                - When you want to obtain a causal graph that represents conditional independence relationships.
                """
            ),
            Tool(
                name="Run_FCI_Algorithm",
                func=self._fci_algorithm,
                description="""
                Runs the FCI algorithm to discover causal relations between variables in the data.
                The only optional input needed is the value of the alpha (default to 0.05).
                Inputs:
                    use_current_dag: Whether to use the current DAG as the background knowledge (1 or 0). Might be usefull for comparisons.
                    alpha: The significance level of the test.
                
                Examples:
                1,0.05
                0,0.05
                
                When it can be useful:
                - When you suspect there might be latent confounders in your data.
                - For both continuous and discrete data.
                - When you want to distinguish between direct causal relationships and relationships due to latent common causes.
                - When you need to handle selection bias in your data.
                - For datasets where PC algorithm might produce misleading results due to hidden variables.
                """
            ),
            Tool(
                name="Run_Lingam_Algorithm",
                func=self._lingam_algorithm,
                description="""
                Runs the LiNGAM (Linear Non-Gaussian Acyclic Model) algorithm to discover causal relations between variables in the data.
                The only optional input needed is the value of the alpha (default to 0.05).
                
                Inputs:
                    use_current_dag: Whether to use the current DAG as the background knowledge (1 or 0). Might be usefull for comparisons.
                    alpha: The significance level of the test.
                    measure: Measure must be "pwling" or "kernel"
                
                Examples:
                1,0.05,pwling
                0,0.05,kernel
                
                When it can be useful:
                - For continuous data that follows non-Gaussian distributions.
                - When you assume linear causal relationships between variables.
                - When you want to determine the causal ordering of variables.
                - In scenarios where methods based on conditional independence tests (like PC) might not be able to determine the direction of causal links.
                - For datasets where you suspect the noise terms are non-Gaussian.
                """
            ),
            Tool(
                name="Run_Granger_Algorithm",
                func=self._granger_algorithm,
                description="""
                Runs the Granger Causality algorithm to discover causal relations between variables in the data.
                The required inputs are the value of alpha and the maximum lag, separated by a comma (e.g., 0.05,3).
                
                Inputs:
                    use_current_dag: Whether to use(1) or not(0) the current DAG as the background knowledge (1 or 0). Might be usefull for comparisons.
                    alpha: The significance level of the test.
                    max_lag: The maximum lag to consider.
                
                Examples:
                1,0.05,2
                0,0.05,1
                
                When it can be useful:
                - Specifically designed for time series data.
                - When you want to test if one time series is useful in forecasting another.
                - When you're interested in lagged causal relationships.
                - For exploring short-term causal effects in temporal data.
                """
            ),
            Tool(
                name="Run_PNL_Algorithm",
                func=self._pnl_algorithm,
                description="""
                Runs the Post-Nonlinear (PNL) Causal Model algorithm to discover causal relations between two variables in the data.
                The required inputs are the names of two variables to be tested, separated by a comma (e.g., x1,x2).
                Only use when it is really needed since it is computationally expensive.
                
                Inputs:
                    x1: The name of the first variable.
                    x2: The name of the second variable.
                
                Examples:
                var_1,var_2
                var_5,var_9
                
                When it can be useful:
                - For pairs of continuous variables where you suspect non-linear causal relationships.
                - When you want to determine the causal direction between two variables.
                - In scenarios where linear methods might fail due to non-linear relationships.
                - When dealing with complex systems where cause-effect relationships might not be linear.
                - For exploratory analysis of potential causal links in complex datasets.
                """
            ),
            Tool(
                name="Run_GIN_Algorithm",
                func=self._gin_algorithm,
                description="""
                Learning causal structure of Latent Variables for Linear Non-Gaussian Latent Variable Model with Generalized Independent Noise Condition Parameters.
                No Inputs needed.
                
                Usefull when the observed variables may not be the underlying causal variables, but are generated by latent causal
                variables or confounders that are causally related. GIN implies that causally earlier latent common causes of variables in
                'Y' d-separate 'Y' from 'Z'. the independent noise condition, i.e., if there is no confounder, causes are independent from the error of regressing
                the effect on the causes, can be seen as a special case of GIN.
                """
            ),
            Tool(
                name="Run_GES_Algorithm",
                func=self._ges_algorithm,
                description="""
                Greedy Equivalence Search (GES) is a causal discovery algorithm that uses a greedy search strategy to find the best causal structure.
                Input:
                    score function to use: ['local_score_CV_general', 'local_score_marginal_general', 'local_score_CV_multi', 'local_score_marginal_multi', 'local_score_BIC', 'local_score_BDeu']:
                Example:
                local_score_CV_general
                local_score_BIC
                
                When it can be useful:
                GES is particularly useful when you have a large number of variables and are willing to assume causal sufficiency. It can often produce
                more accurate results than constraint-based methods when these assumptions hold, especially with larger sample sizes.
                """
                ),
            Tool(
                name="Run_GRaSP_Algorithm",
                func=self._grasp_algorithm,
                description="""
                GRASP is a causal discovery algorithm that uses a greedy search strategy to find the best causal structure.
                Input:
                    score function to use: ['local_score_CV_general', 'local_score_marginal_general', 'local_score_CV_multi', 'local_score_marginal_multi', 'local_score_BIC', 'local_score_BDeu']:
                Example:
                local_score_CV_general
                local_score_BIC
                
                When it can be useful:
                GRASP is particularly useful when you have a large number of variables and are willing to assume causal sufficiency. It can often produce
                more accurate results than constraint-based methods when these assumptions hold, especially with larger sample sizes.
                """
                ),
            Tool(
                name="Update_DAG",
                func=self._update_dag,
                description="""
                Updates the current DAG based on suggested changes.
                Input should be a list of changes in the format: add_edge,node1,node2 or remove_edge,node1,node2
                Multiple changes can be specified, separated by semicolons.
                If a node is not in the current DAG, it will be added (new latent variables) like: add_edge,latentN,nodeX
                Example input:
                add_edge,X,Y;remove_edge,A,B;add_edge,F,G

                This tool will:
                1. Apply the specified changes to the current DAG
                2. Return the updated DAG in node-link format
                
                This is the only tool that can be used to modify the DAG!
                If new links are found, use this tool to update the DAG before finishing the causal discovery process.
                """
            ),
            Tool(
                name="Calculate_Data_Properties",
                func=self._calculate_properties,
                description="""
                Calculates key statistical properties of the data that are relevant for choosing a causal discovery method.
                
                Input should be a comma-separated list of variable names to analyze (with NO spaces after the commas). If left empty, all variables will be analyzed.
                
                Example input: X1,X2,X3,X4
                Or leave empty for all variables
                
                This tool will return:
                1. Shapiro-Wilk test for normality (for each variable)
                2. Pearson correlation coefficient matrix (for linearity between variables)
                3. Durbin-Watson statistic (for autocorrelation, useful for time series)
                4. Augmented Dickey-Fuller test (for stationarity in time series)
                5. First to fourth moments (for mean, variance, skewness, and kurtosis)
                These properties can help in deciding which causal discovery method is most appropriate for the data.
                """
            ),
            Tool(
                name="See_Current_DAG",
                func=self._see_current_dag,
                description="""
                Returns the current DAG in node-link format.
                """
            ),
            Tool(
                name="Error",
                func=self._error,
                description="Returns the error message if the input is not valid. Do not run this!"
            )
        ]
    ############################# 
    # Adapters for the tools
    def _pc_algorithm(self, input_str):
        try: 
            bk, alpha = input_str.split(',')
            return pc_algorithm(self.data, float(alpha), self._get_background_knowledge(bk))
        except Exception as e:
            try:
                return "PC was run with the current DAG and alpha=0.05 \n\n" + pc_algorithm(self.data, float(0.05), self._get_background_knowledge('1'))
            except Exception as e:
                return f"Error while running PC: {e}"
    def _fci_algorithm(self, input_str):
        try: 
            bk, alpha = input_str.split(',')
            return fci_algorithm(self.data, float(alpha), self._get_background_knowledge(bk))
        except Exception as e:
            return f"Error while running FCI: {e}"
    def _lingam_algorithm(self, input_str: str):
        try:
            bk, alpha, measure = input_str.split(',')
            return lingam_algorithm(
                data=self.data,
                alpha=float(alpha),
                measure=measure.strip(),
                background_knowledge=self._get_background_knowledge(bk))
        except Exception as e:
            return f"Error while running LiNGAM: {e}"
    def _granger_algorithm(self, input_str):
        try:
            bk, alpha, max_lag = input_str.split(',')
            return granger_algorithm(self.data, int(max_lag), float(alpha), self._get_background_knowledge(bk))
        except Exception as e:
            return f"Error while running Granger Causality: {e}"
    def _pnl_algorithm(self, input_str: str):
        try:
            x1, x2 = input_str.split(',')
            return pnl_algorithm(self.data, x1.strip(), x2.strip())
        except Exception as e:
            return f"Error while running PNL: {e}"
    def _gin_algorithm(self, _):
        try:
            return gin_algorithm(self.data)
        except Exception as e:
            return f"Error while running GIN: {e}"
        
    def _ges_algorithm(self, input_str: str):
        try:
            sf = input_str.strip()
            if  sf == '' or sf not in ['local_score_CV_general', 'local_score_marginal_general', 'local_score_CV_multi', 'local_score_marginal_multi', 'local_score_BIC', 'local_score_BDeu']:
                sf = 'local_score_BIC'
            return ges_algorithm(self.data, sf)
        except Exception as e:
            return f"Error while running GES: {e}"
    
    def _grasp_algorithm(self, input_str: str):
        try:
            sf = input_str.strip()
            if  sf == '' or sf not in ['local_score_CV_general', 'local_score_marginal_general', 'local_score_CV_multi', 'local_score_marginal_multi', 'local_score_BIC', 'local_score_BDeu']:
                sf = 'local_score_BIC'
            return grasp_algorithm(self.data, sf)
        except Exception as e:
            return f"Error while running GRASP: {e}"
    
    ############################# 
    # Other tools are implemented here        
    def _update_dag(self, input_str):
        try:
            changes: str = input_str.split(';')
            G: nx.Graph = nx.node_link_graph(self.background_knowledge)
            for change in changes:
                action, node1, node2 = change.split(',')
                if action == 'add_edge':
                    G.add_edge(node1.strip(), node2.strip(), weight=1)
                elif action == 'remove_edge':
                    G.add_edge(node1.strip(), node2.strip(), weight=-1)
            self.background_knowledge = nx.node_link_data(G)
            return json.dumps(self.background_knowledge)
        except Exception as e:
            return f"Error while updating DAG: {e}"
    def _see_current_dag(self, _):
        return json.dumps(self.background_knowledge)
    def _calculate_properties(self, input_str):
        data: pd.DataFrame
        if input_str.strip():
            try:
                variables = input_str.split(',')
                data = self.data[variables]
            except Exception as e:
                data = self.data
        else:
            data = self.data
        
        results = "Data Properties:\n\n"
        
        # 1. Shapiro-Wilk test for normality
        results += "1. Shapiro-Wilk Test for Normality:\n"
        results += "Where a statistic closer to 1 indicates a normal distribution.\n"
        results += "Where a p-value less than 0.05 indicates a non-Gaussian distribution.\n\n"
        for column in data.columns:
            try: 
                stat, p = stats.shapiro(data[column])
                results += f"{column}: statistic={stat:.4f}, p-value={p:.4f}\n"
            except Exception as e:
                results += f"{column}: {e}\n"
        
        # 2. Pearson correlation coefficient matrix
        results += "\n2. Pearson Correlation Coefficient Matrix:\n"
        results += "Where a value closer to 1 indicates a strong positive correlation\n"
        results += "and a value closer to -1 indicates a strong negative correlation.\n"
        try: 
            pd.set_option('display.max_colwidth', None)
            corr_matrix = data.corr()
            results += corr_matrix.to_string() + "\n"
        except Exception as e:
            results += f"{e}\n"
        
        # 3. Durbin-Watson statistic
        results += "\n3. Durbin-Watson Statistic (for each variable):\n"
        results += "Where a value closer to 2 indicates no autocorrelation.\n"
        results += "Where a value closer to 0 indicates positive autocorrelation.\n"
        results += "Where a value closer to 4 indicates negative autocorrelation.\n\n"
        for column in data.columns:
            try:
                dw = durbin_watson(data[column])
                results += f"{column}: {dw:.4f}\n"
            except Exception as e:
                results += f"{column}: {e}\n"
        
        # 4. Augmented Dickey-Fuller test
        results += "\n4. Augmented Dickey-Fuller Test (for each variable):\n"
        results += "Where a p-value less than 0.05 indicates a stationary time series.\n\n"
        for column in data.columns:
            try:
                adf = adfuller(data[column])
                results += f"{column}: ADF Statistic: {adf[0]:.4f}, p-value: {adf[1]:.4f}\n"
            except Exception as e:
                results += f"{column}: {e}\n"
                
        # 5. Mean, Variance, Skewness, and Kurtosis
        results += "\n5. Mean, Variance, Skewness, and Kurtosis:\n"
        for column in data.columns:
            try:
                mean = data[column].mean()
                variance = data[column].var()
                skewness = data[column].skew()
                kurtosis = data[column].kurt()
                results += f"{column}: Mean: {mean:.4f}, Variance: {variance:.4f}, Skewness: {skewness:.4f}, Kurtosis: {kurtosis:.4f}\n"
            except Exception as e:
                results += f"{column}: {e}\n"
        
        return results
    
    def _get_background_knowledge(self, use_current_bk: str):
        # To be used as an utility (NOT A TOOL!)
        if(use_current_bk == '0'):
            return None
        else:
            return self.background_knowledge
    def _error(self, input_error: str) -> str:
        return "Parsing error - No Action was taken (no tool) \n\t\t" + input_error
    
    ################################
    ################################
    
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
            kwargs["background_knowledge"] = str(self.background_knowledge)
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

    # Main functions
    
    def create_agent(self):
        prompt = self.CustomPromptTemplate(
            template="""
                Answer the following Question as best as you can. You only have access to the following tools:

                {tools}
                
                The context is:
                
                {context}
                
                Some information about the dataset:

                Columns: {data_columns}
                Shape: {data_shape}
                Head: 
                
                {data_head}
                
                Background Knowledge: 
                
                {background_knowledge}    
                           
                Follow to the following format:

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

    def determine_causal_relationship(self, context: str) -> dict:
        '''
        Run the Agent-based LLM to run causal discovery methods given a context.
        
        context : str
            The context of the dataset for the LLM to run causal discovery algorithms and
            understand the variables involved in the dataset.
        '''
        agent = self.create_agent()
        input_question = f"""
            Can you update the causal graph and find extra causal relationships in the data?
            Your job is to analyze the causal relationships in the dataset to find causal relationships
            using systematic causal inference (tools) to update the causal graph.
            If, given the results, new links between variables are identified, UPDATE the current causal graph.
            The links' weights from the initial causal graph are to be interpreted as follows:
                weight = -1 : There is no direct relationship from Source to Target
                weight > 0 : There is a direct relationship from Source to Target
                no link for A to B: There was no background to support a causal relationship between the two nodes, but latent variables may exist.
                
            Please give an exhaustive interpretation of the causal relationships found in the data given the systematic causal inference results and the final causal graph.
        """

        callback = LoggingCallback()
            
        out = agent.run(input=input_question, context=context, callbacks=[callback])
        
        pred = self.llm.predict(f'''
            > Based on:
            Causal Inference Analysis (systematic approach):
            
            {out}
            
            Some information about the dataset:

            Columns: {", ".join(self.data.columns)}
            
            Head: {self.data.head().to_string()}
            
            Causal Graph: {str(self.background_knowledge)}

            > Construct a Structural Equation Model (SEM) that represents the causal relationships found in the data.
            Follow these guidelines:
            1. Use the syntax compatible with SemoPy.
            2. Include all relevant variables identified in the causal discovery process, with the variable names.
            3. Specify the structural model, measurement model, and residual correlations.
            4. Provide a brief explanation for each latent variable.
            
            Latent variables are variables thought to exist but which can't be directly observed.
            These variables are not given, and you can infer them from the data and analisis.
            If you create a latent variable, please try to give a name to it (such as 'Intelligence' or 'Happiness' or just 'eta1' or 'eta2'...).
            Measurement models are for new latent variables (NOT FOR THE ONES ALREADY IN THE GRAPH).
            
            Format the SEM model description that can be directly used with SemoPy.
            Use the following structure as an EXAMPLE for your output:

            {{
            "model_spec": """
                # structural part (EXAMPLES)
                ## the structural part links latent variables to each other via a system of linear equations
                ## The left side of the operator contains an observed or latent variable,
                ## and the right side contains the predictors separated by plus signs.
                ## if x1 -> x2 and x3 -> x2, then x2 ~ x1 + x3
                eta1 ~ observed_variable1_name + observed_variable4_name + ...
                observed_variable7_name ~ eta1 + observed_variable2_name + ...
                eta2 ~ eta1
                
                # measurement model (EXAMPLES)
                ## the measurement part specifies linear influences of latent variables (unobserved) to observed variables
                ## The left side of the operator contains one LATENT VARIABLE, and the right
                ## contains its manifest variables separated by plus signs.
                ## No observed variable can be on the left side of the operator.
                ## e.g. this is NOT ALLOWED: observed_variable1_name =~ observed_variable1_name
                eta1 =~ observed_variable1_name + observed_variable2_name + observed_variable3_name
                eta2 =~ observed_variable4_name + observed_variable5_name + observed_variable6_name
                # ...
                
                # residual correlations (EXAMPLES)
                observed_variable1_name ~~ observed_variable4_name
                observed_variable2_name ~~ observed_variable5_name + observed_variable6_name
                # ...
                
                
            """,
                "latent_descriptions": {{
                    "latent1": "(EXAMPLE) Description of latent1",
                    "latent2": "(EXAMPLE) Description of latent2",
                    # ... include all other latent variables ...
                }}
            }}

            Ensure that the model accurately represents the findings from the causal analysis and DAG.
    ''')
        
        return {
            "agent_output": out,
            "sem_dict": pred.strip(),
            "graph": self.background_knowledge,
            "full_log": "".join(callback.log)
        }
