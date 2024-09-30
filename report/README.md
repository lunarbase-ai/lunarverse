# Report Component

## Overview

The `Report` component is designed to create an editable report from the input it receives. It processes the provided data and generates a structured output that can be used with the Quill editor format for further editing and presentation.

## Description

The `Report` component takes a dictionary of strings as input and produces a dictionary containing instructions for building a report. The output is formatted for use with the Quill editor, allowing for easy customization and editing of the report content.

## Inputs

- `Inputs` (Dict[str, str]): A dictionary where each key-value pair consists of strings. This dictionary contains the data that will be included in the report.

## Output

- `Output` (Dict): A dictionary containing instructions for building the report using the Quill editor format. This output can be directly used with Quill to render an editable report.

## Input Types

- `Inputs`: AGGREGATED

## Output Type

- `Output`: REPORT

## Configuration Parameters

This component does not require any configuration parameters.