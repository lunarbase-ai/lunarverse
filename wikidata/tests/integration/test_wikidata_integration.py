# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import asyncio
import uuid
import pytest
from unittest.mock import MagicMock

from lunarcore.component_library.wikidata import Wikidata
from lunarcore.core.controllers.workflow_controller import WorkflowController
from lunarcore.core.data_models import ComponentDependency, ComponentInput, WorkflowModel
from lunarcore.core.typings.datatypes import DataType
from lunarcore.core.typings.datatypes import DataType
from lunarcore import COMPONENT_REGISTRY


@pytest.mark.asyncio
def test_wikidata_on_workflow_controller():
    wikidata_client_mock = MagicMock()

    mock_result = """
        Result Q1638872:
        Label: document retrieval
        Description: matching of some stated user query against a set of free-text records
        instance of: specialty, field of study

        Result Q58631505:
        Label: SIGNATURES IN SOME NINETEENTH-CENTURY MASSACHUSETTS DUODECIMOS: A QUERY
        instance of: scholarly article
        publication date: 1948
    """

    _, wikidata = COMPONENT_REGISTRY.get_by_class_name("Wikidata")
    wikidata.configuration = {}
    wikidata.inputs = [
        ComponentInput(
            key="query",
            data_type=DataType.TEXT,
            value="Some query",
        )
    ]

    wikidata_client_mock.run.return_value = mock_result

    wikidata._wikidata = wikidata_client_mock

    wc = WorkflowController({})

    workflow_uuid = uuid.uuid4()
    workflow_model = WorkflowModel(
        id=str(workflow_uuid),
        description="Test Wikidata",
        user_id="some_user_id",
        name="Test Wikidata",
        components=[wikidata],
    )

    workflow_result = asyncio.run(wc.run(workflow_model))
    print(workflow_result)
