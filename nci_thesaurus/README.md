# NCI Thesaurus Component

## Overview

The **NCI Thesaurus** component is designed to retrieve biomedical information from the NCI Thesaurus using SPARQL queries. The results are returned in JSON format, making it easy to integrate with various applications and workflows that require biomedical data.

## Description

The NCI Thesaurus is a reference terminology and biomedical ontology used for coding, organization, and retrieval of clinical and research data. This component facilitates querying the NCI Thesaurus to obtain relevant information through SPARQL, a powerful query language for databases that store data in RDF format.

## Inputs

The component accepts a single input:

- **Query** (type: TEMPLATE): The SPARQL query template that will be executed against the NCI Thesaurus to retrieve the required biomedical information. The query should be crafted according to the SPARQL standards and the structure of the NCI Thesaurus RDF data.

## Output

The output of the component is a JSON object containing the results of the SPARQL query. The structure of the JSON object will depend on the specifics of the query executed.

## Configuration Parameters

This component does not require any additional configuration parameters.

## Usage

The NCI Thesaurus component is straightforward to use. Simply provide a valid SPARQL query template as input, and the component will return the query results in JSON format. Ensure that your SPARQL queries are well-formed and tailored to the NCI Thesaurus data schema for optimal results.

## Notes

- Familiarity with SPARQL and RDF data structures is recommended to effectively utilize this component.
- Ensure that your query is compatible with the NCI Thesaurus RDF schema for accurate data retrieval.

For more information on the NCI Thesaurus and its data schema, refer to the official documentation and resources provided by the National Cancer Institute.