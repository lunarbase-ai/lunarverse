# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional, List

from lunarcore.core.connectors.milvus import MilvusConnector
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType, EmbeddedText
from lunarcore.core.component import BaseComponent


class MilvusRetriever(
    BaseComponent,
    component_name="Milvus retriever",
    component_description="""Queries embeddings from a Milvus server
    Output (List[dict]): A list of dictionaries containing the original text (str) and the 
    embeddings (List[Union[float, int]]) for each text item in the input.""",
    input_types={"query_embedding": DataType.EMBEDDINGS},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    collection_name=None,
    host=None,
    uri=None,
    port=None,
    user="$LUNARENV::MILVUS_USER",
    password="$LUNARENV::MILVUS_PASSWORD",
    token="$LUNARENV::MILVUS_TOKEN",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        connection_args = dict()
        if self.configuration.get("host") is not None:
            connection_args["host"] = self.configuration.get("host")
        if self.configuration.get("port") is not None:
            connection_args["port"] = self.configuration.get("port")
        if self.configuration.get("uri") is not None:
            connection_args["uri"] = self.configuration.get("uri")
        if self.configuration.get("user") is not None:
            connection_args["user"] = self.configuration.get("user")
        if self.configuration.get("password") is not None:
            connection_args["password"] = self.configuration.get("password")
        if self.configuration.get("token") is not None:
            connection_args["token"] = self.configuration.get("token")

        self._milvus_connector = MilvusConnector(collection_name=self.configuration.get("collection_name"),
                                                 connection_args=connection_args)

    def run(self, query_embedding: List):
        results = []
        embedded_text_list = query_embedding
        for embedded_text in embedded_text_list:
            embedded_text = EmbeddedText.parse_obj(embedded_text)
            similarity_search_result = self._milvus_connector.similarity_search_with_score_by_vector(
                embedding=embedded_text.embeddings
            )
            results.extend(similarity_search_result)

        return {"results": results}
