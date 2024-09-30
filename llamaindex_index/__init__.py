# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Dict, Union, List
import json
import os

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

from llama_index.core import Document
from llama_index.core import ServiceContext, VectorStoreIndex, KeywordTableIndex, SummaryIndex, TreeIndex
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding


class LlamaIndexIndexing(
    BaseComponent,
    component_name='LlamaIndex Indexing',
    component_description="""Index documents from a json dict with Azure OpenAI models within LlamaIndex.
Configuration:
  `index_name` (str): A string with one of the four values `summary`, `vector`, `keyword`, or `tree`
  `index_persist_dir` (str): The name for the storage index (e.g. `IsarMathLib-Summary`)
  `openai_api_key` (str),
  `azure_endpoint` (str): e.g. `https://<endpoint>.openai.azure.com/`,
  `api_version` (str): e.g. `2024-02-01`,
  `llm_model_name` (str): e.g. `gpt-4o`,
  `llm_deployment_name` (str): e.g. `deployment-chatgpt-4o`,
  `emb_model_name`: e.g. `text-embedding-ada-002`,
  `emb_deployment_name`: e.g. `deploymnet-embeddings`
Inputs:
  `Documents Json`: A dictionary containg where each key is a document name mapped to a dictionary with the keys `id`, `source`, and the keys in `key_list_json`. E.g. {`document1`: {`text`: `This is a text about Switzerland. Switzerland is a country in Europe. Its capital is Bern.`, `statement`: `Bern is the capital of Switzerland.`, `id`: `abc123`, `source`: `wikipedia`}}
Output (dict): A dictionary containing the keys:
  `original_json` (dict): copy of the input,
  `index_dir` (str): directory where the index is stored,
  `index_name` (str): name of the stored index,
  `keys_list` (list[str]): list of the stored index keys,
  `llm_config` (dict): configuration of the LLM,
  `embed_model_config` (dict): configuration of the embedding model""",
    input_types={'documents': DataType.JSON, "keys_list": DataType.LIST, "index_name": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATABASES,
    openai_api_key="$LUNARENV::LLAMAINDEX_OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::LLAMAINDEX_AZURE_ENDPOINT",
    api_version="$LUNARENV::LLAMAINDEX_OPENAI_API_VERSION",
    llm_model_name="$LUNARENV::LLAMAINDEX_OPENAI_MODEL_NAME",
    llm_deployment_name="$LUNARENV::LLAMAINDEX_OPENAI_DEPLOYMENT_NAME",
    emb_model_name="$LUNARENV::LLAMAINDEX_OPENAI_EMBEDDINGS_MODEL_NAME",
    emb_deployment_name="$LUNARENV::LLAMAINDEX_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"
):
    INDEX_PERSIST_DIR = "IsarMathLib-Summary"
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

        self._index_name = self.configuration.get('index_name')
        assert self._index_name in ['summary', 'vector', 'keyword', 'tree']

        llamaindex_persist_dir = os.path.join(
            self._file_connector.get_absolute_path(""),
            'llamaindex_persist'
        )
        if not os.path.exists(llamaindex_persist_dir):
            os.mkdir(llamaindex_persist_dir)
        index_dir = os.path.join(llamaindex_persist_dir, 'index')
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
        self._index_persist_dir = os.path.join(index_dir, LlamaIndexIndexing.INDEX_PERSIST_DIR)

        if not self.configuration['openai_api_key']:
            self.configuration['openai_api_key'] = os.environ.get('OPENAI_API_KEY', '')
        if not self.configuration['azure_endpoint']:
            self.configuration['azure_endpoint'] = os.environ.get('AZURE_ENDPOINT', '')
        api_key = self.configuration.get('openai_api_key')
        azure_endpoint = self.configuration.get('azure_endpoint')

        api_version = self.configuration.get('api_version')
        self._llm_config = dict(
            model=self.configuration.get('llm_model_name'),
            deployment_name=self.configuration.get('llm_deployment_name'),
            azure_endpoint=azure_endpoint,
            api_version=api_version
        )
        self._embed_model_config = dict(
            model=self.configuration.get('emb_model_name'),
            deployment_name=self.configuration.get('emb_deployment_name'),
            azure_endpoint=azure_endpoint,
            api_version=api_version
        )
    
        self._llm = AzureOpenAI(api_key=api_key, **self._llm_config)
        self._embed_model = AzureOpenAIEmbedding(api_key=api_key, **self._embed_model_config)
        self._service_context = ServiceContext.from_defaults(
            embed_model=self._embed_model,
            llm=self._llm
        )

    def run(self, documents: Dict, keys_list: Union[str, List[str]], index_name: str = "summary"):
        if type(keys_list) is str:
            keys_list = [s.strip() for s in keys_list.split(',')]
        
        json_dic = documents

        documents = []
        for i in json_dic.keys():
            temp_dic = {key: json_dic[i][key] for key in keys_list}
            documents.append(
                Document(
                    text=json.dumps(temp_dic),
                    metadata={'id': json_dic[i]['id'], 'source': json_dic[i]['source']}
                )
            )

        if self._index_name == 'summary':
            index = SummaryIndex.from_documents(documents, service_context=self._service_context)
        elif self._index_name == 'vector':
            index = VectorStoreIndex.from_documents(documents, service_context=self._service_context)
        elif self._index_name == 'keyword':
            index = KeywordTableIndex.from_documents(documents, service_context=self._service_context)
        else:
            index = TreeIndex.from_documents(documents, service_context=self._service_context)
        index.storage_context.persist(persist_dir=self._index_persist_dir)
        return {
            'original_json': json_dic,
            'index_dir': self._index_persist_dir,
            'index_name': self._index_name,
            'keys_list': keys_list,
            'llm_config': self._llm_config,
            'embed_model_config': self._embed_model_config
        }
