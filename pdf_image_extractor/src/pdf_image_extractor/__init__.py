import io
import base64
from typing import List

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType, File, Base64FileContent

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
    output_type=DataType.LIST,
    component_group=ComponentGroup.DATA_EXTRACTION,
):
    def run(self, path: str) -> List:
        pipeline_options = PdfPipelineOptions()

        pipeline_options.do_picture_description = True
        pipeline_options.picture_description_options = PictureDescriptionVlmOptions(
            repo_id="ds4sd/SmolDocling-256M-preview",
            prompt="Describe the image in three sentences. Be concise and accurate."
        )
        pipeline_options.images_scale = 2.0
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = False       
        pipeline_options.generate_picture_images = True

        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        result = doc_converter.convert(path)
        doc = result.document

        image_counter = 0
        output = []
        for item, _ in doc.iterate_items():
            if isinstance(item, PictureItem):
                description = item.caption_text(doc)
                
                pil_image = item.get_image(doc)
                if pil_image:
                    img_byte_arr = io.BytesIO()
                    pil_image.save(img_byte_arr, format='PNG')
                    image_bytes = img_byte_arr.getvalue()

                    base64_encoded_content = base64.b64encode(image_bytes).decode('utf-8')
                    
                    file_content = Base64FileContent(content=base64_encoded_content)
                    
                    file = {
                        "name": f"image_{image_counter}.png",
                        "type": "image/png",
                        "size": len(image_bytes),
                        "description": description,
                        "content": file_content
                    }
                    output.append({"description": description, "file": file})
                    
                    image_counter += 1
                else:
                    print(f"Could not retrieve image for {item.self_ref}")
        return output
    