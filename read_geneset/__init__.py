# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any, Dict
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
import pandas as pd


class UploadGeneSet(
    BaseComponent,
    component_name="Gene Set Upload",
    component_description="""Reads a CSV file with genes and outputs a list of the gene names.
Inputs:
  `Input file` (str): The server path of a CSV file with gene names in a column `gene_name`.
Output (List[str]): A list of the genes found in the column `gene_name` in the inputted CSV file.""",
    input_types={"input_file": DataType.FILE},
    output_type=DataType.LIST,
    component_group=ComponentGroup.BIOMEDICAL,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self, input_file: Dict):
        file_path = self._file_connector.get_absolute_path(input_file.get("path", None))
        df = pd.read_csv(file_path)

        return df['gene_name'].to_list()
