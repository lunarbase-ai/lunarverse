# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import binascii

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class AudioPlayer(
    LunarComponent,
component_name="Audio Player",
    component_description="""Plays audio encoded in base64 format.
Inputs:
  `audio_data` (str): The audio data in base64 (on format f`data:{mime_type};base64,{base64_string}`).
Output (str): The same base64 audio string provided as input.""",
    input_types={"base64_encoded_audio": DataType.TEXT},
    output_type=DataType.AUDIO,
    component_group=ComponentGroup.MUSICGEN,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)

    def run(self, audio_data: str):
        try:
            base64_encoded_audio = audio_data.split(",")[1]
            
            missing_padding = len(base64_encoded_audio) % 4
            if missing_padding:
                base64_encoded_audio += '=' * (4 - missing_padding)
            base64.b64decode(base64_encoded_audio)
        except binascii.Error:
            raise ValueError("Invalid Base64 encoded audio")
        return base64_encoded_audio
