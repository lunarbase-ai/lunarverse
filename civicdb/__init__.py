# Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json

import requests
from typing import Any, Optional, List

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType

from .queries import (
    GENE_ID,
    GENE_DETAILS,
    SOURCE_DETAILS,
    EVIDENCE_ID_THERAPY,
    EVIDENCE_ID_DISEASE,
    EVIDENCE_DETAILS,
    THERAPY_DETAILS,
    DISEASE_DETAILS,
)


class CivicDB(
    BaseComponent,
    component_name="CIViC",
    component_description="Searches for gene information from the CIViC database",
    input_types={
        "genes": DataType.LIST,
        "therapies": DataType.LIST,
        "diseases": DataType.LIST,
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.BIOMEDICAL,
):
    ENDPOINT: str = "https://civicdb.org/api/graphql"

    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model=model, configuration=kwargs)

    def run(
        self,
        genes: List,
        therapies: Optional[List] = None,
        diseases: Optional[List] = None,
    ):
        endpoint = self.__class__.ENDPOINT

        therapies = therapies or []
        diseases = diseases or []

        gene_ids = set()
        for gene in genes:
            resp = requests.post(endpoint, data={"query": GENE_ID % gene}).json()
            if "errors" in resp and "data" not in resp:
                raise ValueError(f"Failed to run query {GENE_ID % gene}: {str(resp)}")
            ids = [r["id"] for r in resp["data"]["molecularProfiles"]["nodes"]]
            gene_ids.update(ids)

        gene_details = [
            requests.post(endpoint, data={"query": GENE_DETAILS % g_id}).json()["data"][
                "gene"
            ]
            for g_id in gene_ids
        ]

        source_ids = set()
        for i, details in enumerate(gene_details):
            info = json.loads(details.get("myGeneInfoDetails", "{}"))
            gene_details[i]["geneAliases"] = info.get("alis", [])
            for src in details["sources"]:
                source_ids.add(src["id"])

        sources = {
            src_id: requests.post(
                endpoint, data={"query": SOURCE_DETAILS % src_id}
            ).json()["data"]["source"]
            for src_id in source_ids
        }

        evidence_ids_therapy = set()
        if therapies:
            for therapy in therapies:
                for details in gene_details:
                    resp = requests.post(
                        endpoint,
                        data={
                            "query": EVIDENCE_ID_THERAPY % (details["name"], therapy)
                        },
                    )
                    evid_ids = [
                        node["id"]
                        for node in resp.json()["data"]["evidenceItems"]["nodes"]
                    ]
                    evidence_ids_therapy.update(evid_ids)

        evidence_ids_disease = set()
        if diseases:
            for disease in diseases:
                for details in gene_details:
                    resp = requests.post(
                        endpoint,
                        data={
                            "query": EVIDENCE_ID_DISEASE % (details["name"], disease)
                        },
                    )
                    evid_ids = [
                        node["id"]
                        for node in resp.json()["data"]["evidenceItems"]["nodes"]
                    ]
                    evidence_ids_disease.update(evid_ids)

        if therapies and diseases:
            evidence_ids = evidence_ids_therapy.intersection(evidence_ids_disease)
        else:
            evidence_ids = evidence_ids_therapy.union(evidence_ids_disease)

        evidences = [
            requests.post(endpoint, data={"query": EVIDENCE_DETAILS % evid_id}).json()[
                "data"
            ]["evidenceItem"]
            for evid_id in evidence_ids
        ]

        therapy_ids = set()
        for evidence in evidences:
            for thp in evidence["therapies"]:
                therapy_ids.add(thp["id"])

        therapy_details = {
            t_id: requests.post(
                endpoint, data={"query": THERAPY_DETAILS % t_id}
            ).json()["data"]["therapy"]
            for t_id in therapy_ids
        }

        disease_ids = set()
        for evidence in evidences:
            disease_ids.add(evidence["disease"]["id"])

        disease_details = {
            d_id: requests.post(
                endpoint, data={"query": DISEASE_DETAILS % d_id}
            ).json()["data"]["disease"]
            for d_id in disease_ids
        }

        for evidence in evidences:
            evidence["disease"] = disease_details[evidence["disease"]["id"]]
            evidence["therapies"] = [
                therapy_details[thp["id"]] for thp in evidence["therapies"]
            ]

        results = {
            "genes": [
                {
                    "name": details["name"],
                    "summary": details["description"],
                    "aliases": details["geneAliases"],
                    "sources": [sources[src["id"]] for src in details["sources"]],
                }
                for details in gene_details
            ],
            "evidences": evidences,
        }

        return results
