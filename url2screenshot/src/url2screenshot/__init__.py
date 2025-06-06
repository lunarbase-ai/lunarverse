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
import base64

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult

class URL2Screenshot(
    LunarComponent,
    component_name="URL2Screenshot",
    component_description="""Captures a screenshot of a web page using web crawling.
    Inputs:
        `url` (str): URL of the page to be captured.
    Output (str): Path of the generated (png) file or None if capture fails.""",
    input_types={"url": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self.temp_dir = tempfile.mkdtemp(prefix="url2screenshot_")

    async def run(self, url: str) -> Optional[str]:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace("www.", "")
        domain = re.sub(r'[^a-zA-Z0-9.-]', '_', domain)
        
        path = parsed_url.path.strip("/")
        if not path:
            path = "index"
        path = re.sub(r'[^a-zA-Z0-9/-]', '_', path)
        
        domain_dir = os.path.join(self.temp_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)
        
        screenshot_path = os.path.join(domain_dir, f"{path}.jpg")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

        async with AsyncWebCrawler() as crawler:
            result: CrawlResult = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(screenshot=True),
            )

            if not result.screenshot:
                return None

            try:
                screenshot_bytes = base64.b64decode(result.screenshot)
                with open(screenshot_path, "wb") as f:
                    f.write(screenshot_bytes)
                return screenshot_path
            except:
                return None
