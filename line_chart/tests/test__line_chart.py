import pytest
from line_chart import LineChart

class TestLineChart:
    def setup_method(self):
        self.line_chart = LineChart()

    def test_plot_line_chart_returns_base64_string_for_valid_data(self):
        input_data = {"1": 1, "2": 2, "3": 3}
        result = self.line_chart.plot_line_chart(input_data)
        assert result.startswith("data:image/png;base64,")

    def test_run_contains_data_key_for_valid_data(self):
        input_data = {"1": 1, "2": 2, "3": 3}
        result = self.line_chart.run(input_data)
        assert "data" in result

    def test_run_contains_images_key_for_valid_data(self):
        input_data = {"1": 1, "2": 2, "3": 3}
        result = self.line_chart.run(input_data)
        assert "images" in result

    def test_run_data_key_matches_input_for_valid_data(self):
        input_data = {"1": 1, "2": 2, "3": 3}
        result = self.line_chart.run(input_data)
        assert result["data"] == input_data

    def test_run_images_key_contains_one_element_for_valid_data(self):
        input_data = {"1": 1, "2": 2, "3": 3}
        result = self.line_chart.run(input_data)
        assert len(result["images"]) == 1

    def test_run_images_key_element_is_base64_string_for_valid_data(self):
        input_data = {"1": 1, "2": 2, "3": 3}
        result = self.line_chart.run(input_data)
        assert result["images"][0].startswith("data:image/png;base64,")

    def test_plot_line_chart_returns_base64_string_for_empty_data(self):
        input_data = {}
        result = self.line_chart.plot_line_chart(input_data)
        assert result.startswith("data:image/png;base64,")

    def test_run_contains_data_key_for_empty_data(self):
        input_data = {}
        result = self.line_chart.run(input_data)
        assert "data" in result

    def test_run_contains_images_key_for_empty_data(self):
        input_data = {}
        result = self.line_chart.run(input_data)
        assert "images" in result


    def test_run_handles_large_data_set(self):
        input_data = {str(i): i for i in range(1000)}
        result = self.line_chart.run(input_data)
        assert "data" in result
        assert "images" in result

    def test_run_handles_negative_values(self):
        input_data = {"1": -1, "2": -2, "3": -3}
        result = self.line_chart.run(input_data)
        assert "data" in result
        assert "images" in result

    def test_run_handles_zero_values(self):
        input_data = {"1": 0, "2": 0, "3": 0}
        result = self.line_chart.run(input_data)
        assert "data" in result
        assert "images" in result