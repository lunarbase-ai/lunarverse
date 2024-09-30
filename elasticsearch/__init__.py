# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional, Dict

from lunarcore.core.component import BaseComponent
from lunarcore.core.connectors.elasticsearch import ElasticsearchConnector
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


class Elasticsearch(
    BaseComponent,
    component_name="Elasticsearch client",
    component_description="""Search data in a given Elasticsearch instance.
    Input (dict): a dict containing data expected by Elasticsearch.
    Output (dict): the query response using the python elasticsearch format.""",
    input_types={"query": DataType.JSON},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    hostname="127.0.0.1",
    port="9200",
    username="$LUNARENV::ELASTICSEARCH_USERNAME",
    password="$LUNARENV::ELASTICSEARCH_PASSWORD",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)
        self._elastic_connector = ElasticsearchConnector(
            hostname_or_ip=self.configuration.get("hostname"),
            port=self.configuration.get("port"),
            username=self.configuration.get("username", None),
            password=self.configuration.get("password", None),
        )

    def run(self, query: Dict):
        queries = [query]

        results = []
        for q in queries:
            query_results = self._elastic_connector.query(
                query=q.get("query", dict()),
                size=int(q.get("size", 10)),
                index=q.get("index", None),
                min_score=None,
                request_timeout=60,
            )
            results.extend(list(query_results))

        return {"results": results}