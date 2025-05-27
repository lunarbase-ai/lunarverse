# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

from typing import Any, Optional
import os
import tempfile
from urllib.parse import urlparse
import re

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult

class URL2HTML(
    LunarComponent,
    component_name="URL2HTML",
    component_description="""Converts web pages to HTML files using asynchronous web crawling.
    Inputs:
        `url` (str): Web page URL to be converted to HTML
    Output (str): Path to the generated HTML file or None if conversion fails""",
    input_types={"url": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self.temp_dir = tempfile.mkdtemp()

    async def run(self, url: str) -> Optional[str]:
        parsed_url = urlparse(url)
        filename = re.sub(r'[^a-zA-Z0-9]', '_', parsed_url.path) or "page"
        html_path = os.path.join(self.temp_dir, f"{filename}.html")

        async with AsyncWebCrawler() as crawler:
            result: CrawlResult = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(html=True),
            )

            if not result.html:
                return None

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(result.html)
            return html_path
