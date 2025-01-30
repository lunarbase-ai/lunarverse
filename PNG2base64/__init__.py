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

import base64

class PNG2Base64(
    BaseComponent,
    component_name="PNG to Base64",
    component_description="""Convert PNG to Base64""",
    input_types={"image_path": DataType.TEXT},
    output_type=DataType.IMAGE,
    component_group=ComponentGroup.UTILS
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(self, image_path: str):

        try:
            with open(image_path, "rb") as image_file:
                base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
                return f"data:image/png;base64,{base64_encoded}"
        except FileNotFoundError:
            return "Error: File not found."
        except Exception as e:
            return f"Error: {str(e)}"
