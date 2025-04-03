from .data_access import DataAccess
import pandas as pd


class CsvDataAccess(DataAccess):
    _data: dict[str, pd.DataFrame] = {}

    def __init__(
        self,
        csv_paths: dict,
        encoding="utf-8",
        separator=",",
        has_header=True,
        ignore_errors=True,
    ):
        self._data = {
            table_name: pd.read_csv(
                csv_paths[table_name], sep=separator, encoding=encoding
            )
            for table_name in csv_paths
        }

    @property
    def tables(self) -> list[str]:
        if not self._tables:
            self._tables = list(self._data.keys())
        return self._tables

    @property
    def samples(self) -> dict[str, pd.DataFrame]:
        if not self._samples:
            self._samples = {
                table_name: self._get_sample(table_name, 5)
                for table_name in self._tables
            }
        return self._samples

    def _get_sample(self, table_name: str, n: int = 5) -> pd.DataFrame:
        sample_df = self._data[table_name].sample(n=n, random_state=0)
        return sample_df
