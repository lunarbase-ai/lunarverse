# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pix2text import Pix2Text

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType


class Pic2Text(
    BaseComponent,
    component_name="Picture Extractor",
    component_description="""Extracts text and math formulas from a picture. The math formulas are outputted in LaTeX style (eg.: `$$f(x)=3 \cdot x^2$$`).
Input:
  `path` (str): A string of the server path of the image to read.
Output (str): A string of the text and the math formulas in the image.""",
    input_types={"file_path": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def run(self, file_path: str):
        p2t = Pix2Text.from_config()
        result = p2t.recognize_text_formula(
            file_path, resized_shape=768, return_text=True
        )
        return result
