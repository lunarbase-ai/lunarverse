# PDF Extractor Component

## Description

The `PDF Extractor` component is designed to extract structured information from PDF files. It processes the PDF to retrieve the title, sections, references, tables, and full text content.

## Inputs

- **File path** (`Union[str, List[str]>`): This can be a single string containing the server path of a PDF file to extract from, or a list of such server paths.

## Output

- **Output** (`Union[Dict, List[Dict]>`): The output is either a dictionary or a list of dictionaries (if multiple PDF file paths are provided). Each dictionary includes the following key-value pairs:
  - **title** (`str`): The title of the PDF file.
  - **sections** (`Dict[str, List[str]>`): A dictionary mapping section titles to their respective contents.
  - **references** (`List[str]>`): A list of bibliographic references found in the PDF file.
  - **tables** (`List[str]>`): A list of record-formatted pandas dataframes.
  - **text** (`List[str]>`): A list of strings containing the full document text.

## Input Types

- **File path**: `TEXT`

## Output Type

- **JSON**

## Configuration Parameters

To use the `PDF Extractor` component, you need to configure the following parameters:

- **client_id**: Your client ID for authentication.
- **client_secret**: Your client secret for authentication.

Ensure that these parameters are properly set before running the component to enable successful extraction and access.

## Summary

The `PDF Extractor` is a powerful tool to automate the extraction of important data from PDF files. By providing the file paths and necessary configuration parameters, users can efficiently extract titles, sections, references, tables, and the complete text of the documents, enabling easy access and processing of the information contained within the PDFs.