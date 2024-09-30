# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, List
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import EmbeddedText, DataType
from langchain_openai import AzureOpenAIEmbeddings


class AzureOpenAIVectorizer(
    BaseComponent,
    component_name="Azure Open AI vectorizer",
    component_description="""Encodes inputted texts as numerical vectors (embeddings) using Azure OpenAI models.
Inputs:
  `documents` (List[str]): A list of texts to encode. If needed, the list can be inputted manually by the user.
Output (List[Dict]): A list of dictionaries -- one for each text in the input. """
    """Each dictionary contains the key `text` (str) mapped to the original text (str), and """
    """the key `embeddings` (str) mapped to the embedding (List[Union[float, int]]).""",
    input_types={"documents": DataType.LIST},
    output_type=DataType.EMBEDDINGS,
    component_group=ComponentGroup.DATA_VECTORIZERS,
    openai_api_version="$LUNARENV::OPENAI_API_VERSION",
    deployment_name="$LUNARENV::DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self._client = AzureOpenAIEmbeddings(**self.configuration)

    def run(self, documents: List[str]):
        embeddings = self._client.embed_documents(documents)
        embedded_texts = []
        for doc, emb in zip(documents, embeddings):
            embedded_texts.append(EmbeddedText(embeddings=emb, text=doc))

        return [emb.dict() for emb in embedded_texts]
