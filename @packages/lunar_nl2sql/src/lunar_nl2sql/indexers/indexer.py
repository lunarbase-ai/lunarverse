from lunar_nl2sql.prompts import NLDBSchemaDescriptionPrompt, NLTableSummaryPrompt
from lunar_nl2sql.services.ai import AIService
from lunar_nl2sql.data_access.data_access import DataAccess
import pandas as pd


class Indexer:
    """
    A Natural Language schema description for each table and table attributes of the provided database.
    """

    _nl_db_schema: dict[str, str] = {}

    """
    A short summary description of each table.
    """
    _nl_tables_summary: dict[str, str] = {}

    def __init__(self, ai_service: AIService, data_access: DataAccess):
        self.ai_service = ai_service
        self.data_access = data_access

    @property
    def nl_db_schema(self) -> dict[str, str]:
        if not self._nl_db_schema:
            prompt = NLDBSchemaDescriptionPrompt(self.ai_service)
            for table_name in self.data_access.tables:
                self._nl_db_schema[table_name] = prompt.run(
                    table_name, self.data_access.samples.get(table_name)
                )
        return self._nl_db_schema

    @property
    def nl_tables_summary(self) -> dict[str, str]:
        if not self._nl_tables_summary:
            prompt = NLTableSummaryPrompt(self.ai_service)
            for table_name in self.data_access.tables:
                self._nl_tables_summary[table_name] = prompt.run(
                    self.nl_db_schema.get(table_name)
                )
        return self._nl_tables_summary

    @property
    def samples(self) -> dict[str, pd.DataFrame]:
        return self.data_access.samples
