from unittest.mock import patch, MagicMock
import pytest
from lyrics_generator import LyricsGenerator


@pytest.fixture
def mock_environment():
    with patch.dict("os.environ", {
        "OPENAI_API_KEY": "mocked_api_key",
        "OPENAI_API_VERSION": "v1",
        "DEPLOYMENT_NAME": "mocked_deployment",
        "AZURE_OPENAI_ENDPOINT": "mocked_endpoint"
    }):
        yield


@pytest.fixture
def mock_invoke():
    with patch("langchain_openai.AzureChatOpenAI.invoke") as mock_invoke:
        yield mock_invoke

def test_run_with_valid_inputs(mock_environment, mock_invoke):
    mock_response = MagicMock()
    mock_response.content = "Generated lyrics"
    mock_invoke.return_value = mock_response

    component = LyricsGenerator()
    result = component.run(
        theme="love",
        mood="happy",
        setting="beach",
        key_words=["sunshine", "waves"],
        other_instructions="Make it rhyme"
    )

    mock_invoke.assert_called_once()  
    assert result == "Generated lyrics"


def test_run_handles_api_error(mock_environment, mock_invoke):
    mock_invoke.side_effect = Exception("API error")

    component = LyricsGenerator()
    
    try:
        component.run(
            theme="hope",
            mood="inspirational",
            setting="mountains",
            key_words=["dream", "sky"],
            other_instructions="Focus on metaphors"
        )

        assert False, "Expected RuntimeError but none was raised"
    
    except RuntimeError as e:
        assert "An error occurred while generating lyrics" in str(e)

    mock_invoke.assert_called_once()


def test_run_with_large_input(mock_environment, mock_invoke):
    mock_response = MagicMock()
    mock_response.content = "Generated lyrics"
    mock_invoke.return_value = mock_response

    large_keywords = ["keyword" + str(i) for i in range(1000)] 

    component = LyricsGenerator()
    result = component.run(
        theme="adventure",
        mood="exciting",
        setting="forest",
        key_words=large_keywords,
        other_instructions="Make it thrilling"
    )

    assert result == "Generated lyrics"
    mock_invoke.assert_called_once()
