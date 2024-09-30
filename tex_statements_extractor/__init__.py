# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later


from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

from lm_theory.paper_extraction.builders.statements_builder import build_statements


class TexStatementsExtractor(
    BaseComponent,
    component_name="Latex Statements Extractor",
    component_description="""Extracts definitions, axioms, lemmas, theorems, and corollaries stated in Latex codes.
Input:
  `papers` (Dict[str, Dict]): A dict where each key is mapped to a dict with the key `processed_tex` mapped to the Latex code to extract statements from. Eg. {`paper1`: {`processed_tex`: `**some tex code**`}}. Pre-process the tex before, removing its comments, to not extract commented-out statements.
Output (Dict(str, Dict)): The same dict as the one inputted, but in each child dict, a new key `statements` mapped to a dict on the following format
  {
    `definitions`: [
      {
        `statement_id`: **uuid4** (str),
        `statement_original_tex`: **extracted statement tex** (str),
        `proof`: **extracted proof** (str)
      },
      ... **more definitions**
    ],
    `axioms`: [
      {
        `statement_id`: **uuid4** (str),
        `statement_original_tex`: **extracted statement tex** (str)
      },
      ... **more axioms**
    ],
    `lemmas`: [
      {
        `statement_id`: **uuid4** (str),
        `statement_original_tex`: **extracted statement tex** (str),
        `proof`: **extracted proof** (str),
        `corollaries`: **corollary ids** (List[str])
      },
      ... **more lemmas**
    ],
    `theorems`: [
      {
        `statement_id`: **uuid4** (str),
        `statement_original_tex`: **extracted statement tex** (str),
        `proof`: **extracted proof** (str),
        `corollaries`: **corollary ids** (List[str])
      },
      ... **more theorems**
    ],
    `corollaries`: [
      {
        `statement_id`: **uuid4** (str),
        `statement_original_tex`: **extracted statement tex** (str),
        `proof`: **extracted proof** (str),
        `parent_id`: **parent id (theorem/lemma)** (str)
      },
      ... **more corollaries**
    ]
  }
""",
    input_types={
        "papers": DataType.JSON,
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def run(self, papers: dict):
        extracted = dict()
        for paper_id, paper_dict in papers.items():
            paper_dict["statements"] = build_statements(
                paper_dict["processed_tex"], paper_id
            ).model_dump()
            extracted[paper_id] = paper_dict
        return extracted
