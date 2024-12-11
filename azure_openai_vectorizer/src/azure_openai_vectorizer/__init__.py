# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, List

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType, EmbeddedText
from langchain_openai import AzureOpenAIEmbeddings


class AzureOpenAIVectorizer(
    LunarComponent,
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
    azure_deployment="$LUNARENV::AZURE_OPENAI_VECTORIZER_DEPLOYMENT_NAME",
    openai_api_key="$LUNARENV::OPENAI_API_KEY",
    azure_endpoint="$LUNARENV::AZURE_OPENAI_ENDPOINT",
    model="$LUNARENV::AZURE_OPENAI_VECTORIZER_MODEL",
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)
        self._client = AzureOpenAIEmbeddings(**self.configuration)

    def run(self, documents: List[str]):
        embeddings = self._client.embed_documents(documents)
        embedded_texts = []
        for doc, emb in zip(documents, embeddings):
            embedded_texts.append(EmbeddedText(embeddings=emb, text=doc))

        return [emb.dict() for emb in embedded_texts]
