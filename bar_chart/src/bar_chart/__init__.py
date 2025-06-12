# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import io
import matplotlib
import matplotlib.pyplot as plt

from typing import Dict

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class BarChart(
    LunarComponent,
    component_name="Bar chart",
    component_description="""Creates bar charts from user-supplied data, providing a clear visual comparison of categorical values or group-based metrics. . The output can be linked to other components.
Inputs:
  `data` (Dict[Any, Union[int, float]]): A dictionary with keys (any data type that can be converted to a str) mapped to numerical values (int or float).
Output (Dict): A dictionary with the key `data` (str) mapped to the original input data (Dict[Any, Union[int, float]]), """ \
  """and the key `images` (str) mapped to a list (List[str]) with one element which is the produced image (the bar chart) encoded in base64 on the format """ \
  """`f`data:image/png;base64,{base64.b64encode(binary_buffer_of_PNG.read()).decode()}`` (str).""",
    input_types={"data": DataType.JSON},
    output_type=DataType.BAR_CHART,
    component_group=ComponentGroup.DATA_VISUALIZATION,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)

    @staticmethod
    def plot_bar_chart(input_dict):
        keys = list(input_dict.keys())
        values = list(input_dict.values())

        matplotlib.use("agg")

        # Plot the bar chart
        plt.bar(keys, values)
        plt.xlabel("Keys")
        plt.ylabel("Values")
        plt.title("Bar Chart")

        # Save the plot to a BytesIO buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)

        # Convert the BytesIO buffer to a base64-encoded PNG string URL
        import base64

        png_string_url = (
            f"data:image/png;base64,{base64.b64encode(buffer.read()).decode()}"
        )

        # Close the plot to free resources
        plt.close()

        return png_string_url

    def run(self, data: Dict):
        plot_data = dict()
        images = [self.__class__.plot_bar_chart(data)]
        plot_data.update(data)
        return {"data": plot_data, "images": images}
