"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
SPDX-License-Identifier: GPL-3.0-or-later
Notes
-----
This package defines the Sleep Lunar component.
"""

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class Range(
    LunarComponent,
    component_name="Range",
    component_description="""Generate a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and stops before a specified number.
Inputs:
  `Start` (int): The number to start from.
  `Stop` (int): The stopping number - it stops before it.
  `Step` (int): The value of the increment
Output (STREAM): The generated sequence as a generator - it needs to be consumed by some downstream component.""",
    input_types={"start": DataType.INT, "stop": DataType.INT, "step": DataType.INT},
    output_type=DataType.STREAM,
    component_group=ComponentGroup.UTILS,
):
    def run(
        self,
        stop: int,
        start: int = 0,
        step: int = 1,
    ):
        yield from range(start, stop, step)