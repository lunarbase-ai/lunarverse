# Audio2Base64 Component

## Description

The `Audio2Base64` component is designed to convert audio files into a Base64-encoded string. This component supports `.mp3` and `.wav` audio formats, generating a Base64 string that can be embedded directly in web pages or used in other applications that require Base64-encoded audio data, e.g. the Audio Player component in Lunar.

## Inputs

- **Audio file path** (`str`): The server path of the audio file to convert. The file must be either in `.mp3` or `.wav` format.

## Output

- **Output** (`str`): A string representing the audio file in Base64 format. The output follows this format: 
  ```
  data:{mime_type};base64,{base64_string}
  ```
  where `mime_type` corresponds to the file type (e.g., `audio/mpeg` for `.mp3` files), and `base64_string` is the Base64-encoded content of the audio file.

## Input Types

- **Audio file path**: `TEMPLATE`

## Output Type

- **TEXT**

## Usage

To use the `Audio2Base64` component, simply provide the path to your audio file. The component will return a Base64-encoded string that can be used in various applications, such as embedding audio in HTML or sending audio data through JSON.

## Summary

The `Audio2Base64` component is a straightforward tool for converting `.mp3` and `.wav` audio files into Base64 strings. This conversion is particularly useful for embedding audio in web applications or transmitting audio data in text-based formats. Simply provide the file path, and the component handles the rest, delivering a ready-to-use Base64 string.