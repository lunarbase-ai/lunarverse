import pytest
from unittest.mock import patch, MagicMock
from gemini_llm import GeminiAIPrompt

class TestGeminiAIPrompt:

    def setup_method(self):
        self.env_patcher = patch.dict('os.environ', {
            'GEMINI_API_KEY': 'mock-api-key'
        })
        self.env_patcher.start()

        self.requests_post_patcher = patch('requests.post')
        self.mock_post = self.requests_post_patcher.start()

    def teardown_method(self):
        self.env_patcher.stop()
        self.requests_post_patcher.stop()

    def test_run_successful_response(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "This is a response from Gemini."}
                        ]
                    }
                }
            ]
        }
        self.mock_post.return_value = mock_response

        prompt = GeminiAIPrompt(api_key="mock-api-key")
        result = prompt.run("What is Gemini AI?")
        assert result == "This is a response from Gemini."
        self.mock_post.assert_called_once()

    def test_run_missing_candidates(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"candidates": []}
        self.mock_post.return_value = mock_response

        prompt = GeminiAIPrompt(api_key="mock-api-key")
        with pytest.raises(ValueError, match="Failed to parse Gemini's response"):
            prompt.run("What is Gemini AI?")

    def test_run_api_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        self.mock_post.return_value = mock_response

        prompt = GeminiAIPrompt(api_key="mock-api-key")
        with pytest.raises(RuntimeError, match="Error: 500 Internal Server Error"):
            prompt.run("What is Gemini AI?")

    def test_run_with_no_api_key(self):
        with patch.dict('os.environ', {'GEMINI_API_KEY': ''}):
            with pytest.raises(ValueError, match="API key is missing. Please provide a valid API key."):
                GeminiAIPrompt()

    def test_run_with_special_characters(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "Response for special characters."}
                        ]
                    }
                }
            ]
        }
        self.mock_post.return_value = mock_response

        prompt = GeminiAIPrompt(api_key="mock-api-key")
        result = prompt.run("!@#$%^&*()")
        assert result == "Response for special characters."
        self.mock_post.assert_called_once()

    def test_run_response_with_extra_whitespace(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "\n   Gemini's response.   \n"}
                        ]
                    }
                }
            ]
        }
        self.mock_post.return_value = mock_response

        prompt = GeminiAIPrompt(api_key="mock-api-key")
        result = prompt.run("Tell me about Gemini AI.")
        assert result == "Gemini's response."
        self.mock_post.assert_called_once()

    def test_run_handles_no_parts(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": []
                    }
                }
            ]
        }
        self.mock_post.return_value = mock_response

        prompt = GeminiAIPrompt(api_key="mock-api-key")
        with pytest.raises(ValueError, match="Failed to parse Gemini's response"):
            prompt.run("What is Gemini AI?")
