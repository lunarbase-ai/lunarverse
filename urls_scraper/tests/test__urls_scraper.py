import requests
from unittest.mock import patch, MagicMock
from urls_scraper import URLsScraper

class TestURLsScraper:

    def setup_method(self):
        self.scraper = URLsScraper()

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_scraper_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Success content"
        mock_get.return_value = mock_response

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": True,
                "content": mock_response.content.decode("utf-8"),
                "code": mock_response.status_code
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_scraper_multiple_urls(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Success content"
        mock_get.return_value = mock_response

        urls = ["http://example.com", "http://example.org"]
        expected_result = {
            "http://example.com": {
                "success": True,
                "content": mock_response.content.decode("utf-8"),
                "code": mock_response.status_code
            },
            "http://example.org": {
                "success": True,
                "content": mock_response.content.decode("utf-8"),
                "code": mock_response.status_code
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_scraper_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = b""
        mock_get.return_value = mock_response

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "code": mock_response.status_code,
                "error": "A http error 404 occurred"
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_scraper_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "A timeout occurred",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_scraper_too_many_redirects(self, mock_get):
        mock_get.side_effect = requests.exceptions.TooManyRedirects

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "Too many redirects",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_url_required(self, mock_get):
        mock_get.side_effect = requests.exceptions.URLRequired

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "A valid URL is required",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_scraper_invalid_url(self, mock_get):
        mock_get.side_effect = requests.exceptions.InvalidURL

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "Invalid URL",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_content_decoding_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ContentDecodingError

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "Error decoding response content",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_retry_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RetryError

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "Request failed after retries",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_ssl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.SSLError

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "SSL error occurred",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "A request exception occurred",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_unknown_exception(self, mock_get):
        mock_get.side_effect = Exception

        urls = ["http://example.com"]
        expected_result = {
            "http://example.com": {
                "success": False,
                "content": "",
                "error": "An unexpected exception occurred",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result

    @patch('urls_scraper.scraper.requests.get')
    def test_urls_scraper_mixed_results(self, mock_get):
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.content = b"Success content"
        
        error_404_response = MagicMock()
        error_404_response.status_code = 404
        error_404_response.content = b""

        mock_get.side_effect = [
            success_response,
            error_404_response,
            requests.exceptions.Timeout
        ]

        urls = ["http://example.com/success", "http://example.com/not_found", "http://example.com/timeout"]
        expected_result = {
            "http://example.com/success": {
                "success": True,
                "content": success_response.content.decode("utf-8"),
                "code": success_response.status_code
            },
            "http://example.com/not_found": {
                "success": False,
                "content": "",
                "code": error_404_response.status_code,
                "error": "A http error 404 occurred"
            },
            "http://example.com/timeout": {
                "success": False,
                "content": "",
                "error": "A timeout occurred",
                "code": 0
            }
        }

        result = self.scraper.run(urls)
        assert result == expected_result