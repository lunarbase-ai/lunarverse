# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, List
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType, File

class SBGNVisualizer(
    BaseComponent,
    component_name="SBGN Visualizer",
    component_description="""Receives a BSGN XML file and creates a graph visualization.""",
    input_types={"sbgn_string": DataType.TEXT, "node_ids": DataType.LIST},
    output_type=DataType.BSGN_GRAPH,
    component_group=ComponentGroup.BIOMEDICAL,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    def run(
        self, sbgn_string: str, node_ids: List
    ):
        return {
            "sbgn_string": sbgn_string,
            "node_ids": node_ids
        }