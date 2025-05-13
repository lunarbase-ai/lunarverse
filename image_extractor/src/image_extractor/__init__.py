


from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

from docling.datamodel.pipeline_options import PdfPipelineOptions, PictureDescriptionVlmOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc import PictureItem

class PDFImageExtractor(
    LunarComponent,
    component_name="PDF Image Extractor",
    component_description="""Extracts images from a PDF file.
    Inputs:
      `path` (str): The path to the PDF file.
    """,
    input_types={"path": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.UTILS,
):
    def run(self, path: str):
        pipeline_options = PdfPipelineOptions()

        pipeline_options.do_picture_description = True

        pipeline_options.picture_description_options = PictureDescriptionVlmOptions(
            repo_id="ds4sd/SmolDocling-256M-preview",
            prompt="Describe the image in three sentences. Be concise and accurate."
        )

        pipeline_options.images_scale = 2.0
        
        pipeline_options.generate_picture_images = True

        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        result = doc_converter.convert(path)
        doc = result.document

        for item, _ in doc.iterate_items():

            if isinstance(item, PictureItem):
                description = item.caption_text(doc)
                print(f"Description for {item.self_ref}: {description}")
            # You can now feed 'description' to your LLM
        return path
    