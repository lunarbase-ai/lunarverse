# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any

from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.data_types import DataType
from pubmed_searcher.src.pubmed_searcher import (
    async_pubmed_scraper as pubmed_scraper,
)

class PubmedSearcher(
    LunarComponent,
    component_name="Pubmed Searcher",
    component_description="""Search article information from Pubmed by keywords
Inputs:
  `Keywords` (str): TODO,
  `From year` (str): TODO,
  `To year` (str): TODO,
  `Max pages` (str): TODO,
Output (List[Dict]): a record formatted pandas dataframe with the search results.""",
    input_types={
        "keywords": DataType.TEXT,
        "from_year": DataType.INT,
        "to_year": DataType.INT,
        "max_pages": DataType.INT,
    },
    output_type=DataType.LIST,
    component_group=ComponentGroup.BIOMEDICAL,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)

    def run(self, keywords: str, from_year: int, to_year: int, max_pages: int):
        results = pubmed_scraper.main(max_pages, keywords, from_year, to_year)

        return results.fillna("").to_dict(orient="records")
