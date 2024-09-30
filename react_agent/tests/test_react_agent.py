# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import unittest.mock as mock

from lunarcore.component_library.react_agent import ReactAgent

from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.datatypes import DataType


@mock.patch(
    "lunarcore.component_library.react_agent.load_tools", mock.MagicMock()
)
@mock.patch(
    "lunarcore.component_library.react_agent.create_react_agent", mock.MagicMock()
)
@mock.patch(
    "lunarcore.component_library.react_agent.AgentExecutor", mock.MagicMock()
)
@mock.patch(
    "lunarcore.component_library.react_agent.hub", mock.MagicMock()
)
@mock.patch.dict(
    os.environ,
    {
        "OPENAI_API_KEY": "test",
    },
)
def test_react_agent():
    react_agent = ReactAgent()

    react_agent.run([
        ComponentInput(
            key="query",
            data_type=DataType.TEXT,
            value="Some query",
        ),
        ComponentInput(
            key="tools",
            data_type=DataType.LIST,
            value=["wolfran-alpha"],
        )
    ])

