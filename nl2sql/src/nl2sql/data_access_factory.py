from nl2sql.types.enums.db_types_enum import DBTypesEnum
import lunar_nl2sql.data_access as data_access
import nl2sql.types.db_types_config as db_types_config
from pydantic import ValidationError


def data_access_factory(db_type: str, config: dict) -> data_access.DataAccess:
    try:
        if db_type == DBTypesEnum.CSV.value:
            db_types_config.CsvConfig(**config)
            return data_access.CsvDataAccess(**config)
        elif db_type == DBTypesEnum.SQLITE.value:
            db_types_config.SqliteConfig(**config)
            return data_access.SqliteDataAccess(**config)
        else:
            raise ValueError(f"No implementation for database type: {db_type}")
    except ValidationError as e:
        raise ValueError(f"Invalid configuration: {e}")
