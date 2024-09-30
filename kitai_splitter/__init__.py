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

class KitsaiSplitter(
    BaseComponent,
    component_name="Kitsai Splitter",
    component_description="""kitai_splitter""",
    input_types={"sound_file": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.MUSICGEN,
    api_key="$LUNARENV::KITSAI_API_KEY",
    client_id="$LUNARENV::KITSAI_CLIENT_ID",
    client_secret="$LUNARENV::KITSAI_CLIENT_SECRET",
):
    URL = "https://arpeggi.io/api/kits/v1/stem-splits"
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(
        self, sound_file: str
    ):
        files = { 'inputFile': open(sound_file, 'rb') }
        headers = { 'Authorization': f'Bearer {self.configuration.get("api_key")}' }

        response = requests.post(url, files=files, headers=headers)
        stem_splitter_job = response.json()

        return str(stem_splitter_job["id"])
