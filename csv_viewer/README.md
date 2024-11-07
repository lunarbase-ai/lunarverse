# Csv Viewer Component

## Overview
The Csv Viewer component is designed to display the contents of .csv files. This component takes in textual input and provides the output in CSV format, allowing users to visualize and interact with CSV data efficiently.

## Description
The Csv Viewer component processes input text representing the content of a .csv file and displays it accordingly. It enables users to handle and view CSV files conveniently within their applications or workflows.

## Input
- **Input text (TEXT):** The raw text input that contains the content of the .csv file.

Example: `"name,age,city\nAlice,30,New York\nBob,25,Los Angeles"`

## Output
- **CSV:** The processed CSV file content.

| name  | age | city        |
|-------|-----|-------------|
| Alice | 30  | New York    |
| Bob   | 25  | Los Angeles |

## Configuration Parameters
The Csv Viewer component supports the following configuration parameters to customize the display and processing of CSV files:

1. **sep:** The delimiter to use for separating values in the CSV file. Common delimiters include commas (`,`), semicolons (`;`), and tabs (`\t`).
2. **lineterminator:** The character sequence to use for terminating lines in the CSV file. This can be set to characters such as newline (`\n`), carriage return (`\r`). Note that only length-1 line terminators are supported. For example, using `\r\n` will raise a `ValueError`.

## Example

See [Lunar](lunar.lunarbase.ai) for an example of how to use this component in a workflow and much more.