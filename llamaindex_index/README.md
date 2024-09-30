# LlamaIndex Indexing Component

## Overview

The **LlamaIndex Indexing** component is designed to index documents from a JSON dictionary using Azure OpenAI models within LlamaIndex. This component allows you to specify which keys from the JSON documents should be indexed and provides various options for the type of index to be created.

## Description

This component indexes documents from a JSON dictionary using Azure OpenAI models within LlamaIndex. Users need to provide:

- A list of keys to be selected (in JSON string format).
- A choice from the available index types: `summary`, `vector`, `keyword`, or `tree`.
- A name for the storage index.
- Relevant Azure OpenAI details.

The output is a dictionary containing the following keys:

- `original_json`: Copy of the input JSON.
- `index_dir`: Directory where the index is stored.
- `index_name`: Name of the stored index.
- `keys_list`: List of the stored index keys.
- `llm_config`: Configuration of the Language Model (LLM).
- `embed_model_config`: Configuration of the embedding model.

## Input Types

- **Documents Json**: JSON - A JSON dictionary containing the documents to be indexed.

## Output Type

- **Output**: JSON - A dictionary containing the following keys:
  - `original_json`: Copy of the input JSON.
  - `index_dir`: Directory where the index is stored.
  - `index_name`: Name of the stored index.
  - `keys_list`: List of the stored index keys.
  - `llm_config`: Configuration of the LLM.
  - `embed_model_config`: Configuration of the embedding model.

## Configuration Parameters

- **keys_list**: A JSON string specifying the list of keys to be selected from the documents.
- **index_name**: A string specifying the type of index to be created (`summary`, `vector`, `keyword`, or `tree`).
- **index_persist_dir**: A string specifying the name for the storage index directory.
- **azure_api_key**: The API key for Azure OpenAI.
- **azure_endpoint**: The endpoint for Azure OpenAI.
- **api_version**: The API version for Azure OpenAI.
- **llm_model_name**: The name of the Language Model (LLM) to be used.
- **llm_deployment_name**: The deployment name for the LLM.
-