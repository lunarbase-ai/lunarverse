# URLs Scraper

The **URLs Scraper** component is designed to scrape content from a list of URLs provided as input. It processes each URL and returns a structured output containing either the scraped content or an error message if the scraping fails.

## Description

This component takes in a list of URLs and attempts to scrape the content from each URL. The output is a dictionary where each URL from the input list is a key. The value for each key is another dictionary that contains either the scraped content or an error message.

## Inputs

- **Urls** (`List[str]`): A list of URLs (strings) that are to be scraped.

## Output

- **Output** (`Dict[str, Dict[str, str]]`): A dictionary where each key is a URL from the input list. The value for each key is another dictionary with:
  - `content` (`str`): The scraped content as a string (if the request was successful).
  - `error` (`str`): A descriptive error message (if the request failed).

## Input Types

- **Urls**: Expected to be a list of strings.

## Output Type

- **Output**: JSON

## Configuration Parameters

This component does not have any configuration parameters.

## Example

Given the following input:
```json
{
  "Urls": ["http://example.com", "http://example.org"]
}
```

The output will be a JSON object where each key is one of the input URLs, and the value is a dictionary containing either the scraped content or an error message:
```json
{
  "http://example.com": {
    "content": "<html>...</html>"
  },
  "http://example.org": {
    "error": "404 Not Found"
  }
}
```
