# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, List

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from .nltsql import NaturalLanguageToSQL
from nl2sql.services.ai import AzureOpenAIService

from .data_sources.csv_data_source import CsvDataSource
# from .indexers import Indexer

class NL2SQL(
    LunarComponent,
    component_name="NL2SQL",
    component_description="""Transforms natural language queries into SQL queries.""",
    input_types={"questions": DataType.LIST, "dict_path_csv": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.NLP,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT"
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self.ai_service = AzureOpenAIService({
            "openai_api_key": self.configuration["openai_api_key"],
            "openai_api_version": self.configuration["openai_api_version"],
            "azure_endpoint": self.configuration["azure_endpoint"],
            "model": self.configuration["deployment_name"]
        })

    def run(self, questions: List[str], dict_path_csv: dict):
        # obj = NaturalLanguageToSQL(
        #     dict_path_csv=dict_path_csv,
        #     ai_service=self.ai_service,
        # )

        data_source = CsvDataSource(dict_path_csv)
        # indexer = Indexer(self.ai_service, data_source)

        print(data_source.tables)
        print(data_source.samples)

        result = {}

        # for nl_query in questions:
        #     # ContextRetrieval  
        #     relevant_tables = obj.retrieve_relevant_tables(nl_query)

        #     relevant_attributes = obj.retrieve_relevant_table_attributes(nl_query, relevant_tables)

        #     reference_values = obj.retrieve_reference_values(nl_query, relevant_tables, relevant_attributes)

        #     # Generation
        #     sql_query = obj.generate_sql_query(nl_query, relevant_tables, relevant_attributes, reference_values)
            
        #     result[nl_query] = sql_query
        return result