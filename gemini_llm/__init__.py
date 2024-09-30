# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from typing import Any, Optional

import requests

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType

from langchain.prompts.prompt import PromptTemplate
from langchain_core.messages import HumanMessage

from lunarcore.errors import ComponentError


class GeminiAIPrompt(
    BaseComponent,
    component_name="Gemini AI prompt",
    component_description="""Connects to Gemini's API, runs natural language prompts and outputs the result as text
    Output (str): The answer provided by the LLM to the prompt.""",
    input_types={"prompt": DataType.TEMPLATE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.GENAI,
    api_key="$LUNARENV::GEMINI_API_KEY",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        if not self.configuration["api_key"]:
            self.configuration["api_key"] = os.environ.get("GEMINI_API_KEY", "")

    def run(self, prompt: str):
        prompt_prefix: str = "Question: "
        prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template=prompt_prefix + "{prompt}",
        )
        message = HumanMessage(content=prompt_template.format(prompt=prompt))

        request_body = {
            "contents": [{"role": "user", "parts": [{"text": message.content}]}]
        }

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.configuration['api_key']}"

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 200:
            data = response.json()
            if (
                len(data["candidates"]) > 0
                and len(data["candidates"][0]["content"]["parts"]) > 0
            ):
                result = data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                raise ValueError(f"Failed to parse Gemini's response: {data}")
        else:
            raise ComponentError(f"Error: {response.status_code} {response.text}")

        return str(result).strip("\n").strip().replace('"', "'")
