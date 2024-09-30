# CIViC Component

## Description

The CIViC component is designed to search for gene information from the CIViC (Clinical Interpretation of Variants in Cancer) database. This component takes specific input parameters related to genes, therapies, and diseases and returns detailed information in a JSON format. The CIViC database is a crowd-sourced and expert-curated platform that provides accessible information about the clinical significance of genetic variants in cancer.

## Inputs

The CIViC component accepts the following input parameters:

- **Genes**: A list of gene names or identifiers for which information is to be retrieved.
- **Therapies**: A list of therapies that are relevant to the search.
- **Diseases**: A list of diseases associated with the search.

The input types are specified as follows:
```json
{
  "Genes": "LIST",
  "Therapies": "LIST",
  "Diseases": "LIST"
}
```

## Output

The output of the CIViC component is in JSON format. The JSON response contains detailed information about the queried genes, including but not limited to, clinical significance, associated diseases, and relevant therapies.

## Configuration Parameters

There are no configuration parameters for the CIViC component. It operates with the provided input lists and returns the corresponding information from the CIViC database.

## Usage

To use the CIViC component, provide the necessary input lists for genes, therapies, and diseases. The component will process these inputs and query the CIViC database, returning the relevant gene information in JSON format.