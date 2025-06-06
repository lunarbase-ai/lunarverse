# Milvus Insert Component

The **Milvus Insert** component is designed to insert documents into a Milvus collection. It provides a simple interface for inserting vector data, with support for connection configuration and error handling.

## Description

This component allows you to insert documents into a Milvus collection. It manages the connection with the Milvus server and provides detailed error information when operations fail. The component uses environment variables for configuration and supports different connection methods.

## Inputs

- **documents** (`List[dict]`): List of documents to insert into the collection

## Output

- **result** (`dict`): A dictionary containing:
  - `inserted`: Number of successfully inserted documents

## Input Types

- **documents**: JSON (List of dictionaries) containing the documents to be inserted

## Output Type

- **result**: JSON (dictionary)

## Configuration Parameters

The component requires the following environment variables:
- `collection_name`: Name of the Milvus collection
- `host`: Milvus server host (optional)
- `port`: Milvus server port (optional)
- `uri`: Milvus connection URI (optional)
- `MILVUS_USER`: Milvus user (default: environment variable)
- `MILVUS_PASSWORD`: Milvus password (default: environment variable)
- `MILVUS_TOKEN`: Milvus authentication token (default: environment variable)

## Use Cases

1. Insert documents into an existing collection
2. Insert vector data for semantic search
3. Update a collection with new documents
4. Manage Milvus server connections
5. Handle insertion errors gracefully

## Notes

- The component automatically manages the Milvus connection
- The connection is established at initialization and closed after each operation
- Error handling is built-in for all operations
- Environment variables must be properly configured
- The component supports different authentication methods
- The connection is released after each operation to prevent resource leaks