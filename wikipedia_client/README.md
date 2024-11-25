# Wikipedia Client

## Description

The Wikipedia Client component is designed to retrieve data from the Wikipedia API. This component takes a query string as input and returns a dictionary containing the content of the found Wikipedia article.

## Input

- `Query` (str): A string representing the query to use for finding the article. For example, `Fermat's last theorem`.

### Input Types

- `Query`: TEXT

## Output

- Output (Dict[str, str]): A dictionary with the key `content` mapped to a string of the content of the found article.

### Output Type

- JSON

## Configuration Parameters

This component does not require any configuration parameters.

## Usage

To use the Wikipedia Client, simply provide a query string, and the component will return a JSON object containing the content of the Wikipedia article corresponding to the query.