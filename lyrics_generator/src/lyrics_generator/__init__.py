# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from typing import Any, Optional

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from langchain_openai import AzureChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.messages import HumanMessage


LYRICS_PROMPT_TEMPLATE = """Write lyrics to a song according to the following instructions:
Theme: {theme}
Mood: {mood}
Setting: {setting}
Key words/phrases: {key_words}
Other instructions: {other_instructions}"""


class LyricsGenerator(
    LunarComponent,
    component_name="Lyrics Generator",
    component_description="""Generates song lyrics from an inputted theme using Azure OpenAI's API (an LLM).
Inputs:
  `Theme` (str): The theme of the song, e.g. `love`.
  `Mood` (str): The mood of the song, e.g. `happy`.
  `Setting` (str): The setting of the song, e.g. `New York`.
  `Key words` (List[str]): Key words in the lyrics, e.g. `[`sunshine`, `forever`]`
  `Other instructions` (str): Other instructions for the generation, e.g. `Each verse should have six lines`
Output (str): The lyrics generated by the LLM.""",
    input_types={
        "theme": DataType.TEXT,
        "mood": DataType.TEXT,
        "setting": DataType.TEXT,
        "key_words": DataType.LIST,
        "other_instructions": DataType.TEMPLATE,
    },
    output_type=DataType.TEXT,
    component_group=ComponentGroup.MUSICGEN,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self._client = AzureChatOpenAI(**self.configuration)

    def run(self, theme: str,
            mood: str,
            setting: str,
            key_words: str,
            other_instructions: str,):

        prompt = PromptTemplate(
            input_variables=[
                "theme",
                "mood",
                "setting",
                "key_words",
                "other_instructions"
            ],
            template=LYRICS_PROMPT_TEMPLATE
        )
        message = HumanMessage(
            content=prompt.format(
                theme=theme,
                mood=mood,
                setting=setting,
                key_words=key_words,
                other_instructions=other_instructions
            )
        )
        try:
            result = self._client.invoke([message]).content
            return str(result).strip("\n").strip().replace('"', "'")
        
        except Exception as e:
            raise RuntimeError(f"An error occurred while generating lyrics: {str(e)}")