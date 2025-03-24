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

    def run(self, questions: List[str], dict_path_csv: dict):

        description = {}
        table_summary = {}
        relevant_table = {}
        step3 = {}
        step4 = {}
        step5 = {}

        obj = NaturalLanguageToSQL(dict_path_csv=dict_path_csv)
        for nl_query in questions:
            # nl_query = nl_query[0].upper() + nl_query[1:]
            print(f"Processing: {nl_query}")

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

            step3[nl_query] = obj.generate(obj.get_prompt_relevant_tables_and_attributes_table_filter(nl_query = nl_query, descriptions = description, tables="\n".join(list(relevant_table.values()))),**self.configuration)

            prompt_chat = [
                {"role": "user", "content": obj.get_prompt_relevant_tables_and_attributes_table_filter(nl_query = nl_query, descriptions = description, tables=step3[nl_query])},
                {"role": "assistant", "content": step3[nl_query]},
                {"role": "user", "content": obj.get_prompt_get_instances(nl_query=nl_query)}
            ]
            step4[nl_query] = obj.generate_list_dict(prompt_chat,**self.configuration)

            step5[nl_query] = obj.generate(obj.get_prompt_nl_to_sql(nl_query=nl_query,step3=step3[nl_query],step4=step4[nl_query],joins=posible_joins["table1_table2"]),**self.configuration)
        return step5