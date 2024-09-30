# GraphQL Query Component

## Description

The **GraphQL Query** component is designed to fetch data from a specified GraphQL endpoint. It processes the provided GraphQL query and returns the response in JSON format.

## Inputs

- **Query** (GRAPHQL): The GraphQL query string that specifies the data to be fetched from the endpoint.

## Output

- **Output** (dict): The response for the query, formatted as a JSON object.

## Configuration Parameters

- **endpoint**: The URL of the GraphQL endpoint from which data will be fetched.

## Usage

The **GraphQL Query** component requires the configuration of the `endpoint` parameter, which is the URL of the GraphQL service. The component takes a GraphQL query string as input and returns the corresponding response in JSON format. Ensure that the query is correctly formatted according to GraphQL specifications to retrieve the desired data.

Note: The actual implementation details of how to invoke the component and handle its output will depend on the specific environment and use case in which this component is deployed.