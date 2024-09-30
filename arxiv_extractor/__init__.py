# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from typing import List

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

from lm_theory.paper_extraction.extraction.tex_extraction.arxiv_extraction import ArxivExtraction


class ArxivExtractor(
    BaseComponent,
    component_name='Arxiv Extractor',
    component_description="""Extracts titles, authors, latex code, etc. of Arxiv papers.
Input:
  `arxiv_ids` (List[str]): A list of strings of Arxiv ID's to extract (eg. [`2406.17837`, `2006.04710`])
Output (Dict[str, Dict]): A dict where each key is a string of the Arxiv ID, and the value is a dict with the following string keys:
  `title` (str): The title of the paper,
  `authors` (List[str]): A list of the authors,
  `tex` (str): The latex code,
  `bibtex` (str): The bibtex of the paper,
  `paper_url` (str): An URL to the arxive paper
""",
    input_types={'arxiv_ids': DataType.LIST},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def run(self, arxiv_ids: List):
        ARXIVE_EXTRACT_DIR = os.path.join(
            self._file_connector.get_absolute_path(""),
            'arxiv_extractions'
        )
        os.makedirs(ARXIVE_EXTRACT_DIR, exist_ok=True)
        arxiv_extractions = {}
        for arxiv_id in arxiv_ids:
            extraction = ArxivExtraction(arxiv_id, ARXIVE_EXTRACT_DIR)
            arxiv_extractions[arxiv_id] = {
                'title': extraction.get_title(),
                'authors': extraction.get_authors(),
                'tex': extraction.get_tex(),
                'bibtex': extraction.get_bibtex(),
                'paper_url': extraction.get_paper_url()
            }

        return arxiv_extractions