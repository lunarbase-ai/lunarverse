# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Any, Optional, List

from lunarcore.core.component import BaseComponent
from lunarcore.core.connectors.elasticsearch import ElasticsearchConnector
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


class ElasticsearchStore(
    BaseComponent,
    component_name="Elasticsearch store",
    component_description="Stores data in a given Elasticsearch instance for future search.",
    input_types={"data": DataType.LIST},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    hostname="127.0.0.1",
    port="9200",
    username="$LUNARENV::ELASTICSEARCH_USERNAME",
    password="$LUNARENV::ELASTICSEARCH_PASSWORD",
    index=None,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self._elastic_connector = ElasticsearchConnector(
            hostname_or_ip=self.configuration.get("hostname"),
            port=self.configuration.get("port"),
            username=self.configuration.get("username", None),
            password=self.configuration.get("password", None),
            default_index=self.configuration.get("index", None),
        )

    def run(self, data: List):
        insert_results = self._elastic_connector.insert(
            data=data,
            index=self.configuration.get("index", None),
            index_mapping=None,
        )

        return {"results": insert_results}
