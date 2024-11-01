"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines the Sleep Lunar component.
"""

from typing import Any
import time
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class Sleep(
    LunarComponent,
    component_name="Sleep",
    component_description="""Sleep (delay execution) for the given number of seconds.
Inputs:
  `Timeout` (int): The number of seconds to delay.
  `Input` (any): The data to pass over.
Output (any): The input data.""",
    input_types={"timeout": DataType.INT, "input": DataType.ANY},
    output_type=DataType.ANY,
    component_group=ComponentGroup.UTILS,
):
    def run(
        self,
        input: Any,
        timeout: int = 0,
    ):
        time.sleep(int(timeout))

        return input
