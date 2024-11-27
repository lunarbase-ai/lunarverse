# SPARQL Query Component

## Overview

The **SPARQL Query** component is designed to fetch data from a SPARQL endpoint. It takes a SPARQL query as input and returns the response in JSON format using the SPARQLWrapper library.

## Description

This component allows users to execute SPARQL queries against a specified SPARQL endpoint. It is particularly useful for interacting with RDF data stores and retrieving structured data based on the provided query.

- **Input (str):** A string that is the SPARQL query.
- **Output (dict):** A dictionary containing the response to the SPARQL query in the Python SPARQLWrapper library format.

## Input Types

- **Query:** A string containing the SPARQL query.

## Output Type

- **JSON:** The output is a JSON object formatted as a dictionary, which includes the response from the SPARQL query.

## Configuration Parameters

- **endpoint:** The URL of the SPARQL endpoint from which the data will be fetched.

## Usage

To use the SPARQL Query component, you need to provide a valid SPARQL query and configure the endpoint parameter to point to the desired SPARQL endpoint URL. The component will process the query and return the results in JSON format.