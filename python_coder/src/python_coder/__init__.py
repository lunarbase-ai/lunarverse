# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from black.parsing import parse_ast
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class PythonCoder(
    LunarComponent,
    component_name="Python coder",
    component_description="""Enables the execution of arbitrary Python code, allowing users to perform dynamic computations, data analysis, and automation tasks on the fly. Outputs the value that the Python variable `result` is set to during the execution of the Python code.
Inputs:
  `Code` (str): A string of the Python code to execute.  If needed, the Python code can be inputted manually by the user.
Output (Any): The value of the variable `result` in the Python code after execution.""",
    input_types={"code": DataType.CODE},
    output_type=DataType.ANY,
    component_group=ComponentGroup.CODERS,
):
    def _execute(self, code: str):
        local_vars = {}
        exec(code, local_vars)
        return local_vars.get("result", None)

    def run(self, code: str):
        try:
            parse_ast(code.strip())
        except SyntaxError as e:
            raise e
        code_out = self._execute(code)

        return code_out
