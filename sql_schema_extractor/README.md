# SQL Schema Extractor

## Overview
The **SQL Schema Extractor** is a component designed to connect to a SQL database and retrieve its schema, specifically the Data Definition Language (DDL). The output is a JSON object that describes the database schema.

## Features
- Connects to a specified SQL database.
- Extracts the schema information.
- Outputs the schema in a JSON format.

## Input Types
The component accepts the following input type:

- **URL**: A TEMPLATE type input, which should contain the connection string or URL needed to access the SQL database.

## Output Type
The component produces the following output type:

- **TEXT**: A JSON formatted string that describes the database schema.

## Configuration Parameters
This component does not require any additional configuration parameters.

## Usage
To use the **SQL Schema Extractor**, provide the necessary database connection URL as input. The component will connect to the database, retrieve the schema information, and output it as a JSON string.

## Example
- Input: 
  ```json
  {
      "URL": "your-database-connection-url"
  }
  ```
- Output:
  ```json
  {
      "tables": [
          {
              "name": "table_name",
              "columns": [
                  {
                      "name": "column_name",
                      "type": "data_type",
                      "constraints": ["constraint1", "constraint2"]
                  }
              ],
              "constraints": ["table_constraint1", "table_constraint2"]
          }
      ]
  }
  ```

Ensure you have the necessary permissions and access rights to connect to the SQL database and retrieve its schema before using the component.