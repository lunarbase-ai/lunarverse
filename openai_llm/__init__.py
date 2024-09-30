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
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain

class OpenAIPrompt(
    BaseComponent,
    component_name="OpenAI prompt",
    component_description="""Connects to OpenAI's API, runs natural language prompts and outputs the result as text
    Output (str): The answer provided by the LLM to the prompt.""",
    input_types={"prompt": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.GENAI,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    model_name="$LUNARENV::OPENAI_MODEL_NAME",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

        self._client = ChatOpenAI(**self.configuration)

    def run(
        self, prompt: str
    ):
        prompt_prefix: str = "Question: "
        prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template=prompt_prefix + "{prompt}",
        )
        chain = LLMChain(llm=self._client, prompt=prompt_template)
        chain_results = chain({"prompt": prompt})

        return str(chain_results.get("text", None)).strip("\n").strip()