# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional
from langchain_community.tools.wikidata.tool import WikidataQueryRun

from lunarcore.component_library.wikidata.wikidata.custom_api_wrapper import CustomWikidataAPIWrapper
from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

class Wikidata(
    BaseComponent,
    component_name="Wikidata client",
    component_description="""Retrieves data from Wikidata API (a knowledge graph / knowledge base).
Inputs:
  `Query` (str): A string of the the term to search for in Wikidata. E.g. `Barack Obama`.
Output (Dict[str, List[Dict]]): A dictionary with the key `results` (str), mapped to a list containing one dictionary of information/knowledge for each query match. E.g. `{`results`: [{`description`: `President of the United States from 2009 to 2017`, ...}]}`. The list is sorted with the best match first.""",
    input_types={"query": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.API_TOOLS,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self._wikidata = WikidataQueryRun(api_wrapper=CustomWikidataAPIWrapper())

    def run(self, query:str):
        return {
            "results": self._wikidata.run(query)
        }
