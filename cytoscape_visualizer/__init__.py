# SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from typing import Any, Optional, Union, List, Dict
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType, File


class CytoscapeVisualizer(
    BaseComponent,
    component_name="Cytoscape Visualizer",
    component_description="""Receives a Cytoscape formatted JSON and creates a graph visualization.""",
    input_types={"cytoscape_JSON": DataType.JSON},
    output_type=DataType.CYTOSCAPE,
    component_group=ComponentGroup.DATA_VISUALIZATION,
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    def run(
        self,
        cytoscape_JSON: Dict,
    ):
        if isinstance(cytoscape_JSON, list):
            cytoscape_JSON = cytoscape_JSON[0]
        return cytoscape_JSON
