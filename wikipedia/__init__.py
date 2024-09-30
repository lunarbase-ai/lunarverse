# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import wikipedia

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

class Wikipedia(
    BaseComponent,
    component_name="Wikipedia client",
    component_description="""Retrieves data from Wikipedia API.
Input:
  `Query` (str): A string of the query to use for finding the article. Eg. `Fermats last theorem`.
Output (Dict[str, str]): A dictionary with the string `content` mapped to a string of the content of the found article.""",
    input_types={"query": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.API_TOOLS,
):
    def run(self, query: str):
        page = None
        try:
            page = wikipedia.page(query)
        except wikipedia.exceptions.DisambiguationError as e:
            pass

        return {
            # "results": wikipedia.search(inputs.value),
            "content": page.content,
            "summary": page.summary
        }
