# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.connectors.sparql import SPARQLConnector
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


class Nextprot(
    BaseComponent,
    component_name="NeXtProt",
    component_description="""Fetch data from neXtProt: an on-line knowledge platform on human proteins, such as their function, subcellular location, expression, interactions and role in diseases. 
    Input (str): A string that is the SPARQL query.
    Output (dict): A dictionary containing the response to the SPARQL query in the Python [SPARQLWrapper](https://sparqlwrapper.readthedocs.io/en/latest/) library format.""",
    input_types={"query": DataType.SPARQL},
    output_type=DataType.JSON,
    component_group=ComponentGroup.BIOMEDICAL,
    endpoint="https://sparql.nextprot.org",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        endpoint = self.configuration.get("endpoint")
        self.connector = SPARQLConnector(endpoint=endpoint)

    def run(self, query: str):
        result = self.connector.query(query_string=query)
        return result
