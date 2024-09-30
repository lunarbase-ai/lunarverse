# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from langchain.embeddings import HuggingFaceEmbeddings
from typing import Any, Optional, Union, List
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import EmbeddedText, DataType


class HuggingfaceVectorizer(
    BaseComponent,
    component_name="HuggingFace vectorizer",
    component_description="""Encode texts using HuggingFace's models. The output is the embeddings
    Output (List[dict]): A list of dictionaries containing the original text (str) and the 
    embeddings (List[Union[float, int]]) for each text item in the input.""",
    input_types={"text": DataType.LIST},
    output_type=DataType.EMBEDDINGS,
    component_group=ComponentGroup.DATA_VECTORIZERS,
    model_name="$LUNARENV::HUGGINGFACE_VECTORIZER_MODEL_NAME",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)
        self._model_name = self.configuration.get("model_name")

    def run(self, text: Union[List[str], str]):
        documents = text
        if not isinstance(documents, list):
            documents = [documents]
        embeddings = HuggingFaceEmbeddings(model_name=self._model_name).embed_documents(
            documents
        )

        embedded_texts = []
        for doc, emb in zip(documents, embeddings):
            embedded_texts.append(EmbeddedText(embeddings=emb, text=doc))

        return embedded_texts
