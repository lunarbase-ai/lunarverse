from lunar_nl2sql.data_access.types import Tables, TableSamples
from lunar_nl2sql.indexers.types import NLDBSchema
from lunar_nl2sql.retrievers.types import TableAttributesCollection, TableReferenceValuesCollection, Context
from lunar_nl2sql.services.ai import AIService
from lunar_nl2sql.indexers.indexer import Indexer
from lunar_nl2sql.prompts import (
    RetrieveRelevantTablesPrompt,
    RetrieveRelevantTableAttributesPrompt,
    RetrieveReferenceValuesPrompt,
)


class ContextRetriever:

    def __init__(self, ai_service: AIService, indexer: Indexer) -> None:
        self.ai_service = ai_service
        self.indexer = indexer

    def retrieve(self, nl_query: str) -> Context:
        relevant_tables = self._retrieve_relevant_tables(nl_query)

        relevant_nl_db_schema = self._retrieve_relevant_nl_db_schema(relevant_tables)

        relevant_attributes = self._retrieve_relevant_table_attributes(
            nl_query, relevant_nl_db_schema
        )
        reference_values = self._retrieve_reference_values(
            nl_query, relevant_attributes, relevant_nl_db_schema
        )

        relevant_sample_data = self._retrieve_relevant_sample_data(relevant_tables)

        return Context(
            relevant_tables=relevant_tables,
            relevant_attributes=relevant_attributes,
            reference_values=reference_values,
            relevant_sample_data=relevant_sample_data,
            relevant_nl_db_schema=relevant_nl_db_schema,
        )

    def _retrieve_relevant_tables(self, nl_query: str) -> Tables:
        prompt = RetrieveRelevantTablesPrompt(self.ai_service)
        return Tables(prompt.run(nl_query, self.indexer.nl_db_schema))

    def _retrieve_relevant_nl_db_schema(self, relevant_tables: Tables) -> NLDBSchema:
        return NLDBSchema({table: self.indexer.nl_db_schema[table] for table in relevant_tables})

    def _retrieve_relevant_table_attributes(
        self, nl_query: str, relevant_nl_db_schema: NLDBSchema
    ) -> TableAttributesCollection:
        prompt = RetrieveRelevantTableAttributesPrompt(self.ai_service)
        return TableAttributesCollection(prompt.run(nl_query, relevant_nl_db_schema))
    
    def _retrieve_reference_values(
        self,
        nl_query: str,
        relevant_attributes: TableAttributesCollection,
        relevant_nl_db_schema: NLDBSchema,
    ) -> TableReferenceValuesCollection:
        prompt = RetrieveReferenceValuesPrompt(self.ai_service)
        return TableReferenceValuesCollection(prompt.run(nl_query, relevant_nl_db_schema, relevant_attributes))

    def _retrieve_relevant_sample_data(
        self, relevant_tables: Tables
    ) -> TableSamples:
        relevant_sample_data = {
            table: self.indexer.samples[table] for table in relevant_tables
        }
        return TableSamples(relevant_sample_data)
