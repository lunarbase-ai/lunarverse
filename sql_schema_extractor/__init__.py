# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional, List

from sqlalchemy import MetaData
from sqlalchemy.sql.ddl import CreateTable

from lunarcore.core.component import BaseComponent
from lunarcore.core.connectors.sql import SQLConnector
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType


class SQLSchemaExtractor(
    BaseComponent,
    component_name="SQL Schema Extractor",
    component_description="""Connects to a SQL database and retrieves its schema, i.e., data definition language.
    Output (dict): a json describing the database schema.""",
    input_types={
        "tables": DataType.LIST,
    },
    output_type=DataType.TEXT,
    component_group=ComponentGroup.DATABASES,
    driver_name="",
    username="$LUNARENV::SQL_SCHEMA_EXTRACTOR_USERNAME",
    password="$LUNARENV::SQL_SCHEMA_EXTRACTOR_PASSWORD",
    host=None,
    port=None,
    database=None,
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

        meta = MetaData()
        meta.reflect(bind=sql_engine.engine)

        ddl = []
        for table in meta.sorted_tables:
            if len(tables) > 0 and table.name not in tables:
                continue

            table_sql = str(
                CreateTable(table).compile(dialect=sql_engine.dialect)
            ).strip()
            ddl.append(table_sql)
        if len(ddl) > 0:
            return "; ".join(ddl)
        return None
