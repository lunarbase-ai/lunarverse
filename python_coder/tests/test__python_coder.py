import pytest
from python_coder import PythonCoder

class TestPythonCoder:
    def setup_method(self):
        self.coder = PythonCoder()

    def test_run_valid_code(self):
        code = "result = 1 + 1"
        assert self.coder.run(code) == 2

    def test_run_invalid_code(self):
        code = "result = 1 / 0"
        with pytest.raises(ZeroDivisionError):
            self.coder.run(code)

    def test_run_syntax_error(self):
        code = "result ="
        with pytest.raises(SyntaxError):
            self.coder.run(code)

    def test_run_no_result(self):
        code = "a = 1 + 1"
        assert self.coder.run(code) is None