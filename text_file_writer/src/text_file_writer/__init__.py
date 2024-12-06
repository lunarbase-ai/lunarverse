"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines FileWriter Lunar component.
"""
from typing import Dict, Union

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType, File


class TextFileWriter(
    LunarComponent,
    component_name="Text File Writer",
    component_description="""Write text to file.
Inputs:
  `input_text` (str): The text to be written to the file.
  `input_file` (File or Dict): The file object as a File data type (a Lunar-specific File object) or a json object with the attributes expected by File.
Output (str): NULL.""",
    input_types={"input_text": DataType.TEXT, "input_file": DataType.FILE},
    output_type=DataType.NULL,
    component_group=ComponentGroup.IO,
):
    def run(
        self,
        input_text: str,
        input_file: Union[Dict, File]
    ):
        if not isinstance(input_file, File):
            input_file = File.model_validate(input_file)

        with open(input_file.path, "w+") as f:
            return f.write(input_text)
