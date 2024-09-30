# Gene Set Upload Component

## Description
The **Gene Set Upload** component reads a CSV file containing gene names and outputs a list of the gene names. This component is essential for processing and extracting gene information from structured data files.

## Inputs
- **Input file** (`str`): The server path of a CSV file with gene names. The CSV file must contain a column named `gene_name` which includes the gene names.

## Output
- **Output** (`List[str]`): A list of genes extracted from the `gene_name` column in the inputted CSV file.

## Configuration Parameters
This component does not require any configuration parameters.

## Usage
To use the **Gene Set Upload** component, provide the file path to the CSV file containing the gene names in the `gene_name` column. The component will process the file and return a list of gene names found in that column.

Ensure the CSV file is formatted correctly with the `gene_name` column to avoid errors during processing.