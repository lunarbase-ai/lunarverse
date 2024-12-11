from unittest.mock import patch, MagicMock
from wikipedia_client import Wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
import pytest


class TestWikipedia:

    @patch('wikipedia.page')
    def test_run_success(self, mock_wikipedia_page):
        mock_page = MagicMock()
        mock_page.content = "Sample content"
        mock_page.summary = "Sample summary"
        mock_wikipedia_page.return_value = mock_page

        wikipedia_client = Wikipedia()

        result = wikipedia_client.run("Sample query")

        assert result == {
            "content": "Sample content",
            "summary": "Sample summary"
        }

    @patch('wikipedia.page')
    def test_run_disambiguation_error(self, mock_wikipedia_page):
        mock_wikipedia_page.side_effect = DisambiguationError("Sample query", ["Option1", "Option2"])

        wikipedia_client = Wikipedia()

        with pytest.raises(DisambiguationError):
            wikipedia_client.run("Sample query")

    @patch('wikipedia.page')
    def test_run_page_error(self, mock_wikipedia_page):
        mock_wikipedia_page.side_effect = PageError("Sample query", "Page not found")

        wikipedia_client = Wikipedia()

        with pytest.raises(PageError):
            wikipedia_client.run("Sample query")

    @patch('wikipedia.page')
    def test_run_empty_query(self, mock_wikipedia_page):
        wikipedia_client = Wikipedia()

        with pytest.raises(ValueError):
            wikipedia_client.run("")

    @patch('wikipedia.page')
    def test_run_general_exception(self, mock_wikipedia_page):
        mock_wikipedia_page.side_effect = Exception("General error")

        wikipedia_client = Wikipedia()

        with pytest.raises(Exception):
            wikipedia_client.run("Sample query")