# SPDX-FileCopyrightText: Copyright © 2024 Eliezer Silva <djosacv@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from lunarcore.core.component import BaseComponent
from lunarcore.component_library.table2text.table2text.metadata import TableMetadata
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentModel, ComponentInput
from lunarcore.core.typings.datatypes import DataType

from io import StringIO
from typing import Any, Optional
import pandas as pd

class Table2Text(
    BaseComponent,
    component_name="Table2Text",
    component_description="""Takes a CSV formatted table as input and converts it to a text by sentencifying each row.
Inputs:
  `Table` (str): A string of the table on CSV format.
Output (Dict): A dictionary containing only the key `results` which is mapped to a list of the sentences corresponding to the inputted table rows.""",
    input_types={"table": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    """Creates Lunarverse Table2Text component.
    Table component is used to represent tabular data in Lunarverse.
    It is a wrapper around the TableMetadata Class, that takes as input a pandas dataframe and a row to generate a phrase.
    """

    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def add_table_str(self, table_str: str):
        # convert string csv to pandas dataframe
        if table_str is not None:
            str_io = StringIO(table_str)
            self.table = TableMetadata(pd.read_csv(str_io))
            self.table.process_all()
            self.table, _ = self.table.switch_to_multiindex()

    def run(self, table: str):
        tables = []
        try:
            str_io = StringIO(table)
            meta = TableMetadata(pd.read_csv(str_io))
            meta.process_all()
            table, _ = meta.switch_to_multiindex()
            phrases = "\n".join(table.generate_all_phrases())
            tables.append(phrases)
        except Exception as e:
            raise e

        return {"results": tables}
