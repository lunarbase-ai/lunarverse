from pandas import DataFrame

class Indexer:
    """
    A Natural Language schema description for each table and table attributes of the provided database. 
    """
    _nl_db_schema: dict[str, str] = {}

    """
    A short summary description of each table.
    """
    _nl_tables_summary: dict[str, str] = {}