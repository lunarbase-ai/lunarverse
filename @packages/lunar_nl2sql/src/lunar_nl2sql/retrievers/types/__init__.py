from pydantic import RootModel, BaseModel
from typing import List

class TableAttributes(BaseModel):
    table: str
    attributes: List[str]

class TableAttributesCollection(RootModel):
    root: List[TableAttributes]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]