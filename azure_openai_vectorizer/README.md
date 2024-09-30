# Azure Open AI Vectorizer

## Overview

The **Azure Open AI Vectorizer** component encodes inputted texts as numerical vectors (embeddings) using Azure OpenAI models. This component is designed to take a list of texts and transform each text into its corresponding embedding, which can then be used for various downstream tasks such as text classification, clustering, or similarity comparisons.

## Inputs

- **Text list** (`List[str]`): A list of texts to encode. Users can input this list manually if needed.

## Output

- `List[Dict]`: A list of dictionaries -- one for each text in the input. Each dictionary contains:
  - `text` (str): The original text.
  - `embeddings` (List[Union[float, int]]): The embedding of the text as a list of numerical values.

## Configuration Parameters

To configure the Azure Open AI Vectorizer component, you need to provide the following parameters:

- **openai_api_type**: The type of OpenAI API being used.
- **openai_api_version**: The version of the OpenAI API.
- **deployment**: The deployment configuration for your Azure OpenAI model.
- **openai_api_key**: The API key for accessing the OpenAI service.
- **azure_endpoint**: The endpoint URL for your Azure OpenAI service.

Ensure that you have the necessary access and permissions to use the Azure OpenAI service and the corresponding API key.

## Usage

To use the Azure Open AI Vectorizer component, you need to provide a list of texts and configure the necessary parameters for your Azure OpenAI setup. The component will process each text and return a list of dictionaries containing the original texts and their corresponding embeddings.

This component is ideal for applications that require text embeddings for machine learning models, natural language processing tasks, and other AI-driven solutions.