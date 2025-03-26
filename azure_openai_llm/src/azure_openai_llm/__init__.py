# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from openai import AzureOpenAI

SYSTEM_PROMPT = "You are a helpful AI assistant. Your name is AI Rover."

class AzureOpenAIPrompt(
    LunarComponent,
    component_name="Azure Open AI prompt",
    component_description="""Connects to Azure OpenAI's API (an LLM), runs an inputted natural language prompt (str), and outputs the result as text (str).
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
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        # Configure the OpenAI library for Azure OpenAI usage.
        self._client = AzureOpenAI(
            api_key=self.configuration["openai_api_key"],
            api_version=self.configuration["openai_api_version"],
            base_url=self.configuration["azure_endpoint"]
        )

    def run(self, user_prompt: str, system_prompt: str = SYSTEM_PROMPT):
        # Create the messages list in the required format.
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Call the OpenAI Chat Completion endpoint.
        response = self._client.chat.completions.create(
            model=self.configuration["deployment_name"],
            messages=messages,
        )
        # Extract the assistant's reply from the response.
        result = response.choices[0].message.content

        # Clean up the result string and return it.
        return str(result).strip("\n").strip().replace('"', "'")
