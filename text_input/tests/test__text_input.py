from text_input import TextInput

class TestTextInput:

    def setup_method(self):
        self.text_input = TextInput()

    def test_text_input_run(self):
        input_text = "Hello, World!"
        expected_output = "Hello, World!"

        output = self.text_input.run(input=input_text)

        assert output == expected_output
