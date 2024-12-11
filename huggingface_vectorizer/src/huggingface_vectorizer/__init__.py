# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Union, List

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType, EmbeddedText
from transformers import AutoTokenizer, AutoModel

class HuggingfaceVectorizer(
    LunarComponent,
    component_name="HuggingFace vectorizer",
    component_description="""Encode texts using HuggingFace's models. The output is the embeddings
    Input (text: List[str], model_name: str): A list of text items to encode and the name of the model to use.
    Output (List[dict]): A list of dictionaries containing the original text (str) and the 
    embeddings (List[Union[float, int]]) for each text item in the input.""",
    input_types={"text": DataType.LIST, "model_name": DataType.TEXT},
    output_type=DataType.EMBEDDINGS,
    component_group=ComponentGroup.DATA_VECTORIZERS,
):
    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)

    def _validate_model_name(self, model_name: str):
        try:
            AutoModel.from_pretrained(model_name)
            AutoTokenizer.from_pretrained(model_name)
        except:
            raise ValueError(f"Model {model_name} not found. Please check the model name.")

    def run(self, text: Union[List[str], str], model_name: str):
        self._validate_model_name(model_name)

        documents = text
        if not isinstance(documents, list):
            documents = [documents]
        embeddings = HuggingFaceEmbeddings(model_name=model_name).embed_documents(documents)

        embedded_texts = []
        for doc, emb in zip(documents, embeddings):
            embedded_texts.append(EmbeddedText(embeddings=emb, text=doc))

        return embedded_texts
    

    