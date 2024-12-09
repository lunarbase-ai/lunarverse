import pytest
from unittest.mock import MagicMock, patch
from wikidata import Wikidata

class TestWikidata:
    @patch('wikidata.WikidataQueryRun')
    @patch('wikidata.CustomWikidataAPIWrapper')
    def test_wikidata_run(self, mock_api_wrapper, mock_query_run):

        mock_query_run_instance = MagicMock()
        mock_query_run_instance.run.return_value = [{"description": "President of the United States from 2009 to 2017"}]
        mock_query_run.return_value = mock_query_run_instance

        wikidata = Wikidata()


        result = wikidata.run("Barack Obama")

        assert result == {
            "results": [{"description": "President of the United States from 2009 to 2017"}]
        }
        mock_query_run_instance.run.assert_called_once_with("Barack Obama")

    @patch('wikidata.__init__.WikidataQueryRun')
    @patch('wikidata.__init__.CustomWikidataAPIWrapper')
    def test_wikidata_empty_query(self, mock_api_wrapper, mock_query_run):

        mock_query_run_instance = MagicMock()
        mock_query_run_instance.run.return_value = []
        mock_query_run.return_value = mock_query_run_instance

        wikidata = Wikidata()


        result = wikidata.run("")

        assert result == {
            "results": []
        }
        mock_query_run_instance.run.assert_not_called()