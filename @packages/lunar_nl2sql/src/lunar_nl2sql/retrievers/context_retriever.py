
from lunar_nl2sql.services.ai import AIService
from lunar_nl2sql.indexers.indexer import Indexer
from lunar_nl2sql.prompts import (
    RetrieveRelevantTablesPrompt,
    RetrieveRelevantTableAttributesPrompt,
    RetrieveReferenceValuesPrompt
)

class ContextRetriever:
    
    def __init__(self, ai_service: AIService, indexer: Indexer) -> None:
        self.ai_service = ai_service
        self.indexer = indexer
        
    def retrieve(self, nl_query: str) -> dict[str, str]:
        relevant_tables = self._retrieve_relevant_tables(nl_query)

        relevant_nl_db_schema = {table: self.indexer.nl_db_schema[table] for table in relevant_tables}

        relevant_attributes = self._retrieve_relevant_table_attributes(
            nl_query, relevant_nl_db_schema
        )
        reference_values = self._retrieve_reference_values(
            nl_query, relevant_attributes, relevant_nl_db_schema
        )

        relevant_sample_data = self._retrieve_relevant_sample_data(relevant_tables)

        return {
            "relevant_tables": relevant_tables,
            "relevant_attributes": relevant_attributes,
            "reference_values": reference_values,
            "relevant_sample_data": relevant_sample_data,
            "relevant_nl_db_schema": relevant_nl_db_schema
        }

    def _retrieve_relevant_tables(self, nl_query: str) -> dict[str, str]:
        prompt = RetrieveRelevantTablesPrompt(self.ai_service)
        return prompt.run(nl_query, self.indexer.nl_db_schema)

    def _retrieve_relevant_table_attributes(self, nl_query: str, relevant_nl_db_schema: dict[str, str]) -> dict[str, str]:
        prompt = RetrieveRelevantTableAttributesPrompt(self.ai_service)
        return prompt.run(nl_query, relevant_nl_db_schema)

    def _retrieve_reference_values(self, nl_query: str, relevant_attributes: dict[str, str], relevant_nl_db_schema: dict[str, str]) -> dict[str, str]:
        prompt = RetrieveReferenceValuesPrompt(self.ai_service)
        return prompt.run(nl_query, relevant_nl_db_schema, relevant_attributes)

    def _retrieve_relevant_sample_data(self, relevant_tables: list[str]) -> dict[str, str]:
        relevant_sample_data = {table: self.indexer.samples[table] for table in relevant_tables}
        return relevant_sample_data
