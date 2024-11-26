# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PIL import Image
import pytesseract
import sympy as sp

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class Pic2Text(
    LunarComponent,
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
        # Open the image file
        img = Image.open(file_path)
        
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        
        # Extract math formulas (basic example)
        result_lines = []
        for line in text.split('\n'):
            try:
                expr = sp.parsing.sympy_parser.parse_expr(line)
                latex_formula = sp.latex(expr)
                result_lines.append(f"$$ {latex_formula} $$")
            except:
                result_lines.append(line)
        
        # Combine text and formulas
        result = '\n'.join(result_lines)
        
        return result