# Htmls2Texts Component

## Overview
The `Htmls2Texts` component is designed to convert HTML content into plain text. This component processes a dictionary of URLs, where each URL is mapped to its corresponding HTML content. The output is a modified dictionary where the HTML content is supplemented with the extracted text. If there are any errors with a URL, it remains unchanged.

## Inputs
- **Scraper_results**: A JSON object (dictionary) with URLs as keys. Each URL is mapped to a sub-dictionary which contains:
  - `content`: The HTML content of the page, provided as a string.
  
  **Example Input:**
  ```json
  {
    "https://example.com": {
      "content": "<html><body>Hello World</body></html>"
    }
  }
  ```

## Output
- **Output**: A JSON object (dictionary) similar to the input, but with an additional key `text` in each URL sub-dictionary. This `text` key contains the plain text extracted from the HTML content. URLs with errors remain unchanged.

  **Example Output:**
  ```json
  {
    "https://example.com": {
      "content": "<html><body>Hello World</body></html>",
      "text": "Hello World"
    }
  }
  ```

## Configuration Parameters
This component does not require any configuration parameters.

## Notes
- URLs that encounter errors during processing will not have the `text` field added and will remain unchanged in the output dictionary.
- Ensure that the input JSON structure is correctly formatted to avoid processing errors.

By using the `Htmls2Texts` component, you can easily extract and access the plain text content from multiple HTML pages, simplifying further text processing tasks.