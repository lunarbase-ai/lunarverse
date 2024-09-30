# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Simon Ljungbeck <simon.ljungbeck@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

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


class SunoMusicGenerator(
    BaseComponent,
    component_name="Suno Music Generator",
    component_description="""Generates music using Suno.
Inputs:
  `Title` (str): The title of the song, e.g. `Blinding Lights`.
  `Lyrics` (str): The lyrics of the song e.g. `[Verse 1]I have been tryna call, I have been on my own for long enough, ..., [Chorus]..., ...`.
  `Genres` (List[str]): The genres of the song, e.g. `[`rock`, `indie`]`.
  `Tempo` (str): The tempo of the song, e.g. `171 BPM`, `adagio`, `moderato`, `allegro`, etc. (also `slow`, `fast`, etc. works)
  `Instruments` (List[str]): The instruments mood of the song, e.g. `[`piano`, `guitar`]`.
  `Other instructions` (str): Other instructions for the generation, e.g. `Keep the outro short`.
Output (List[str]): A list of the ID's of the generated songs (normally, two songs are generated).
NOTE: this component assumes that the suno api (https://github.com/gcui-art/suno-api) has been downloaded and started locally
""",
    input_types={
        "title": DataType.TEXT,
        "lyrics": DataType.TEXT,
        "genres": DataType.LIST,
        "tempo": DataType.TEXT,
        "instruments": DataType.LIST,
        "other_instructions": DataType.TEMPLATE,
    },
    output_type=DataType.LIST,
    component_group=ComponentGroup.MUSICGEN,
    suno_api_base_url=None
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs: Any):
        super().__init__(model=model, configuration=kwargs)

    def run(self,
            title: str,
            lyrics: str,
            genres: List[str],
            tempo: str,
            instruments: List[str],
            other_instructions: str
            ):

        base_url = self.configuration["suno_api_base_url"]
        url = f"{base_url}/api/custom_generate"

        prompt = SUNO_PROMPT_TEMPLATE.format(
            lyrics=lyrics,
            genres=genres,
            tempo=tempo,
            instruments=instruments,
            other_instructions=other_instructions
        )

        data = {
            "prompt": prompt,
            "tags": " ".join(genres),
            "title": title,
            "make_instrumental": bool(lyrics),
            "wait_audio": True
        }

        response = requests.post(url, json=data)
        song_ids = []
        for song_data in response.json():
            id = song_data.get('id', '')
            if id:
                song_ids.append(id)

        return song_ids