# Spacy NER Component

## Overview
The **Spacy NER** component is designed to perform Named Entity Recognition (NER) on a given text. It leverages the capabilities of the Spacy library to identify and classify named entities within the text.

## Description
Named Entity Recognition (NER) is the process of identifying and classifying named entities in text into predefined categories such as person names, organizations, dates, etc. The **Spacy NER** component processes the input text and returns a list of entities found within the text, along with their corresponding labels.

## Inputs
- `Text` (str): The text to perform NER on.

## Output
- `List[Dict[str, str]]`: A list of dictionaries where each dictionary contains two keys:
  - `text` (str): The word or text that has been identified as a named entity.
  - `label` (str): The NER label assigned to the text (e.g., `PERSON`, `DATE`).

Example output:
```json
[
  {"text": "Albert Einstein", "label": "PERSON"},
  {"text": "1879", "label": "DATE"}
]
```

## Configuration Parameters
- `model_name` (str): The name of the pre-trained Spacy model to use for NER. Users can specify different models based on their requirements. Examples include `en_core_web_sm`, `en_core_web_md`, etc.

## Input Types
- `Text`: TEMPLATE

## Output Type
- LIST

## Requirements
To use the **Spacy NER** component, you need to have the Spacy library installed along with the appropriate pre-trained model. You can install Spacy and its models using the following commands:
```sh
pip install spacy
python -m spacy download <model_name>
```

Replace `<model_name>` with the desired Spacy model name. For example:
```sh
python -m spacy download en_core_web_sm
```

## Configuration
Set the `model_name` parameter to the desired Spacy model name:
```python
model_name = "en_core_web_sm"
```

This parameter allows the component to load the specified Spacy model to perform NER on the provided text.

## Notes
- Ensure that the Spacy model specified by `model_name` is already downloaded and available in your environment.
- The performance and accuracy of the NER component can