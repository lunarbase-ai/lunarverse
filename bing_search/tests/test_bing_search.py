from unittest.mock import patch
import pytest
from bing_search import BingSearch


@pytest.fixture
def mock_environment():
    with patch.dict("os.environ", {
        "BING_SUBSCRIPTION_KEY": "mocked_api_key",
    }):
        yield


@pytest.fixture
def mock_results():
    with patch("langchain_community.utilities.BingSearchAPIWrapper.results") as mock_results:
        yield mock_results


def test_bing_search(mock_environment, mock_results):
    bing_search = BingSearch()
    bing_search.run("test")
    mock_results.assert_called_once_with("test", 10)


def test_bing_search_failure(mock_environment, mock_results):
    mock_results.side_effect = Exception("mocked exception")
    bing_search = BingSearch()
    with pytest.raises(RuntimeError):
        bing_search.run("test")

def test_custom_total_results(mock_environment, mock_results):
    bing_search = BingSearch(total_results=20)
    bing_search.run("test")
    mock_results.assert_called_once_with("test", 20)