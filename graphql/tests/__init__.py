# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from lunarcore.component_library.graphql import GraphQLQuery
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.datatypes import DataType

DEFAULT_ENDPOINT = "https://civicdb.org/api/graphql"


def test_graphql_query(endpoint: Optional[str] = None):
    if endpoint is None:
        endpoint = DEFAULT_ENDPOINT
    gql = GraphQLQuery(
        endpoint= endpoint
    )

    gql_input = ComponentInput(
        key="query",
        data_type=DataType.GRAPHQL,
        value="""{
                "query": "query phenotype($id: Int!) {
      phenotype(id: $id) {
        description
        hpoId
        id
        link
        name
        url
      }
    }",
                "variables": {"id": 7467}
            }""",
    )
    result = gql.run(gql_input)
    print(result)


if __name__ == "__main__":
    test_graphql_query()

