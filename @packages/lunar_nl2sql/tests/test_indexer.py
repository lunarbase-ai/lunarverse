import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from lunar_nl2sql.indexers.indexer import Indexer
from lunar_nl2sql.services.ai import AIService
from lunar_nl2sql.data_access.data_access import DataAccess
from lunar_nl2sql.data_access.types import Tables, TableSamples
from lunar_nl2sql.indexers.types import NLDBSchema, NLTablesSummary


@pytest.fixture
def mock_ai_service():
    ai_service = MagicMock(spec=AIService)
    return ai_service

@pytest.fixture
def mock_data_access():
    data_access = MagicMock(spec=DataAccess)
    
    # Mock tables property
    tables = Tables(root=['users', 'orders'])
    data_access.tables = tables
    
    # Mock samples property
    samples = TableSamples({
        'users': pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        }),
        'orders': pd.DataFrame({
            'id': [101, 102, 103],
            'user_id': [1, 2, 3],
            'amount': [100, 200, 300]
        })
    })
    data_access.samples = samples
    
    return data_access

@pytest.fixture
def indexer(mock_ai_service, mock_data_access):
    return Indexer(mock_ai_service, mock_data_access)

def test_indexer_initialization(mock_ai_service, mock_data_access):
    indexer = Indexer(mock_ai_service, mock_data_access)
    assert indexer.ai_service == mock_ai_service
    assert indexer.data_access == mock_data_access

def test_nl_db_schema_property(indexer, mock_data_access):
    users_response = "users; table containing user information\nid; user ID; integer; numeric; true\nname; user name; string; text; false\nage; user age; integer; numeric; false"
    orders_response = "orders; table containing order information\nid; order ID; integer; numeric; true\nuser_id; user ID; integer; numeric; false\namount; order amount; decimal; currency; false"
    
    with patch('lunar_nl2sql.indexers.indexer.NLDBSchemaDescriptionPrompt') as MockPromptClass:
        mock_prompt_instance = MagicMock()
        mock_prompt_instance.run.side_effect = [users_response, orders_response]
        MockPromptClass.return_value = mock_prompt_instance


        schema = indexer.nl_db_schema


        assert isinstance(schema, NLDBSchema)
        assert schema['users'] == users_response
        assert schema['orders'] == orders_response

        mock_prompt_instance.run.assert_any_call('users', mock_data_access.samples['users'])
        mock_prompt_instance.run.assert_any_call('orders', mock_data_access.samples['orders'])

def test_nl_tables_summary_property(indexer):
    users_summary = "The users table contains basic user information including ID, name, and age."
    orders_summary = "The orders table tracks order information with fields for ID, user reference, and amount."

    indexer._nl_db_schema = NLDBSchema({
        'users': 'users table schema description',
        'orders': 'orders table schema description'
    })
    
    with patch('lunar_nl2sql.indexers.indexer.NLTableSummaryPrompt') as MockPromptClass:
        mock_prompt_instance = MagicMock()
        mock_prompt_instance.run.side_effect = [users_summary, orders_summary]
        MockPromptClass.return_value = mock_prompt_instance


        summaries = indexer.nl_tables_summary

        assert isinstance(summaries, NLTablesSummary)
        assert summaries['users'] == users_summary
        assert summaries['orders'] == orders_summary

        mock_prompt_instance.run.assert_any_call(indexer._nl_db_schema['users'])
        mock_prompt_instance.run.assert_any_call(indexer._nl_db_schema['orders'])
