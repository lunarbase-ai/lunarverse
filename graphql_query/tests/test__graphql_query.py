import pytest
import requests
from unittest.mock import patch
from lunarcore.component.data_types import DataType
from graphql_query import GraphQLQuery 

class TestGraphQLQuery:
    @pytest.fixture
    def graphql_component(self):
        return GraphQLQuery(endpoint="https://mock-graphql-endpoint.com")

    @patch("requests.post")
    def test_run_successful_query(self, mock_post, graphql_component):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {"countries": [{"name": "Testland", "code": "TST"}]}
        }

        query = """
        {
          countries {
            name
            code
          }
        }
        """
        result = graphql_component.run(query=query)


        assert mock_post.called, "requests.post was not called"
        assert result["data"]["countries"][0]["name"] == "Testland"
        assert result["data"]["countries"][0]["code"] == "TST"

    @patch("requests.post")
    def test_run_query_error_response(self, mock_post, graphql_component):
        mock_post.status_code = 400
        mock_post.json.return_value = {"errors": [{"message": "Bad request"}]}
        
        mock_post.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Client Error: Bad Request for url")
        
        mock_post.return_value = mock_post

        query = """
        {
        countries {
            name
            code
        }
        }
        """

        with pytest.raises(requests.exceptions.HTTPError):
            graphql_component.run(query=query)

    @patch("requests.post")
    def test_run_invalid_endpoint(self, mock_post):
        component = GraphQLQuery(endpoint="https://invalid-endpoint.com")
        mock_post.side_effect = requests.exceptions.ConnectionError

        query = """
        {
          countries {
            name
            code
          }
        }
        """

        with pytest.raises(requests.exceptions.ConnectionError):
            component.run(query=query)

    @patch("requests.post")
    def test_run_empty_response(self, mock_post, graphql_component):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}

        query = """
        {
          countries {
            name
            code
          }
        }
        """

        result = graphql_component.run(query=query)

        # Assertions
        assert mock_post.called, "requests.post was not called"
        assert result == {}, "The response should be empty"

    @patch("requests.post")
    def test_run_missing_query(self, mock_post, graphql_component):
        mock_post.return_value.status_code = 400

        with pytest.raises(TypeError):
            graphql_component.run(query=None)
