# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json

import requests
from typing import Any, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


class GraphQLQuery(
    BaseComponent,
    component_name="GraphQL",
    component_description="""Fetches data from a GraphQL endpoint
    Output (dict): The response for the query""",
    input_types={"query": DataType.GRAPHQL},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    endpoint="",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self.endpoint = self.configuration.get("endpoint")

    def run(self, query: str):
        endpoint = self.endpoint
        query = json.loads(query, strict=False)

        response = requests.post(endpoint, json=query)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            response.raise_for_status()
