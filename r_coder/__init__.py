# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from rpy2 import robjects

CODE_INPUT_NAME = "Code"


class RCoder(
    BaseComponent,
    component_name="R coder",
    component_description="""Performs customized R code execution. Outputs the value that the R variable `result` is set to during the execution of the R code.
Inputs:
  `Code` (str): A string of the R code to execute.  If needed, the R code can be inputted manually by the user.
Output (Any): The value of the variable `result` in the R code after execution.""",
    input_types={"code": DataType.R_CODE},
    output_type=DataType.ANY,
    component_group=ComponentGroup.CODERS,
    openai_api_version="$LUNARENV::R_CODER_OPENAI_API_VERSION",
    deployment_name="$LUNARENV::R_CODER_DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::R_CODER_OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::R_CODER_AZURE_OPENAI_ENDPOINT",
):
    def __init__(
        self,
        model: Optional[ComponentModel] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, configuration=kwargs)
        # TODO: Code generation needs to be handled from within the component.

    def run(self, code: str):
        robjects.r(code)
        return robjects.r["result"][0]
