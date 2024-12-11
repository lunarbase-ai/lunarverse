# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Union
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
import pandas as pd
from io import StringIO


class CsvViewer(
    LunarComponent,
    component_name="Csv Viewer",
    component_description="""Displays .csv files Output (str): csv file""",
    input_types={"input_text": DataType.TEXT},
    output_type=DataType.CSV,
    component_group=ComponentGroup.DATA_VISUALIZATION,
    sep=',',
    lineterminator='\n',
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)

    def run(self, input_text: str) -> str:
        csv_str: Union[StringIO, str] = StringIO(input_text)
        df = pd.read_csv(
            csv_str,
            sep=self.configuration.get("sep", ","),
            lineterminator=self.configuration.get("lineterminator", "\n"),
        )
        return df.to_csv(
            index=False,
              sep=self.configuration.get("sep", ","),
        )