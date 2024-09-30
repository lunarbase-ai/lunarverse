from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from langchain.schema import AgentAction, AgentFinish
from langchain.callbacks.base import BaseCallbackHandler
from typing import List, Union
from semopy import Model, calc_stats
import pandas as pd
import re

class LoggingCallback(BaseCallbackHandler):
    def __init__(self):
        self.log = []

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.log.append(f"--- LLM started with: ---")
        self.log.append(f"Prompts: {prompts}")
        self.log.append(f"-------------------")

    def on_llm_end(self, response, **kwargs):
        self.log.append(f"--- LLM responded: ---")
        self.log.append(f"Response: {response}")
        self.log.append(f"-------------------")
        self.log.append(f"Actions taken: ")

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.log.append(f"> Tool started with input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        self.log.append(f"> Tool ended with output: {output}")

    def on_agent_action(self, action, **kwargs):
        self.log.append(f"> Agent action: {action.tool} with input: {action.tool_input}")

    def on_agent_finish(self, finish, **kwargs):
        self.log.append(f"> Agent finished with output: {finish.return_values['output']}")
        
###################################################################################
###################################################################################

class SEMEnvironment:
    def __init__(self, initial_model: str, data: pd.DataFrame):
        self.current_model = initial_model
        self.rollback_model = initial_model
        self.data = data
        self.fitted_model = None
        self.fit_model()

    def add_latent_variable(self, latent_var: str, indicators: List[str]) -> str:
        new_lines = [f"{latent_var} =~ {' + '.join(indicators)}"]
        self.rollback_model = self.current_model
        self.current_model = self.current_model + "\n" + "# measurement model\n".join(new_lines)
        return f"Added latent variable {latent_var} with indicators {', '.join(indicators)}"

    def add_covariance(self, var1: str, var2: str) -> str:
        new_line = f"{var1} ~~ {var2}"
        self.rollback_model = self.current_model
        self.current_model = self.current_model + "\n"+ "# new covariance\n" + new_line
        return f"Added covariance between {var1} and {var2}"

    def fit_model(self, obj='MLW', solver='SLSQP') -> str:
        try:
            mod = Model(description=self.current_model)
            mod.fit(self.data, obj=obj, solver=solver)
            self.fitted_model = mod
            res_df : pd.DataFrame = mod.inspect()
            return 'Model fitted successfully. \n'
        except Exception as e:
            self.current_model = self.rollback_model
            return f"Error fitting model: {str(e)}\n Rolling back to previous model:\n {self.rollback_model}"

    def get_model(self) -> str:
        return self.current_model
    
    def get_metrics(self) -> str:
        if (self.fitted_model == None): return "Error, the SEM has not been fitted"
        try:
            return calc_stats(self.fitted_model).to_string()
        except Exception as e:
            return f"Error while getting the stats: {str(e)}"
        
###################################################################################
###################################################################################

class SEMAgentLLM:
    def __init__(self, client, sem_env):
        self.llm = client
        self.sem_env : SEMEnvironment = sem_env
        self.tools = [
            Tool(
                name="AddLatentVariable",
                func=self._add_latent_variable,
                description="""
                Adds a latent variable to the SEM model with as many indicators as needed.
                Input should be: latent_var_name,indicator1_name,indicator2_name,indicator3_name
                """
            ),
            Tool(
                name="AddCovariance",
                func=self._add_covariance,
                description="""
                Adds a covariance between two variables in the SEM model. Input should be: var1,var2
                """
            ),
            Tool(
                name="FitModel",
                func=self._fit_model,
                description="Fits the current SEM model and returns the results. No input needed"
            ),
            Tool(
                name="GetCurrentModel",
                func=self._get_current_model,
                description="Returns the current SEM model specification string. No input needed"
            ),
            Tool(
                name="GetStatistics",
                func=self._get_current_stats,
                description="Returns the DataFrame of the statistics of the SEM model as a console friendly string. No input needed"
            ),
            Tool(
                name="RollbackModel",
                func=self._rollback_model,
                description="Rolls back the current SEM model to the previous model. No input needed"
            ),
            Tool(
                name="Error",
                func=self._error,
                description="Returns the error message if the input is not valid. Do not run this!"
            )
        ]
    def _rollback_model(self, _: str) -> str:
        self.sem_env.current_model = self.sem_env.rollback_model
        return "Model rolled back to: \n" + self.sem_env.current_model
    def _error(self, input_error: str) -> str:
        return "No Action taken \n" + input_error
    def _add_latent_variable(self, input_str: str) -> str:
        latent_var, *indicators = input_str.split(',')
        return self.sem_env.add_latent_variable(latent_var.strip(), indicators)

    def _add_covariance(self, input_str: str) -> str:
        var1, var2 = input_str.split(',')
        return self.sem_env.add_covariance(var1.strip(), var2.strip())

    def _fit_model(self, _: str) -> str:
        return self.sem_env.fit_model()

    def _get_current_model(self, _: str) -> str:
        return self.sem_env.get_model()
    def _get_current_stats(self, _: str) -> str:
        return self.sem_env.get_metrics()

    class CustomPromptTemplate(StringPromptTemplate):
        template: str
        tools: List[Tool]
        sem_env: SEMEnvironment
        
        def format(self, **kwargs) -> str:
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            kwargs["agent_scratchpad"] = thoughts
            kwargs["data_columns"] = ", ".join(self.sem_env.data.columns)
            kwargs["data_shape"] = str(self.sem_env.data.shape)
            kwargs["data_head"] = str(self.sem_env.data.head().to_string())
            kwargs["current_model"] = str(self.sem_env.current_model)
            kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
            kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
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
                regex = r"Action: (\w+)"
                match = re.search(regex, llm_output, re.DOTALL)
                if not match:
                    return AgentAction(tool="Error", tool_input="", log=llm_output)
                action = match.group(1)
                return AgentAction(tool=action, tool_input='', log=llm_output)
                
            action = match.group(1)
            action_input = match.group(2)
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

    def _create_agent(self):
        prompt = self.CustomPromptTemplate(
            template="""You are an AI assistant tasked with improving a Structural Equation Model (SEM).
            Your goal is to refine the model based on theoretical knowledge and model fit results
            After every model change, get the new model statistics, compare AIC and BIC metrics to determine if the model is improving.
            Never return a final answer without first checking if the model is improving. (rollback model if not improving)
            You have access to the following tools:

            {tools}
            
            Some information about the dataset:

                Columns: {data_columns}
                Shape: {data_shape}
                Head: {data_head}
                
            Current Model:
            {current_model}
            
            Use the following format for correct parsing and processing:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of {tool_names}
            Action Input: the input to the action (needed even if left empty)
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question
            
            Begin!

            Question: {input}
            Thought: Let's start by examining the current model and then decide on improvements.
            {agent_scratchpad}
            """,
            sem_env=self.sem_env,
            tools=self.tools,
            input_variables=["input", "intermediate_steps"]
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        tool_names = [tool.name for tool in self.tools]
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=self.CustomOutputParser(),
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools, verbose=True, max_iterations=30, max_execution_time=2000)

    def improve_sem_model(self, context) -> dict:
        agent = self._create_agent()
        input_question = """
        Can you enhance the current SEM model to enhance its metrics? Please provide a detailed explanation of the changes made and the reasoning behind them;
        Include why the model has or hasn't been improved by comparing current and previous metrics (such as CFI, p-values, AIC, BIC...).
        - Analyze the current SEM (Run get statistics) and suggest improvements.
        - Consider adding latent variables if there are multiple indicators measuring a single construct,
        or adding covariances between error terms or exogenous variables if theoretically justified.
        - After each modification, fit the model, calculate the metrics, and compare them to the previous model.
        - Revert changes if the current model is worst or if it seems off.
        - Don't stop until the model metrics are optimal.
        Context: {context}
        """

        callback = LoggingCallback()
            
        out = agent.run(input=input_question, callbacks=[callback])
        
        final_model = self._get_current_model("")
        final_stats = self._get_current_stats("")
        
        pred = self.llm.predict(f'''
            Based on the following information:
            {out}
            
            SEM model:
            {self._get_current_model("")}
            
            Stats:
            {self._get_current_stats("")}
            
            Give me an interpretation of the SEM results with insights on
            how can an intervention be planned given the following context:
            {context}
            ''')
            
        
        return {
            "agent_output": out,
            "interpretation": pred,
            "final_model": final_model,
            "metrics": final_stats,
            "full_log": "\n\n".join(callback.log) + "\nFittend Model:\n" + self.sem_env.fitted_model.inspect().to_string() + "\nFinal Interpretation:\n" + pred
        }

