# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional, Dict
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType, File
import pandas as pd


class Report(
    BaseComponent,
    component_name="Report",
    component_description="""Creates an editable report from the input it gets.
Inputs:
  `Inputs` (Dict[str, str]): A dictionary containing of strings mapped to strings, containing data to be included in the report.
Output (Dict): A dictionary containing instructions for building the report using the Quill editor format.""",
    input_types={"inputs": DataType.AGGREGATED},
    output_type=DataType.REPORT,
    component_group=ComponentGroup.UTILS,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    def run(
        self, inputs: Dict
    ):
        operations = []
        for input_key, input_value in inputs.items():
            if "CHART" in input_key:
                operations.append("<p></p>")
                for image in input_value["images"]:
                    operations.append(f"<img src='{image}'/>")
                operations.append("<p></p>")
            elif isinstance(input_value, File):
                if input_value.type == '.csv':
                    df = pd.read_csv(input_value.path)
                    csv_html = df.to_html()
                    operations.append(csv_html)
            elif type(input_value) is str:
                if "data::image/" in input_value:
                    operations.append(f"<img src='{input_value}'/>")
                    operations.append("<p></p>")
                else:
                    replaced_text = input_value.replace('\n', '<p></p>')
                    operations.append("<p></p>")
                    operations.append(f"<p>{replaced_text}</p>")
                    operations.append("<p></p>")
            elif type(input_value) is dict:
                operations.append({"insert": "\n"})
                for key, value in input_value.items():
                    if "IMAGE" in key:
                        operations.append(f"<img src='{value}'/>")
                        operations.append("<p></p>")
                    else:
                        operations.append("<p></p>")
                        operations.append(f"<p>{value}</p>")
                        operations.append("<p></p>")

        return ''.join(operations)
