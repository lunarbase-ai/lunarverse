# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Lunarbase <contact@lunarbase.ai>
#
# SPDX-License-Identifier: LicenseRef-lunarbase

from typing import Any, Optional, Dict
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult, LLMExtractionStrategy, LLMConfig

class URL2LLM(
    LunarComponent,
    component_name="URL2LLM",
    component_description="Extracts information from web pages using LLM. Input: url (str): Web page URL, instruction (str): LLM instruction. Output: JSON with url and extracted_content",
    input_types={"url": DataType.TEXT, "instruction": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
    api_key_token="$LUNARENV::API_KEY_TOKEN",
    base_url="$LUNARENV::BASE_URL",
    provider="$LUNARENV::PROVIDER",
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self.llm_config = LLMConfig(
            provider=self.configuration["provider"],
            base_url=self.configuration["base_url"],
            api_token=self.configuration["api_key_token"]
        )

    async def run(self, url: str, instruction: str) -> Optional[Dict[str, str]]:
        extraction_strategy = LLMExtractionStrategy(
            llm_config=self.llm_config,
            instruction=instruction,
        )

        config = CrawlerRunConfig(
            extraction_strategy=extraction_strategy,
            exclude_external_links=True        
            )

        async with AsyncWebCrawler() as crawler:
            result: CrawlResult = await crawler.arun(url, config=config)

            if not result.extracted_content:
                return None

            return {
                "url": url,
                "extracted_content": result.extracted_content.strip()
            } 