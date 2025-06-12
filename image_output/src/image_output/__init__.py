# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import base64

from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from lunarcore.component.lunar_component import LunarComponent


class ImageOutput(
    LunarComponent,
    component_name="Image Output",
    component_description="""Decodes and visualizes base64-encoded images directly in the interface, enabling quick inspection without needing external viewers. """,
    input_types={"base64_string": DataType.TEXT},
    output_type=DataType.IMAGE,
    component_group=ComponentGroup.IO
):

    def run(self, base64_string: str):
        try:
            base64_string_no_prefix = base64_string.split(",")[-1]
            base64.b64decode(base64_string_no_prefix)
            return f"data:image;base64,{base64_string_no_prefix}"
        except Exception as e:
            raise ValueError("Invalid base64 string") from e
