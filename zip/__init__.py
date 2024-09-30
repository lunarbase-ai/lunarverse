# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os.path
from typing import Optional, Any
from zipfile import ZipFile
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

CONFIG_FILE = "./resources/controller.conf"

# TODO: This needs redoing using the file uploader example (for access to the persistence layer)


class ZipFileExtractor(
    BaseComponent,
    component_name="Zip file extractor",
    component_description="""Extracts files from a ZIP file (.zip file) on the server.
Inputs:
  `File path` (str): A string of the server path to the ZIP file to extract. E.g. `/path/on/server/my_zip.zip`
Output (List[str]): A list of the server paths of the files/directories of the extracted ZIP file. E.g. `[`/path/on/server/file1_in_my_zip.txt`, `/path/on/server/file2_in_my_zip.txt`, `/path/on/server/directory1_in_my_zip/`]`""",
    input_types={"file_path": DataType.TEXT},
    output_type=DataType.LIST,
    component_group=ComponentGroup.UTILS,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(self, file_path: str):
        if not isinstance(file_path, str) or not file_path.endswith(".zip"):
            raise ValueError("Input is not a zip file!")

        zfilename = file_path.split(os.path.sep)[-1].split(".")[0]
        with ZipFile(file_path) as zfile:
            os.makedirs(
                os.path.join(self._file_connector.get_absolute_path(""), zfilename),
                exist_ok=True,
            )
            zfile.extractall(
                os.path.join(self._file_connector.get_absolute_path(""), zfilename)
            )
        files = os.listdir(
            os.path.join(self._file_connector.get_absolute_path(""), zfilename)
        )

        return [
            os.path.join(
                self._file_connector.get_absolute_path(""), zfilename, filename
            )
            for filename in files
        ]
