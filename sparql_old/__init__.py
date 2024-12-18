# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional


from lunarcore.connectors.sparql import SPARQLConnector
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class SPARQLQuery(
    LunarComponent,
    component_name="SPARQL Query",
    component_description="""Fetch data from a SPARQL endpoint.
    Input (str): A string that is the SPARQL query.
    Output (dict): A dictionary containing the response to the SPARQL query in the python SPARQLWrapper library format.""",
    input_types={"query": DataType.SPARQL},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    endpoint="",
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
        endpoint = self.configuration.get("endpoint")
        self.connector = SPARQLConnector(endpoint=endpoint)

    def run(self, query: str):
        result = self.connector.query(query_string=query)
        return result
