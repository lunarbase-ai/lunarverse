# Csv Upload Component

The **Csv Upload** component is designed to read and process a CSV file that contains a header row, i.e., the first line of the CSV file represents the column titles. This component reads the input CSV file and provides a preview of the data in a formatted string.

## Description

The component reads a CSV file specified by the user, ensuring that the file contains a header row. It then generates a preview of the first ten rows of the data, formatted as a string.

## Inputs

- **Input file** (File): A File object that includes a field `path` (str), which specifies the local path to the CSV file to read. This component should only be used if the CSV file has a header row.

## Outputs

- **Output** (File): A File object with a field `preview` containing a string representation of the first ten rows of the data from the input CSV file. The format of this preview is akin to a pandas DataFrame converted to CSV, illustrating the top rows of the CSV data.

## Configuration Parameters

- **sep** (str): The delimiter to use for separating columns in the CSV file. This parameter allows customization of the CSV parsing process to accommodate different delimiter types (e.g., comma, semicolon, tab).

### Summary

The Csv Upload component facilitates the reading of CSV files with headers and provides an easy-to-read preview of the top rows of the data. It accepts a file path as input and outputs a formatted string preview of the data, making it simple to quickly inspect the contents of the CSV file.