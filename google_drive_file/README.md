# Google Drive File Component

## Description

The **Google Drive File** component is designed to download files from Google Drive using a shared link. It authenticates with a Google Cloud service account and retrieves the file, saving it locally. The component returns the local path to the downloaded file upon success. This is useful for pipelines that depend on external file resources managed in Google Drive.

## Inputs

| input name       | input data type | example value                                                                 | description                                                                                   |
|------------------|-----------------|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| file_link        | str             | `https://drive.google.com/file/d/1aBcDeFgHijklMnOPq/view?usp=sharing`         | A shareable Google Drive link pointing to the file to download.                              |
| credentials_json | str             | `/path/to/your/service_account_credentials.json`                              | Path to a Google Cloud service account JSON file with access to the file in Google Drive.    |

## Outputs

The component outputs a string representing the **local file path** where the downloaded file was saved.

| output name | output data type | example value                | description                                                                 |
|-------------|------------------|------------------------------|-----------------------------------------------------------------------------|
| result      | str              | `/tmp/downloaded_file.xlsx` | Path to the file saved locally after being downloaded from Google Drive.   |

## Usage

To use the **Google Drive File** component, provide:

1. A valid shareable `file_link` from Google Drive.
2. The path to a `credentials_json` file from a Google Cloud service account that has permission to access the file.

The component will authenticate using the service account, download the file, and return the local path to the saved file.

> Note: The file must be either public or explicitly shared with the service account's email address.

## Example

If your inputs are:

"file_link": "https://drive.google.com/file/d/1aBcDeFgHijklMnOPq/view?usp=sharing",
"credentials_json": "/secrets/gdrive-service-account.json"

The output might be:

```bash
/tmp/downloaded_file.xlsx
```