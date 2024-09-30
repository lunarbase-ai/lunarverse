# HuggingFace Vectorizer

## Overview

The **HuggingFace Vectorizer** is a component designed to encode texts using HuggingFace's models. It processes input text and generates embeddings, which are numerical representations of the text. These embeddings can then be used for various natural language processing (NLP) tasks, such as semantic similarity, clustering, or classification.

## Features

- **Text Encoding**: Convert input texts into embeddings using pre-trained HuggingFace models.
- **Output**: Provides a list of dictionaries containing the original text and its corresponding embeddings.

## Inputs

- **Text**: A list of strings (`LIST`) that you want to encode.

## Outputs

- **Embeddings**: The output is a list of dictionaries. Each dictionary contains:
  - `original_text` (str): The original text.
  - `embeddings` (List[Union[float, int]]): The embeddings generated for the text.

## Configuration Parameters

- **model_name**: The name of the pre-trained HuggingFace model to use for encoding the texts. This should be a string representing a valid model name available in the HuggingFace model hub.

## Usage

To use the HuggingFace Vectorizer, you need to provide a list of texts to be encoded and specify the `model_name` to be used for encoding. The component will then return the embeddings for each text.

## Example Configuration

```yaml
model_name: 'distilbert-base-uncased'
```

In this example, the component will use the `distilbert-base-uncased` model from HuggingFace to encode the input texts.

## Summary

The HuggingFace Vectorizer is a powerful tool for transforming texts into embeddings using state-of-the-art NLP models from HuggingFace. By configuring the component with a specific model name, you can leverage different pre-trained models for various text encoding tasks. The output embeddings can then be utilized in a wide range of applications in the field of NLP.