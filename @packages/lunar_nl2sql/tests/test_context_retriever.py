import pytest
from unittest.mock import MagicMock, patch
from lunar_nl2sql.data_access.types import Tables, TableSamples
from lunar_nl2sql.indexers.types import NLDBSchema
from lunar_nl2sql.retrievers.types import (
    TableAttributesCollection,
    TableAttributes,
    TableReferenceValuesCollection,
    TableReferenceValues,
    Context,
)
from lunar_nl2sql.retrievers.context_retriever import ContextRetriever
from lunar_nl2sql.services.ai import AIService
from lunar_nl2sql.indexers.indexer import Indexer
import pandas as pd

@pytest.fixture
def ai_service():
    return MagicMock(spec=AIService)

@pytest.fixture
def indexer():
    indexer = MagicMock(spec=Indexer)
    indexer.nl_db_schema = {
        'table1': 'table1 description',
        'table2': 'table2 description'
    }
    indexer.samples = {
        'table1': pd.DataFrame([{'id': 1, 'name': 'John'}]),
        'table2': pd.DataFrame([{'id': 1, 'age': 30}])
    }
    return indexer

@pytest.fixture
def context_retriever(ai_service, indexer):
    return ContextRetriever(ai_service, indexer)

def test_init(context_retriever, ai_service, indexer):
    assert context_retriever.ai_service == ai_service
    assert context_retriever.indexer == indexer

def test_retrieve(context_retriever):
    nl_query = "Find users older than 30"
    
    with patch('lunar_nl2sql.retrievers.context_retriever.RetrieveRelevantTablesPrompt') as mock_tables_prompt, \
         patch('lunar_nl2sql.retrievers.context_retriever.RetrieveRelevantTableAttributesPrompt') as mock_attributes_prompt, \
         patch('lunar_nl2sql.retrievers.context_retriever.RetrieveReferenceValuesPrompt') as mock_values_prompt:
        
        mock_tables_prompt.return_value.run.return_value = ['table2']
        mock_attributes_prompt.return_value.run.return_value = [{'table': 'table2', 'attributes': ['age']}]
        mock_values_prompt.return_value.run.return_value = [
            {
                'table': 'table2',
                'attribute': 'age',
                'values': ['30', '40']
            }
        ]
        
        result = context_retriever.retrieve(nl_query)
        
        assert isinstance(result, Context)
        assert result.relevant_tables == Tables(['table2'])
        assert isinstance(result.relevant_attributes, TableAttributesCollection)
        assert isinstance(result.reference_values, TableReferenceValuesCollection)
        assert isinstance(result.relevant_sample_data, TableSamples)
        assert isinstance(result.relevant_nl_db_schema, NLDBSchema)

def test_retrieve_relevant_tables(context_retriever):
    nl_query = "Find users older than 30"
    mock_prompt = MagicMock()
    mock_prompt.run.return_value = ['table2']
    
    with patch('lunar_nl2sql.retrievers.context_retriever.RetrieveRelevantTablesPrompt', return_value=mock_prompt):
        result = context_retriever._retrieve_relevant_tables(nl_query)
        assert result == Tables(['table2'])

def test_retrieve_relevant_nl_db_schema(context_retriever):
    relevant_tables = Tables(['table2'])
    
    result = context_retriever._retrieve_relevant_nl_db_schema(relevant_tables)
    assert result == NLDBSchema({'table2': 'table2 description'})

def test_retrieve_relevant_table_attributes(context_retriever):
    nl_query = "Find users older than 30"
    relevant_nl_db_schema = NLDBSchema({'table2': 'users table with age information'})
    
    mock_prompt = MagicMock()
    mock_prompt.run.return_value = [{'table': 'table2', 'attributes': ['age']}]
    
    with patch('lunar_nl2sql.retrievers.context_retriever.RetrieveRelevantTableAttributesPrompt', return_value=mock_prompt):
        result = context_retriever._retrieve_relevant_table_attributes(nl_query, relevant_nl_db_schema)
        assert result == TableAttributesCollection([
            TableAttributes(table='table2', attributes=['age'])
        ])

def test_retrieve_reference_values(context_retriever):
    nl_query = "Find users older than 30"
    relevant_attributes = TableAttributesCollection([
        TableAttributes(table='table2', attributes=['age'])
    ])
    relevant_nl_db_schema = NLDBSchema({'table2': 'Table containing user information with age'})
    
    mock_prompt = MagicMock()
    mock_prompt.run.return_value = [
        {
            'table': 'table2',
            'attribute': 'age',
            'values': ['30', '40']
        }
    ]
    
    with patch('lunar_nl2sql.retrievers.context_retriever.RetrieveReferenceValuesPrompt', return_value=mock_prompt):
        result = context_retriever._retrieve_reference_values(nl_query, relevant_attributes, relevant_nl_db_schema)
        assert result == TableReferenceValuesCollection([
            TableReferenceValues(table='table2', attribute='age', values=['30', '40'])
        ])

def test_retrieve_relevant_sample_data(context_retriever):
    relevant_tables = Tables(['table2'])
    result = context_retriever._retrieve_relevant_sample_data(relevant_tables)

    assert 'table2' in result.root

    assert result.root['table2'].iloc[0, 0] == 1

    assert result.root['table2'].iloc[0, 1] == 30