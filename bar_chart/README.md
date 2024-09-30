# Bar Chart Component

## Description
The Bar Chart component is designed to plot a bar chart based on a provided dictionary containing numerical values. It is capable of generating an output that can be linked to a report component.

## Inputs
- `Data` (Dict[Any, Union[int, float]]): A dictionary where keys (any data type that can be converted to a string) are mapped to numerical values (either integers or floats). This dictionary serves as the data source for the bar chart.

## Output
The component produces the following output:
- A dictionary with the following keys:
  - `data` (str): This key holds the original input data in its original dictionary format.
  - `images` (str): This key contains a list with one element, which is the bar chart image encoded in base64 format. The encoded image string follows the format `f"data:image/png;base64,{base64.b64encode(binary_buffer_of_PNG.read()).decode()}"`.

## Input Types
This component accepts the following input types:
- `Data`: JSON

## Output Type
This component produces output in the following type:
- `BAR_CHART`

## Configuration Parameters
This component does not require any configuration parameters.

## Usage
To use the Bar Chart component, you need to provide a dictionary with numerical values as input. The component will generate a bar chart from the input data and output a dictionary containing the original data and the base64 encoded image of the bar chart.

Thank you for using the Bar Chart component. If you encounter any issues or have any questions, please refer to the documentation or contact support.