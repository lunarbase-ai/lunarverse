# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional
from black.parsing import parse_ast
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType

CODE_INPUT_NAME = "Code"


class PythonCoder(
    BaseComponent,
    component_name="Python coder",
    component_description="""Performs customized Python code execution. Outputs the value that the Python variable `result` is set to during the execution of the Python code.
Inputs:
  `Code` (str): A string of the Python code to execute.  If needed, the Python code can be inputted manually by the user.
Output (Any): The value of the variable `result` in the Python code after execution.""",
    input_types={"code": DataType.CODE},
    output_type=DataType.ANY,
    component_group=ComponentGroup.CODERS,
    openai_api_version="$LUNARENV::PYTHON_CODER_OPENAI_API_VERSION",
    deployment_name="$LUNARENV::PYTHON_CODER_DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::PYTHON_CODER_OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::PYTHON_CODER_AZURE_OPENAI_ENDPOINT",
):
    def __init__(
        self,
        model: Optional[ComponentModel] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, configuration=kwargs)
        #TODO: Code generation needs to be handled from within the component.

    @staticmethod
    def execute(code: str):
        local_vars = {}
        exec(code, local_vars)
        return local_vars.get("result", None)

    def run(self, code: str):
        try:
            parse_ast(code.strip())
        except SyntaxError as e:
            raise e
        code_out = PythonCoder.execute(code)

        return code_out
