from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import AgentAction, AgentFinish
from langchain.callbacks.base import BaseCallbackHandler
from typing import List, Union
import re

class LoggingCallback(BaseCallbackHandler):
    def __init__(self):
        self.log = []

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.log.append(f"--- LLM started ---")

    def on_llm_end(self, response, **kwargs):
        self.log.append(f"--- LLM ended ---")

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.log.append(f"> Tool started with input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        self.log.append(f"> Tool ended with output: {output}")

    def on_agent_action(self, action, **kwargs):
        self.log.append(f"> Agent action: {action.tool} with input: {action.tool_input}")

    def on_agent_finish(self, finish, **kwargs):
        self.log.append(f"> Agent finished with output: {finish.return_values['output']}")

class CausalDiscoveryAgentLLM:
    def __init__(self, client, wiki):
        self.llm = client
        self.wikipedia = wiki
        self.tools = [
            Tool(
                name="Wikipedia",
                func=self.wikipedia.run,
                description="""
                Useful for querying information from Wikipedia.
                Input should be a search query like: variable name
                Don't use quotes or special characters.
                (e.g. "variable name" => variable name)
                If the variable is more than word, use spaces, not underscores.
                (e.g. variable_name_here => variable name here)
                """
            )
        ]

    class CustomPromptTemplate(StringPromptTemplate):
        template: str
        tools: List[Tool]
        
        def format(self, **kwargs) -> str:
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            kwargs["agent_scratchpad"] = thoughts
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
                return AgentAction(tool="Error", tool_input=llm_output, log=llm_output)
            action = match.group(1)
            action_input = match.group(2)
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

    def create_agent(self):
        prompt = self.CustomPromptTemplate(
            template="""Answer the following question as best you can. You ONLY have access to the following tools:

                {tools}

                Use the following format:

                Question: the input question you must answer
                Thought: you should always think about what to do
                Action: the action to take, should be one of {tool_names}
                Action Input: the input to the action
                Observation: the result of the action
                ... (this Thought/Action/Action Input/Observation can repeat N times)
                Thought: I now know the final answer
                Final Answer: the final answer to the original input question
                If a Wikipedia search doesn't provide useful information, you should try searching for individual terms separately.

                Begin!

                Question: {input}
                Thought: To answer this question, I need to research about {var_1} and {var_2}
                and their potential causal relationship in the context of: 
                
                {context}
                
                Let me start by looking up information on Wikipedia.
                {agent_scratchpad}""",
            tools=self.tools,
            input_variables=["input", "var_1", "var_2", "context", "intermediate_steps"]
        )

        llm_chain = LLMChain(llm=self.llm, prompt=prompt)
        tool_names = [tool.name for tool in self.tools]
        agent = LLMSingleActionAgent(
            llm_chain=llm_chain,
            output_parser=self.CustomOutputParser(),
            stop=["\nObservation:"],
            allowed_tools=tool_names
        )
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools, verbose=True)

    def determine_causal_relationship(self, var_1: str, var_2: str, context: str) -> dict:
        '''
        Run the Agent-based LLM to create a causal hypothesis given a context.
        
        var_1 : str
            The first variable's name to be reseaced for a causal relashionship.
        var_2 : str
            The second variable's name to be reseaced for a causal relashionship.
        context : str
            The context of the dataset for the LLM to run causal discovery algorithms and
            understand the variables involved in the dataset.
        '''
        
        agent = self.create_agent()
        input_question = f"""
        Does {var_1} cause {var_2} or the other way around?
        We assume the following definition of causation:
        if we change A, B will also change.
        The relationship does not have to be linear or monotonic.
        We are interested in all types of causal relationships,
        including partial and indirect relationships,
        given that our definition holds.
        If the initial search doesn't provide useful information,
        search for '{var_1}' and '{var_2}' separately.
        Finally, if there us a causal relationship,
        print which variable causes the other variable,
        or print that there is no causal relationship.
        Always give the reasoning behind your answer.
        """

        callback = LoggingCallback()
            
        out = agent.run(input=input_question, var_1=var_1, var_2=var_2, context=context, callbacks=[callback])
            
        pred = self.llm.predict(f'''
        We assume the following definition of causation:
        if we change A, B will also change.
        The relationship does not have to be linear or monotonic.
        We are interested in all types of causal relationships,
        including partial and indirect relationships,
        given that our definition holds.
        
        With the given context:

        {context}
        
        And based on the following information:
        
        {out},
        
        print (0,1) if {var_1} causes {var_2},
        print (1,0) if {var_2} causes {var_1},
        print (0,0) if there is no causal relationship between {var_1} and {var_2}.
        print (-1,-1) if you don't know. Importantly, don't try to
        make up an answer if you don't know.''')
        
        return {
            "agent_output": out,
            "prediction": pred.strip(),
            "full_log": "\n\n".join(callback.log)
        }