# Line Chart Component

## Description

The **Line Chart** component is designed to plot a line chart from a given dictionary with `x` and `y` arrays. The component processes the input data and generates a line chart image, which can be linked to a report component.

## Inputs

- **Data** (`Dict[str, List[Union[int, float]]`): A dictionary with keys `x` and `y` mapped to lists of numerical values (int or float). This dictionary represents the data points for the line chart.

## Outputs

- **Output** (`Dict`): A dictionary containing two keys:
  - `data` (`Dict[str, List[Union[int, float]]]`): The original input data.
  - `images` (`List[str]`): A list with a single element, which is the produced line chart image encoded in base64 format. The image is encoded as `data:image/png;base64,{base64_encoded_image}`.

## Input Types

- `Data`: JSON

## Output Type

- LINE_CHART

## Configuration Parameters

This component does not require any configuration parameters.

## Example

Given the following input data:
```json
{
  "x": [1, 2, 3, 4, 5],
  "y": [1, 2, 3, 4, 5]
}
```

The output will be:
```json
{
  "data": "{\"1\": 10, \"2\": 20, \"3\": 30, \"4\": 40, \"5\": 50}",
  "images": ["data:image/png;base64,iVBORw..."]
}
```
(The value of `images` is truncated for brevity.)

## Notes

- The image is provided in the base64-encoded PNG format, which allows for easy embedding in web pages and reports.
- Ensure that the input dictionary contains only numerical data types (integers or floats) for both keys and values to avoid errors in chart generation.