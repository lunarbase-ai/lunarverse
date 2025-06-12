# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later


import requests

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class GraphQLQuery(
    LunarComponent,
    component_name="GraphQL",
    component_description="""Sends queries to a GraphQL API, enabling precise retrieval of structured data from servers.
Output (dict): The response for the query""",
    input_types={"query": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    endpoint="",
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
        self.endpoint = self.configuration.get("endpoint")

    def run(self, query: str):
        if not query:
            raise TypeError("The query parameter cannot be None or empty.")

        response = requests.post(self.endpoint, json={"query": query})

        # Check for HTTP error response
        response.raise_for_status()

        data = response.json()
        return data
