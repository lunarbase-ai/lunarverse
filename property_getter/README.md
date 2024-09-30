# Property Getter Component

## Overview
The **Property Getter** component is designed to extract the mapped value of a specified key, field, or attribute from an inputted object or data structure. This component can work with various types of input objects, including dictionaries, lists, and file objects.

## Inputs
1. **Input** (Any): 
   - This is the object from which the value will be extracted. The input object can be of various types such as a dictionary, a list, or a file object.

2. **Selected property** (str): 
   - This is a string representing the name of the key, field, or attribute to be extracted from the inputted object. 
   - For nested objects or dictionaries, nested keys can be accessed by concatenating keys with dots (e.g., `parent_dict_key.dict_key`).
   - For lists of dictionaries (List[Dict]), list indices are used as keys (e.g., `list_index.dict_key`).

## Output
- **Output** (Any): 
  - The component returns the value mapped to the specified key, field, or attribute within the inputted object.

## Input Types
The input types for the component are as follows:
- **Input**: JSON
- **Selected property**: PROPERTY_GETTER

## Output Type
- **Output**: ANY

## Configuration Parameters
This component does not require any configuration parameters.

## Usage
The Property Getter component is useful in scenarios where you need to dynamically access and retrieve values from complex data structures based on user-specified keys or attributes.