# Online Spreadsheet Component

## Description
The **Online Spreadsheet** component is designed to download and output the content of an online spreadsheet. It supports various online storage services and outputs the spreadsheet data as a list of records.

## Supported Services
- Nextcloud folder with `.xlsx` files
- Owncloud `.xlsx` files
- Google Drive **published** spreadsheets

## Inputs
- **Url** (`str`): The URL of the online spreadsheet.
  - Supported formats:
    - Nextcloud folder with `.xlsx` files
    - Owncloud `.xlsx` files
    - Google Drive **published** spreadsheets
- **Filename** (`str`): (Optional) The name of the file to download when using Owncloud or Nextcloud.
- **Folder_password** (`str`): (Optional) The password of the shared folder when using Owncloud or Nextcloud.

## Outputs
- **List[Dict]**: A list where each item is a dictionary representing a record from the spreadsheet.

## Input Types
- **Url**: `TEXT`
- **Filename**: `TEXT`
- **Folder_password**: `TEXT`

## Output Type
- **List**

## Configuration Parameters
This component does not require any configuration parameters.

## Usage
To use the **Online Spreadsheet** component, provide the required inputs (`Url`, `Filename`, and `Folder_password` if applicable) to download and process the spreadsheet data. The component will return a list of records from the spreadsheet in dictionary format.