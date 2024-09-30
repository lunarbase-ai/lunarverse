# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
"""
Save to a online spreadsheet then and forward the content
Inputs:
  Content (list[dict]): list of the record to save as a spreadsheet
  Url (str): URL of the spreadsheet. The following are supported:
    - nextcloud folder with xslx files
    - owncloud xslx file
  Filename (str): for owncloud/nextcloud only, name of the file to download
  Folder_password (str): for owncloud/nextcloud only, password of the shared folder
  Merge (int): if set to 1, will keep the added columns that already exist in the destination
Outputs (list[dict]): list of the records of the spreadsheet
"""

import json
from os import unlink
from typing import Any, List, Optional, Dict

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
from uuid import uuid4
import pandas as pd
import owncloud
from pathlib import Path


class OnlineSpreadsheetIO(
    BaseComponent,
    component_name="Online Spreadsheet IO",
    component_description="Save to a online spreadsheet then and forward the content",
    input_types={
        "content": DataType.LIST,
        "url": DataType.TEXT,
        "filename": DataType.TEXT,
        "folder_password": DataType.TEXT,
        "merge": DataType.BOOL,
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

    def run(
        self,
        content: List[Dict],
        url: str,
        filename: str,
        folder_password: Optional[str] = None,
        merge: bool = False,
    ):
        df = pd.DataFrame.from_records(content)
        df.to_excel(filename, index=False)
        # Assuming owncloud links
        if folder_password is None or folder_password == "":
            oc = owncloud.Client.from_public_link(url)
        else:
            oc = owncloud.Client.from_public_link(url, folder_password=folder_password)
        # hack from https://github.com/owncloud/pyocclient/issues/282
        oc._session.headers.update({"X-Requested-With": "XMLHttpRequest"})
        if merge:
            local_filename = f"{str(uuid4())}-{filename}"
            local_filename = Path(__file__).parent / local_filename
            if oc.get_file(filename, local_filename):
                previous_df = pd.read_excel(local_filename)
                # Align df to the columns of previous_df
                aligned_df = df.reindex(columns=previous_df.columns)
                # Update previous_df using combine_first
                updated_df = aligned_df.combine_first(previous_df)
                updated_df.to_excel(filename, index=False)
                data = updated_df.to_json(orient="records")
                content = json.loads(data)
                unlink(local_filename)
        oc.drop_file(filename)
        unlink(filename)
        return content
