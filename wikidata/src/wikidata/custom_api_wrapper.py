# SPDX-FileCopyrightText: Copyright © 2024 João Gabriel Oliveira <jgoliveira84@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from typing import Optional
from langchain_community.tools.wikidata.tool import WikidataAPIWrapper

logger = logging.getLogger(__name__)

WIKIDATA_MAX_QUERY_LENGTH = 300

class CustomWikidataAPIWrapper(WikidataAPIWrapper):
    def _item_to_structured_document(self, qid: str) -> Optional[dict]:
        from wikibase_rest_api_client.utilities.fluent import FluentWikibaseClient

        fluent_client: FluentWikibaseClient = FluentWikibaseClient(
            self.wikidata_rest, supported_props=self.wikidata_props, lang=self.lang
        )
        resp = fluent_client.get_item(qid)

        if not resp:
            logger.warning(f"Could not find item {qid} in Wikidata")
            return None

        doc = {}
        if resp.label:
            doc["label"] = resp.label
        if resp.description:
            doc["description"] = resp.description
        if resp.aliases:
            doc["aliases"] = resp.aliases
        for prop, values in resp.statements.items():
            if values:
                doc[prop.label] = values

        return doc

    def run(self, query: str) -> str:
        clipped_query = query[:WIKIDATA_MAX_QUERY_LENGTH]
        items = self.wikidata_mw.search(clipped_query, results=self.top_k_results)

        docs = []
        for item in items[: self.top_k_results]:
            docs.append(self._item_to_structured_document(item))
        if not docs:
            return "No good Wikidata Search Result was found"

        return docs
