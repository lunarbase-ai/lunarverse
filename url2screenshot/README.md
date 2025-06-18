# URL2Screenshot Component

The **URL2Screenshot** component is designed to capture a screenshot of a web page (via AsyncWebCrawler) and return the path of the generated (png) file.

## Description

This component takes a URL as input, crawls the page asynchronously, and captures a screenshot. The screenshot is saved in a temporary directory (created on instantiation) and the path (a string) is returned. If the capture fails (for example, if the page does not render a screenshot), the output is None.

## Inputs

- **url** (`str`): The web page URL to be captured.

## Output

- **result** (`str`): The path (a string) of the generated (png) file in a temporary directory. Returns None if the capture fails.

## Input Types

- **url**: Expected to be a string containing a valid URL.

## Output Type

- **result**: Text (string path)

## Configuration Parameters

This component does not have any configuration parameters.

## Notes

- The component uses asynchronous web crawling (via AsyncWebCrawler) for better performance.
- The component requires internet access to download and render the web page.
- Screenshots are saved in a temporary directory (created on instantiation) and the filename is derived from the URL path (with non alphanumeric characters replaced by underscores).
- If the URL path is empty, the file is named "page.png".
