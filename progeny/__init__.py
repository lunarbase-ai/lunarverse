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
import decoupler as dc
import pandas as pd


class Progeny(
    BaseComponent,
    component_name="PROGENy",
    component_description="""PROGENy is the definitive resource for pathways and target genes, with weights for each interaction. It requires two CSV files as input. decoupler https://decoupler-py.readthedocs.io/en/latest/notebooks/progeny.html | paper: Schubert, M., Klinger, B., Klünemann, M. et al. Perturbation-response genes reveal signaling footprints in cancer gene expression. Nat Commun 9, 20 (2018). https://doi.org/10.1038/s41467-017-02391-6 (https://www.nature.com/articles/s41467-017-02391-6)""",
    input_types={"adata": DataType.TEXT, "progeny": DataType.TEXT},
    output_type=DataType.LIST,
    component_group=ComponentGroup.DATA_EXTRACTION,
    client_id="$LUNARENV::PROGENY_CLIENT_ID",
    client_secret="$LUNARENV::PROGENY_CLIENT_SECRET",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(self, adata: str, progeny: str):
        adata = pd.read_csv(adata)
        adata.set_index("index", inplace=True)
        progeny = pd.read_csv(progeny)
        estimate, pvals = dc.run_mlm(
            mat=adata,
            net=progeny,
            source="source",
            target="target",
            weight="weight",
            verbose=False,
        )

        estimate_path = "/".join(adata.split("/")[:-1]) + "/estimate.csv"
        estimate.to_csv(estimate_path)
        pvals_path = "/".join(adata.split("/")[:-1]) + "/pvals.csv"
        pvals.to_csv(pvals_path)

        return [estimate_path, pvals_path]
