import pytest
from bar_chart import BarChart



class TestBarChart:
    def setup_method(self):
        self.bar_chart = BarChart()

    def test_plot_bar_chart_returns_base64_string_for_valid_data(self):
        input_data = {"A": 1, "B": 2, "C": 3}
        result = self.bar_chart.plot_bar_chart(input_data)
        assert result.startswith("data:image/png;base64,")

    def test_run_contains_data_key_for_valid_data(self):
        input_data = {"A": 1, "B": 2, "C": 3}
        result = self.bar_chart.run(input_data)
        assert "data" in result

    def test_run_contains_images_key_for_valid_data(self):
        input_data = {"A": 1, "B": 2, "C": 3}
        result = self.bar_chart.run(input_data)
        assert "images" in result

    def test_run_data_key_matches_input_for_valid_data(self):
        input_data = {"A": 1, "B": 2, "C": 3}
        result = self.bar_chart.run(input_data)
        assert result["data"] == input_data

    def test_run_images_key_contains_one_element_for_valid_data(self):
        input_data = {"A": 1, "B": 2, "C": 3}
        result = self.bar_chart.run(input_data)
        assert len(result["images"]) == 1

    def test_run_images_key_element_is_base64_string_for_valid_data(self):
        input_data = {"A": 1, "B": 2, "C": 3}
        result = self.bar_chart.run(input_data)
        assert result["images"][0].startswith("data:image/png;base64,")

    def test_plot_bar_chart_returns_base64_string_for_empty_data(self):
        input_data = {}
        result = self.bar_chart.plot_bar_chart(input_data)
        assert result.startswith("data:image/png;base64,")

    def test_run_contains_data_key_for_empty_data(self):
        input_data = {}
        result = self.bar_chart.run(input_data)
        assert "data" in result

    def test_run_contains_images_key_for_empty_data(self):
        input_data = {}
        result = self.bar_chart.run(input_data)
        assert "images" in result

    def test_run_handles_invalid_data_type(self):
        input_data = {"A": "invalid", "B": 2, "C": 3}
        with pytest.raises(TypeError):
            self.bar_chart.run(input_data)

    def test_run_handles_large_data_set(self):
        input_data = {f"Key{i}": i for i in range(1000)}
        result = self.bar_chart.run(input_data)
        assert "data" in result
        assert "images" in result

    def test_run_handles_negative_values(self):
        input_data = {"A": -1, "B": -2, "C": -3}
        result = self.bar_chart.run(input_data)
        assert "data" in result
        assert "images" in result

    def test_run_handles_zero_values(self):
        input_data = {"A": 0, "B": 0, "C": 0}
        result = self.bar_chart.run(input_data)
        assert "data" in result
        assert "images" in result