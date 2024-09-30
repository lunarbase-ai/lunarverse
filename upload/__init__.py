# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any, Dict
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentModel
from lunarcore.core.typings.datatypes import DataType, File


class UploadComponent(
    BaseComponent,
    component_name="File Upload",
    component_description="""Uploads local files to the server.
    Input (str): A string of the local path of the local file to upload to the server. If needed, tha local path can be inputted manually by the user.
    Output (str): A string of the server path of the uploaded file.""",
    input_types={"input_file": DataType.FILE},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.IO,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self, input_file: Dict):
        if not isinstance(input_file, File):
            input_file = File.model_validate(input_file)
        return self._file_connector.get_absolute_path(input_file.get("path"))
