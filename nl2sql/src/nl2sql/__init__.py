# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, List

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from lunar_nl2sql.services.ai import AzureOpenAIService
from lunar_nl2sql.indexers.indexer import Indexer
from lunar_nl2sql.retrievers.context_retriever import ContextRetriever
from lunar_nl2sql.generators.generator import Generator
from nl2sql.data_source_factory import data_source_factory

class NL2SQL(
    LunarComponent,
    component_name="NL2SQL",
    component_description="""Transforms natural language queries into SQL queries.""",
    input_types={"questions": DataType.LIST, "db_type": DataType.TEXT, "db_config": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.NLP,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT"
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self.ai_service = AzureOpenAIService({
            "openai_api_key": self.configuration["openai_api_key"],
            "openai_api_version": self.configuration["openai_api_version"],
            "azure_endpoint": self.configuration["azure_endpoint"],
            "model": self.configuration["deployment_name"]
        })

    def run(self, questions: List[str], db_type: str, db_config: dict) -> dict:
        data_source = data_source_factory(db_type, db_config)

        indexer = Indexer(self.ai_service, data_source)
        context_retriever = ContextRetriever(self.ai_service, indexer)

        generator = Generator(self.ai_service, context_retriever)

        result = {}
        for nl_query in questions:
            result[nl_query] = generator.generate(nl_query)
        return result