import pytest
from unittest.mock import patch, MagicMock
from sql_schema_extractor import SQLSchemaExtractor
import json

@pytest.fixture
def mock_sql_connector():
    with patch("sql_schema_extractor.SQLConnector") as MockSQLConnector:
        mock_connector_instance = MockSQLConnector.return_value
        mock_connector_instance.engine = MagicMock()
        yield mock_connector_instance


@pytest.fixture
def mock_inspect():
    with patch("sql_schema_extractor.inspect") as mock_inspect_fn:
        yield mock_inspect_fn


class TestSQLSchemaExtractor:
    @pytest.fixture(autouse=True)
    def setup(self, mock_sql_connector, mock_inspect):
        self.mock_sql_connector = mock_sql_connector
        self.mock_inspect = mock_inspect
        self.schema_extractor = SQLSchemaExtractor()

    def test_empty_schema(self):
        self.mock_inspect.return_value.get_table_names.return_value = []


        result = self.schema_extractor.run()

        assert result == json.dumps({"tables": []})

    def test_schema_with_one_table(self):
        self.mock_inspect.return_value.get_table_names.return_value = ["users"]
        self.mock_inspect.return_value.get_columns.return_value = [
            {"name": "id", "type": "INTEGER", "primary_key": True},
            {"name": "name", "type": "TEXT", "nullable": False}, 
        ]
        self.mock_inspect.return_value.get_pk_constraint.return_value = {
            "constrained_columns": ["id"],
            "name": "pk_users",
        }

        self.mock_inspect.return_value.get_foreign_keys.return_value = []
        self.mock_inspect.return_value.get_unique_constraints.return_value = []

        result = self.schema_extractor.run()

        expected_result = json.dumps({
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "INTEGER", "constraints": ["primary_key"]},
                        {"name": "name", "type": "TEXT", "constraints": []} 
                    ],
                    "constraints": ["pk_users"] 
                }
            ]
        })
        assert result == expected_result

    def test_schema_with_nullable_column(self):
        self.mock_inspect.return_value.get_table_names.return_value = ["users"]
        self.mock_inspect.return_value.get_columns.return_value = [
            {"name": "id", "type": "INTEGER", "primary_key": True},
            {"name": "name", "type": "TEXT", "nullable": True},  # Nullable column
        ]
        self.mock_inspect.return_value.get_pk_constraint.return_value = {
            "constrained_columns": ["id"],
            "name": "pk_users",
        }

        # Mock foreign key and unique constraints as empty
        self.mock_inspect.return_value.get_foreign_keys.return_value = []
        self.mock_inspect.return_value.get_unique_constraints.return_value = []


        result = self.schema_extractor.run()

        expected_result = json.dumps({
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "INTEGER", "constraints": ["primary_key"]},
                        {"name": "name", "type": "TEXT", "constraints": ["nullable"]}
                    ],
                    "constraints": ["pk_users"] 
                }
            ]
        })

        assert result == expected_result


    def test_schema_with_foreign_keys(self):
        self.mock_inspect.return_value.get_table_names.return_value = ["orders"]
        self.mock_inspect.return_value.get_columns.return_value = [
            {"name": "id", "type": "INTEGER", "primary_key": True},
            {"name": "user_id", "type": "INTEGER", "nullable": False},
        ]
        self.mock_inspect.return_value.get_pk_constraint.return_value = {
            "constrained_columns": ["id"],
            "name": "pk_orders",
        }
        self.mock_inspect.return_value.get_foreign_keys.return_value = [
            {
                "constrained_columns": ["user_id"],
                "referred_table": "users",
                "referred_columns": ["id"],
                "name": "fk_orders_user_id",
            }
        ]

        result = self.schema_extractor.run()


        expected_result = json.dumps({
            "tables": [
                {
                    "name": "orders",
                    "columns": [
                        {"name": "id", "type": "INTEGER", "constraints": ["primary_key"]},
                        {"name": "user_id", "type": "INTEGER", "constraints": []},
                    ],
                    "constraints": [
                        "pk_orders", 
                        "foreign_key(['user_id'] -> users.['id'])"
                    ],
                }
            ]
        })
        assert result == expected_result

    def test_filter_tables(self):
        self.mock_inspect.return_value.get_table_names.return_value = ["users", "orders"]
        self.mock_inspect.return_value.get_columns.side_effect = lambda table_name: [
            {"name": "id", "type": "INTEGER", "primary_key": True},
            {"name": "name", "type": "TEXT", "nullable": False},
        ] if table_name == "users" else []
        self.mock_inspect.return_value.get_pk_constraint.side_effect = lambda table_name: {
            "constrained_columns": ["id"],
            "name": f"pk_{table_name}",
        } if table_name == "users" else {"constrained_columns": [], "name": None}


        result = self.schema_extractor.run(tables=["users"])

        expected_result = json.dumps({
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "INTEGER", "constraints": ["primary_key"]},
                        {"name": "name", "type": "TEXT", "constraints": []},
                    ],
                    "constraints": ["pk_users"],
                }
            ]
        })
        assert result == expected_result
