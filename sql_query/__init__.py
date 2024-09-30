# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import csv
import io
from typing import Union, List, Any, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.connectors.sql import SQLConnector
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from lunarcore.errors import ComponentError


class SQLQuery(
    BaseComponent,
    component_name="SQL Query",
    component_description="""Connects to a SQL database and returns the result of a query
    Output (str): the query result.""",
    input_types={"query": DataType.SQL},
    output_type=DataType.CSV,
    component_group=ComponentGroup.DATABASES,
    driver_name="",
    username="$LUNARENV::SQL_USERNAME",
    password="$LUNARENV::SQL_PASSWORD",
    host=None,
    database=None,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self.sql_connector = SQLConnector(
            driver_name=self.configuration.get("driver_name") or "",
            username=self.configuration.get("username") or "",
            password=self.configuration.get("password") or "",
            host=self.configuration.get("host") or "",
            database=self.configuration.get("database") or "",
        )

    def run(self, query: str):
        result = self.sql_connector.query(query)
        output = io.StringIO()
        if len(result) > 0:
            headers = list(result[0].keys())
            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()
            writer.writerows(result)

        return "\n".join(output.getvalue().splitlines())