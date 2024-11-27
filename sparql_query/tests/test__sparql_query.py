import pytest
from unittest.mock import patch
from lunarcore.connectors.sparql import SPARQLConnector
from sparql_query import SPARQLQuery

class TestSPARQLQuery:
    @patch.object(SPARQLConnector, 'query', return_value={"head": {}, "results": {"bindings": []}})
    def test_run_query_success(self, mock_query):
        config = {"endpoint": "http://example.com/sparql"}
        sparql_component = SPARQLQuery(**config)

        query = "SELECT ?person WHERE { ?person rdf:type dbo:Person } LIMIT 10"

        result = sparql_component.run(query)

        assert result == {"head": {}, "results": {"bindings": []}}
        mock_query.assert_called_once_with(query_string=query)


    @patch.object(SPARQLConnector, 'query', side_effect=Exception("SPARQL query failed"))
    def test_run_query_error_handling(self, mock_query):
        config = {"endpoint": "http://example.com/sparql"}
        sparql_component = SPARQLQuery(**config)

        query = "SELECT ?person WHERE { ?person rdf:type dbo:Person } LIMIT 10"

        with pytest.raises(Exception):
            sparql_component.run(query)

    @patch.object(SPARQLConnector, 'query', return_value={"head": {}, "results": {"bindings": [{"person": {"value": "http://dbpedia.org/resource/Albert_Einstein"}}]}})
    def test_run_query_with_results(self, mock_query):
        config = {"endpoint": "http://example.com/sparql"}
        sparql_component = SPARQLQuery(**config)

        query = "SELECT ?person WHERE { ?person rdf:type dbo:Person } LIMIT 10"

        result = sparql_component.run(query)

        assert result == {"head": {}, "results": {"bindings": [{"person": {"value": "http://dbpedia.org/resource/Albert_Einstein"}}]}}
        mock_query.assert_called_once_with(query_string=query)

