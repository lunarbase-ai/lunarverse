import pytest
import sqlite3
import pandas as pd
from lunar_nl2sql.data_access.sqlite_data_access import SqliteDataAccess
from lunar_nl2sql.data_access.types import Tables, TableSamples


@pytest.fixture
def sqlite_data_access(tmp_path):
    """Fixture that creates a SqliteDataAccess instance with a temporary database containing test data."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO test_table (name) VALUES ('test1'), ('test2')")
    conn.commit()
    conn.close()

    return SqliteDataAccess(str(db_path))


def test_connection_is_established(sqlite_data_access):
    assert sqlite_data_access.connection is not None


def test_get_tables_returns_correct_tables(sqlite_data_access):
    tables = sqlite_data_access._get_tables()
    assert isinstance(tables, Tables)
    assert "test_table" in tables.root


def test_get_sample_returns_correct_dataframe(sqlite_data_access):
    sample = sqlite_data_access._get_sample("test_table", n=2)
    assert isinstance(sample, pd.DataFrame)
    assert len(sample) == 2
    assert "id" in sample.columns
    assert "name" in sample.columns


def test_samples_property_returns_correct_samples(sqlite_data_access):

    sqlite_data_access.tables

    samples = sqlite_data_access.samples
    assert isinstance(samples, TableSamples)
    assert "test_table" in samples.root
    assert isinstance(samples.root["test_table"], pd.DataFrame)
    assert len(samples.root["test_table"]) == 2
    assert "id" in samples.root["test_table"].columns
    assert "name" in samples.root["test_table"].columns


def test_connection_cleanup_closes_connection(sqlite_data_access):
    sqlite_data_access.__del__()
    with pytest.raises(sqlite3.ProgrammingError):
        sqlite_data_access.connection.execute("SELECT 1;")


@pytest.mark.parametrize("invalid_table", ["non_existent_table", "123", ""])
def test_get_sample_raises_error_for_invalid_table(sqlite_data_access, invalid_table):
    with pytest.raises(sqlite3.OperationalError):
        sqlite_data_access._get_sample(invalid_table)


def test_tables_property_returns_correct_tables(sqlite_data_access):
    tables = sqlite_data_access.tables
    assert isinstance(tables, Tables)
    assert "test_table" in tables.root
