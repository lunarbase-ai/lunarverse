# Indra Network Assembler

## Description
The **Indra Network Assembler** is a powerful component designed to retrieve literature related to a set of genes. This tool leverages various databases and APIs to provide comprehensive and relevant information about the genes of interest, facilitating research and data analysis.

## Inputs
- **Genes (LIST)**: A list of gene identifiers for which literature information needs to be retrieved.

## Output
- **JSON**: The output is provided in JSON format containing the relevant literature data associated with the specified genes.

## Configuration Parameters
To effectively use the Indra Network Assembler, the following configuration parameters need to be set:

- **max_papers_per_gene**: This parameter defines the maximum number of papers to retrieve for each gene. Adjusting this parameter can help manage the volume of data and focus on the most relevant literature.
  
- **elsevier_api_key**: An API key for accessing Elsevier's databases. This key is necessary to authenticate and retrieve data from Elsevier’s resources.
  
- **output_properties**: This parameter specifies the properties of the output JSON. It allows customization of the information included in the output, ensuring that only the necessary details are provided.

## Usage
To use the Indra Network Assembler, ensure that you have a list of genes and the necessary configuration parameters set up. The component will process the input list of genes and retrieve the relevant literature information, which will be outputted in JSON format.

---

Make sure to replace the placeholder values in the configuration parameters with actual data to ensure proper functionality. The Indra Network Assembler is a valuable tool for researchers and analysts looking to gather comprehensive literature data on specific genes efficiently.