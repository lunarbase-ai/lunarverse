# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import io
import matplotlib
import matplotlib.pyplot as plt
from typing import Dict
import base64

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class LineChart(
    LunarComponent,
    component_name="Line chart",
    component_description="""Plots a line chart given a dictionary with numerical keys and values. The output can be linked to a report component.
Inputs:
  `Data` (Dict[Union(int,float), Union(int,float)]): A dictionary with keys (int or float) mapped to numerical values (int or float).
Output (Dict): A dictionary with the key `data` (str) mapped to the original input data (Dict[Any, Union[int, float]]), """ \
        """and the key `images` (str) mapped to a list (List[str]) with one element which is the produced image (the line chart) encoded in base64 on the format """ \
        """`f`data:image/png;base64,{base64.b64encode(binary_buffer_of_PNG.read()).decode()}`` (str).""",
    input_types={"data": DataType.JSON},
    output_type=DataType.LINE_CHART,
    component_group=ComponentGroup.DATA_VISUALIZATION,
):
    def __init__(self,**kwargs):
        super().__init__(configuration=kwargs)

    @staticmethod
    def plot_line_chart(input_dict):
        keys = list(map(lambda key: int(key), input_dict.keys()))
        values = list(input_dict.values())

        matplotlib.use("agg") 

        plt.plot(keys, values)
        plt.xlabel("Keys")
        plt.ylabel("Values")
        plt.title("Line Chart")

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        png_string_url = f"data:image/png;base64,{base64.b64encode(buffer.read()).decode()}"

        plt.close()

        return png_string_url

    def run(
        self,
        data: Dict,
    ):
        images = [self.__class__.plot_line_chart(data)]
        return {"data": data, "images": images}
