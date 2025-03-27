from .data_source import DataSource
import pandas as pd

class CsvDataSource(DataSource):
    _data: dict[str, pd.DataFrame] = {}
    
    def __init__(self, dict_path_csv: dict,encoding="utf-8",separator=",",has_header=True,ignore_errors=True):
        self._data = {table_name: pd.read_csv(dict_path_csv[table_name], sep=separator, encoding=encoding) for table_name in dict_path_csv}

    @property
    def tables(self) -> list[str]:
        if not self._tables:
            self._tables = list(self._data.keys())
        return self._tables

    @property
    def samples(self) -> dict[str, pd.DataFrame]:
        if not self._samples:
            self._samples = {table_name: self._get_sample(table_name, 5) for table_name in self._tables}
        return self._samples


    def _get_sample(self, table_name: str, n: int = 5) -> pd.DataFrame:
        sample_df = self._data[table_name].sample(n=n, random_state=0)
        return sample_df
