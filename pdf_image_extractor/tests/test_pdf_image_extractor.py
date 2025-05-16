import pytest
from unittest.mock import Mock, patch
from pdf_image_extractor import PDFImageExtractor
from docling_core.types.doc import PictureItem
import base64
from lunarcore.component.component_group import ComponentGroup
from PIL import Image
import io

MOCK_PDF_PATH = "test.pdf"
MOCK_IMAGE_DESCRIPTION = "A test image description"
MOCK_IMAGE_BYTES = b"fake_image_bytes"
MOCK_BASE64_CONTENT = base64.b64encode(MOCK_IMAGE_BYTES).decode('utf-8')

@pytest.fixture
def mock_image():
    image = Image.new('RGB', (100, 100), color='red')
    return image

@pytest.fixture
def mock_picture_item(mock_image):
    mock_item = Mock(spec=PictureItem)
    mock_item.self_ref = "test_ref"
    mock_item.get_image.return_value = mock_image
    mock_item.caption_text.return_value = MOCK_IMAGE_DESCRIPTION
    return mock_item

@pytest.fixture
def mock_document(mock_picture_item):
    mock_doc = Mock()
    mock_doc.iterate_items.return_value = [
        (mock_picture_item, None),
        (mock_picture_item, None)
    ]
    return mock_doc

@pytest.fixture
def component(mock_document):
    with patch('pdf_image_extractor.DocumentConverter') as mock_converter_class:
        mock_converter = mock_converter_class.return_value
        mock_result = Mock()
        mock_result.document = mock_document
        mock_converter.convert.return_value = mock_result
        yield PDFImageExtractor()

def test_init():
    with patch('pdf_image_extractor.DocumentConverter'):
        component = PDFImageExtractor()
        assert component.component_name == "PDF Image Extractor"
        assert component.component_group == ComponentGroup.DATA_EXTRACTION

def test_run_returns_correct_number_of_images(component):
    result = component.run(MOCK_PDF_PATH)
    assert len(result) == 2

def test_run_image_has_description(component):
    result = component.run(MOCK_PDF_PATH)
    assert "description" in result[0]
    assert result[0]["description"] == MOCK_IMAGE_DESCRIPTION

def test_run_image_has_file(component):
    result = component.run(MOCK_PDF_PATH)
    assert "file" in result[0]
    file = result[0]["file"]
    assert file["name"] == "image_0.png"
    assert file["type"] == "image/png"

def test_run_image_has_metadata(component):
    result = component.run(MOCK_PDF_PATH)
    file = result[0]["file"]
    assert "size" in file
    assert file["description"] == MOCK_IMAGE_DESCRIPTION

def test_run_image_has_base64_content(component):
    result = component.run(MOCK_PDF_PATH)
    file = result[0]["file"]
    assert file["content"]["type"] == "base64"
    content = file["content"]["content"]
    assert isinstance(content, str)

def test_run_image_content_is_valid(component):
    result = component.run(MOCK_PDF_PATH)
    file = result[0]["file"]
    content = file["content"]["content"]
    image_bytes = base64.b64decode(content)
    image = Image.open(io.BytesIO(image_bytes))
    assert image.size == (100, 100)
    assert image.mode == "RGB"

def test_run_no_images(component, mock_document):
    mock_document.iterate_items.return_value = []
    result = component.run(MOCK_PDF_PATH)
    assert result == []

def test_run_image_retrieval_failure(component, mock_picture_item):
    mock_picture_item.get_image.return_value = None
    result = component.run(MOCK_PDF_PATH)
    assert result == []

def test_run_doc_converter_error(component):
    with patch('pdf_image_extractor.DocumentConverter') as mock_converter_class:
        mock_converter = mock_converter_class.return_value
        mock_converter.convert.side_effect = Exception("Conversion failed")
        with pytest.raises(Exception, match="Conversion failed"):
            component.run(MOCK_PDF_PATH) 