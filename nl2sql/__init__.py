# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sqlparse
import re
from typing import Optional, Any

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentModel, ComponentInput
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType


class NL2SQL(
    BaseComponent,
    component_name="Natural language to SQL Query",
    component_description="""Produces an SQL query based on a natural language query statement 
    and a data definition schema. 
    The data definition should be a JSON with table names as keys 
    and dicts of type {<column_name>: <column_type>} as values. 
    
    Output (str): the resulting SQL query.""",
    input_types={"query": DataType.TEMPLATE, "schema": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.NLP,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
):
    SYSTEM_PROMPT_TEMPLATE = """
    SYSTEM: You are an SQL developer assistant. Given the following SQL tables, your job is to write queries following a user's request. 
    Where possible, use the LIKE operator in WHERE clauses with string wildcards. 
    Add all columns in the query to the result and output only the resulting query as a string with no additional text or extra quoting.

    Tables:

    {{schema}}
    """

    USER_PROMPT_TEMPLATE = """
    USER: {{query}}    
    """

    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        if not self.configuration["openai_api_key"]:
            self.configuration["openai_api_key"] = os.environ.get("OPENAI_API_KEY", "")
        if not self.configuration["azure_endpoint"]:
            self.configuration["azure_endpoint"] = os.environ.get("AZURE_ENDPOINT", "")

        self._client = AzureChatOpenAI(**self.configuration)

    @staticmethod
    def parse_schema(schema: str):
        def get_table_name(tokens):
            for token in reversed(tokens):
                if token.ttype is None:
                    return token.value
            return None

        parse = sqlparse.parse(schema)
        ddl = dict()
        for stmt in parse:
            # Get all the tokens except whitespaces
            tokens = [
                t
                for t in sqlparse.sql.TokenList(stmt.tokens)
                if t.ttype != sqlparse.tokens.Whitespace
            ]
            is_create_stmt = False
            for i, token in enumerate(tokens):
                # Is it a create statements ?
                if token.match(sqlparse.tokens.DDL, "CREATE"):
                    is_create_stmt = True
                    continue

                # If it was a create statement and the current token starts with "("
                if is_create_stmt and token.value.startswith("("):
                    # Get the table name by looking at the tokens in reverse order till you find
                    # a token with None type
                    table_name = get_table_name(tokens[:i])
                    if not table_name:
                        continue

                    ddl_text = re.sub(r"[\n\t]+", "", stmt.value)
                    ddl[table_name] = {"ddl": ddl_text, "columns": []}

                    # Now parse the columns
                    txt = token.value
                    columns = txt[1 : txt.rfind(")")].replace("\n", "").split(",")
                    for column in columns:
                        c = " ".join(column.split()).split()
                        c_name = c[0].replace('"', "")
                        ddl[table_name]["columns"].append(c_name)
                    break
        return ddl

    @staticmethod
    def extract_executable_sql(text: str) -> str:
        sql_keywords = r"(SELECT|INSERT INTO|UPDATE|DELETE FROM|CREATE TABLE|DROP TABLE|ALTER TABLE)"
        match = re.search(
            rf"({sql_keywords}\s+.*?)(;|$)", text, re.DOTALL | re.IGNORECASE
        )

        if match:
            return match.group(1).strip()
        return text

    def run(self, query: str, schema: str):
        """
        ###########################THIS PART NEEDS INPROVMENT###########################
        ddl = self.__class__.parse_schema(schema)
        translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
        q = re.sub("\s+", " ", nl_query.translate(translator))
        q_tokens = {word for word in q.lower().split()}

        filtered_ddl = []
        for tname, data in ddl.items():
            translated_tname = re.sub("\s+", " ", tname.translate(translator))
            tname_tokens = {word for word in translated_tname.split()}

            translated_columns = [
                re.sub("\s+", " ", c.translate(translator)) for c in data["columns"]
            ]
            column_tokens = [{ct for ct in tcol.split()} for tcol in translated_columns]

            if (
                q_tokens.intersection(set(data["columns"]))
                or tname in q_tokens
                or q_tokens.intersection(tname_tokens)
                or any([q_tokens.intersection(tcol) for tcol in column_tokens])
            ):
                filtered_ddl.append(ddl[tname]["ddl"])

        if len(filtered_ddl) > 0:
            schema = ";\n".join(filtered_ddl)
        """

        user_prompt_template = PromptTemplate(
            input_variables=["query"],
            template=self.USER_PROMPT_TEMPLATE,
            template_format="jinja2",
        )
        system_prompt_template = PromptTemplate(
            input_variables=["schema"],
            template=self.SYSTEM_PROMPT_TEMPLATE,
            template_format="jinja2",
        )
        system_message = SystemMessage(
            content=system_prompt_template.format(schema=schema)
        )
        user_message = HumanMessage(content=user_prompt_template.format(query=query))

        messages = [system_message, user_message]
        result = self._client.invoke(messages).content

        sql_query = str(result).strip("\n").strip("`").strip()
        sql_query = self.__class__.extract_executable_sql(sql_query)
        return sql_query
