# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional
import base64
import binascii
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


class AudioPlayer(
    BaseComponent,
component_name="Audio Player",
    component_description="""Plays audio encoded in base64 format.
Inputs:
  `Base64 encoded audio` (str): The audio data in base64 (on format f`data:{mime_type};base64,{base64_string}`).
Output (str): The same base64 audio string provided as input.""",
    input_types={"base64_encoded_audio": DataType.TEXT},
    output_type=DataType.AUDIO,
    component_group=ComponentGroup.MUSICGEN,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    def run(self, base64_encoded_audio: str):
        try:
            base64.decodestring(base64_encoded_audio)
        except binascii.Error:
            raise ValueError("Invalid Base64 encoded audio")
        return base64_encoded_audio
