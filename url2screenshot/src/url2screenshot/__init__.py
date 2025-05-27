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

class URL2Screenshot(
    LunarComponent,
    component_name="URL2Screenshot",
    component_description="""Captures a screenshot of a web page (via AsyncWebCrawler) and returns the path of the generated (png) file.
    Inputs:
        `url` (str): URL of the page to be captured.
    Output (str): Path of the generated (png) file or None if capture fails.""",
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
        screenshot_path = os.path.join(self.temp_dir, f"{filename}.png")

        async with AsyncWebCrawler() as crawler:
            result: CrawlResult = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(),
            )

            if not result.screenshot:
                return None

            with open(screenshot_path, "wb") as f:
                f.write(result.screenshot)
            return screenshot_path
