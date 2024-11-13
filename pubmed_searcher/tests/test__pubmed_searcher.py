import pytest
from unittest.mock import patch, AsyncMock
import pandas as pd
from pubmed_searcher import PubmedSearcher  # Adjust the import path if necessary

class TestPubmedSearcher:
    def setup_method(self):
        """
        Setup method to initialize PubmedSearcher before each test.
        """
        self.searcher = PubmedSearcher()

    @patch('pubmed_searcher.pubmed_scraper.main')
    def test_run_calls_main_with_correct_arguments(self, mock_main):
        """
        Test that the `run` method calls `pubmed_scraper.main` with the correct arguments.
        """
        # Arrange
        keywords = 'cancer'
        from_year = 2020
        to_year = 2023
        max_pages = 5

        # Act
        self.searcher.run(keywords, from_year, to_year, max_pages)

        # Assert
        mock_main.assert_called_once_with(max_pages, keywords, from_year, to_year)

    @patch('pubmed_searcher.pubmed_scraper.main')
    def test_run_returns_correctly_processed_results(self, mock_main):
        """
        Test that the `run` method correctly processes the results returned by `pubmed_scraper.main`.
        """
        # Arrange
        keywords = 'cancer'
        from_year = 2020
        to_year = 2023
        max_pages = 5

        # Mock DataFrame returned by main
        mock_data = pd.DataFrame({
            'authors': ['Author X', None, 'Author Z'],
            'journal': ['Journal 1', 'Journal 2', 'Journal 3'],
            'title': ['Study A', 'Study B', None],
        })
        mock_main.return_value = mock_data

        expected = [
            {'title': 'Study A', 'authors': 'Author X', 'journal': 'Journal 1'},
            {'title': 'Study B', 'authors': '', 'journal': 'Journal 2'},
            {'title': '', 'authors': 'Author Z', 'journal': 'Journal 3'}
        ]
        result = self.searcher.run(keywords, from_year, to_year, max_pages)

        assert result == expected