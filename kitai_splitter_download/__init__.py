# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, Any, List

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

import os
import requests


def download_audio_url(audio_url, filename):
    response = requests.get(audio_url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return filename    

class KitsaiSplitterDownload(
    BaseComponent,
    component_name="Kitsai Splitter Download",
    component_description="""Download the result of a split opperation from Kits.ai""",
    input_types={"split_id": DataType.TEXT},
    output_type=DataType.JSON,
    component_group=ComponentGroup.MUSICGEN,
    client_id="$LUNARENV::KITSAI_CLIENT_ID",
    client_secret="$LUNARENV::KITSAI_CLIENT_SECRET",
):
    URL = "https://arpeggi.io/api/kits/v1/stem-splits"
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)

    def run(
        self, split_id: str
    ):
        url = f"{URL}/{split_id}"
        headers = { 'Authorization': f'Bearer {self.configuration.get("api_key")}' }

        response = requests.request("GET", url, headers=headers)
        
        response_json = response.json()

        if 'status' in response_json:
            if response_json['status'] == "success":
                urls = {}
                for key in ["vocalAudioFileUrl","lossyVocalAudioFileUrl","backingAudioFileUrl","stemFileUrls","lossyStemFileUrls"]:
                    if key in response_json:
                        urls[key] = response_json[key]

                output = {}
                for key in ["vocalAudioFileUrl","backingAudioFileUrl"]:  # TODO: also handle mp3 files ('lossy' files)
                    if key in urls and urls[key]:
                        filename = os.path.join(self._file_connector.get_absolute_path(""), f'{key}.wav')
                        saved_file = download_audio_url(urls[key], filename)
                        if saved_file:
                            output[key] = saved_file
                if 'stemFileUrls' in urls and urls['stemFileUrls']:
                    for stem_data in urls['stemFileUrls']:
                        url = stem_data['url']
                        instrument = stem_data['instrument']
                        filename = os.path.join(self._file_connector.get_absolute_path(""), f'{instrument}.wav')
                        saved_file = download_audio_url(url, filename)
                        if saved_file:
                            output[instrument] = saved_file
                
                return output

            return {"status": response_json['status']}
        
        return {"error": response_json['message']}
