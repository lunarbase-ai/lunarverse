# URL2HTML Component

## Description

The **URL2HTML** component converts web pages to HTML files using asynchronous web crawling. It takes a URL as input, downloads the web page content, saves it as an HTML file in a temporary directory, and returns the path to the generated file. The component handles URL parsing, file naming, and asynchronous web crawling to ensure efficient HTML generation.

## Inputs

- **url** (str): The web page URL to be converted to HTML. Example: `https://example.com/page`

## Outputs

- **result** (str): The path to the generated HTML file in a temporary directory. Returns None if the conversion fails.

## Usage

To use the **URL2HTML** component, you need:

1. A valid web page URL that you want to convert to HTML

The component will:
1. Create a temporary directory to store the HTML file
2. Parse the URL to generate a valid filename
3. Download the web page content asynchronously
4. Save the HTML content in the temporary directory
5. Return the path to the generated HTML file

## Example

Input URL:
```
https://www.example.com/
```

Output path:
```
/tmp/tmpdir123/example_com.html
```

## Notes

- The component uses asynchronous web crawling for better performance
- The component requires internet access to download web pages
- HTML files are saved in a temporary directory that is created when the component is instantiated
- Special characters in URLs are replaced with underscores in the filename
- If the URL path is empty, the file will be named "page.html"
- The HTML content is saved with UTF-8 encoding to properly handle special characters
