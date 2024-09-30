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

import requests

class Kitsai(
    BaseComponent,
    component_name="Kitsai",
    component_description="""Kits streamlines and improves producer workflows with AI audio tools built for music. This component connects to Kits's API.""",
    input_types={"sound_file": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.MUSICGEN,
    api_key="$LUNARENV::KITSAI_API_KEY",
    voice_model_id=None,
    client_id="$LUNARENV::KITSAI_CLIENT_ID",
    client_secret="$LUNARENV::KITSAI_CLIENT_SECRET",
):

    URL = "https://arpeggi.io/api/kits/v1/voice-conversions"
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(
        self, sound_file: str
    ):
        data = { 'voiceModelId': self.configuration.get("voice_model_id")}
        headers = { 'Authorization': f'Bearer {elf.configuration.get("api_key")}' }
        files = { 'soundFile': open(sound_file, 'rb') }
        

        response = requests.post(URL, data=data, files=files, headers=headers)
        vocal_conversion_job = response.json()

        return str(vocal_conversion_job["id"])
