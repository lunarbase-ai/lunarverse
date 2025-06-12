"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines <COMPONENT NAME HERE> Lunar component.
"""

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

class TextInput(
    LunarComponent,
    component_name="Text Input",
    component_description="""Allows the input of text data that is then be used in other downstream components. It can also be used as an output to show the textual result of a previous component.
Inputs:
  `input` (str): The text to output.
Output (str): The inputted text.""",
    input_types={"input": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.IO,
):
    def run(
        self,
        input: str,
    ):
        return input
