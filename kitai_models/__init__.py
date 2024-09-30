# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any, List

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

import json
import requests

class Kitai_Models(
    BaseComponent,
    component_name="kitai models",
    component_description="""kitai models""",
    input_types={},
    output_type=DataType.LIST,
    component_group=ComponentGroup.MUSICGEN,
    api_key="$LUNARENV::KITSAI_API_KEY",
    client_id="$LUNARENV::KITSAI_CLIENT_ID",
    client_secret="$LUNARENV::KITSAI_CLIENT_SECRET",
):
    URL = "https://arpeggi.io/api/kits/v1/voice-models"
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(
        self, inputs: List[ComponentInput]
    ):
        headers = {"Authorization": f"Bearer {self.configuration.get('api_key)')}"}

        response = requests.request("GET", URL, headers=headers)

        response = json.loads(response.text)

        output = []
        for d in response["data"][:6]:
            output.append({})
            output[-1]["id"] = d["id"]
            output[-1]["title"] = d["title"]
            output[-1]["tags"] = d["tags"]
            output[-1]["demoUrl"] = d["demoUrl"]

        return output
