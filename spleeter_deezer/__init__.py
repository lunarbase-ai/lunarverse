# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any, List

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

import os

class DeezerSpleeter(
    BaseComponent,
    component_name="Deezer Spleeter",
    component_description="""Deezer Spleeter""",
    input_types={"input_folder": DataType.TEXT},
    output_type=DataType.LIST,
    component_group=ComponentGroup.MUSICGEN,
    client_id="$LUNARENV::DEEZER_CLIENT_ID",
    client_secret="$LUNARENV::DEEZER_CLIENT_SECRET",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(
        self, input_folder: str
    ):
        output = "/".join(inputs.value.split("/")[:-2])
        os.system(f"spleeter separate -p spleeter:5stems -o {output} {input_folder}")

        return [f'{output}/{inputs.value.split("/")[-1].split(".")[0]}/{file}' for file in ["vocals.wav","piano.wav","drums.wav","bass.wav","other.wav"]]
