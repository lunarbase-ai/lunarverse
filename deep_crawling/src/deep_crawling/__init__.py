# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional, Dict, List

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult, LLMExtractionStrategy, LLMConfig, BFSDeepCrawlStrategy

class DeepCrawling(
    LunarComponent,
    component_name="DeepCrawling",
    component_description="Extracts information from web pages using LLM with BFS traversal. Inputs: url (str): Starting URL, instruction (str): LLM instruction, include_external (bool): Follow external links, max_depth (int): BFS depth. Output: Dict with url and extracted_content",
    input_types={
        "url": DataType.TEXT,
        "instruction": DataType.TEXT,
        "include_external": DataType.BOOL,
        "max_depth": DataType.INT
    },
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

    async def run(
        self,
        url: str,
        instruction: str,
        include_external: bool = False,
        max_depth: int = 2
    ) -> Optional[Dict[str, Any]]:
        extraction_strategy = LLMExtractionStrategy(
            llm_config=self.llm_config,
            instruction=instruction,
        )

        config = CrawlerRunConfig(
            extraction_strategy=extraction_strategy,
            exclude_external_links=not include_external,
            deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=max_depth, include_external=include_external)
        )

        async with AsyncWebCrawler() as crawler:
            results: List[CrawlResult] = await crawler.arun(url, config=config)

            if not results:
                return None

            combined_content = []
            for result in results:
                if result.extracted_content:
                    combined_content.append(result.extracted_content.strip())

            if not combined_content:
                return None

            return {
                "url": url,
                "extracted_content": "\n\n".join(combined_content)
            } 