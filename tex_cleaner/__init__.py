# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Dict

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

from lm_theory.paper_extraction.utils.tex_processing import process_tex_extraction


class TexCleaner(
    BaseComponent,
    component_name="Latex Cleaner",
    component_description="""Cleans up Latex codes a by removing its comments and expanding its restatables.
Input:
  `papers` (Dict[str, Dict]): A dict where each key is mapped to a dict with the key `tex` mapped to the Latex code to process. Eg. {`paper1`: {`tex`: `**some tex code**`}}.
Output (Dict(str, Dict)): The same dict as the one inputted, but in each child dict, a new key `processed_tex` is mapped to the processed Latex code.
""",
    input_types={
        "papers": DataType.JSON,
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def run(self, papers: Dict):
        extracted = dict()
        for paper_key, paper_dict in papers.items():
            tex = paper_dict["tex"]
            processed_tex = process_tex_extraction(tex)
            paper_dict["processed_tex"] = processed_tex
            extracted[paper_key] = paper_dict
        return extracted
