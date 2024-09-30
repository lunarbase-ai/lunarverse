# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import unittest.mock as mock

from unittest.mock import MagicMock

from lunarcore.component_library.wolfran_alpha import WolframAlpha
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.datatypes import DataType


@mock.patch.dict(
    os.environ,
    {
        "WOLFRAM_ALPHA_APPID": "test",
    },
)
def test_wolfran_alpha():
    wolfran_alpha = WolframAlpha()
    wolfran_alpha_client_mock = MagicMock()

    mock_result = "x = 2/5"

    wolfran_alpha_client_mock.run.return_value = mock_result

    wolfran_alpha._wolfram = wolfran_alpha_client_mock

    assert wolfran_alpha.run(
        ComponentInput(
            key="query",
            data_type=DataType.TEXT,
            value="Some query",
        )
    ) == mock_result
