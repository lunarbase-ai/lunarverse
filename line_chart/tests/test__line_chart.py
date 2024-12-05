import pytest
from line_chart import LineChart

class TestLineChart:
    def setup_method(self):
        self.line_chart = LineChart()

    def test_plot_line_chart_returns_base64_string_for_valid_data(self):
        input_data = {"x": [1, 2, 3], "y": [1, 2, 3]}
        result = self.line_chart.plot_line_chart(input_data)
        assert result.startswith("data:image/png;base64,")

    def test_run_contains_data_key_for_valid_data(self):
        input_data = {"x": [1, 2, 3], "y": [1, 2, 3]}
        result = self.line_chart.run(input_data)
        assert "data" in result

    def test_run_contains_images_key_for_valid_data(self):
        input_data = {"x": [1, 2, 3], "y": [1, 2, 3]}
        result = self.line_chart.run(input_data)
        assert "images" in result

    def test_run_data_key_matches_input_for_valid_data(self):
        input_data = {"x": [1, 2, 3], "y": [1, 2, 3]}
        result = self.line_chart.run(input_data)
        assert result["data"] == input_data

    def test_run_images_key_contains_one_element_for_valid_data(self):
        input_data = {"x": [1, 2, 3], "y": [1, 2, 3]}
        result = self.line_chart.run(input_data)
        assert len(result["images"]) == 1

    def test_run_raises_value_error_for_mismatched_data(self):
        input_data = {"x": [1, 2, 3], "y": [1, 2, 3, 4]}
        with pytest.raises(ValueError, match="x and y must have the same length"):
            self.line_chart.run(input_data)

    def test_run_replaces_none_with_zero(self):
        input_data = {"x": [1, None, 3], "y": [1, 2, 3]}
        result = self.line_chart.run(input_data)
        assert "data" in result
        assert "images" in result
        assert result["images"][0].startswith("data:image/png;base64,")

    def test_plot_line_chart_raises_key_error_for_missing_x(self):
        input_data = {"y": [1, 2, 3]}
        with pytest.raises(KeyError, match="Input dictionary must contain both 'x' and 'y' keys"):
            self.line_chart.plot_line_chart(input_data)

    def test_plot_line_chart_raises_key_error_for_missing_y(self):
        input_data = {"x": [1, 2, 3]}
        with pytest.raises(KeyError, match="Input dictionary must contain both 'x' and 'y' keys"):
            self.line_chart.plot_line_chart(input_data)