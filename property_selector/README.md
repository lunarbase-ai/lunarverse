# Property Selector Component

## Overview
The **Property Selector** component is designed to extract values of specified properties (keys) from an inputted dictionary. This component is particularly useful for retrieving nested properties from complex dictionaries.

## Inputs
1. **Inputs** (`Dict[str, Any]`): 
   - A dictionary from which values will be extracted.
   - Example: 
     ```json
     {
       "keyA": {"keyB": 123},
       "keyC": {"keyD": 456}
     }
     ```

2. **Selected properties** (`str`): 
   - A comma-separated string of the properties (keys) to extract, using dots for nested properties.
   - Example: `keyA,keyC.keyD`

## Output
Returns a dictionary (`Dict`) containing the selected properties and their corresponding values.
- Example: 
  ```json
  {
    "keyA": {"keyB": 123},
    "keyC.keyD": 456
  }
  ```

## Input Types
- **Inputs**: `AGGREGATED`
- **Selected properties**: `PROPERTY_SELECTOR`

## Output Type
- `JSON`

## Configuration Parameters
There are no configuration parameters required for this component.

## Usage
1. Provide the input dictionary.
2. Specify the properties to be extracted in a comma-separated string format.
3. The component will return a dictionary containing the selected properties and their values.

This component effectively simplifies the process of accessing nested properties within complex dictionaries, making data retrieval more straightforward and efficient.