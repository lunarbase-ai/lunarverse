

from abc import ABC, abstractmethod
from pandas import DataFrame
from typing import Optional


class DataSource(ABC): 
    _tables: Optional[list[str]] = None
    _samples: Optional[dict[str, DataFrame]] = None
    
    @property
    @abstractmethod
    def samples(self) -> dict[str, DataFrame]:
        pass

    @property
    @abstractmethod
    def tables(self) -> list[str]:
        pass