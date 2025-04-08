from lunar_nl2sql.prompts import NLDBSchemaDescriptionPrompt, NLTableSummaryPrompt
from lunar_nl2sql.services.ai import AIService
from lunar_nl2sql.data_access.data_access import DataAccess
from lunar_nl2sql.data_access.types import TableSamples
from lunar_nl2sql.indexers.types import NLDBSchema, NLTablesSummary


class Indexer:
    """
    A Natural Language schema description for each table and table attributes of the provided database.
    """

    _nl_db_schema: NLDBSchema = {}

    """
    A short summary description of each table.
    """
    _nl_tables_summary: NLTablesSummary = {}

    def __init__(self, ai_service: AIService, data_access: DataAccess):
        self.ai_service = ai_service
        self.data_access = data_access

    @property
    def nl_db_schema(self) -> NLDBSchema:
        if not self._nl_db_schema:
            prompt = NLDBSchemaDescriptionPrompt(self.ai_service)
            nl_db_schema = {}
            for table_name in self.data_access.tables:
                nl_db_schema[table_name] = prompt.run(
                    table_name, self.data_access.samples[table_name]
                )
            self._nl_db_schema = NLDBSchema(nl_db_schema)
        print(self._nl_db_schema)
        return self._nl_db_schema

    @property
    def nl_tables_summary(self) -> NLTablesSummary:
        if not self._nl_tables_summary:
            prompt = NLTableSummaryPrompt(self.ai_service)
            summary = {}
            for table_name in self.data_access.tables:
                summary[table_name] = prompt.run(self.nl_db_schema[table_name])
            self._nl_tables_summary = NLTablesSummary(summary)
        return self._nl_tables_summary

    @property
    def samples(self) -> TableSamples:
        return self.data_access.samples
