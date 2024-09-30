# Gemini AI Prompt Component

## Description

The **Gemini AI Prompt** component connects to Gemini's API, executes natural language prompts, and outputs the result as text. This component leverages Gemini's advanced language model to process and respond to user-provided prompts with high-quality textual answers.

## Inputs

- **Prompt (TEMPLATE)**: The natural language prompt that you want to submit to Gemini's language model for processing. This input should be a well-formed question or directive that the model can understand and generate a meaningful response to.

## Output

- **Output (str)**: The answer provided by the language model in response to the input prompt. The output is a string of text containing the model's interpretation and response to the given prompt.

## Configuration Parameters

- **api_key**: A valid API key that authenticates your access to Gemini's API. This key is necessary for establishing a secure connection and ensuring that your prompts are processed correctly.

---

Ensure that you have a valid API key before using this component to interact with Gemini's API. Properly format your prompts to achieve the best results from the language model. The component will handle the connection and response handling, delivering the model's output as a text string.