# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import base64
import mimetypes

from typing import Any, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


def convert_audio_to_data_uri(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        if file_path.endswith('.mp3'):
            mime_type = 'audio/mpeg'
        elif file_path.endswith('.wav'):
            mime_type = 'audio/wav'
    
    with open(file_path, "rb") as audio_file:
        binary_data = audio_file.read()
        base64_string = base64.b64encode(binary_data).decode('utf-8')
        data_uri = f"data:{mime_type};base64,{base64_string}"
        
    return data_uri


class Audio2Base64(
    BaseComponent,
    component_name="Audio2Base64",
    component_description="""Converts an audio file (.mp3 or .wav) to a base64 string.
Inputs:
  `Audio file path` (str): A string of the path of the audio file (.mp3 or .wav) to convert to a base64 string.
Output (str): A string on the following format: f`data:{mime_type};base64,{base64_string}`.
""",
    input_types={"Audio file path": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.MUSICGEN,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    def run(self, audio_file_path: str):
        data_uri_audio = convert_audio_to_data_uri(audio_file_path)
        return data_uri_audio
