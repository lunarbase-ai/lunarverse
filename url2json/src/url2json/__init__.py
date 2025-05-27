# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

from typing import Any, Optional, Dict
import os
import tempfile
from urllib.parse import urlparse
import re
import json

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult

class URL2JSON(
    LunarComponent,
    component_name="URL2JSON",
    component_description="""Converts web pages to JSON using asynchronous web crawling.\nInputs:\n    `url` (str): Web page URL to be converted to JSON\nOutput (dict): A JSON dict with keys 'url' and 'html_content' or None if conversion fails""",
    input_types={"url": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)

    async def run(self, url: str) -> Optional[Dict[str, str]]:
        async with AsyncWebCrawler() as crawler:
            result: CrawlResult = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(html=True),
            )

            if not result.html:
                return None

            return {
                "url": url,
                "html_content": result.html
            } 