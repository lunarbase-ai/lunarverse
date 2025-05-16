# PDF Image Extractor Component

## Overview

The PDF Image Extractor component extracts images from PDF files and returns them in a structured format with descriptions and metadata.

## Description

The PDF Image Extractor component processes PDF files to extract embedded images, their descriptions, and metadata. It uses Docling's document processing pipeline to handle the PDF extraction and image processing.

### Output

- **Output (List):** A list of extracted images, each containing:
  - Description of the image
  - File information (name, type, size)
  - Base64-encoded image content

## Inputs

- **path (TEXT):** The path to the PDF file to process

## Output

- **List:** A list of dictionaries, each containing:
  - `description`: Text description of the image
  - `file`: Dictionary containing:
    - `name`: Generated filename (e.g., "image_0.png")
    - `type`: MIME type of the image (e.g., "image/png")
    - `size`: Size of the image in bytes
    - `description`: Same as the top-level description
    - `content`: Dictionary containing:
      - `type`: Always "base64"
      - `content`: Base64-encoded image data

## Configuration

The component uses Docling's PDF processing pipeline with the following default settings:
- Image scaling: 2.0x
- Picture description: Enabled
- OCR: Disabled
- Table structure: Disabled
