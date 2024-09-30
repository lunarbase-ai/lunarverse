# Wikidata Client

## Overview

The `Wikidata Client` component is designed to interact with the Wikidata API, a comprehensive knowledge graph and knowledge base. This component retrieves detailed information for a given search term, making it accessible and useful for various applications such as data enrichment, knowledge discovery, and more.

## Description

The `Wikidata Client` component allows you to query the Wikidata API with a search term and retrieve structured data about the term. This is particularly useful for obtaining information about notable individuals, places, events, and other entities.

### Inputs

- **Query** (`str`): A string representing the term to search for in Wikidata. For example, `Barack Obama`.

### Output

- **Output** (`Dict[str, List[Dict]]`): A dictionary with a single key, `results`, which maps to a list of dictionaries. Each dictionary contains information and knowledge related to the query match. The list is sorted with the best match first.
  - Example output:
    ```json
    {
      "results": [
        {
          "description": "President of the United States from 2009 to 2017",
          ...
        }
      ]
    }
    ```

### Input Types

- **Query**: `TEXT`

### Output Type

- **Output**: `JSON`

### Configuration Parameters

This component does not require any configuration parameters.

## Key Features

- **Simple Query Interface**: Input a search term and get structured data back.
- **Sorted Results**: Results are sorted by relevance, with the best match appearing first.
- **Comprehensive Data**: Leverage the vast knowledge base of Wikidata for rich, detailed information.

## Usage

To use the `Wikidata Client` component, provide a search term via the `Query` input. The component will return a JSON object containing the search results, with each result providing detailed information about the best matches found in the Wikidata database.

This component is ideal for applications that need to enrich data with additional context or for users who wish to access detailed information about various entities quickly and efficiently.