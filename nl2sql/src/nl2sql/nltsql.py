import numpy as np
import pandas as pd
from io import StringIO
from nl2sql.services.ai import AIService
from nl2sql.prompts import (
    NLDBSchemaDescriptionPrompt, 
    NLTableSummaryPrompt,
    RetrieveRelevantTablesPrompt,
    RetrieveRelevantTableAttributesPrompt,
    RetrieveReferenceValuesPrompt,
    GenerateSQLQueryPrompt
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

    """
    List of table names.
    """
    table_names: list[str] = []

    """
    Sample data for each table.
    """
    sample_data: dict[str, pd.DataFrame] = {}

    """
    Imported data for each table.
    """
    data: dict[str, pd.DataFrame] = {}

    """
    String columns for each table.
    """
    string_columns_df: dict[str, pd.DataFrame] = {}


    def __init__(self, ai_service: AIService, dict_path_csv,encoding="utf-8",separator=",",has_header=True,ignore_errors=True):
        self.ai_service = ai_service

        # Importer
        self.data = {table_name: pd.read_csv(dict_path_csv[table_name], sep=separator, encoding=encoding) for table_name in dict_path_csv}

        self.string_columns_df = {table_name: self.data[table_name].select_dtypes(include=['object']) for table_name in dict_path_csv}

        # Indexer / Preprocessing
        self.table_names = list(self.data.keys())
        self.sample_data = {table_name: self.get_sample(table_name, 5) for table_name in self.table_names}

    # Indexer / Preprocessing
    def get_nl_db_schema(self) -> dict[str, str]:
        if not self._nl_db_schema:
            prompt = NLDBSchemaDescriptionPrompt(self.ai_service)
            self._nl_db_schema = {
                table_name: prompt.run(table_name, self.sample_data.get(table_name)) for table_name in self.table_names
            }
        return self._nl_db_schema
    
    # Indexer / Preprocessing
    def get_nl_tables_summary(self) -> dict[str, str]:
        if not self._nl_tables_summary:
            prompt = NLTableSummaryPrompt(self.ai_service)
            for table_name in self.table_names:
                self._nl_tables_summary[table_name] = prompt.run(self.get_nl_db_schema()[table_name])
        return self._nl_tables_summary

    # Indexer / Preprocessing
    def get_sample(self, table_name: str, n: int = 5) -> pd.DataFrame:
        sample_df = self.data[table_name].sample(n=n, random_state=0)
        return sample_df


    # Context Retrieval
    def retrieve_relevant_tables(self, nl_query:str) -> dict:
        prompt = RetrieveRelevantTablesPrompt(self.ai_service)
        return prompt.run(nl_query, self.get_nl_db_schema())

    # Context Retrieval
    def retrieve_relevant_table_attributes(self, nl_query:str, relevant_tables: list[str]) -> dict:

        nl_description_filtered = {table: self.get_nl_db_schema()[table] for table in relevant_tables}
        prompt = RetrieveRelevantTableAttributesPrompt(self.ai_service)
        return prompt.run(nl_query, nl_description_filtered)

    # Context Retrieval
    def retrieve_reference_values(self, nl_query:str, relevant_tables: list[str], relevant_attributes: dict[str, list[str]]):
        nl_description_filtered = {table: self.get_nl_db_schema()[table] for table in relevant_tables}
        prompt = RetrieveReferenceValuesPrompt(self.ai_service)
        return prompt.run(nl_query, nl_description_filtered, relevant_attributes)

    # Generator
    def generate_sql_query(self, nl_query:str, relevant_tables: list[str], relevant_attributes: dict[str, list[str]], reference_values: dict[str, list[str]]):
        prompt = GenerateSQLQueryPrompt(self.ai_service)

        table_attributes_context = ""
        sample_data_context = ""

        for table in relevant_tables:
            sample_table_data = self.sample_data[table]

            table_attributes_context += f"- Table: `{table}` "

            attributes = []
            for value in relevant_attributes:
                if value["table"] == table:
                    for attribute in value["attributes"]:
                        attributes.append(f"`{attribute}`")

                        attribute_sample_data = sample_table_data[attribute].to_list()
                        sample_data_context += f"`{table}.{attribute}` = {', '.join([f'{value}' for value in attribute_sample_data])}\n"
                        
            if len(attributes) > 0:
                table_attributes_context += f"; Attributes: {', '.join(attributes)}"

            table_attributes_context += "\n"

        reference_values_context = ""

        for entry in reference_values:
            reference_values_context += f"`{entry['table']}.{entry['attribute']}` = {', '.join([f'{value}' for value in entry['values']])}\n"

        return prompt.run(nl_query, table_attributes_context, reference_values_context, sample_data_context)
        