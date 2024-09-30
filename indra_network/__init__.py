# Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from lunarcore.core.component import BaseComponent
from .indra_data_manager import IndraDataManager

class IndraNetwork(
    BaseComponent,
    component_name="Indra Network Assembler",
    component_description="Retrieve literature related to a set of genes",
    input_types={"genes": DataType.LIST},
    output_type=DataType.JSON,
    component_group=ComponentGroup.BIOMEDICAL,
    max_papers_per_gene=3,
    elsevier_api_key="$LUNARENV::ELSEVIER_API_KEY",
    output_properties=""
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)
        self.properties = [
            "gene_doc_map",
            "papers",
            "pubmed_statements",
            "assembled_statements",
            "sbgn_model",
            "cyjs_model"
        ]

    def run(self, genes: List[str], **kwargs: Any):
        miner = IndraDataManager(
            genes,
            max_papers_per_gene=int(self.configuration["max_papers_per_gene"]),
            elsevier_api_key=self.configuration["elsevier_api_key"],
        )

        result = dict()
        configured_out_props = {
            cfg.strip().lower()
            for cfg in self.configuration["output_properties"].split(",")
        }
        for out_prop in self.properties:
            if out_prop in configured_out_props:
                result[out_prop] = getattr(miner, out_prop)

        return result
