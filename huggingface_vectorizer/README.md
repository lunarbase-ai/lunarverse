# HuggingFace Vectorizer

## Overview

The **HuggingFace Vectorizer** is a component designed to encode texts using HuggingFace's models. It processes input text and generates embeddings, which are numerical representations of the text. These embeddings can then be used for various natural language processing (NLP) tasks, such as semantic similarity, clustering, or classification.

## Features

- **Text Encoding**: Convert input texts into embeddings using pre-trained HuggingFace models.
- **Output**: Provides a list of dictionaries containing the original text and its corresponding embeddings.

## Inputs

- **text**: A list of strings (`LIST`) that you want to encode. Ex: `["Hello, world!", "How are you?"]`
- **model_name**: A string with the name of the Huggingface model you want to use. Ex: `distilbert-base-uncased`

## Outputs

- **Embeddings**: The output is a list of dictionaries. Each dictionary contains:
  - `original_text` (str): The original text.
  - `embeddings` (List[Union[float, int]]): The embeddings generated for the text.

## Configuration Parameters

There is no configuration parameter for this component.

## Usage

To use the HuggingFace Vectorizer, you need to provide a list of texts to be encoded and specify the `model_name` to be used for encoding. The component will then return the embeddings for each text.


## Summary

The HuggingFace Vectorizer is a powerful tool for transforming texts into embeddings using state-of-the-art NLP models from HuggingFace. By configuring the component with a specific model name, you can leverage different pre-trained models for various text encoding tasks. The output embeddings can then be utilized in a wide range of applications in the field of NLP.