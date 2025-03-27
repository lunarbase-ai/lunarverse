from nl2sql.services.ai import AIService
from nl2sql.data_sources.data_source import DataSource

class Indexer:
    """
    A Natural Language schema description for each table and table attributes of the provided database. 
    """
    _nl_db_schema: dict[str, str] = {}

    """
    A short summary description of each table.
    """
    _nl_tables_summary: dict[str, str] = {}

    def __init__(self, ai_service: AIService, data_source: DataSource):
        self.ai_service = ai_service
        self.data_source = data_source