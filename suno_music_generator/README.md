# Suno Music Generator Component

## Description

The `Suno Music Generator` component enables the generation of music tracks using the Suno API. By providing inputs such as the title, lyrics, genres, tempo, instruments, and additional instructions, this component generates music that aligns with the specified parameters.

## Inputs

- **Title** (`str`): The title of the song (e.g., "Blinding Lights").
- **Lyrics** (`str`): The lyrics of the song, formatted as text (e.g., `[Verse 1]I have been tryna call, I have been on my own for long enough, ..., [Chorus]..., ...`).
- **Genres** (`List[str]`): A list of genres for the song (e.g., `["rock", "indie"]`).
- **Tempo** (`str`): The tempo of the song (e.g., "171 BPM", "adagio", "moderato", "allegro", or general terms like "slow", "fast").
- **Instruments** (`List[str]`): The instruments or instrumental mood for the song (e.g., `["piano", "guitar"]`).
- **Other instructions** (`str`): Additional instructions for the music generation (e.g., "Keep the outro short").

## Output

- **Output** (`List[str]`): A list of IDs for the generated songs. Typically, two songs are generated per request.

## Input Types

- **Title**: `TEXT`
- **Lyrics**: `TEXT`
- **Genres**: `LIST`
- **Tempo**: `TEXT`
- **Instruments**: `LIST`
- **Other instructions**: `TEXT`

## Output Type

- **LIST**

## Configuration Parameters

To use the `Suno Music Generator` component, ensure that the following configuration parameters are set:

- **suno_api_base_url**: The base URL for the Suno API. By default, this should point to a locally hosted Suno API instance (e.g., `http://localhost:3000`).

Ensure that the Suno API (available at [suno-api](https://github.com/gcui-art/suno-api)) is downloaded and running locally.

## Usage

To generate music, provide the necessary inputs such as the title, lyrics, genres, tempo, and instruments. The component will send a request to the Suno API, which will return a list of IDs for the generated songs. These IDs can be used to retrieve or manage the songs generated.

## Summary

The `Suno Music Generator` component is a powerful tool for creating custom music tracks based on detailed input parameters. By leveraging the Suno API, users can generate high-quality music that fits specific criteria, making this component ideal for musicians, producers, and creative projects. Configure the Suno API, provide your song details, and the component will generate unique music tracks based on your inputs.