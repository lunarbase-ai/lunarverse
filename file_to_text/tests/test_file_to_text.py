import pytest
from unittest.mock import MagicMock, patch
from pdf_to_text.src.pdf_to_text import PDFtoText


@pytest.fixture
def mock_converter():
    mock = MagicMock()
    mock.convert.return_value.document.export_to_text.return_value = "# Mocked Text Output"
    return mock


@patch("pdf_to_text.src.pdf_to_text.DocumentConverter")
def test_pdf_to_text(mock_doc_converter, mock_converter):
    mock_doc_converter.return_value = mock_converter

    component = PDFtoText()
    file_input = "test.pdf"
    result = component.run(file_input)

    mock_converter.convert.assert_called_once_with(file_input)
    assert result == "# Mocked Text Output"
