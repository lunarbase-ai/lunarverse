# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

from typing import Any, Optional, Dict

from lunarcore.core.component import BaseComponent
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.typings.datatypes import DataType

from lm_theory.paper_extraction.data_models.paper_database import PaperDatabase


class PaperDatabaseBuilder(
    BaseComponent,
    component_name="Paper Database Builder",
    component_description="""Builds a JSON with data of scientific papers.
Input:
  `papers` (Dict[str, Dict]): A dict where each key is a string of the Arxiv ID, and the value is a dict with the following string keys:
    `title` (str): The title of the paper,
    `authors` (List[str]): A list of the authors,
    `tex` (str): The latex code,
    `bibtex` (str): The bibtex of the paper,
    `paper_url` (str): An URL to the paper
  `loaded_database_json` (str): JSON str of an existing database to extend (set empty if there is no yet)
  `save_path` (str): A path to a JSON file where the database will be saved (set empty to not save)
  `pages_root` (str): The path to the root directory of generated HTML pages (set empty if no HTML pages are to be generated)
Output (Dict(str, Any)): A dict with data extracted 
""",
    input_types={
        "papers": DataType.JSON,
        "loaded_database_json": DataType.TEXT,
        "save_path": DataType.TEXT,
        "pages_root": DataType.TEXT,
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
    extend_db=1,
    overwrite_existing_db=0,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        print(kwargs)
        super().__init__(model=model, configuration=kwargs)

    def run(self, 
            papers: Dict,
            loaded_database_json: str,
            save_path: str,
            pages_root: str):
                
        if loaded_database_json:
            db = PaperDatabase.model_validate_json(loaded_database_json)
        else:
            arxiv_extract_dir = os.path.join(
                self._file_connector.get_absolute_path(""), "arxiv_extractions"
            )
            db = PaperDatabase(
                db_path=save_path,
                extraction_dir=arxiv_extract_dir,
                pages_root=pages_root,
            )
        db.add_dict_papers(papers)
        if self.configuration["extend_db"] in [True, 1, "True", "1"]:
            db.extend(
                overwrite=self.configuration["overwrite_existing_db"]
                in [True, 1, "True", "1"]
            )
        db.add_dict_papers(papers)
        if self.configuration['extend_db'] in [True, 1, 'True', '1']:
            db.extend(overwrite=self.configuration['overwrite_existing_db'] in [True, 1, 'True', '1'])
        if save_path:
            db.db_path = save_path
            db.save()
        return db.model_dump()
