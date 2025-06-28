# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

from typing import Any, Optional, Dict
from dotenv import load_dotenv
import psycopg2
import json

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

load_dotenv()

class PostgresQuery(
    LunarComponent,
    component_name="PostgresQuery",
    component_description="""Executes SQL queries against a PostgreSQL database.
    Inputs:
        `statement` (str): SQL query to execute
        `params` (str, optional): JSON string of parameters. 
    Output (dict): Query results with columns and rows or error information""",
    input_types={
        "statement": DataType.TEXT,
        "params": DataType.TEXT
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    database="$LUNARENV::DATABASE",
    user="$LUNARENV::PG_USER",
    host="$LUNARENV::HOST",
    password="$LUNARENV::PASSWORD",
    port="$LUNARENV::PORT",
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self.config = {
            'database': self.configuration["database"],
            'user': self.configuration["user"],
            'host': self.configuration["host"],
            'password': self.configuration["password"],
            'port': self.configuration["port"],
        }

    def run(self, statement: str, params: Optional[str] = None) -> Optional[Dict]:
        query_params = None
        if params:
            try:
                parsed = json.loads(params)
                if isinstance(parsed, list):
                    if len(parsed) > 0 and isinstance(parsed[0], list):
                        query_params = parsed
                    else:
                        query_params = tuple(parsed)
                elif isinstance(parsed, (int, float, str, bool)):
                    query_params = (parsed,)
                else:
                    query_params = parsed
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format for params")

        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cursor:
                if isinstance(query_params, list) and len(query_params) > 0 and isinstance(query_params[0], list):
                    cursor.executemany(statement, query_params)
                else:
                    cursor.execute(statement, query_params)
                if cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    return {"columns": columns, "rows": rows}
                else:
                    conn.commit()
                    return {"columns": [], "rows": []}