# Property Getter Component

## Overview
The **Property Getter** component is designed to extract the mapped value of a specified key, field, or attribute from an inputted object or data structure.It supports nested objects and dictionaries, allowing access to nested keys by concatenating keys with dots (e.g., `parent_dict_key.dict_key`). For lists of dictionaries (List[Dict]), list indices are used as keys (e.g., `list_index.dict_key`).

## Inputs
- **Input** (`Any`): An object to extract a value from. The object can be a dictionary, a list, or a file object.
- **Selected property** (`str`): The name of the key, field, or attribute to extract from the inputted object. Nested keys can be accessed by concatenating keys with dots.

## Outputs
- **Output** (`Any`): The mapped value of the inputted key, field, or attribute in the inputted object.

## Input Types
- **Input**: `JSON`
- **Selected property**: `PROPERTY_GETTER`

## Output Type
- **Output**: `ANY`

## Configuration Parameters
This component does not require any configuration parameters.

## Usage
The Property Getter component is useful in scenarios where you need to dynamically access and retrieve values from complex data structures based on user-specified keys or attributes.
