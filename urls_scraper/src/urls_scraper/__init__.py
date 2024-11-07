# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
from typing import Any, List
from urls_scraper.scraper import scrape_urls
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

class URLsScraper(
    LunarComponent,
    component_name="URLs Scraper",
    component_description="""Scrapes URLs.
Inputs:
  `Urls` (List[str]): A list of URLs (strings) that are to be scraped
Output (Dict[str, Dict[str, str]]): A dictionary where each key is a URL from the input list. The value for each key is another dictionary with either a key `content` (str) containing the scraped content as a string (if the request was successful), or a key `error` with a descriptive error message (if the request failed).""",
    input_types={"urls": DataType.LIST},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def __init__(
        self,
        **kwargs: Any,
    ):
        super().__init__(configuration=kwargs)

    def run(self, urls: List[str]):
        if urls and isinstance(urls[0], dict):
            urls = [a["URL"] for a in urls]
        return scrape_urls(urls)
