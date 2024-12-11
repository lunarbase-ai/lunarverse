from html2text.extractor import HTMLTextExtractor
import pytest 
from pydantic import AnyUrl

class TestHTMLTextExtractor:
    
    def setup_method(self):
        self.extractor = HTMLTextExtractor()

    def test_extract_valid_html(self):
        html_content_mapper = {
            "http://example.com": {
                "content": "Hello, <b>world</b>! This is a test."
            }
        }
        expected_result = {
            AnyUrl("http://example.com"): {
                "content": "Hello, <b>world</b>! This is a test.",
                "text": "Hello, world ! This is a test."
            }
        }
        result = self.extractor.extract(html_content_mapper)

        assert result == expected_result

    def test_extract_invalid_html(self):
        html_content_mapper = {
            "invalid-url": {
                "content": "Hello, <b>world</b>! This is a test."
            }
        }
        with pytest.raises(ValueError, match="Invalid Html content mapper"):
            self.extractor.extract(html_content_mapper)

    def test_extract_empty_html(self):
        html_content_mapper = {
            "http://example.com": {
                "content": ""
            }
        }
        expected_result = {
            AnyUrl("http://example.com"): {
                "content": "",
                "text": ""
            }
        }
        result = self.extractor.extract(html_content_mapper)
        assert result == expected_result

    def test_extract_html_with_special_characters(self):
        html_content_mapper = {
            "http://example.com": {
                "content": "Hello, &amp; welcome to the <b>world</b> of <i>Python</i>!"
            }
        }
        expected_result = {
            AnyUrl("http://example.com"): {
                "content": "Hello, &amp; welcome to the <b>world</b> of <i>Python</i>!",
                "text": "Hello, & welcome to the world of Python !"
            }
        }
        result = self.extractor.extract(html_content_mapper)
        assert result == expected_result