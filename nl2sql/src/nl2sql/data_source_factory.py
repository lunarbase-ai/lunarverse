from nl2sql.types.enums.db_types_enum import DBTypesEnum
import lunar_nl2sql.data_sources as data_sources
import nl2sql.types.db_types_config as db_types_config
from pydantic import ValidationError


def data_source_factory(db_type: str, config: dict) -> data_sources.DataSource:
    try:
        if db_type == DBTypesEnum.CSV.value:
            db_types_config.CsvConfig(**config)
            return data_sources.CsvDataSource(**config)
        elif db_type == DBTypesEnum.SQLITE.value:
            db_types_config.SqliteConfig(**config)
            return data_sources.SqliteDataSource(**config)
        else:
            raise ValueError(f"No implementation for database type: {db_type}")
    except ValidationError as e:
        raise ValueError(f"Invalid configuration: {e}")
