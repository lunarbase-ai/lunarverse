# URL2PDF Component

## Description

The **URL2PDF** component converts web pages to PDF using asynchronous web crawling. It takes a URL as input, downloads the web page content, saves it as a PDF file in a temporary directory, and returns the path to the generated file. The component handles URL parsing, file naming, and asynchronous web crawling to ensure efficient PDF generation.

## Inputs

- **url** (str): The web page URL to be converted to PDF. Example: `https://example.com/page`

## Outputs

- **result** (str): The path to the generated PDF file in a temporary directory. Returns None if the conversion fails.

## Usage

To use the **URL2PDF** component, you need:

1. A valid web page URL that you want to convert to PDF

The component will:
1. Create a temporary directory to store the PDF
2. Parse the URL to generate a valid filename
3. Download the web page content asynchronously
4. Convert the content to PDF
5. Save the PDF file in the temporary directory
6. Return the path to the generated PDF file

## Example

Input URL:
```
https://www.example.com/
```

Output path:
```
/tmp/tmpdir123/example_com.pdf
```

## Notes

- The component uses asynchronous web crawling for better performance
- The component requires internet access to download web pages
- PDFs are saved in a temporary directory that is created when the component is instantiated
- Special characters in URLs are replaced with underscores in the filename
- If the URL path is empty, the file will be named "page.pdf"