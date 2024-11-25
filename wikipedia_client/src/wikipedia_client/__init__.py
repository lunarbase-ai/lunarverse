# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import wikipedia

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType


class Wikipedia(
    LunarComponent,
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
            "content": page.content,
            "summary": page.summary
        }
