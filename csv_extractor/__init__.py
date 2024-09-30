# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any, Dict
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType, File
import pandas as pd


class CsvExtractor(
    BaseComponent,
    component_name="Csv Upload",
    component_description="""Reads a CSV file with a header.
Inputs:
  `Input file` (File): A File object with a field `path` (str) containing the local path to the local CSV file to read. Use this component only if the CSV file has a header, i.e. if the first line of the CSV file is the column titles!
Output (File): A File object with a field `preview` which has the value pandas.read_csv(file_path, nrows=10).head().to_csv(). This means that the field contains a record formatted pandas dataframe of the data in the inputted CSV file (if we see the CSV file as a m*n matrix M, the format becomes a string `,M(1,1),M(1,2),...,M(1,n)\\n 0,M(2,1),...,M(2,n)\\n 1,M(3,n),... ... M(m,n)`).""",
    input_types={"input_file": DataType.FILE},
    output_type=DataType.FILE,
    component_group=ComponentGroup.IO,
    sep=None,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self, input_file: Dict):
        input_file = File.model_validate(input_file)

        file_path = self._file_connector.get_absolute_path(input_file.path)

        df = pd.read_csv(file_path, nrows=10, sep=self.configuration["sep"])

        file = File(
            path=file_path,
            name=input_file.name,
            preview=df.head().to_csv(),
            type=".csv",
        )

        return file
