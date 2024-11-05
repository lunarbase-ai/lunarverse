from html2text.extractor import TextParser

class TestTextParser:
    
    def setup_method(self):
        self.parser = TextParser()

    def test_get_text_simple_html(self):
        html_content = "Hello, <b>world</b>! This is a test."
        self.parser.feed(html_content)
        extracted_text = self.parser.get_text()
        assert extracted_text == "Hello, world ! This is a test."

    def test_get_text_with_nested_tags(self):
        html_content = "<div>Hello, <span>world</span>! <p>This is a <b>test</b>.</p></div>"
        self.parser.feed(html_content)
        extracted_text = self.parser.get_text()
        assert extracted_text == "Hello, world ! This is a test ."

    def test_get_text_with_special_characters(self):
        html_content = "Hello, &amp; welcome to the <b>world</b> of <i>Python</i>!"
        self.parser.feed(html_content)
        extracted_text = self.parser.get_text()
        assert extracted_text == "Hello, & welcome to the world of Python !"

    def test_get_text_empty_html(self):
        html_content = ""
        self.parser.feed(html_content)
        extracted_text = self.parser.get_text()
        assert extracted_text == ""

    def test_get_text_only_tags(self):
        html_content = "<div><span></span></div>"
        self.parser.feed(html_content)
        extracted_text = self.parser.get_text()
        assert extracted_text == ""