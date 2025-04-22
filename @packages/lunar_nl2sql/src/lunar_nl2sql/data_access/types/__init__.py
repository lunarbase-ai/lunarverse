from typing import List, Dict
from pandas import DataFrame
from pydantic import RootModel, ConfigDict


class Tables(RootModel):
    root: List[str]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]


class TableSamples(RootModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    root: Dict[str, DataFrame]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
