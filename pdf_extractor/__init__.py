# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from typing import Optional, Any

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType
from pdf_extract.pdfservices import PDFServices


CONFIG_FILE = "./resources/controller.conf"


class PDFExtractor(
    BaseComponent,
    component_name="PDF extractor",
    component_description="""Extracts title, sections, references, tables and text from PDF files.
Inputs:
  `File path` (Union[str, List[str]]): A string containing the server path of a PDF file to extract from, or a list of such a server paths.
Output (Dict): A dictionary containing the key-value pairs:
  `title` (str): The title of the PDF file, 
  `sections` (List[Dict]): A list of dictionaries where each dictionary contains a key `title` mapped to the title of the section, and a key `content` mapped to a list of strings of the text content in the section.
  `references` (List[str]): A list of bibliografic references in the PDF file.
  `tables` (List[List[Dict]]]): A list of all tables (created by `table.astype(str).to_dict(orient=`records`) for table in doc_info.tables` where `doc_info = PDFServices(path, credentials).extract(extract_file_path)` from Adobe PDF Services API).
  `text` (List[str]): A list of strings containing the full document text.""",
    input_types={"file_path": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.DATA_EXTRACTION,
    client_id="$LUNARENV::PDFEXTRACTOR_CLIENT_ID",
    client_secret="$LUNARENV::PDFEXTRACTOR_CLIENT_SECRET",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)
        path = self._file_connector.get_absolute_path("")
        credentials = {
            "client_id": self.configuration.get("client_id") or os.environ.get('ADOBE_PDF_CLIENT_ID'),
            "client_secret": self.configuration.get("client_secret") or os.environ.get('ADOBE_PDF_API_KEY')
        }

        self._pdfserv = PDFServices(path, credentials)

    def run(
        self, file_path: str
    ):
        if not isinstance(file_path, str) or not file_path.endswith('.pdf'):
            raise ValueError("Input is not a pdf file!")
        
        doc_info = self._pdfserv.extract(
            self._file_connector.get_absolute_path(file_path)
        )
        
        if (doc_info):
            result = {
                "title": doc_info.title,
                "sections": doc_info.sections,
                "references": doc_info.references,
                "tables": [table.astype(str).to_dict(orient="records") for table in doc_info.tables],
                "text": doc_info.text,
            }
        else:
            result = {
                "title": "",
                "sections": [],
                "references": [],
                "tables": [],
                "text": [],
                "error": "There was a parsing problem with this document"
            }

        return result
