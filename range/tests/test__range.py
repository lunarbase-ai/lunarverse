import pytest
from range import Range

class TestRange:
    def setup_method(self):
        self.component = Range()

    def test_generates_standard_one_step_sequence(self):
        result = list(self.component.run(start=0, stop=5, step=1))
        assert result == [0, 1, 2, 3, 4]

    def test_generates_custom_step_sequence(self):
        result = list(self.component.run(start=2, stop=10, step=2))
        assert result == [2, 4, 6, 8]

    def test_generates_negative_sequences(self):
        result = list(self.component.run(start=10, stop=2, step=-2))
        assert result == [10, 8, 6, 4]

    def test_raises_type_error_for_non_integer_start(self):
        with pytest.raises(TypeError):
            list(self.component.run(start='a', stop=5, step=1))

    def test_raises_value_error_for_zero_step(self):
        with pytest.raises(ValueError):
            list(self.component.run(start=0, stop=5, step=0))

    def test_returns_empty_list_when_start_equals_stop(self):
        result = list(self.component.run(start=5, stop=5, step=1))
        assert result == []

    def test_returns_single_element_for_large_step(self):
        result = list(self.component.run(start=0, stop=1, step=2))
        assert result == [0]

    def test_output_is_generator(self):
        result = self.component.run(start=0, stop=5, step=1)
        assert hasattr(result, '__iter__')