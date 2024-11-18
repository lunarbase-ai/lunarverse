# HTML Reports Builder

## Description

The `HTML Reports Builder` component is designed to build HTML reports using a Jinja2 template and a set of data inputs. The component takes a Jinja2 template as a string and a dictionary of data, and outputs a dictionary where each key is mapped to a rendered HTML report.

## Inputs

### Template_j2 (str)

- **Description**: A Jinja2 template of the HTML report template as a string.
- **Type**: TEXT
- **Example**: 
  ```html
  <html><head><title>{{ title }}</title></head></html>
  ```

### Data (Dict[str, Dict[str, str]])

- **Description**: A dictionary with labels (strings) as keys. Each label is mapped to a dictionary used for rendering the template. In this sub-dictionary, each key-value pair represents a template variable and its value.
- **Type**: JSON
- **Example**:
  ```json
    {
        "report1": {"title": "Report 1 Title"},
        "report2": {"title": "Report 2 Title"}
    }
  ```

## Outputs

### Output (Dict[str, str])

- **Description**: A dictionary where each inputted label is mapped to the corresponding rendered template.
- **Type**: JSON
- **Example**:
  ```json
    {
        "report1": "<html><head><title>Report 1 Title</title></head></html>",
        "report2": "<html><head><title>Report 2 Title</title></head></html>"
    }
  ```

## Configuration Parameters

This component does not require any configuration parameters.

## Summary

The `HTML Reports Builder` component leverages Jinja2 templating to generate HTML reports from a given template and data. By providing a Jinja2 template as a string and a dictionary of data, users can obtain a dictionary of rendered HTML reports, making it a versatile tool for dynamic HTML report generation.