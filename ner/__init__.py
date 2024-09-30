# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any
import re
import spacy
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType


def clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = text.strip()
    text = re.sub("r\n{2,}", "\n", text)
    return text


class Ner(
    BaseComponent,
    component_name="Spacy NER",
    component_description="""Performs Named Entity Recognition (NER).
Inputs:
  `Text` (str): The text to perform NER on.
Output (List[Dict[str, str]]): A list of dictionaries containing two keys: `text` (str) mapped to the word/text (str), and `label` (str) mapped to the NER label (str). Eg. [{`text`: `Albert Einstein`, `label`: `PERSON`}, {`text`: `1879`, `label`: `DATE`}]""",
    input_types={"text": DataType.TEMPLATE},
    output_type=DataType.LIST,
    component_group=ComponentGroup.NLP,
    model_name="en_core_web_sm",
):
    def __init__(
        self,
        model: Optional[ComponentModel] = None,
        **kwargs,
    ):
        super().__init__(model=model, configuration=kwargs)
        model_name = self.configuration.get("model_name")
        if not spacy.util.is_package(model_name):
            spacy.cli.download(model_name)
        self._nlp = spacy.load(model_name)

    @property
    def nlp(self):
        return self._nlp

    @staticmethod
    def get_subject_phrase(sentence, full_text: Optional = None):
        for token in sentence:
            if "subj" in token.dep_ or "ROOT" in token.dep_:
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                if full_text is None:
                    yield sentence[start:end]
                else:
                    yield full_text[start:end]

    @staticmethod
    def get_object_phrase(sentence, full_text: Optional = None):
        for token in sentence:
            if "obj" in token.dep_:
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                if full_text is None:
                    yield sentence[start:end]
                else:
                    yield full_text[start:end]

    def run(
        self,
        text: str,
    ):
        processed_text = self._nlp(clean_text(text))
        entities = [
            {"text": ent.text, "label": ent.label_} for ent in processed_text.ents
        ]
        return entities
