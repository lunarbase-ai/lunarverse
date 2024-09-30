"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines a JSON Input Lunar component.
"""


from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType
import json


class JSONInput(
    BaseComponent,
    component_name="JSON Input",
    component_description="""Allows the input of a JSON text (potentially with template variables) that can then be used in other downstream components. It can also be used as an output if useful.
Inputs:
  `input` (str): A valid json.
  Output (dict): The input json as a Python dict.""",
    input_types={"input": DataType.TEMPLATE},
    output_type=DataType.JSON,
    component_group=ComponentGroup.IO,
):
    def run(
        self,
        input: str,
    ):
        input_obj = json.loads(input)
        return input_obj
