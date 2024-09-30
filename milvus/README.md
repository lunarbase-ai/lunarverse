# Milvus Retriever

## Overview
The Milvus Retriever is a component designed to query embeddings from a Milvus server. This component outputs a list of dictionaries, each containing the original text and the corresponding embeddings for each text item in the input.

## Description
The Milvus Retriever connects to a Milvus server and retrieves embeddings based on the input query embeddings. This can be particularly useful in scenarios where you need to fetch similar items or perform nearest-neighbor searches based on vector similarity.

## Input Type
- **Query embedding**: The query embeddings that will be used to search the Milvus server. This input should be in the form of `EMBEDDINGS`.

## Output Type
- **JSON**: The output is a JSON object, which is a list of dictionaries. Each dictionary contains:
  - `original_text` (str): The original text corresponding to the retrieved embeddings.
  - `embeddings` (List[Union[float, int]]): The embedding vectors for the corresponding text item.

## Configuration Parameters
To configure the Milvus Retriever, the following parameters need to be set:

- **collection_name**: The name of the collection in the Milvus server from which embeddings are to be retrieved.
- **host**: The hostname or IP address of the Milvus server.
- **uri**: The URI of the Milvus server.
- **port**: The port number on which the Milvus server is listening.
- **user**: The username for authentication with the Milvus server.
- **password**: The password for authentication with the Milvus server.
- **token**: The token for authentication if token-based authentication is used.

## Summary
The Milvus Retriever component is a powerful tool for querying embeddings from a Milvus server. By setting the appropriate configuration parameters, you can efficiently retrieve and use embeddings for various applications, such as similarity searches and data analysis. The output is a JSON object containing the original text and their corresponding embeddings, providing a structured and easy-to-use format for further processing.