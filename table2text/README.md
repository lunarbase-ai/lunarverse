# Table2Text Component

## Overview

The `Table2Text` component is designed to convert a CSV formatted table into a text format by transforming each row into a sentence. This can be particularly useful for generating human-readable summaries or descriptions from tabular data.

## Description

The `Table2Text` component takes a string input in CSV format and processes each row, converting it into a sentence. The output is a JSON object containing a list of sentences corresponding to each row of the input table.

## Inputs

- `Table` (str): A string representing the table in CSV format. Each row in the table should be a separate line, and columns should be separated by commas.

## Output

- (Dict): A dictionary with a single key `results`, which maps to a list of sentences. Each sentence corresponds to a row in the inputted table.

## Input Types

- `Table`: TEXT

## Output Type

- JSON

## Configuration Parameters

This component does not require any configuration parameters.

## Usage

This component is useful when you need to transform tabular data into a more readable text format. It can be integrated into data processing pipelines where human-readable output is required from CSV data.

## Example

Given the following CSV input:

```
Name, Age, Occupation
Alice, 30, Engineer
Bob, 25, Designer
Charlie, 35, Teacher
```

The `Table2Text` component will produce the following output:

```json
{
  "results": [
    "Name is Alice, Age is 30, Occupation is Engineer.",
    "Name is Bob, Age is 25, Occupation is Designer.",
    "Name is Charlie, Age is 35, Occupation is Teacher."
  ]
}
```

This example demonstrates how each row in the CSV table is converted into a sentence, providing a clear and readable text representation of the tabular data.