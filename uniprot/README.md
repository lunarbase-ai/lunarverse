# UniProt Component

## Overview
The `UniProt` component is designed to fetch data from UniProt, a database known for its high-quality, comprehensive, and freely accessible protein sequence and functional information. This component takes a SPARQL query as input and returns the response in a dictionary format.

## Description
The `UniProt` component allows users to interact with the UniProt database using SPARQL queries. It leverages the [SPARQLWrapper](https://sparqlwrapper.readthedocs.io/en/latest/) library to execute these queries and process the results.

### Input
- **Query (str)**: A string that contains the SPARQL query to be executed.

### Output
- **Response (dict)**: A dictionary containing the response to the SPARQL query in the format provided by the SPARQLWrapper library.

### Configuration Parameters
- **endpoint (str)**: The SPARQL endpoint URL that the component will query against.

## Input Types
The component accepts the following input types:
- **Query**: SPARQL

## Output Type
The component returns output in the following format:
- **Response**: JSON

## Configuration
To configure the `UniProt` component, you need to specify the SPARQL endpoint URL. This endpoint is where the SPARQL queries will be sent.

### Example Configuration
```json
{
  "endpoint": "https://sparql.uniprot.org/sparql"
}
```

## Dependencies
The `UniProt` component relies on the following Python library:
- **SPARQLWrapper**: This library is used to interact with SPARQL endpoints and process query results.

For more information on how to use the SPARQLWrapper library, please refer to the [SPARQLWrapper documentation](https://sparqlwrapper.readthedocs.io/en/latest/).