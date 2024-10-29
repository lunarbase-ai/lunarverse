from text_input import TextInput

class TestTextInput:

    def setup_method(self):
        self.text_input = TextInput()

    def test_text_input_run(self):
        input_text = "The quick brown fox jumps over the lazy dog"
        expected_output = "The quick brown fox jumps over the lazy dog"

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_empty_string(self):
        input_text = ""
        expected_output = ""

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_special_characters(self):
        input_text = "!@#$%^&*()_+"
        expected_output = "!@#$%^&*()_+"

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_numbers(self):
        input_text = "1234567890"
        expected_output = "1234567890"

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_whitespace(self):
        input_text = "   "
        expected_output = "   "

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_newlines(self):
        input_text = "Line1\nLine2\nLine3"
        expected_output = "Line1\nLine2\nLine3"

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_tabs(self):
        input_text = "Tab\tSeparated\tValues"
        expected_output = "Tab\tSeparated\tValues"

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_unicode(self):
        input_text = "こんにちは世界"  # "Hello, World" in Japanese
        expected_output = "こんにちは世界"

        output = self.text_input.run(input=input_text)

        assert output == expected_output

    def test_text_input_long_string(self):
        input_text = "a" * 1000
        expected_output = "a" * 1000

        output = self.text_input.run(input=input_text)

        assert output == expected_output
