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
        obj = NaturalLanguageToSQL(
            dict_path_csv=dict_path_csv,
            ai_service=self.ai_service,
        )

        # Indexing / Preprocessing
        description = obj.get_nl_db_schema()
        table_summary = obj.get_nl_tables_summary()


        # Generation
        step3 = {}
        step4 = {}
        step5 = {}

        for nl_query in questions:
            # ContextRetrieval  
            relevant_tables = obj.retrieve_relevant_tables(nl_query)

            relevant_attributes = obj.retrieve_relevant_table_attributes(nl_query, relevant_tables)

            reference_values = obj.retrieve_reference_values(nl_query, relevant_tables, relevant_attributes)

            # step3[nl_query] = obj.generate(obj.get_prompt_relevant_tables_and_attributes_table_filter(nl_query = nl_query, descriptions = description, tables="\n".join(relevant_tables)))


            # prompt_chat = [
            #     {"role": "user", "content": obj.get_prompt_relevant_tables_and_attributes_table_filter(nl_query = nl_query, descriptions = description, tables=step3[nl_query])},
            #     {"role": "assistant", "content": step3[nl_query]},
            #     {"role": "user", "content": obj.get_prompt_get_instances(nl_query=nl_query)}
            # ]
            # step4[nl_query] = obj.generate_list_dict(prompt_chat)

            # posible_joins = {}
            # posible_joins["table1_table2"] = ""
            # step5[nl_query] = obj.generate(obj.get_prompt_nl_to_sql(nl_query=nl_query,step3=step3[nl_query],step4=step4[nl_query],joins=posible_joins["table1_table2"]))
        return {}