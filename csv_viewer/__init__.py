# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any, Union
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType, File
import pandas as pd
from io import StringIO


class CsvViewer(
    BaseComponent,
    component_name="Csv Viewer",
    component_description="""Displays .csv files Output (str): csv file""",
    input_types={"input_text": DataType.TEXT},
    output_type=DataType.CSV,
    component_group=ComponentGroup.DATA_VISUALIZATION,
    sep=None,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self, input_text: str):
        csv_str: Union[StringIO, str] = StringIO(input_text)
        df = pd.read_csv(
            csv_str,
            sep=self.configuration["sep"],
        )

        return df.to_csv()