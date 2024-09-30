# PROGENy Component

## Overview

The PROGENy component serves as the definitive resource for pathways and target genes, providing weights for each interaction. It is designed to work with two CSV files as input. This component can be particularly useful for analyzing signaling footprints in cancer gene expression.

## Description

PROGENy (Pathway RespOnsive GENes) is a computational approach that infers pathway activities from gene expression data. It uses perturbation-response genes to reveal signaling footprints, making it a valuable tool for researchers studying cancer and other diseases.

For more information on the decoupler package that works with PROGENy, visit the [decoupler documentation](https://decoupler-py.readthedocs.io/en/latest/notebooks/progeny.html).

## Reference

Schubert, M., Klinger, B., Klünemann, M. et al. Perturbation-response genes reveal signaling footprints in cancer gene expression. Nat Commun 9, 20 (2018). [DOI: 10.1038/s41467-017-02391-6](https://doi.org/10.1038/s41467-017-02391-6). [Read the paper](https://www.nature.com/articles/s41467-017-02391-6).

## Input Types

The component requires the following input types:

- `adata` (TEXT): The first CSV file containing gene expression data.
- `progeny` (TEXT): The second CSV file containing pathway and target gene information.

## Output Type

The output of this component is a:

- `LIST`: A list of pathways and their corresponding target genes along with the weights for each interaction.

## Configuration Parameters

The component requires the following configuration parameters:

- `client_id`: The client ID for accessing the service.
- `client_secret`: The client secret for accessing the service.

## Usage

To use the PROGENy component, ensure that you have the required input CSV files and configuration parameters ready. The component will process the input files and generate a list of pathways and target genes with their respective interaction weights.

For further details on usage, please refer to the [decoupler documentation](https://decoupler-py.readthedocs.io/en/latest/notebooks/progeny.html).