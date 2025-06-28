# URL2MD Component

The **URL2MD** component is designed to convert web pages to Markdown format using asynchronous web crawling. It takes a URL as input and returns the path to the generated Markdown file.

## Description

This component takes a URL as input and converts the web page content to Markdown format. The component handles URL parsing, file naming, and asynchronous web crawling to ensure efficient Markdown generation. The output is the path to the generated Markdown file in a temporary directory.

## Inputs

- **url** (`str`): The web page URL to be converted to Markdown.

## Output

- **result** (`str`): The path to the generated Markdown file in a temporary directory. Returns None if the conversion fails.

## Input Types

- **url**: Expected to be a string containing a valid URL.

## Output Type

- **result**: Text (string path)

## Configuration Parameters

This component does not have any configuration parameters.

## Example

Given the following input:
```
https://www.example.com/
```

The output will be a string containing the path to the generated Markdown file:
```
/tmp/tmpdir123/example_com.md
```

## Notes

- The component uses asynchronous web crawling for better performance
- The component requires internet access to download web pages
- Markdown files are saved in a temporary directory that is created when the component is instantiated
- Special characters in URLs are replaced with underscores in the filename
- If the URL path is empty, the file will be named "page.md"
