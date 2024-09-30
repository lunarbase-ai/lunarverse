"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines <COMPONENT NAME HERE> Lunar component.
"""

from typing import Any

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType


class TextInput(
    BaseComponent,
    component_name="Text Input",
    component_description="""Allows the input of text (potentially with template variables) that can then be used in other downstream components. It can also be used as an output if useful.
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
