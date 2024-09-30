# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, List, Optional
from lunarcore.core.connectors.milvus import MilvusConnector
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType, EmbeddedText
from lunarcore.core.component import BaseComponent


class MilvusVectorstore(
    BaseComponent,
    component_name="Milvus vectorstore",
    component_description="""Store embeddings on a Milvus server
    Output (dict): a dictionary with a single key (stored), containing the number of stored embeddings.""",
    input_types={"embeddings": DataType.EMBEDDINGS},
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

        self._milvus_connector = MilvusConnector(
            collection_name=self.configuration.get("collection_name"),
            connection_args=connection_args,
        )

    def run(self, embeddings: List):
        embedded_texts: List[DataType.EMBEDDINGS.value] = [
            EmbeddedText.parse_obj(val) for val in embeddings
        ]

        self._milvus_connector.add_texts(
            texts=map(lambda embedded_text: embedded_text.text, embedded_texts),
            embeddings=list(
                map(lambda embedded_text: embedded_text.embeddings, embedded_texts)
            ),
        )

        return {"stored": self._milvus_connector.get_num_entities()}