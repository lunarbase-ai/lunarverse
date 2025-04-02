import sqlite3
import pandas as pd
from .data_source import DataSource


class SqliteDataSource(DataSource):

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)

    @property
    def tables(self) -> list[str]:
        if not self._tables:
            self._tables = self._get_tables()
        return self._tables

    def _get_tables(self) -> list[str]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables

    @property
    def samples(self) -> dict[str, pd.DataFrame]:
        if not self._samples:
            self._samples = {
                table_name: self._get_sample(table_name, 5)
                for table_name in self._tables
            }
        return self._samples

    def _get_sample(self, table_name: str, n: int = 5) -> pd.DataFrame:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT {n};")

        df = pd.DataFrame(
            cursor.fetchall(), columns=[desc[0] for desc in cursor.description]
        )
        cursor.close()

        return df

    def __del__(self):
        self.connection.close()
