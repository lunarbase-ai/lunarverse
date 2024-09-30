# Lyrics Generator Component

## Description

The `Lyrics Generator` component creates song lyrics based on user-defined parameters using Azure OpenAI's language model (LLM). By providing the theme, mood, setting, key words, and additional instructions, this component generates lyrics that match the specified criteria.

## Inputs

- **Theme** (`str`): The central theme of the song (e.g., "love").
- **Mood** (`str`): The mood or tone of the song (e.g., "happy").
- **Setting** (`str`): The setting or location where the song is set (e.g., "New York").
- **Key words** (`List[str]`): A list of key words or phrases that should appear in the lyrics (e.g., `["sunshine", "forever"]`).
- **Other instructions** (`str`): Any additional instructions for the lyrics (e.g., "Each verse should have six lines").

## Output

- **Output** (`str`): A string containing the generated song lyrics based on the provided inputs.

## Input Types

- **Theme**: `TEXT`
- **Mood**: `TEXT`
- **Setting**: `TEXT`
- **Key words**: `LIST`
- **Other instructions**: `TEXT`

## Output Type

- **TEXT**

## Configuration Parameters

To use the `Lyrics Generator` component, ensure that the following parameters are configured:

- **openai_api_key**: Your API key for Azure OpenAI (set empty to use OPENAI_API_KEY environment variable).
- **azure_endpoint**: The endpoint for your Azure OpenAI service (set empty to use AZURE_ENDPOINT environemnt variable).
- **openai_api_version**: The API version to use (e.g., `2024-02-01`).
- **deployment_name**: The name of the deployment for the Azure OpenAI model (e.g., `lunar-chatgpt-4o`).

Note that some of these parameters can be provided through environment variables.

## Usage

To generate song lyrics, provide the necessary inputs, including the theme, mood, setting, key words, and any other specific instructions. The component will use the Azure OpenAI API to produce lyrics that align with your inputs, returning a text string with the generated content.

## Summary

The `Lyrics Generator` is a versatile tool for creating song lyrics tailored to specific themes, moods, and settings. By leveraging Azure OpenAI's powerful language model, users can generate high-quality lyrics quickly and easily, making this component an invaluable asset for musicians, songwriters, and creative professionals. Simply configure the necessary API credentials, provide the input parameters, and the component will do the rest, delivering custom lyrics that fit your creative vision.