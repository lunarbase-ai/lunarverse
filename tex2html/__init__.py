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

from lm_theory.paper_extraction.utils.tex_processing import tex2html


class Tex2HTML(
    BaseComponent,
    component_name='Latex2HTML',
    component_description="""Converts Latex codes to HTML with Mathjax.
Input:
  `papers` (Dict[str, Dict]): A dict where each key is mapped to a dict with the key `tex` mapped to the Latex code to convert.
Output (Dict(str, Dict)): The same dict as the one inputted, but in each child dict, a new key `html` mapped to a string with the HTML that the corresponding Latex has been converted to.
""",
    input_types={
        'papers': DataType.JSON,
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def run(self, papers: Dict):
        extracted = dict()
        for paper_key, paper_dict in papers.items():
            paper_dict['html'] = tex2html(paper_dict['tex'])
            extracted[paper_key] = paper_dict
        return extracted