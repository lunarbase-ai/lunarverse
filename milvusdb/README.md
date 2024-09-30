# Milvus Vectorstore Component

## Description

The **Milvus Vectorstore** component is designed to store embeddings on a Milvus server. The component takes embeddings as input and stores them in the specified Milvus collection. Upon successful storage, it outputs a JSON object containing the number of stored embeddings.

## Inputs

- **Embeddings** (`EMBEDDINGS`): The embeddings that need to be stored in the Milvus server. This input is expected to be in the form of embeddings data.

## Outputs

- **Output** (`JSON`): A dictionary with a single key `stored`, which contains the number of embeddings that were successfully stored in the Milvus server.

  ```json
  {
      "stored": <number_of_stored_embeddings>
  }
  ```

## Configuration Parameters

To configure the **Milvus Vectorstore** component, the following parameters need to be specified:

- **collection_name**: The name of the collection in the Milvus server where the embeddings will be stored.
- **host**: The hostname or IP address of the Milvus server.
- **uri**: The URI of the Milvus server.
- **port**: The port number on which the Milvus server is listening.
- **user**: The username for authentication with the Milvus server.
- **password**: The password for authentication with the Milvus server.
- **token**: The authentication token for the Milvus server, if applicable.

## Usage

To use the **Milvus Vectorstore** component, ensure that you have properly configured the above parameters and provided the required embeddings. Once executed, the component will store the embeddings in the specified collection on the Milvus server and return a JSON object indicating the number of embeddings stored.