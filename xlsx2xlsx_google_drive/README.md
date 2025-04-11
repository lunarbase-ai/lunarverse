# xlsx2xlsx Google Drive Component

## Description

The **xlsx2xlsx Google Drive** component automates the workflow of downloading an `.xlsx` file from Google Drive, updating it with content from another Excel file, and re-uploading it back to Google Drive. The new content is written to a specific sheet, either updating it or creating it if it does not exist.

## Inputs

- **file_link** (str): The public or shareable Google Drive link of the file to be updated. Example: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`.
- **credentials_json** (str): Path to the Google Cloud service account credentials JSON file.
- **excel_file** (str): Path to the local Excel file from which data will be read and written into the Google Drive file.
- **sheet_name** (str): The name of the sheet in the Google Drive Excel file where the new data will be written. If the sheet does not exist, it will be created.

## Outputs

- **result** (str): The name of the file after it is successfully updated and re-uploaded to Google Drive.

## Usage

To use the **xlsx2xlsx Google Drive** component, you need:

1. A shareable Google Drive link to an Excel file (.xlsx).
2. A service account credentials file with access to that file.
3. A local Excel file whose data will be read and written into the Drive file.
4. The name of the sheet to update (will be created if it doesn't exist).

This component reads all visible columns (ignoring 'Unnamed' columns), maps their contents into cell values, updates the specified sheet in the Google Drive file, saves the changes, and uploads it back to the same file location.


## Example

If your inputs are:

"file_link": "https://drive.google.com/file/d/1aBcDeFgHijklMnOPq/view?usp=sharing",
"credentials_json": "/path/to/service_account.json",
"excel_file": "/path/to/local_data.xlsx",
"sheet_name": "UpdatedData"

The output might be:

my_file.xlsx