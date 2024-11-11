import pytest

from unittest.mock import patch
from sql_query import SQLQuery

class TestSQLQuery:
    @pytest.fixture
    def sql_query(self):
        return SQLQuery(
            driver_name="postgresql",
            username="test_user",
            password="test_password",
            host="localhost",
            port=5432,
            database="test_database",
            ssl_mode="require"
        )

    @pytest.fixture
    def mock_sql_connector(self, sql_query):
        with patch.object(sql_query, 'sql_connector', autospec=True) as mock_connector:
            yield mock_connector

    def test_sql_query_run(self, sql_query, mock_sql_connector):
        # Mock the SQLConnector's query method
        mock_sql_connector.query.return_value = [
            {"column1": "value1", "column2": "value2"},
            {"column1": "value3", "column2": "value4"}
        ]

        query = "SELECT * FROM test_table"
        result = sql_query.run(query)

        expected_output = "column1,column2\nvalue1,value2\nvalue3,value4"
        assert result == expected_output
        mock_sql_connector.query.assert_called_once_with(query)


    def test_sql_query_run_with_exception(self, sql_query, mock_sql_connector):
        # Mock the SQLConnector's query method to raise an exception
        mock_sql_connector.query.side_effect = Exception("Database error")

        query = "SELECT * FROM test_table"
        with pytest.raises(Exception, match="Database error"):
            sql_query.run(query)
        mock_sql_connector.query.assert_called_once_with(query)

    def test_sql_query_run_with_null_values(self, sql_query, mock_sql_connector):
        # Mock the SQLConnector's query method to return rows with null values
        mock_sql_connector.query.return_value = [
            {"column1": "value1", "column2": None},
            {"column1": None, "column2": "value4"}
        ]

        query = "SELECT * FROM test_table"
        result = sql_query.run(query)

        expected_output = "column1,column2\nvalue1,\n,value4"
        assert result == expected_output
        mock_sql_connector.query.assert_called_once_with(query)

    def test_sql_query_run_with_special_characters(self, sql_query, mock_sql_connector):
        # Mock the SQLConnector's query method
        mock_sql_connector.query.return_value = [
            {"column1": "value1", "column2": "value,2"},
            {"column1": "value3", "column2": "value\"4"}
        ]

        query = "SELECT * FROM test_table"
        result = sql_query.run(query)

        expected_output = 'column1,column2\nvalue1,"value,2"\nvalue3,"value""4"'
        assert result == expected_output
        mock_sql_connector.query.assert_called_once_with(query)

    def test_sql_query_run_with_different_data_types(self, sql_query, mock_sql_connector):
        # Mock the SQLConnector's query method
        mock_sql_connector.query.return_value = [
            {"column1": 123, "column2": "string"},
            {"column1": 23123, "column2": None}
        ]

        query = "SELECT * FROM test_table"
        result = sql_query.run(query).rstrip()  # Strip trailing newlines

        expected_output = "column1,column2\n123,string\n23123,"
        assert result == expected_output
        mock_sql_connector.query.assert_called_once_with(query)