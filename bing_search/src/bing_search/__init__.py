# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from langchain_community.utilities import BingSearchAPIWrapper


class BingSearch(
    LunarComponent,
    component_name="Bing Search client",
    component_description="Searches data using Bing Search API.",
    input_types={"query": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.API_TOOLS,
    bing_search_url="https://api.bing.microsoft.com/v7.0/search",
    bing_subscription_key="$LUNARENV::BING_SUBSCRIPTION_KEY",
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)
        self._search = BingSearchAPIWrapper(
            bing_search_url=self.configuration.get("bing_search_url", ""),
            bing_subscription_key=self.configuration.get("bing_subscription_key"),
        )

    def run(self, query: str):
        results = self._search.results(str(query).strip(), 10)

        return {"results": results}