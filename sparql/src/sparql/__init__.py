# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Dict

from SPARQLWrapper import SPARQLWrapper, JSON
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from lunarcore.component.lunar_component import LunarComponent


class SPARQLQuery(
    LunarComponent,
    component_name="SPARQL Query",
    component_description="""Runs a SPARQL query on a SPARQL endpoint.
Inputs:  query: str
Outputs: The query result in JSON format
Expected configuration includes: endpoint: str, defaultGraph: Optional[str] = None., etc.
See https://sparqlwrapper.readthedocs.io/en/latest/main.html for more information.
""",
    input_types={"query": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    datasource=None,
    endpoint=None,
    updateEndpoint=None,
    user=None,
    passwd=None,
    # http_auth="BASIC",
    # onlyConneg=False,
    # customHttpHeaders=None,
    # timeout=30,
    # parameters=None
):
    def __init__(self, configuration: Optional[Dict] = None):
        super().__init__(configuration=configuration)

        self.sparql = SPARQLWrapper(
            endpoint=self.configuration.pop("endpoint", None),
            returnFormat=JSON,
            **self.configuration
        )

    def run(self, query: str):
        self.sparql.resetQuery()
        self.sparql.setQuery(query=query)
        try:
            result = self.sparql.queryAndConvert()
            return result
        except Exception as e:
            raise ConnectionError(str(e))
