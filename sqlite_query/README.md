# Sqlite Query Component

## Description

The **Sqlite Query** component is designed to connect to a local SQLite database file, execute a SQL query, and return the result in CSV format. This component streamlines the process of querying a SQLite database and retrieving results programmatically.

## Inputs

- **db_path (TEXT)**: The local path to the SQLite database file.
- **query (TEXT)**: The SQL query string to be executed against the database.

## Outputs

- **Output (CSV)**: The result of the executed SQL query in CSV format (including headers).

## Configuration Parameters

This component does not require any additional configuration parameters.

## Usage

The **Sqlite Query** component is straightforward to use:
1. Provide the local path of the SQLite database file (`db_path`).
2. Provide the SQL query you wish to execute (`query`).
3. The component will handle the database connection, execute the query, and return the results as a CSV string.

