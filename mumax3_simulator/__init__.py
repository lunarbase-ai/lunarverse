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
    output_type=DataType.JSON,
    component_group=ComponentGroup.SIMULATIONS
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(self, input_mx3_file: str):
        url = "http://20.29.51.115:8000"
        # returned_value = os.system(f"./mumax3 {input_mx3_file} 2> {os.getcwd()}/error.txt")
        with open(input_mx3_file, "rb") as file:
            files = {"file": file}
            headers = {"accept": "application/json"}
            headers = {
                'accept': 'application/json',
            }
            response = requests.post(url+"/upload/", headers=headers, files=files)

        file_name = input_mx3_file.split("/")[-1]

        response = requests.get(url+"/run-command/", params={"file_name": f"{file_name}"})
        
        if response.status_code != 200:
            raise Exception(f'There has been an error {response.status_code}')

        response = response.json()

        return {"result": response["error"].strip(),"images": []} if (response["error"] and "main.go" in response["error"]) else {"result": "Success","images": response['images']}
