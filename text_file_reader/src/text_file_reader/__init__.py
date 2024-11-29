"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines FileReader Lunar component.
"""
from typing import Dict, Union

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType, File


class TextFileReader(
    LunarComponent,
    component_name="Text File Reader",
    component_description="""Allows for the upload (if necessary) and reading of a text file. 
Inputs:
  `input` (str): The file name.
Output (str): The file content.""",
    input_types={"input_file": DataType.FILE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.IO,
):
    def run(
        self,
        input_file: Union[Dict, File]
    ):
        if not isinstance(input_file, File):
            input_file = File.model_validate(input_file)

        with open(input_file.file_path, "r") as f:
            return f.read().rstrip()
