# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

import re
import os
import json
import numpy as np
import pandas as pd
from io import StringIO
from openai import AzureOpenAI

def read_questions_from_file(question_file_path):
    with open(question_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        questions = re.findall(r"'(.*?)'", content, re.DOTALL)
        
    return questions

class NL2SQLL:
    def __init__(self, dict_path_csv,encoding="latin-1",separator=",",has_header=True,ignore_errors=True):
        
        # self.data = {table_name: pl.read_csv(dict_path_csv[table_name], ignore_errors=ignore_errors, has_header=has_header, separator=separator, encoding=encoding) for table_name in dict_path_csv}
        self.data = {table_name: pd.read_csv(dict_path_csv[table_name], sep=separator, encoding=encoding) for table_name in dict_path_csv}
        self.string_columns_df = {table_name: self.data[table_name].select_dtypes(include=['object']) for table_name in dict_path_csv}

    def get_attributes(self, table_name:str) -> list:
        return list(self.data[table_name].columns.tolist())
    
    def filter_values(self, column: str, value: str):
        return {table_name: df[df[column].str.contains(value, na=False)] for table_name, df in self.data.items()}
    
    def get_sample(self, table_name: str, n: int = 5) -> str:
        sample_df = self.data[table_name].sample(n=n, random_state=0)  # Sample n rows with a fixed random state
        output = StringIO()  # Create an in-memory text stream
        sample_df.to_csv(output, index=False)  # Write the DataFrame to the stream without the index
        return output.getvalue()  # Return the CSV content as a string

    def get_sample_prompt(self, number_of_samples: int) -> list:
        prompts = {}
        for table in self.data:
            prompt = f"""Given the table sample below:

Table name: {table}
{self.get_sample(table,number_of_samples)}

Create a list of with a description of the the table and attribute in the following format:
    Table name; natural language description of the table
    Attribute name; natural language description of the table; attribute type; format; primary key

where:
    Attribute type contains the basic type of the attribute.
    Format contains a description of the value format (e.g. date format, separators, etc).
    Primary key: a boolean true | false in case the attribute is likely to be a primary key.

Important: 
    Must do it for all attributes. Just return the list.
    Do not return the original table sample."""
            prompts[table] = prompt
            
        return prompts

    def check_all_columns(self, model_reponse:str, table:str) -> list:
        missing = []
        for c in self.data[table].columns:
            c = c.strip()
            if c not in model_reponse:
                missing.append(c)
        return missing
    
    def generate_list_dict(self,prompt:list,openai_api_version,deployment_name,openai_api_key,azure_endpoint):
        client = AzureOpenAI(
            api_key=openai_api_key,
            api_version=openai_api_version,
            azure_endpoint=azure_endpoint
        )
    
        response = client.chat.completions.create(model=deployment_name, messages=prompt)
        
        return response.choices[0].message.content.strip()

    def generate(self,prompt:str,openai_api_version,deployment_name,openai_api_key,azure_endpoint):
    
        client = AzureOpenAI(
            api_key=openai_api_key,
            api_version=openai_api_version,
            azure_endpoint=azure_endpoint
        )
    
        response = client.chat.completions.create(model=deployment_name, messages=[
            {"role": "user", "content": prompt},
        ])

        return response.choices[0].message.content.strip()

    def get_prompt_relevant_tables(self, nl_query:str, list_of_tables:str):
        prompt = f"""Select from the list of tables below, the tables which are relevant to answer the following natural language query: {nl_query} 

Instructions:
Just return the list of table names.

List of Tables:
{list_of_tables}
"""
        return prompt
    
    def get_prompt_summary_prompt(self, schema_description:str):
        prompt = f"""Given the schema description below, provide a summary description of the table limited to 3 sentences.
{schema_description}
"""
        return prompt
    
    def get_prompt_correct_sqlquery(self, error:str):
        prompt = f"""Correct this sql query:
{error}

Ouput only the new sql query"""
        return prompt
    
    def get_unique_values(self) -> dict:
        unique_values = {}
        for table_name in self.string_columns_df:
            unique_values[table_name] = {}
            for col in self.string_columns_df[table_name].columns:
                unique_values[table_name][col] = self.string_columns_df[table_name][col].unique()
        return unique_values
    
    def get_prompt_relevant_tables_and_attributes_table_filter(self, nl_query:str, descriptions:dict, tables:str):
        prompt = f"""Select the relevant tables and attributes given the natural language query below. Return only the list of tables and attributes.
{nl_query} 
And the set of tables:
"""
        for table in descriptions:
            if table in tables:
                prompt += f"{descriptions[table]}\n\n"
        return prompt
    
    def get_prompt_get_instances(self, nl_query:str):
        prompt = f"""Given the following natural language query to be mapped to an SQL query:
{nl_query} 
Determine the set of references to values in the table, i.e. terms which are likely to map to VALUES in a WHERE = ‘VALUE’ clause."""
        return prompt
    
    def get_prompt_nl_to_sql(self,nl_query:str,step3:str,step4:str,joins,num_examples:int=3):
        query_plan_context = f"{step3}\n{step4}\n"
        should_add_where = True
        unique_values = self.get_unique_values()
        for table in unique_values:
            # print(f"Keys: {unique_values[table].keys()}")
            for column in unique_values[table]:
                if (table.strip() in step4 or table.strip() in step3) and (column.strip() in step3 or column.strip() in step4):
                    if should_add_where:
                        query_plan_context += "Here are examples of the style of data stored in the database:\n"
                        should_add_where = False
                    # print(unique_values[table][column])
                    # print(','.join(np.random.choice(unique_values[table][column], 2, replace=False)))
                    query_plan_context += f"{table}.{column}: {','.join(np.random.choice(unique_values[table][column], num_examples if len(unique_values[table][column])>=num_examples else len(unique_values[table][column]), replace=False))}\n"
        query_plan_context += f"{joins}\n"
        prompt = f"""Given the natural language query: 
{nl_query}
and the set of relevant tables, attributes, target values and joins in:
{query_plan_context}
Write the corresponding SQL query.
Build the SQL query in a step-wise manner:
    Determine the table and the projection attributes.
    Determine the select statement clauses.
    Determine the joins.
    Define the aggregation operations (if applicable).
Return only the SQL query."""
        return prompt
    

class NL2SQL(
    BaseComponent,
    component_name="NL2SQL",
    component_description="""ConNL2SQL.""",
    input_types={"question_file_path": DataType.TEXT, "dict_path_csv": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.NLP,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT"
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self, question_file_path: str, dict_path_csv: str):

        questions = read_questions_from_file(question_file_path)
        
        with open(dict_path_csv, "r") as f:
            dict_path_csv = json.load(f)

        description = {}
        table_summary = {}
        relevant_table = {}

        for nl_query in questions:
            nl_query = nl_query[0].upper() + nl_query[1:]
            obj = NL2SQLL(dict_path_csv=dict_path_csv)

            for table in dict_path_csv:
                if table not in description:
                    prompt = [
                        {"role": "user", "content": obj.get_sample_prompt(5)[table]},
                    ]
                    description[table] = obj.generate_list_dict(prompt,**self.configuration)
                    missing = obj.check_all_columns(description[table], table)
                    if len(missing):
                        prompt.append({"role": "assistant", "content": description[table]})
                        prompt.append({"role": "user", "content": f"You are missing: {','.join(missing)}\nWrite only about the columns not already described"})

            posible_joins = {}
            posible_joins["table1_table2"] = ""

            for table in dict_path_csv:
                if table not in table_summary:
                    table_summary[f"{table}"] = obj.generate(obj.get_prompt_summary_prompt(description[table]),**self.configuration)

            list_of_tables = ""

            table_items = list(dict_path_csv.items())

            for i in range(0, len(table_items), 20):

                table_batch = table_items[i:i + 20]

                for table_name, table_path in table_batch:
                    list_of_tables += f"Table name: {table_name}\n"
                    list_of_tables += f"Description: {description[table_name]}\n"
                    list_of_tables += f"Attributes: {', '.join(obj.get_attributes(table_name))}\n\n"
                if i not in relevant_table:
                    relevant_table[i] = obj.generate(obj.get_prompt_relevant_tables(nl_query,list_of_tables),**self.configuration)

            step3 = {}
            step3[nl_query] = obj.generate(obj.get_prompt_relevant_tables_and_attributes_table_filter(nl_query = nl_query, descriptions = description, tables="\n".join(list(relevant_table.values()))),**self.configuration)

            step4 = {}
            prompt_chat = [
                {"role": "user", "content": obj.get_prompt_relevant_tables_and_attributes_table_filter(nl_query = nl_query, descriptions = description, tables=step3[nl_query])},
                {"role": "assistant", "content": step3[nl_query]},
                {"role": "user", "content": obj.get_prompt_get_instances(nl_query=nl_query)}
            ]
            step4[nl_query] = obj.generate_list_dict(prompt_chat,**self.configuration)

            step5 = {}
            step5[nl_query] = obj.generate(obj.get_prompt_nl_to_sql(nl_query=nl_query,step3=step3[nl_query],step4=step4[nl_query],joins=posible_joins["table1_table2"]),**self.configuration)
            return step5[nl_query]