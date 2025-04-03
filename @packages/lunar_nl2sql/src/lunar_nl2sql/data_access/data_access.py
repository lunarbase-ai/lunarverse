from abc import ABC, abstractmethod
from lunar_nl2sql.data_access.typing import TableSamples, Tables


class DataAccess(ABC):
    _tables: Tables = []
    _samples: TableSamples = {}

    @property
    @abstractmethod
    def samples(self) -> TableSamples:
        pass

    @property
    @abstractmethod
    def tables(self) -> Tables:
        pass
