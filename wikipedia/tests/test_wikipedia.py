# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import unittest.mock as mock

from unittest.mock import MagicMock

from lunarcore.component_library.wikipedia import Wikipedia
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.datatypes import DataType


@mock.patch(
    "wikipedia.search"
)
@mock.patch(
    "wikipedia.page"
)
def test_wikipedia(mock_wikipedia_page, mock_wikipedia_search):
    wikipedia = Wikipedia()

    mock_result = [
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
    mock_page_result = MagicMock()

    mock_wikipedia_search.return_value = mock_result
    mock_wikipedia_page.return_value = mock_page_result

    results = wikipedia.run(
        ComponentInput(
            key="query",
            data_type=DataType.TEXT,
            value="Query plan",
        )
    )

    assert results == {
        "results": mock_result,
        "page": mock_page_result
    }

