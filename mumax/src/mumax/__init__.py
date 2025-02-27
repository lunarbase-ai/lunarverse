# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional
import requests

from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.data_types import DataType


class Mumax(
    LunarComponent,
    component_name="MuMax3 Simulator",
    component_description="""The MuMax3 Simulator component provides an interface to run MuMax3 simulations. """,
    input_types={"input_mx3_file": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.UNCLASSIFIED
):

    def run(self, input_mx3_file: str):
        url = "http://20.29.51.115:8000"
        # returned_value = os.system(f"./mumax3 {input_mx3_file} 2> {os.getcwd()}/error.txt")
        with open(input_mx3_file, "rb") as file:
            files = {"file": file}
            headers = {
                'accept': 'application/json',
            }
            requests.post(url + "/upload/", headers=headers, files=files)

        file_name = input_mx3_file.split("/")[-1]

        response = requests.get(url + "/run-command/", params={"file_name": f"{file_name}"})

        if response.status_code != 200:
            raise Exception(f'There has been an error {response.status_code}')

        response = response.json()

        return {"result": response["error"].strip(), "images": []} if (
                    response["error"] and "main.go" in response["error"]) else {"result": "Success",
                                                                                "images": response['images']}
