# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Dict
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType, File


class FileUpload(
    LunarComponent,
    component_name="File Upload",
    component_description="""Uploads local files to the server.
    Input (str): A string of the local path of the local file to upload to the server. If needed, tha local path can be inputted manually by the user.
    Output (str): A string of the server path of the uploaded file.""",
    input_types={"input_file": DataType.FILE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.IO,
):
    def run(self, input_file: Dict):
        if not isinstance(input_file, File):
            input_file = File.model_validate(input_file)
        return self._file_connector.get_absolute_path(input_file.get("path"))
