# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List
import json
from sqlalchemy import inspect
from lunarcore.connectors.sql import SQLConnector
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

class SQLSchemaExtractor(
    LunarComponent,
    component_name="SQL Schema Extractor",
    component_description="""Connects to a SQL database and retrieves its schema, i.e., data definition language.
    Output (dict): a json describing the database schema.""",
    input_types={ "tables": DataType.LIST },
    output_type=DataType.TEXT,
    component_group=ComponentGroup.DATABASES,
    driver_name="",
    username="$LUNARENV::SQL_SCHEMA_EXTRACTOR_USERNAME",
    password="$LUNARENV::SQL_SCHEMA_EXTRACTOR_PASSWORD",
    host=None,
    port=None,
    database=None,
    ssl_mode="require"
):
    def run(self, tables: List[str] = None):

        tables = set(tables or [])
        

        sql_engine = SQLConnector(
            driver_name=self.configuration.get("driver_name"),
            username=self.configuration.get("username"),
            password=self.configuration.get("password"),
            host=self.configuration.get("host"),
            port=self.configuration.get("port"),
            database=self.configuration.get("database")
        )


        inspector = inspect(sql_engine.engine)
        

        schema = {"tables": []}

        for table_name in inspector.get_table_names():

            if tables and table_name not in tables:
                continue

            columns = []
            for column in inspector.get_columns(table_name):
                column_info = {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "constraints": []
                }

                if column.get("primary_key"):
                    column_info["constraints"].append("primary_key")

                if column.get("nullable") is True:
                    column_info["constraints"].append("nullable")

                if column.get("default") is not None:
                    column_info["constraints"].append(f"default: {column['default']}")

                columns.append(column_info)

            table_constraints = []


            pk_constraint = inspector.get_pk_constraint(table_name)
            if pk_constraint:
                table_constraints.append(f"pk_{table_name}")


            for fk in inspector.get_foreign_keys(table_name):
                table_constraints.append(
                    f"foreign_key({fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']})"
                )

            for constraint in inspector.get_unique_constraints(table_name):
                table_constraints.append(f"unique({constraint['name']})")

            schema["tables"].append({
                "name": table_name,
                "columns": columns,
                "constraints": table_constraints,
            })

        return json.dumps(schema)
