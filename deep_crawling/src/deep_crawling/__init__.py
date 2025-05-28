# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional, Dict

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult, LLMExtractionStrategy, LLMConfig

class DeepCrawling(
    LunarComponent,
    component_name="DeepCrawling",
    component_description="""Extracts information from web pages and their linked pages using LLM (Large Language Model) with BFS traversal.\nInputs:\n    `url` (str): Starting web page URL\n    `instruction` (str): Instruction for the LLM to extract desired information\n    `include_external` (bool): Whether to follow external links\n    `max_depth` (int): Maximum depth for BFS traversal\nOutput (dict): A dictionary with 'url' and 'extracted_content' keys containing the LLM response for each visited page""",
    input_types={
        "url": DataType.TEXT,
        "instruction": DataType.TEXT,
        "include_external": DataType.BOOLEAN,
        "max_depth": DataType.NUMBER
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
    provider="$LUNARENV::PROVIDER",
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self.llm_config = LLMConfig(
            provider=self.configuration["provider"],
            base_url=self.configuration["azure_endpoint"],
            api_token=self.configuration["openai_api_key"]
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
            max_pages=max_depth
        )

        async with AsyncWebCrawler() as crawler:
            result: CrawlResult = await crawler.arun(url, config=config)

            if not result.extracted_content:
                return None

            return {
                "url": url,
                "extracted_content": result.extracted_content.strip(),
                "visited_urls": result.visited_urls,
                "depth": result.depth
            } 