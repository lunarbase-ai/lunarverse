# PostgreSQL Query Component

The **PostgreSQL Query** component is designed to execute SQL queries against a PostgreSQL database. It provides a simple interface for running queries and handling their results, with support for parameterized queries and error handling.

## Description

This component allows you to execute any SQL query against a PostgreSQL database. It handles both SELECT queries (returning results) and non-SELECT queries (returning affected rows). The component uses environment variables for database configuration and provides detailed error information when queries fail.

## Inputs

- **query** (`str`): The SQL query to execute
- **params** (`tuple`, optional): Parameters for the query (for parameterized queries)

## Output

- **result** (`dict`): A dictionary containing:
  - For SELECT queries:
    - `success`: Boolean indicating if the query was successful
    - `columns`: List of column names
    - `rows`: List of query results
  - For non-SELECT queries:
    - `success`: Boolean indicating if the query was successful
    - `message`: Success message
    - `rows_affected`: Number of rows affected
  - For failed queries:
    - `success`: False
    - `error`: Error message

## Input Types

- **query**: String containing a valid SQL query
- **params**: JSON (tuple) containing query parameters

## Output Type

- **result**: JSON (dictionary)

## Configuration Parameters

The component requires the following environment variables:
- `DATABASE`: Database name (default: 'default_db')
- `PG_USER`: Database user (default: 'default_user')
- `HOST`: Database host (default: 'localhost')
- `PASSWORD`: Database password (default: '')
- `PORT`: Database port (default: '5432')

## Example Use Cases

1. Execute SELECT queries to retrieve data
2. Run INSERT, UPDATE, or DELETE operations
3. Create or modify database schema
4. Execute parameterized queries safely
5. Handle database errors gracefully

## Notes

- The component uses connection pooling for better performance
- All queries are executed in a transaction
- Results are automatically committed for non-SELECT queries
- Error handling is built-in for all database operations
- Environment variables must be properly configured
- The component supports both synchronous and asynchronous operations 