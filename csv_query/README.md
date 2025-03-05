# CsvQuery Component

## Description
The CsvQuery component is designed to query CSV files using SQL. It allows users to execute SQL queries on CSV files and returns the results in JSON format.

## Inputs
- `query (str)`: A SQL query string to be executed on the provided CSV files.
- `csv_files (dict)`: A dictionary where keys are table names and values are file paths to the CSV files. 


## Output
The component produces the following output:

- A CSV string containing the results of the executed SQL query.

## Input Types
This component accepts the following input types:

- query: `TEXT`
- csv_files: `JSON`

## Output Type
This component produces output in the following type:

`JSON`

## Configuration Parameters
This component does not require any configuration parameters.

## Usage

To use the CsvQuery component, you need to provide a SQL query string and a dictionary of CSV files as input. The component will execute the SQL query on the provided CSV files and return the results as a CSV string.

-- 

Thank you for using the CsvQuery component. If you encounter any issues or have any questions, please refer to the documentation or contact support.