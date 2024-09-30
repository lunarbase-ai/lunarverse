# LlamaIndex Querying Component

## Description

The **LlamaIndex Querying** component allows users to query data from a LlamaIndex index. Users can provide a query prefix if needed and specify whether the query should be retrieval-only. The output of the query will be in JSON format.

## Input Types

- **Index Details Json** (JSON): A JSON object containing the details of the LlamaIndex.
- **Query** (TEMPLATE): The query template to be executed against the LlamaIndex.

## Output Type

- **Output** (JSON): The result of the query execution, returned in JSON format.

## Configuration Parameters

- **query_prefix**: An optional prefix to be added to the query.
- **retrieval_only**: A boolean flag to indicate whether the query should be retrieval-only. Set this to `True` if only retrieval is needed, otherwise set it to `False`.
- **top_k**: An integer k specifying how many of the best matches should be outputed if retrival-only.

## Usage

To use the LlamaIndex Querying component, provide the necessary input types and configure the parameters according to your needs. The component will execute the query on the provided LlamaIndex and return the results in JSON format.

For any further details or questions, please refer to the official documentation or support resources.