import numpy as np
import pandas as pd
from io import StringIO
from nl2sql.services.ai import AIService
from nl2sql.prompts import (
    NLDBSchemaDescriptionPrompt, 
    NLTableSummaryPrompt
)

class NaturalLanguageToSQL:
    """
    A Natural Language schema description for each table and table attributes of the provided database. 
    """
    _nl_db_schema: dict[str, str] = {}

    """
    A short summary description of each table.
    """
    _nl_tables_summary: dict[str, str] = {}


    def __init__(self, ai_service: AIService, dict_path_csv,encoding="utf-8",separator=",",has_header=True,ignore_errors=True):
        self.ai_service = ai_service

        # Importer
        self.data = {table_name: pd.read_csv(dict_path_csv[table_name], sep=separator, encoding=encoding) for table_name in dict_path_csv}

        self.string_columns_df = {table_name: self.data[table_name].select_dtypes(include=['object']) for table_name in dict_path_csv}

        # Indexer / Preprocessing
        self.tables = list(self.data.keys())
        self.sample_data = {table_name: self.get_sample(table_name, 5) for table_name in self.tables}

    # Indexer / Preprocessing
    def get_nl_db_schema(self) -> dict[str, str]:
        if not self._nl_db_schema:
            prompt = NLDBSchemaDescriptionPrompt(self.ai_service)
            self._nl_db_schema = {
                table_name: prompt.run(table_name, self.sample_data.get(table_name)) for table_name in self.tables
            }
        return self._nl_db_schema
    
    # Indexer / Preprocessing
    def get_nl_tables_summary(self) -> dict[str, str]:
        if not self._nl_tables_summary:
            prompt = NLTableSummaryPrompt(self.ai_service)
            for table_name in self.tables:
                self._nl_tables_summary[table_name] = prompt.run(self.get_nl_db_schema()[table_name])
        return self._nl_tables_summary

    # Utils, Data Layer
    def get_table_attributes(self, table_name:str) -> list:
        return list(self.data[table_name].columns.tolist())
    
    # Utils, Data Layer
    def filter_values(self, column: str, value: str):
        return {table_name: df[df[column].str.contains(value, na=False)] for table_name, df in self.data.items()}
    
    # Indexer / Preprocessing
    def get_sample(self, table_name: str, n: int = 5) -> str:
        sample_df = self.data[table_name].sample(n=n, random_state=0)  # Sample n rows with a fixed random state
        output = StringIO()  # Create an in-memory text stream
        sample_df.to_csv(output, index=False)  # Write the DataFrame to the stream without the index
        return output.getvalue()  # Return the CSV content as a string

    # Utils, Data Layer
    def check_all_columns(self, model_reponse:str, table:str) -> list:
        missing = []
        for c in self.data[table].columns:
            c = c.strip()
            if c not in model_reponse:
                missing.append(c)
        return missing
    
    # Caller
    def generate_list_dict(self,prompt:list):
        response = self.ai_service.run(messages=prompt)
    
        return response.choices[0].message.content.strip()

    # Caller
    def generate(self,prompt:str):
        response = self.ai_service.run(messages=[
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
