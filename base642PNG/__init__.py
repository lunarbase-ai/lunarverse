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

class Base64PNG(
    BaseComponent,
    component_name="Base64 to PNG",
    component_description="""Convert Base64 to PNG""",
    input_types={"base64_text": DataType.TEXT},
    output_type=DataType.IMAGE,
    component_group=ComponentGroup.UTILS
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(self, base64_text: str):

        return base64_text
