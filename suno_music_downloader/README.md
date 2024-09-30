# Suno Music Downloader Component

## Description

The `Suno Music Downloader` component is designed to download songs from the Suno API using provided song IDs. This component retrieves the audio files and stores them locally, returning details about each downloaded song, including the title and file path.

## Inputs

- **Song IDs** (`List[str]`): A list of song IDs to download (e.g., `["6f4b42b8-9c48-4dde-91e3-c79a23cad679", "95e66c84-9b31-4adc-8ddf-35d32eef0643"]`).

## Output

- **Output** (`Dict[str, Dict]`): A dictionary where each key is a song ID and the corresponding value is another dictionary containing:
  - **title** (`str`): The title of the song.
  - **file_path** (`str`): The server path where the downloaded MP3 file is stored.

## Input Types

- **Song IDs**: `LIST`

## Output Type

- **JSON**

## Configuration Parameters

To use the `Suno Music Downloader` component, ensure that the following configuration parameters are set:

- **suno_api_base_url**: The base URL for the Suno API. This should point to a locally hosted Suno API instance (e.g., `http://localhost:3000`).

Ensure that the Suno API (available at [suno-api](https://github.com/gcui-art/suno-api)) is downloaded and running locally.

## Usage

To download songs, provide the list of song IDs that you wish to retrieve. The component will send a request to the Suno API and download the audio files associated with each ID. The downloaded files are saved locally, and the component returns a dictionary with information about each song, including the title and the path to the downloaded MP3 file.

## Summary

The `Suno Music Downloader` component simplifies the process of downloading and organizing music generated via the Suno API. By inputting the song IDs, users can quickly retrieve and store music files on their server, making this tool valuable for music enthusiasts, developers, and content creators. Configure the Suno API, provide the song IDs, and this component will handle the download and storage of your music tracks.