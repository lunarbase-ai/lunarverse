import pytest
from unittest.mock import MagicMock
from lunar_nl2sql.services.ai import AIService
from lunar_nl2sql.retrievers.context_retriever import ContextRetriever
from lunar_nl2sql.generators.generator import Generator
from lunar_nl2sql.prompts import GenerateSQLQueryPrompt, DoubleCheckQueryPrompt
from lunar_nl2sql.retrievers.types import (
    Tables,
    TableAttributesCollection,
    TableAttributes,
    TableReferenceValuesCollection,
    TableReferenceValues,
    Context,
)
from lunar_nl2sql.data_access.types import TableSamples
from pandas import DataFrame

@pytest.fixture
def ai_service():
    return MagicMock(spec=AIService)

@pytest.fixture
def context_retriever():
    return MagicMock(spec=ContextRetriever)

@pytest.fixture
def generator(ai_service, context_retriever):
    return Generator(ai_service, context_retriever)

@pytest.fixture
def context_with_attributes():
    return Context(
        relevant_tables=Tables(['users']),
        relevant_attributes=TableAttributesCollection([
            TableAttributes(table='users', attributes=['age', 'name'])
        ]),
        reference_values=TableReferenceValuesCollection([
            TableReferenceValues(table='users', attribute='age', values=['30', '40'])
        ]),
        relevant_sample_data=TableSamples({
            'users': DataFrame([{'age': 30, 'name': 'John'}])
        }),
        relevant_nl_db_schema={'users': 'Users table with age and name'}
    )

@pytest.fixture
def context_without_attributes():
    return Context(
        relevant_tables=Tables(['users']),
        relevant_attributes=TableAttributesCollection([]),
        reference_values=TableReferenceValuesCollection([]),
        relevant_sample_data=TableSamples({
            'users': DataFrame([{'age': 30, 'name': 'John'}])
        }),
        relevant_nl_db_schema={'users': 'Users table with age and name'}
    )

@pytest.fixture
def mock_prompts():
    generator_prompt = MagicMock(spec=GenerateSQLQueryPrompt)
    double_check_prompt = MagicMock(spec=DoubleCheckQueryPrompt)
    return generator_prompt, double_check_prompt

def test_generator_init(generator, ai_service, context_retriever):
    assert generator.ai_service == ai_service
    assert generator.context_retriever == context_retriever
    assert isinstance(generator.generator_prompt, GenerateSQLQueryPrompt)
    assert isinstance(generator.double_check_prompt, DoubleCheckQueryPrompt)

def test_generator_generate(generator, context_retriever, context_with_attributes, mock_prompts):
    generator_prompt, double_check_prompt = mock_prompts
    
    # Set up the mocks
    context_retriever.retrieve.return_value = context_with_attributes
    generator_prompt.run.return_value = "SELECT * FROM users WHERE age > 30"
    double_check_prompt.run.return_value = "SELECT * FROM users WHERE age > 30"
    
    # Replace the prompts in the generator instance
    generator.generator_prompt = generator_prompt
    generator.double_check_prompt = double_check_prompt
    
    # Test the generate method
    nl_query = "Find users older than 30"
    result = generator.generate(nl_query)
    
    # Verify the context retriever was called
    context_retriever.retrieve.assert_called_once_with(nl_query)
    
    # Verify the prompts were called with correct arguments
    generator_prompt.run.assert_called_once()
    double_check_prompt.run.assert_called_once()
    
    # Verify the final result
    assert result == "SELECT * FROM users WHERE age > 30"

def test_generator_generate_with_no_attributes(generator, context_retriever, context_without_attributes, mock_prompts):
    generator_prompt, double_check_prompt = mock_prompts
    
    # Set up the mocks
    context_retriever.retrieve.return_value = context_without_attributes
    generator_prompt.run.return_value = "SELECT * FROM users"
    double_check_prompt.run.return_value = "SELECT * FROM users"
    
    # Replace the prompts in the generator instance
    generator.generator_prompt = generator_prompt
    generator.double_check_prompt = double_check_prompt
    
    # Test the generate method
    nl_query = "Show me all users"
    result = generator.generate(nl_query)
    
    assert result == "SELECT * FROM users"