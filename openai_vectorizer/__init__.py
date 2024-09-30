# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, Optional, List
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import EmbeddedText, DataType
from langchain.embeddings import OpenAIEmbeddings


class OpenAIVectorizer(
    BaseComponent,
    component_name="OpenAI vectorizer",
    component_description="""Use OpenAI models to encode texts. The output is the embeddings
    Output (List[dict]): A list of dictionaries containing the original text (str) and the 
    embeddings (List[Union[float, int]]) for each text item in the input.""",
    input_types={"documents": DataType.LIST},
    output_type=DataType.EMBEDDINGS,
    component_group=ComponentGroup.DATA_VECTORIZERS,
    openai_api_version="$LUNARENV::OPENAI_VECTORIZER_API_VERSION",
    openai_api_key="$LUNARENV::OPENAI_VECTORIZER_API_KEY",
    model_name="$LUNARENV::OPENAI_VECTORIZER_MODEL_NAME",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self._client = OpenAIEmbeddings(**self.configuration)

    def run(self, documents: List[str]):
        embeddings = self._client.embed_documents(documents)

        embedded_texts = []
        for doc, emb in zip(documents, embeddings):
            embedded_texts.append(EmbeddedText(embeddings=emb, text=doc))

        return [emb.dict() for emb in embedded_texts]
