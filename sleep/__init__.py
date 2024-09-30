"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines the Sleep Lunar component.
"""

from typing import Any, List
import time
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType


class Sleep(
    BaseComponent,
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
