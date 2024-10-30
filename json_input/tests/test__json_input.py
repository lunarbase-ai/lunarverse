import pytest
from json_input import JSONInput
import json

class TestJSONInput:
    def setup_method(self):
        self.json_input = JSONInput()

    def test_valid_json_input(self):
        input_str = '{"key": "value"}'
        expected_output = {"key": "value"}
        assert self.json_input.run(input=input_str) == expected_output

    def test_invalid_json_input(self):
        input_str = '{"key": "value"'
        with pytest.raises(json.JSONDecodeError):
            self.json_input.run(input=input_str)

    def test_empty_json_input(self):
        input_str = '{}'
        expected_output = {}
        assert self.json_input.run(input=input_str) == expected_output