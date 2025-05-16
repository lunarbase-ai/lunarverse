# Azure OpenAI Image Structured LLM Component

## Overview

The Azure OpenAI Image Structured LLM component connects to Azure OpenAI's API to analyze images and return structured responses based on a provided JSON schema.

## Description

The Azure OpenAI Image Structured LLM component uses Azure's OpenAI service to analyze images and return structured responses. The component takes an image, a user prompt, and a JSON schema as input, and returns a structured response that matches the provided schema.

### Output

- **Output (JSON):** A structured response that matches the provided JSON schema.

## Inputs

- **user_prompt (TEMPLATE):** The natural language prompt to analyze the image
- **system_prompt (TEMPLATE, optional):** Custom system prompt for the AI (defaults to "You are a helpful AI assistant. Your name is AI Rover.")
- **image (JSON):** The image to analyze, either as a File object with base64 content or a dictionary with base64 content
- **schema (JSON):** The JSON schema that defines the structure of the expected response

## Output

- **JSON:** A structured response that matches the provided JSON schema.

## Configuration

The component requires the following environment variables:
- `OPENAI_API_KEY`: Your Azure OpenAI API key
- `OPENAI_API_VERSION`: The API version to use (e.g., "2024-02-15-preview")
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `DEPLOYMENT_NAME`: The name of your Azure OpenAI deployment
