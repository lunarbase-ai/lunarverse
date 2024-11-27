# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json

import requests

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class GraphQLQuery(
    LunarComponent,
    component_name="GraphQL",
    component_description="""Fetches data from a GraphQL endpoint
    Output (dict): The response for the query""",
    input_types={"query": DataType.GRAPHQL},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    endpoint="",
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
        self.endpoint = self.configuration.get("endpoint")
    def run(self, query: str):
        endpoint = self.endpoint

        response = requests.post(endpoint, json={"query": query})

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            response.raise_for_status()
