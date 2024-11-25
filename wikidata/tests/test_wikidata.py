# # SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
# #
# # SPDX-License-Identifier: GPL-3.0-or-later

# from unittest.mock import MagicMock

# from lunarcore.component_library.wikidata import Wikidata
# from lunarcore.core.data_models import ComponentInput
# from lunarcore.core.typings.datatypes import DataType
# from lunarcore.core.typings.datatypes import DataType


# def test_wikidata():
#     wikidata = Wikidata()
#     wikidata_client_mock = MagicMock()

#     mock_result = [
#         {
#             "id": "Q1638872",
#             "label": "document retrieval",
#             "description": "matching of some stated user query against a set of free-text records",
#             "instance_of": ["specialty", "field of study"],
#         },
#         {
#             "id": "Q58631505",
#             "label": "SIGNATURES IN SOME NINETEENTH-CENTURY MASSACHUSETTS DUODECIMOS: A QUERY",
#             "instance_of": ["scholarly article"],
#             "publication_date": "1948",
#         },
#     ]

#     wikidata_client_mock.run.return_value = mock_result

#     wikidata._wikidata = wikidata_client_mock

#     assert wikidata.run(
#         ComponentInput(
#             key="query",
#             data_type=DataType.TEXT,
#             value="Some query",
#         )
#     ) == {
#         "results": mock_result
#     }
