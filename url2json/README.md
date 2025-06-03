# URL2JSON Component

## Description

The **URL2JSON** component converts web pages to JSON using asynchronous web crawling. It takes a URL as input, downloads the web page content, and returns a JSON dictionary containing the URL and HTML content. The component handles URL parsing and asynchronous web crawling to ensure efficient JSON generation.

## Inputs

- **url** (str): The web page URL to be converted to JSON. Example: `https://example.com/page`

## Outputs

- **result** (dict): A JSON dictionary with keys `url` and `html`. Returns None if the conversion fails.

## Usage

To use the **URL2JSON** component, you need:

1. A valid web page URL that you want to convert to JSON

The component will:
1. Parse the URL to ensure it's valid
2. Download the web page content asynchronously
3. Return a JSON dictionary containing the URL and HTML content

## Example

Input URL:
```
https://www.example.com/
```

Output JSON:
```
{
    "url": "https://www.example.com/",
    "html": "<!DOCTYPE html>..."
}
```

## Notes

- The component uses asynchronous web crawling for better performance
- The component requires internet access to download web pages
- The output is a Python dictionary that can be easily converted to JSON if needed
- The HTML content is returned with UTF-8 encoding to properly handle special characters

## Features

- Asynchronous web crawling
- JSON content return
- Valid URL support
- Error handling and failure cases

## Requirements

- Python 3.8+
- crawl4ai
- lunarcore

## Installation

```