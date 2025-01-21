"""
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>

SPDX-License-Identifier: GPL-3.0-or-later

Notes
-----
This package defines FileReader Lunar component.
"""

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from lunarcore.data_sources import DataSourceType


class TextFileReader(
    LunarComponent,
    component_name="Text File Reader",
    component_description="""Reads a text file and returns its content.
Output (str): The file content as string.""",
    input_types={},
    data_source_types={"file": DataSourceType.LOCAL_FILE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.IO,
):
    def run(
        self
    ):
        file_connection = self.connections.get("file")
        return file_connection.read()
