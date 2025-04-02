from nl2sql.types.enums.db_types_enum import DBTypesEnum
from pydantic import BaseModel


class DBTypesConfig(BaseModel):
    db_type: DBTypesEnum


class CsvConfig(BaseModel):
    csv_paths: dict[str, str]


__all__ = ["DBTypesConfig", "CsvConfig"]
