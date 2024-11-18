import pytest
from html_reports_builder import HTMLReportsBuilder

class TestHTMLReportsBuilder:
    def setup_method(self):
        self.html_reports_builder = HTMLReportsBuilder()

    def test_run_returns_correct_output_for_valid_template_and_data(self):
        template_j2 = "<html><head><title>{{ title }}</title></head></html>"
        data = {"william": {"title": "William is cool"}}
        result = self.html_reports_builder.run(template_j2, data)
        assert result == {"william": "<html><head><title>William is cool</title></head></html>"}

    def test_run_handles_multiple_entries_in_data(self):
        template_j2 = "<html><head><title>{{ title }}</title></head></html>"
        data = {
            "william": {"title": "William is cool"},
            "john": {"title": "John is awesome"}
        }
        result = self.html_reports_builder.run(template_j2, data)
        assert result == {
            "william": "<html><head><title>William is cool</title></head></html>",
            "john": "<html><head><title>John is awesome</title></head></html>"
        }

    def test_run_handles_empty_data(self):
        template_j2 = "<html><head><title>{{ title }}</title></head></html>"
        data = {}
        result = self.html_reports_builder.run(template_j2, data)
        assert result == {}

    def test_run_handles_missing_template_variable(self):
        template_j2 = "<html><head><title>{{ title }}</title></head></html>"
        data = {"william": {}}
        result = self.html_reports_builder.run(template_j2, data)
        assert result == {"william": "<html><head><title></title></head></html>"}

    def test_run_handles_none_template_variable(self):
        template_j2 = "<html><head><title>{{ title }}</title></head></html>"
        data = {"william": {"title": None}}
        result = self.html_reports_builder.run(template_j2, data)
        assert result == {"william": "<html><head><title></title></head></html>"}

    def test_run_handles_invalid_template(self):
        template_j2 = "<html><head><title>{{ title }</title></head></html>"  # Missing closing brace
        data = {"william": {"title": "William is cool"}}
        with pytest.raises(Exception):
            self.html_reports_builder.run(template_j2, data)

    def test_run_handles_large_data_set(self):
        template_j2 = "<html><head><title>{{ title }}</title></head></html>"
        data = {f"user{i}": {"title": f"User {i} is cool"} for i in range(1000)}
        result = self.html_reports_builder.run(template_j2, data)
        assert len(result) == 1000
        assert result["user0"] == "<html><head><title>User 0 is cool</title></head></html>"

    def test_run_handles_special_characters_in_template(self):
        template_j2 = "<html><head><title>{{ title }}</title></head></html>"
        data = {"william": {"title": "William & Co."}}
        result = self.html_reports_builder.run(template_j2, data)
        assert result == {"william": "<html><head><title>William &amp; Co.</title></head></html>"}