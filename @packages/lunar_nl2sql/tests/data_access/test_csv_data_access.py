import pytest
import pandas as pd
from pathlib import Path
from lunar_nl2sql.data_access.csv_data_access import CsvDataAccess
from lunar_nl2sql.data_access.types import Tables, TableSamples


@pytest.fixture
def csv_files(tmp_path):
    """Fixture that creates temporary CSV files for testing"""
    # Create test CSV files with more rows
    test_df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "name": [
                "Alice",
                "Bob",
                "Charlie",
                "David",
                "Eve",
                "Frank",
                "Grace",
                "Hank",
                "Ivy",
                "Jack",
            ],
            "age": [25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
        }
    )

    test_df2 = pd.DataFrame(
        {
            "order_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            "product": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "quantity": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        }
    )

    # Save to temporary files
    test_path = tmp_path / "test.csv"
    test_df.to_csv(test_path, index=False)

    test_path2 = tmp_path / "test2.csv"
    test_df2.to_csv(test_path2, index=False)

    return {"test_table": str(test_path), "test_table2": str(test_path2)}


@pytest.fixture
def csv_data_access(csv_files):
    """Fixture that creates a CsvDataAccess instance with test data"""
    return CsvDataAccess(csv_files)


def test_csv_data_access_initialization(csv_data_access):
    """Test that CsvDataAccess initializes correctly with CSV files"""
    assert isinstance(csv_data_access._data, dict)
    assert len(csv_data_access._data) == 2
    assert "test_table" in csv_data_access._data
    assert "test_table2" in csv_data_access._data


def test_tables_property_returns_correct_tables(csv_data_access):
    """Test that tables property returns correct table names"""
    tables = csv_data_access.tables
    assert isinstance(tables, Tables)
    assert len(tables.root) == 2
    assert "test_table" in tables.root
    assert "test_table2" in tables.root


def test_samples_property_returns_correct_samples(csv_data_access):
    """Test that samples property returns correct table samples"""
    # First get tables to ensure they're loaded
    csv_data_access.tables

    samples = csv_data_access.samples
    assert isinstance(samples, TableSamples)
    assert len(samples.root) == 2
    assert "test_table" in samples.root
    assert "test_table2" in samples.root

    # Verify sample data structure
    test_sample = samples.root["test_table"]
    assert isinstance(test_sample, pd.DataFrame)
    assert len(test_sample) == 5  # sample size is 5
    assert "id" in test_sample.columns
    assert "name" in test_sample.columns
    assert "age" in test_sample.columns


def test_get_sample_returns_correct_dataframe(csv_data_access):
    """Test that _get_sample returns correct sample data"""
    sample = csv_data_access._get_sample("test_table", n=2)
    assert isinstance(sample, pd.DataFrame)
    assert len(sample) == 2
    assert "id" in sample.columns
    assert "name" in sample.columns
    assert "age" in sample.columns


def test_get_sample_with_invalid_table(csv_data_access):
    """Test that _get_sample raises KeyError for non-existent tables"""
    with pytest.raises(KeyError):
        csv_data_access._get_sample("non_existent_table")


def test_csv_data_access_with_custom_separator(tmp_path):
    """Test CsvDataAccess with custom separator"""
    # Create CSV with custom separator
    test_df = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})

    test_path = tmp_path / "test_custom.csv"
    test_df.to_csv(test_path, index=False, sep=";")

    # Initialize with custom separator
    csv_access = CsvDataAccess({"test_table": str(test_path)}, separator=";")

    # Verify data is loaded correctly
    data = csv_access._data["test_table"]
    assert len(data) == 3
    assert "id" in data.columns
    assert "name" in data.columns


def test_csv_data_access_with_encoding(tmp_path):
    """Test CsvDataAccess with custom encoding"""
    # Create CSV with special characters
    test_df = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Böb", "Chárlie"]})

    test_path = tmp_path / "test_encoding.csv"
    test_df.to_csv(test_path, index=False, encoding="utf-8")

    # Initialize with specific encoding
    csv_access = CsvDataAccess({"test_table": str(test_path)}, encoding="utf-8")

    # Verify data is loaded correctly
    data = csv_access._data["test_table"]
    assert len(data) == 3
    assert "id" in data.columns
    assert "name" in data.columns
    assert data.loc[1, "name"] == "Böb"  # Verify special character is preserved
