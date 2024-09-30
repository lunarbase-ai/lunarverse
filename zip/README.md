# Zip File Extractor

## Description

The **Zip File Extractor** component is designed to extract files from a ZIP file (.zip file) located on the server. This component simplifies the process of unzipping files and directories from a specified ZIP file path and provides the list of extracted files and directories.

## Inputs

- **File path** (`str`): A string representing the server path to the ZIP file that needs to be extracted.
  - Example: `/path/on/server/my_zip.zip`

## Output

- **Output** (`List[str]`): A list of server paths of the files and directories that were extracted from the ZIP file.
  - Example: 
    - `/path/on/server/file1_in_my_zip.txt`
    - `/path/on/server/file2_in_my_zip.txt`
    - `/path/on/server/directory1_in_my_zip/`

## Input Types

- **File path**: `TEXT`

## Output Type

- **Output**: `LIST`

## Configuration Parameters

This component does not require any configuration parameters. 

## Usage

This component can be used in any scenario where there is a need to extract files from a ZIP file on the server and retrieve the paths of the extracted files and directories.