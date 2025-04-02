from abc import ABC, abstractmethod
from pandas import DataFrame


class DataSource(ABC):
    _tables: list[str] = []
    _samples: dict[str, DataFrame] = {}

    @property
    @abstractmethod
    def samples(self) -> dict[str, DataFrame]:
        pass

    @property
    @abstractmethod
    def tables(self) -> list[str]:
        pass
