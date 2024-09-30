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

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


SYSTEM_PROMPT = "You are a helpful AI assistant. Your name is AI Rover."

class AzureOpenAIPrompt(
    BaseComponent,
    component_name="Azure Open AI prompt",
    component_description="""Connects to Azure OpenAI's API (an LLM), runs an inputted natural language prompt (str), and output the result as text (str).
Inputs:
    `user_prompt` (str): The user prompt to provide the LLM with. If needed, the prompt can be inputted manually by the user.
    `system_prompt` (str): The system prompt to provide the LLM with. If needed, the prompt can be inputted manually by the user.
Output (str): The answer provided by the LLM to the prompt.""",
    input_types={"system_prompt": DataType.TEMPLATE, "user_prompt": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.GENAI,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        self._client = AzureChatOpenAI(**self.configuration)

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

        messages = [system_message, user_message]
        result = self._client(messages).content

        return str(result).strip("\n").strip().replace('"', "'")
