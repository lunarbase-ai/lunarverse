# Online Spreadsheet IO Component

## Overview

The **Online Spreadsheet IO** component is designed to facilitate the saving of data to an online spreadsheet and subsequently forward the content. This component is particularly useful for applications that need to store and manipulate data in a structured format on an online platform and then distribute or process that data further.

## Description

The Online Spreadsheet IO component takes various input parameters including the data content, a URL to the spreadsheet, a filename, a folder password, and a merge option. It processes these inputs to save the data into the specified online spreadsheet and then forwards the content as a list.

## Inputs

The component accepts the following inputs:

- **Content (LIST)**: The data to be saved into the online spreadsheet. This should be provided in a list format.
- **Url (TEXT)**: The URL of the online spreadsheet where the data will be saved.
- **Filename (TEXT)**: The name of the file where the data will be stored within the online spreadsheet.
- **Folder_password (TEXT)**: The password for the folder containing the online spreadsheet, if applicable.
- **Merge (INT)**: An integer value indicating whether to merge the data with existing content in the spreadsheet (1 for merge, 0 for overwrite).

## Output

The component produces the following output:

- **Output (LIST)**: A list containing the forwarded content after the data has been saved to the online spreadsheet.

## Configuration Parameters

This component does not require any additional configuration parameters.

## Example Usage

To use the Online Spreadsheet IO component, provide the necessary inputs such as the content to be saved, the URL of the online spreadsheet, the filename, the folder password, and the merge option. Once the data is processed and saved, the component will output the forwarded content as a list.

Please refer to the user guide or API documentation for more detailed information on how to integrate and utilize the Online Spreadsheet IO component in your application.