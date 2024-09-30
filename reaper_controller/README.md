# Reaper Controller Component

## Description

The `Reaper Controller` component allows users to control and edit Reaper projects (a digital audio workstation) through natural language commands. This component interprets instructions, modifies the Reaper project accordingly, and generates a new audio file in the specified format.

## Inputs

- **RPP path** (`str`): The server path to the Reaper project file (with `.RPP` extension).
- **Instruction** (`str`): A natural language instruction describing how to edit the Reaper project.
- **Audio output path** (`str`): The path where the newly generated audio file will be saved. The file extension determines the format (`.wav` or `.mp3`). If left empty, a `.wav` file with the same name as the RPP file will be created.

## Output

- **Output** (`str`): The path to the newly created audio file.

## Input Types

- **RPP path**: `TEXT`
- **Instruction**: `TEMPLATE`
- **Audio output path**: `TEXT`

## Output Type

- **TEXT**

## Configuration Parameters

To utilize the `Reaper Controller` component, ensure that the following configuration parameters are set:

- **openai_api_key**: Your OpenAI API key.
- **azure_endpoint**: Azure endpoint URL (if using Azure OpenAI).
- **audio_format**: The default audio format for rendering, either `wav` or `mp3`. This will be overwritten by the file extension in the `Audio output path`, if provided.

Note that Reaper must be open and running in the background, and the Python library `reapy` must be installed and configured according to its installation instructions. This includes running the Python code `import reapy; reapy.configure_reaper()`.

## Usage

1. **Specify the RPP Path**: Provide the path to your Reaper project file (`.RPP`).
2. **Provide an Instruction**: Use natural language to describe the modifications you want to make to the project. The component will convert these instructions into Python code that interacts with the Reaper API.
3. **Set the Output Path**: Choose the path and format for the output audio file. If left empty, the component will default to saving a `.wav` file with the same name as the RPP file.

The component processes the input instruction, executes the corresponding Python code to edit the Reaper project, and then renders and saves the audio file at the specified location.

## Summary

The `Reaper Controller` component is a powerful tool for automating and simplifying the editing of Reaper projects. With the ability to interpret natural language instructions, this component makes it easy to perform complex audio editing tasks. Whether you need to add tracks, adjust volume, or apply effects, the Reaper Controller can streamline your workflow and generate high-quality audio outputs.