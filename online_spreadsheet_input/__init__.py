# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
"""
Download and forward the content of online spreadsheet
Inputs:
  Url (str): URL of the spreadsheet. The following are supported:
    - nextcloud folder with xslx files
    - owncloud xslx file
    - google drive **published** spreadsheet
  Filename (str): for owncloud/nextcloud only, name of the file to download
  Folder_password (str): for owncloud/nextcloud only, password of the shared folder
Outputs (list[dict]): list of the records of the spreadsheet
"""

import json
from os import unlink
from typing import Any, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from uuid import uuid4
import pandas as pd
import owncloud
from pathlib import Path


class OnlineSpreadsheetInput(
    BaseComponent,
    component_name="Online Spreadsheet",
    component_description="""Downloads and outputs the content of an online spreadsheet.
Inputs:
  `Url` (str): URL of the online spreadsheet. The following are supported:
    - nextcloud folder with xslx files
    - owncloud xslx file
    - google drive **published** spreadsheet
  `Filename` (str): The name of the file to download (for owncloud/nextcloud only)
  `Folder_password` (str): Password of the shared folder (for owncloud/nextcloud only)
Outputs (List[Dict]): A list of the records of the spreadsheet.""",
    input_types={
        "url": DataType.TEXT,
        "filename": DataType.TEXT,
        "folder_password": DataType.TEXT,
    },
    output_type=DataType.LIST,
    component_group=ComponentGroup.UTILS,
):
    def __init__(
        self,
        model: Optional[ComponentModel] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, configuration=kwargs)

    def run(self, url: str, filename: str, folder_password: Optional[str] = None):
        # Assuming owncloud links (TODO support google link)
        if "google" in url:
            df = pd.read_excel(url)
            data = df.to_json(orient="records")
            return json.loads(data)
        else:
            if folder_password is None or folder_password == "":
                oc = owncloud.Client.from_public_link(url)
            else:
                oc = owncloud.Client.from_public_link(
                    url, folder_password=folder_password
                )
                # hack from https://github.com/owncloud/pyocclient/issues/282
                oc._session.headers.update({"X-Requested-With": "XMLHttpRequest"})
            local_filename = f"{str(uuid4())}-{filename}"
            local_filename = Path(__file__).parent / local_filename
            if not oc.get_file(filename, local_filename):
                raise Exception("error with owncloud access")
            df = pd.read_excel(local_filename)
            data = df.to_json(orient="records")
            unlink(local_filename)
            return json.loads(data)
