# Deep Crawling Component

The **Deep Crawling** component is designed to extract information from web pages and their linked pages using LLM (Large Language Model) with BFS traversal. It takes a starting URL, an instruction, and crawling parameters as input and returns a dictionary containing the extracted content and crawling information.

## Description

This component uses an LLM to extract specific information from web pages based on a provided instruction, while traversing linked pages using BFS (Breadth-First Search). The component can be configured to follow external links and control the maximum depth of traversal.

## Inputs

- **url** (`str`): The starting web page URL to begin crawling
- **instruction** (`str`): The instruction for the LLM to extract desired information
- **include_external** (`bool`): Whether to follow external links during crawling
- **max_depth** (`int`): Maximum depth for BFS traversal

## Output

- **result** (`dict`): A dictionary containing:
  - `url`: The starting URL
  - `extracted_content`: Content extracted by the LLM
  - `visited_urls`: List of URLs visited during crawling
  - `depth`: Maximum depth reached during crawling
  Returns `None` if extraction fails

## Input Types

- **url**: String containing a valid URL
- **instruction**: String containing the instruction for the LLM
- **include_external**: Boolean indicating whether to follow external links
- **max_depth**: Integer specifying the maximum depth for crawling

## Output Type

- **result**: JSON (dictionary)

## Configuration Parameters

The component requires the following environment variables:
- `OPENAI_API_VERSION`: Azure OpenAI API version
- `DEPLOYMENT_NAME`: Azure OpenAI deployment name
- `OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL
- `PROVIDER`: LLM provider configuration

## Example Use Cases

1. Extract information from a website and its internal pages
2. Gather data from multiple related pages
3. Analyze content across a domain
4. Collect information from a network of linked pages
5. Perform deep content analysis of a website

## Notes

- The component uses BFS traversal to visit linked pages
- External link following can be enabled/disabled
- Maximum depth can be configured to control crawling scope
- The component returns detailed information about the crawling process
- Environment variables must be properly configured for the LLM to work
- The component handles rate limiting and respects website crawling policies 