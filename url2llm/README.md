# URL2LLM Component

The **URL2LLM** component is designed to extract information from web pages using LLM (Large Language Model). It takes a URL and an instruction as input and returns a dictionary containing the URL and the content extracted by the LLM.

## Description

This component uses an LLM to extract specific information from web pages based on a provided instruction. The LLM analyzes the page content and returns the information requested in the instruction.

## Inputs

- **url** (`str`): The web page URL to be analyzed.
- **instruction** (`str`): The instruction for the LLM to extract desired information.

## Output

- **result** (`dict`): A dictionary with `url` and `extracted_content` keys. Returns `None` if extraction fails.

## Input Types

- **url**: Expected to be a string containing a valid URL.
- **instruction**: Expected to be a string containing the instruction for the LLM.

## Output Type

- **result**: JSON (dictionary)

## Configuration Parameters

The component requires the following environment variables:
- `OPENAI_API_VERSION`: Azure OpenAI API version
- `DEPLOYMENT_NAME`: Azure OpenAI deployment name
- `OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL

## Example

The component can be used to extract various types of information from web pages. For instance:

1. Extract product information from e-commerce pages
2. Summarize news articles
3. Extract contact information from business websites
4. Get key points from documentation pages
5. Extract structured data from government websites

Here's a specific example using Wikipedia:

Input:
- URL: "https://en.wikipedia.org/wiki/Artificial_intelligence"
- Instruction: "Extract the main definition of artificial intelligence and list its key applications"

The LLM will analyze the Wikipedia page and return a structured response containing the requested information.

## Notes

- The component uses a configured LLM to extract specific information
- The component requires internet access to access web pages
- The instruction should be clear and specific for better results
- The component returns `None` if it fails to extract content or if the URL is invalid
- Environment variables must be properly configured for the LLM to work 