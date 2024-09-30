# Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import requests
import sqlite3
import json
import networkx as nx
from typing import List, Set, Dict
from time import sleep
from random import random
from bs4 import BeautifulSoup
from xml.etree.ElementTree import ParseError
from indra import literature
from indra.literature.elsevier_client import extract_text
from indra.tools.gene_network import GeneNetwork
from indra.statements import Modification, RegulateActivity
from indra.statements.statements import Statement, stmts_from_json, stmts_to_json
from indra.assemblers.indranet import IndraNetAssembler, IndraNet
from tqdm import tqdm
from indra.assemblers.sbgn.assembler import SBGNAssembler, states
from indra.assemblers.cyjs.assembler import CyJSAssembler


class IndraDataManager:
    REACH_API_URL = "http://api.indra.bio:8000/reach/process_text"
    ASSEMBLER_API_URL = "http://api.indra.bio:8000/assemblers/english"
    PREASSEMBLY_API_URL = "http://api.indra.bio:8000/preassembly"

    PM_CACHE_PATH = "/tmp/pm_cache.db"
    PM_CACHE = None

    PMIDS = set()
    PMIDS_EXCLUDE = set()

    def __init__(
        self,
        genes: List[str],
        max_papers_per_gene: int = 0,
        elsevier_api_key: str = "",
    ):
        self.__class__.init()

        self._genes = genes
        self._gene_doc_map: Dict[str, Set[str]] = dict()
        self._papers: Dict[str, str] = dict()
        self._pm_statements: Dict[str, dict] = dict()
        self._gn_statements: List[Statement] = list()
        self._all_statements: List[Statement] = list()
        self._assembled_statements: Dict[str, str] = dict()
        self._pm_mem = dict()
        self._sbgn_model = None
        self._cyjs_model = None
        self.max_papers_per_gene: int = max_papers_per_gene
        self.elsevier_api_key = elsevier_api_key

        if elsevier_api_key:
            os.environ["ELSEVIER_API_KEY"] = elsevier_api_key

    @classmethod
    def init(cls):
        cache_new = os.path.exists(cls.PM_CACHE_PATH)
        cls.PM_CACHE = sqlite3.connect(cls.PM_CACHE_PATH)

        cur = cls.PM_CACHE.cursor()
        if not cache_new:
            cur.execute("create table if not exists pm_cache (pmid varchar, data json)")
            cur.execute("create table if not exists pm_exclude (pmid varchar)")
            cur.execute("create unique index if not exists idx_pmid on pm_cache(pmid)")

        cur.execute("select pmid from pm_cache")
        cls.PMIDS.update([row[0] for row in cur.fetchall()])
        cur.execute("select pmid from pm_exclude")
        cls.PMIDS_EXCLUDE.update([row[0] for row in cur.fetchall()])
        cur.close()

    @staticmethod
    def fetch_pm_cache(pmid: str) -> dict:
        cur = IndraDataManager.PM_CACHE.cursor()
        pm_data = cur.execute(
            "select data from pm_cache where pmid = ?", (pmid,)
        ).fetchone()
        cur.close()
        return json.loads(pm_data[0])

    @staticmethod
    def set_pm_cache(pmid: str, data: dict):
        cur = IndraDataManager.PM_CACHE.cursor()
        pm_data = cur.execute(
            "select data from pm_cache where pmid = ?", (pmid,)
        ).fetchone()
        if pm_data:
            data = json.loads(pm_data[0]) | data
            cur.execute(
                "update pm_cache set data = ? where pmid = ?", (json.dumps(data), pmid)
            )
        else:
            cur.execute("insert into pm_cache values (?, ?)", (pmid, json.dumps(data)))
        cur.close()
        IndraDataManager.PM_CACHE.commit()

    @staticmethod
    def set_pm_exlude(pmid: str):
        cur = IndraDataManager.PM_CACHE.cursor()
        cur.execute("insert into pm_exclude values (?)", (pmid,))
        cur.close()
        IndraDataManager.PM_CACHE.commit()
        IndraDataManager.PMIDS_EXCLUDE.add(pmid)

    @staticmethod
    def call_reach_process_text(text: str, offline: bool = False) -> Dict[str, dict]:
        params = {"text": text, "offline": offline, "url": None}

        sleep(random())
        response = requests.post(IndraDataManager.REACH_API_URL, json=params)
        result = (
            response.json()["statements"] if (response.status_code == 200) else None
        )

        if result is None:
            print(f"Request failed with status code {response.status_code}")
            print("Response text:")
            print(response.text)

        return result

    @staticmethod
    def call_preassembly_statements(statements: List[Statement]) -> List[Statement]:
        params = {
            "statements": [stt.to_json() for stt in statements],
            "grounding_map": {},
            "misgrounding_map": {},
            "agent_map": "string",
            "ignores": ["string"],
            "use_adeft": True,
            "gilda_mode": "string",
            "grounding_map_policy": "replace",
        }
        grounding_response = requests.post(
            f"{IndraDataManager.PREASSEMBLY_API_URL}/map_grounding", json=params
        )
        grounded_statements = (
            grounding_response.json()["statements"]
            if (grounding_response.status_code == 200)
            else None
        )

        if grounded_statements is None:
            print(
                f"Grounding request failed with status code {grounding_response.status_code}"
            )
            print(f"Response text: {grounding_response.text}")
            grounded_statements = [stt.to_json() for stt in statements]

        params.update({"statements": grounded_statements})
        sequence_response = requests.post(
            f"{IndraDataManager.PREASSEMBLY_API_URL}/map_sequence", json=params
        )
        sequenced_statements = (
            sequence_response.json()["statements"]
            if (sequence_response.status_code == 200)
            else None
        )

        if sequenced_statements is None:
            print(
                f"Sequence request failed with status code {sequence_response.status_code}"
            )
            print(f"Response text: {sequence_response.text}")
            sequenced_statements = grounded_statements

        params.update({"statements": sequenced_statements})
        preassembly_response = requests.post(
            f"{IndraDataManager.PREASSEMBLY_API_URL}/run_preassembly", json=params
        )
        preassembled_statements = (
            preassembly_response.json()["statements"]
            if (preassembly_response.status_code == 200)
            else None
        )

        if preassembled_statements is None:
            print(
                f"Preassembly request failed with status code {preassembly_response.status_code}"
            )
            print(f"Response text: {preassembly_response.text}")
            preassembled_statements = sequenced_statements

        return stmts_from_json(preassembled_statements)

    @staticmethod
    def call_assemble_statements(statements: List[Statement]) -> List[Statement]:
        params = {"statements": [stt.to_json() for stt in statements]}

        response = requests.post(IndraDataManager.ASSEMBLER_API_URL, json=params)
        result = response.json() if (response.status_code == 200) else None

        if result is None:
            print(f"Request failed with status code {response.status_code}")
            print("Response text:")
            print(response.text)

        return result

    @staticmethod
    def get_gn_statements(genes: List[str]) -> List[Statement]:
        gn = GeneNetwork(genes)
        biopax_stmts = gn.get_biopax_stmts()
        bel_stmts = gn.get_bel_stmts()

        return biopax_stmts + bel_stmts

    @staticmethod
    def assemble_network(statements) -> IndraNet:
        indranet_assembler = IndraNetAssembler(statements=statements)
        indranet = indranet_assembler.make_model()

        return indranet

    def get_ids(self, genes: List[str]) -> List[str]:
        pmids = set()
        for gene in tqdm(genes, desc="Getting gene PMIDs"):
            gene_pmids = literature.pubmed_client.get_ids_for_gene(gene)
            pmids.update(gene_pmids)
            self._gene_doc_map[gene] = (
                set(gene_pmids)
                if (self.max_papers_per_gene == 0)
                else set(gene_pmids[: self.max_papers_per_gene])
            )

        return sorted(pmids)

    def get_full_text(self, pubmed_ids: List[str]) -> Dict[str, str]:
        paper_contents = dict()

        for pmid in tqdm(pubmed_ids, desc="Getting papers"):
            if pmid in IndraDataManager.PMIDS_EXCLUDE:
                continue
            if pmid in IndraDataManager.PMIDS:
                pm_data = (
                    self._pm_mem[pmid]
                    if pmid in self._pm_mem
                    else IndraDataManager.fetch_pm_cache(pmid)
                )
                content, content_type = pm_data["content"], pm_data["content_type"]
            else:
                content, content_type = literature.get_full_text(pmid, "pmid")

            if content_type == "abstract":
                paper_contents[pmid] = content
            elif content_type == "pmc_oa_xml":
                if content.startswith("<?xml"):
                    soup = BeautifulSoup(content, features="xml")
                    body = soup.find_all("body")
                    paper_contents[pmid] = body[0].text if body else ""
                else:
                    paper_contents[pmid] = content
            elif content_type == "elsevier_xml" and os.environ.get(
                "ELSEVIER_API_KEY", ""
            ):
                try:
                    paper_contents[pmid] = extract_text(content)
                except ParseError:
                    paper_contents[pmid] = ""
            else:
                paper_contents[pmid] = content

            if pmid in paper_contents and not paper_contents[pmid]:
                del paper_contents[pmid]
                IndraDataManager.set_pm_exlude(pmid)

            if pmid in paper_contents and pmid not in IndraDataManager.PMIDS:
                pm_data = {
                    "content": paper_contents[pmid],
                    "content_type": content_type,
                }
                IndraDataManager.set_pm_cache(pmid, pm_data)
                self._pm_mem[pmid] = pm_data | IndraDataManager.fetch_pm_cache(pmid)
                IndraDataManager.PMIDS.add(pmid)

        return paper_contents

    def load_pm_mem(self, pmids: List[str]):
        cur = IndraDataManager.PM_CACHE.cursor()
        pm_data = cur.execute(
            f"select pmid, data from pm_cache where pmid in ({','.join(pmids)})"
        )
        for pmid, data in pm_data.fetchall():
            self._pm_mem[pmid] = json.loads(data)
        cur.close()

    @property
    def pubmed_statements(self) -> Dict[str, dict]:
        if (not self._pm_statements):
            self.get_ids(self._genes)
            pmids = set()
            for pmid_set in self._gene_doc_map.values():
                pmids.update(pmid_set)
            self.load_pm_mem(list(pmids))
            self._papers = self.get_full_text(list(pmids))
            self._pm_statements = dict()
            for pmid in tqdm(self._papers, desc="Getting statements..."):
                if pmid in IndraDataManager.PMIDS:
                    pm_data = self._pm_mem[pmid] if pmid in self._pm_mem else IndraDataManager.fetch_pm_cache(pmid)
                    if "pm_statements" in pm_data:
                        self._pm_statements[pmid] = pm_data["pm_statements"]

                if pmid not in self._pm_statements:
                    self._pm_statements[pmid] = IndraDataManager.call_reach_process_text(self._papers[pmid])
                    IndraDataManager.set_pm_cache(pmid, {"pm_statements": self._pm_statements[pmid]})
                    self._pm_mem[pmid] = {"pm_statements": self._pm_statements[pmid]} | IndraDataManager.fetch_pm_cache(pmid)

        return self._pm_statements

    @property
    def gene_doc_map(self) -> dict:
        if (not self._gene_doc_map):
            self.get_ids(self._genes)

        return {k: list(v) for k, v in self._gene_doc_map.items()}

    @property
    def papers(self) -> Dict[str, str]:
        if (not self._papers):
            _ = self.pubmed_statements

        return self._papers

    @property
    def statements(self) -> List[Statement]:
        if (not self._all_statements):
            self._gn_statements = IndraDataManager.get_gn_statements(self._genes)
            statements = stmts_from_json(self.pubmed_statements.values()) + self._gn_statements
            statements = IndraDataManager.call_preassembly_statements(statements)
            self._gn_statements = stmts_to_json(self._gn_statements)
            self._all_statements = statements

        return self._all_statements

    @property
    def assembled_statements(self) -> dict:
        if (not self._assembled_statements):
            self._assembled_statements = IndraDataManager.call_assemble_statements(self.statements)["sentences"]

        return self._assembled_statements


    @property
    def sbgn_model(self) -> str:
        # Deal with a bug in indra's SBGN assembler
        global states
        states["myristoylation"] = ['n', 'y']

        if (not self._sbgn_model):
            self._sbgn_model = SBGNAssembler(statements=self.statements).make_model()

        return self._sbgn_model.decode("utf-8")

    @property
    def cyjs_model(self) -> str:
        if (not self._cyjs_model):
            self._cyjs_model = CyJSAssembler(stmts=self.statements).make_model(grouping=True)

        # indranet = IndraDataManager.assemble_network(statements)
        # self.network = nx.to_dict_of_dicts(indranet)

        return self._cyjs_model
