# Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os.path
import requests
from typing import Optional, Any
from zipfile import ZipFile
from owlready2 import get_ontology, default_world

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

OWL_URL = "https://evs.nci.nih.gov/ftp1/NCI_Thesaurus/archive/23.12d_Release/Thesaurus_23.12d.OWL.zip"
THESAURUS_FILE = OWL_URL.split("/")[-1]


class NCIThesaurus(
    BaseComponent,
    component_name="NCI Thesaurus",
    component_description="Retrieve biomedical information from the NCI Thesaurus, via SPARQL query",
    input_types={"query": DataType.TEMPLATE},
    output_type=DataType.JSON,
    component_group=ComponentGroup.BIOMEDICAL
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)
        path = self._file_connector.get_absolute_path("")
        owl_path = os.path.join(path, THESAURUS_FILE)
        if not os.path.exists(owl_path):
            req = requests.get(OWL_URL)
            with open(owl_path, "wb") as owl_file:
                owl_file.write(req.content)
            with ZipFile(owl_path) as owl_zip:
                owl_zip.extractall(path)
        self.onto = get_ontology(owl_path.replace(THESAURUS_FILE, "Thesaurus.owl")).load()

    def run(
        self, query: str
    ):
        result = {"result": list(default_world.sparql(str(query).strip()))}

        return result