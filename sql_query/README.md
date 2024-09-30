# SQL Query Component

## Description
The `SQL Query` component is designed to connect to a SQL database, execute a provided SQL query, and return the result in CSV format. This component simplifies the process of querying a SQL database and obtaining results programmatically.

## Inputs
- `SQL` (str): The SQL query string that will be executed against the database.

## Outputs
- `Output` (CSV): The result of the executed SQL query in CSV format.

## Configuration Parameters
To use the `SQL Query` component, you need to configure the following parameters:

1. **driver_name**: The name of the database driver to use for the connection (e.g., `com.mysql.jdbc.Driver`).
2. **username**: The username required to authenticate with the SQL database.
3. **password**: The password required to authenticate with the SQL database.
4. **host**: The host address of the SQL database server (e.g., `localhost`, `192.168.1.1`).
5. **database**: The name of the database to connect to.

Ensure that these parameters are correctly set to establish a successful connection and execute the query.

## Example Configuration
```json
{
  "driver_name": "com.mysql.jdbc.Driver",
  "username": "your_username",
  "password": "your_password",
  "host": "localhost",
  "database": "your_database"
}
```

## Notes
- Make sure the database server is accessible from the network where this component is running.
- Ensure that the provided credentials have the necessary permissions to execute the query on the specified database.
- Handle sensitive information such as passwords securely and avoid exposing them in logs or error messages.

By configuring and utilizing the `SQL Query` component, you can easily run SQL queries and retrieve the results in a structured CSV format for further processing or analysis.