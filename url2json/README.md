# URL2JSON Component

The **URL2JSON** component is designed to convert web pages to JSON using asynchronous web crawling. It takes a URL as input and returns a JSON dictionary containing the URL and HTML content.

## Description

This component takes a URL as input and converts the web page content to a JSON dictionary. The JSON contains the keys `url` and `html_content`. The component handles URL parsing and asynchronous web crawling to ensure efficient JSON generation.

## Inputs

- **url** (`str`): The web page URL to be converted to JSON.

## Output

- **result** (`dict`): A JSON dictionary with keys `url` and `html_content`. Returns None if the conversion fails.

## Input Types

- **url**: Expected to be a string containing a valid URL.

## Output Type

- **result**: JSON (dictionary)

## Configuration Parameters

This component does not have any configuration parameters.

## Example

Given the following input:
```
https://www.example.com/
```

The output will be a dictionary:
```python
{
    "url": "https://www.example.com/",
    "html_content": "<html>...content...</html>"
}
```

## Notes

- The component uses asynchronous web crawling for better performance
- The component requires internet access to download web pages
- The output is a Python dictionary that can be easily converted to JSON if needed 