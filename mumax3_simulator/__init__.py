# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

import requests

class Mumax(
    BaseComponent,
    component_name="MuMax3 Simulator",
    component_description="""MuMax3 Simulator""",
    input_types={"input_mx3_file": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.SIMULATIONS
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(self, input_mx3_file: str):

        # returned_value = os.system(f"./mumax3 {input_mx3_file} 2> {os.getcwd()}/error.txt")
        file_content = {"file": (f"{input_mx3_file}", "mumax file content", "text/plain")}
        response = requests.post("http://20.29.51.115:8000/upload/", files=file_content)
        assert response.status_code == 200

        file_name = input_mx3_file.split("/")[-1]

        response = requests.get("http://20.29.51.115:8000/run-command/", params={"file_name": f"{file_name}"})

        return "Success" if response.status_code == 200 else f"Failure {response.status_code}"
