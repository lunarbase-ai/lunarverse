from typing import Any

from docling.document_converter import DocumentConverter
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
from lunarcore.component.lunar_component import LunarComponent

class FileToText(
    LunarComponent,
    component_name="File to Text",
    component_description="""Converts a file to text using Docling. It receives the file path as input.""",
    input_types={"file_input": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.UTILS,
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)

    def run(self, file_input: str):
        converter = DocumentConverter()
        result = converter.convert(file_input)
        return result.document.export_to_text()
