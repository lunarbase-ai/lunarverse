# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List
from pymilvus import connections, Collection

from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from lunarcore.component.lunar_component import LunarComponent


class MilvusInsert(
    LunarComponent,
    component_name="Milvus Insert",
    component_description="""Generic Milvus document inserter
    Input: List of documents with any structure
    Output: Number of inserted documents""",
    input_types={"documents": DataType.JSON},
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
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
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

        connections.connect(**connection_args)
        self.collection_name = self.configuration.get("collection_name")

    def run(self, documents: List[dict]):
        collection = Collection(self.collection_name)

        collection.insert(documents)

        connections.disconnect("default")

        return {"inserted": len(documents)} 