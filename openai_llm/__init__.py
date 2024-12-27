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

from langchain.prompts.prompt import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from openai import OpenAI

SYSTEM_PROMPT = "You are a helpful AI assistant. Your name is AI Rover."

class OpenAIPrompt(
    BaseComponent,
    component_name="OpenAI prompt",
    component_description="""Connects to OpenAI's API, runs natural language prompts and outputs the result as text
    Output (str): The answer provided by the LLM to the prompt.""",
    input_types={"system_prompt": DataType.TEMPLATE, "user_prompt": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.GENAI,
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    openai_model="$LUNARENV::OPENAI_MODEL",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

        self._client = OpenAI(api_key=self.configuration.get('openai_api_key'))

    def run(self, user_prompt: str, system_prompt: str = SYSTEM_PROMPT):
        user_prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template="{prompt}",
        )
        system_prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template="{prompt}",
        )

        system_message = SystemMessage(content=system_prompt_template.format(prompt=system_prompt))
        user_message = HumanMessage(content=user_prompt_template.format(prompt=user_prompt))

        messages = [
            {"role": "system", "content": system_message.content},
            {"role": "user", "content": user_message.content}
        ]

        chat_completion = self._client.chat.completions.create(
            messages=messages,
            model=self.configuration.get('openai_model'),
        )

        return chat_completion.choices[0].message.content