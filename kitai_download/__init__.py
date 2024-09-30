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

import os
import requests

class KitsaiDownload(
    BaseComponent,
    component_name="Kitsai download",
    component_description="""Download music file from Kits.ai""",
    input_types={"conversion_id": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.MUSICGEN,
    api_key="$LUNARENV::KITSAI_API_KEY",
    client_id="$LUNARENV::KITSAI_CLIENT_ID",
    client_secret="$LUNARENV::KITSAI_CLIENT_SECRET",
):
    URL = "https://arpeggi.io/api/kits/v1/voice-conversions"
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(
        self, conversion_id: str
    ):
        url = f"{URL}/{conversion_id}"
        headers = { 'Authorization': f'Bearer {self.configuration.get("api_key")}' }

        response = requests.request("GET", url, headers=headers)

        response_json = response.json()

        if 'status' in response_json:
            if response_json['status'] == "success":

                response = requests.get(response_json["outputFileUrl"], stream=True)
                output_path = os.path.join(self._file_connector.get_absolute_path(""), "generated_audio.wav")
                with open(output_path, "wb") as handle:
                    for data in response.iter_content():
                        handle.write(data)

                return output_path

            return response_json['status']
        return response_json['message']
