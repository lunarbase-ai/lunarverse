import pytest
from unittest.mock import MagicMock, patch
from file_to_markdown.src.file_to_markdown import FileToMarkdown


@pytest.fixture
def mock_converter():
    mock = MagicMock()
    mock.convert.return_value.document.export_to_markdown.return_value = "# Mocked Markdown Output"
    return mock


@patch("file_to_markdown.src.file_to_markdown.DocumentConverter")
def test_file_to_markdown(mock_doc_converter, mock_converter):
    mock_doc_converter.return_value = mock_converter

    component = FileToMarkdown()
    file_input = "test.pdf"
    result = component.run(file_input)

    mock_converter.convert.assert_called_once_with(file_input)
    assert result == "# Mocked Markdown Output"
