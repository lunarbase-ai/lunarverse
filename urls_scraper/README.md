# URLs Scraper

The **URLs Scraper** component is designed to scrape content from a list of URLs provided as input. It processes each URL and returns a structured output containing either the scraped content.

## Description

This component takes in a list of URLs and attempts to scrape the content from each URL. The output is a dictionary where each URL from the input list is a key. The value for each key is another dictionary that contains scraped content, a success flag, the HTTP code of the request, and an error message if scraping fails.

## Inputs

- **Urls** (`List[HttpUrl]`): A list of URLs (strings) that are to be scraped.

## Output

- **Output** (`Dict[HttpUrl, ScraperResultModel]`): A dictionary where each key is a URL from the input list. The value for each key is another dictionary with:
  - `content` (`str`): The scraped content as a string. On fail it returns an empty string
  - `error` (`str`): A descriptive error message if it fails.
  - `success`: A flag indicating whether it failed or succeded in scraping content
  - `code`: The HTTP code of the request made for scraping content

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
  "Urls": ["http://example.com", "http://example/NOT_FOUND"]
}
```

The output will be a JSON object where each key is one of the input URLs, and the value is a dictionary containing::
```json
{
  "http://example.com": {
    "content": "<html>...</html>"
    "success": True,
    "code": 200,
  },
  "http://example/NOT_FOUND": {
    "error": "A http error 404 ocurred",
    "success": False,
    "code": 404,
    "content": ""
  }
}
```
