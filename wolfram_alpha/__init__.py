# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

class WolframAlpha(
    BaseComponent,
    component_name="WolframAlpha client",
    component_description="Obtains a response from the WolframAlpha API.",
    input_types={"query": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.API_TOOLS,
    wolfram_alpha_appid="$LUNARENV::WOLFRAM_ALPHA_APPID",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self._wolfram = WolframAlphaAPIWrapper(
            wolfram_alpha_appid=self.configuration.get(
                "wolfram_alpha_appid", ""
            )
        )

    def run(self, query: str):
        return self._wolfram.run(query)
