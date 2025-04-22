from pydantic import RootModel, BaseModel
from typing import List
from lunar_nl2sql.data_access.types import Tables, TableSamples
from lunar_nl2sql.indexers.types import NLDBSchema


class TableAttributes(BaseModel):
    table: str
    attributes: List[str]


class TableAttributesCollection(RootModel):
    root: List[TableAttributes]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class TableReferenceValues(BaseModel):
    table: str
    attribute: str
    values: List[str]


class TableReferenceValuesCollection(RootModel):
    root: List[TableReferenceValues]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class Context(BaseModel):
    relevant_tables: Tables
    relevant_attributes: TableAttributesCollection
    reference_values: TableReferenceValuesCollection
    relevant_sample_data: TableSamples
    relevant_nl_db_schema: NLDBSchema
