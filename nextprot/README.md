# NeXtProt Component

## Overview
The `NeXtProt` component fetches data from neXtProt, an online knowledge platform dedicated to human proteins. neXtProt provides extensive information on various aspects of human proteins, including their function, subcellular location, expression, interactions, and roles in diseases.

## Functionality
This component allows users to execute SPARQL queries against the neXtProt database. The input to the component is a SPARQL query string, and the output is a dictionary containing the response formatted according to the [SPARQLWrapper](https://sparqlwrapper.readthedocs.io/en/latest/) library.

## Input
- **Query (str)**: A string that represents the SPARQL query to be executed.

## Output
- **Output (dict)**: A dictionary containing the response to the SPARQL query, formatted in the standard output format of the SPARQLWrapper library.

## Configuration Parameters
- **endpoint**: The SPARQL endpoint URL for the neXtProt database.

## Usage
The `NeXtProt` component requires a SPARQL query string as input and will return the query results in JSON format. The endpoint for the SPARQL query must be configured appropriately.

## Dependencies
- [SPARQLWrapper](https://sparqlwrapper.readthedocs.io/en/latest/): A Python wrapper around a SPARQL service.

## Notes
Ensure that the SPARQL query provided as input is valid and correctly formatted to avoid errors in fetching data. The endpoint URL must be correctly configured to point to the neXtProt SPARQL endpoint.

For more details on formulating SPARQL queries and using the SPARQLWrapper library, please refer to the [SPARQLWrapper documentation](https://sparqlwrapper.readthedocs.io/en/latest/).