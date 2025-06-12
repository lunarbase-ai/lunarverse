# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional
from langchain_community.tools.wikidata.tool import WikidataQueryRun

from wikidata.custom_api_wrapper import CustomWikidataAPIWrapper

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

class Wikidata(
    LunarComponent,
    component_name="Wikidata client",
    component_description="""Retrieves data from Wikidata, enabling users to access structured, linked information from a vast open knowledge base.
Inputs:
  `Query` (str): A string of the the term to search for in Wikidata. E.g. `Barack Obama`.
Output (Dict[str, List[Dict]]): A dictionary with the key `results` (str), mapped to a list containing one dictionary of information/knowledge for each query match. E.g. `{`results`: [{`description`: `President of the United States from 2009 to 2017`, ...}]}`. The list is sorted with the best match first.""",
    input_types={"query": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.API_TOOLS,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
        self._wikidata = WikidataQueryRun(api_wrapper=CustomWikidataAPIWrapper())

    def run(self, query:str):
        if not query:
            return {"results": []}
        return {
            "results": self._wikidata.run(query)
        }
