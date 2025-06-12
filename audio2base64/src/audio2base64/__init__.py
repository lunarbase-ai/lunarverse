# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from audio2base64.audio_uri_converter import AudioUriConverter

class Audio2Base64(
    LunarComponent,
    component_name="Audio2Base64",
    component_description="""Encodes raw audio data (.mp3 or .wav) into base64 format, transforming it into a text-based representation for easy transmission and storage.
Inputs:
  `Audio file path` (str): A string of the path of the audio file (.mp3 or .wav) to convert to a base64 string.
Output (str): A string on the following format: f`data:{mime_type};base64,{base64_string}`.
""",
    input_types={"Audio file path": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.MUSICGEN,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
        self._converter = AudioUriConverter()

    def run(self, audio_file_path: str):
        data_uri_audio = self._converter.convert(audio_file_path)
        return data_uri_audio
