# Audio Player Component

## Description

The Audio Player component is designed to handle audio data encoded in base64 format. It processes and returns the same base64-encoded audio string provided as input, making it suitable for applications where audio data needs to be played or transmitted without modification.

## Inputs

- **Base64 encoded audio** (str): A string containing audio data encoded in base64. The format should be `data:{mime_type};base64,{base64_string}`, where `{mime_type}` represents the type of the audio (e.g., `audio/mpeg` for MP3), and `{base64_string}` is the actual base64-encoded audio data.

## Output

- **Output** (str): The output is the same base64-encoded audio string provided as input. This allows the audio data to be easily handled, played, or transmitted in its encoded form without alteration.

## Input Types

- **Base64 encoded audio**: TEXT

## Output Type

- **AUDIO**

## Configuration Parameters

This component does not require any configuration parameters for its operation. It simply processes and returns the base64-encoded audio data as provided.

## Summary

The Audio Player component is a straightforward tool for managing base64-encoded audio data. By accepting and returning base64-encoded audio strings, it facilitates the playback and transmission of audio data in its encoded form, making it a useful component for audio processing pipelines that require base64 encoding.