# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import requests
from typing import Any, Optional, List

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType


SUNO_PROMPT_TEMPLATE = """Lyrics: {lyrics}
Genres: {genres}
Recommended tempo: {tempo}
Recommended instruments: {instruments}
Other instructions: {other_instructions}
"""


class SunoMusicDownloader(
    BaseComponent,
    component_name="Suno Music Downloader",
    component_description="""Downloads songs from Suno.
Inputs:
  `Song IDs` (List[str]): A list of the IDs of the songs to download, e.g. `[`6f4b42b8-9c48-4dde-91e3-c79a23cad679`, `95e66c84-9b31-4adc-8ddf-35d32eef0643`]`.
Output (Dict[str, Dict]): A dictionary with each inputted song ID mapped to a dict with data about the song, including the keys `title` (mapped to the title (str)) and `file_path` (mapped to the server path of the downloaded mp3 file (str)).
NOTE: this component assumes that the suno api (https://github.com/gcui-art/suno-api) has been downloaded and started locally
""",
    input_types={
        "song_ids": DataType.LIST
    },
    output_type=DataType.JSON,
    component_group=ComponentGroup.MUSICGEN,
    suno_api_base_url="http://localhost:3000",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self, song_ids: List[str]):
        base_url = self.configuration["suno_api_base_url"]
        url = f"{base_url}/api/get"
        params = {"ids": ",".join(song_ids)}
        response = requests.get(url, params=params)
        response_json = response.json()
        id2song_data = {song_data.get('id'): song_data for song_data in response_json}

        for song_id in song_ids:
            song_data = id2song_data.get(song_id)
            if not song_data:
                continue
            audio_url = song_data.get('audio_url')
            if not audio_url:
                continue
            download_dir_path = self._file_connector.get_absolute_path("")
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                audio_file_path = os.path.join(download_dir_path, f"{song_id}.mp3")
                with open(audio_file_path, "wb") as file:
                    file.write(audio_response.content)
                song_data['file_path'] = audio_file_path
    
        return id2song_data
