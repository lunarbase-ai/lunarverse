# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import unittest.mock as mock

from lunarcore.component_library.bing_search import BingSearch
from unittest.mock import MagicMock

from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.datatypes import DataType


@mock.patch.dict(
    os.environ,
    {
        "BING_SUBSCRIPTION_KEY": "test",
        "BING_SEARCH_URL": "https://www.example.com",
    },
)
def test_bing_search():
    bing_search = BingSearch()
    bing_client_mock = MagicMock()
    bing_client_mock.results.return_value = [
        {
            "title": "Title 1",
            "snippet": "Description 1",
            "link": "https://www.example.com/1",
        },
        {
            "title": "Title 2",
            "snippet": "Description 2",
            "link": "https://www.example.com/2",
        },
    ]
    bing_search._search = bing_client_mock

    bing_search.run(
        ComponentInput(
            key="query",
            data_type=DataType.TEXT,
            value="Some query",
        )
    )

