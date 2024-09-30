# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from typing import Any, Optional, Dict

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

from llama_index.core import ServiceContext, StorageContext, load_index_from_storage
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.retrievers.bm25 import BM25Retriever


class LlamaIndexQuerying(
    BaseComponent,
    component_name="LlamaIndex Querying",
    component_description="""Querying from LlamaIndex index.
Configuration:
  `retrieval_only` (str): A string with the value `True` or `False`.
  `top_k` (str): The number k of the best matches that should be retrived if retrival_only
Inputs:
  `Index Details Json` (dict): A dictionary containing the keys:
  `original_json` (dict): copy of the input,
  `index_dir` (str): directory where the index is stored,
  `index_name` (str): name of the stored index,
  `keys_list` (list[str]): list of the stored index keys,
  `llm_config` (dict): configuration of the LLM,
  `embed_model_config` (dict): configuration of the embedding model
Output: A dictionary with the keys `Top_1`, `Top_2`, ..., `Top_k` if retrival_only, else a dictionary with the key `Response`""",
    input_types={"index_details_json": DataType.JSON, "query": DataType.TEMPLATE},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    retrieval_only="True",
    top_k=3,
    openai_api_key="$LUNARENV::LLAMAINDEX_OPENAI_API_KEY",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self._retrieval_only = self.configuration.get("retrieval_only")
        assert self._retrieval_only in ["True", "False"]
        self._retrieval_only = True if self._retrieval_only == "True" else False
        self._top_k = self.configuration.get("top_k")

    def run(self, index_details_json: Dict, query: str):
        original_json = index_details_json["original_json"]
        id_to_data = {
            original_json[key]["id"]: original_json[key] for key in original_json.keys()
        }
        keys_list = index_details_json["keys_list"]
        index_dir = index_details_json["index_dir"]
        llm_config = index_details_json["llm_config"]
        embed_model_config = index_details_json["embed_model_config"]

        if not self.configuration['openai_api_key']:
            self.configuration['openai_api_key'] = os.environ.get('OPENAI_API_KEY', '')
        api_key = self.configuration.get('openai_api_key')

        llm = AzureOpenAI(api_key=api_key, **llm_config)
        embed_model = AzureOpenAIEmbedding(api_key=api_key, **embed_model_config)
        service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(
            storage_context, service_context=service_context
        )

        res = {"Query": query}
        if self._retrieval_only:
            retriever = BM25Retriever.from_defaults(
                docstore=index.docstore,
                similarity_top_k=min(len(original_json), self._top_k)
            )
            nodes = retriever.retrieve(res["Query"])
            for i in range(len(nodes)):
                res[f"Top {i+1}"] = {
                    key: id_to_data[nodes[i].metadata["id"]][key] for key in keys_list
                }
        else:
            query_engine = index.as_query_engine()
            response = query_engine.query(res["Query"])
            response = response.__dict__
            response['source_nodes'] = [node_with_score.to_dict() for node_with_score in response['source_nodes']]
            res["Response"] = response
        return res
