import os
import requests
import json
import base64
from msal import ConfidentialClientApplication
from typing import Optional

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

class UpdateExcel(
    BaseComponent,
    component_name="Update Excel",
    component_description="Updates a specified Excel workbook hosted on Microsoft SharePoint with input data.",
    input_types={"shared_url": DataType.TEXT, "input_string": DataType.TEXT, "sheet": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.IO,
    client_id="$LUNARENV::OUTLOOK_CLIENT_ID",
    client_secret="$LUNARENV::OUTLOOK_CLIENT_SECRET",
    tenant_id="$LUNARENV::OUTLOOK_TENANT_ID",
):
    def __init__(self, model: Optional[ComponentModel] = None, **kwargs):
        super().__init__(model, configuration=kwargs)
        self.client_id = kwargs.get("client_id", os.getenv("OUTLOOK_CLIENT_ID"))
        self.client_secret = kwargs.get("client_secret", os.getenv("OUTLOOK_CLIENT_SECRET"))
        self.tenant_id = kwargs.get("tenant_id", os.getenv("OUTLOOK_TENANT_ID"))

        if not self.client_id or not self.client_secret or not self.tenant_id:
            raise ValueError("Missing required configuration for Outlook API integration.")

    def run(self, shared_url: str, input_string: str, sheet: str) -> str:
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        scopes = ["https://graph.microsoft.com/.default"]

        app = ConfidentialClientApplication(
            self.client_id,
            client_credential=self.client_secret,
            authority=authority
        )

        token_response = app.acquire_token_for_client(scopes=scopes)
        token = token_response.get("access_token")

        if not token:
            raise Exception("Failed to acquire access token")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        base64_value = base64.b64encode(shared_url.encode('utf-8')).decode('utf-8')
        encoded_url = "u!" + base64_value.rstrip('=').replace('/', '_').replace('+', '-')

        share_url = f"https://graph.microsoft.com/v1.0/shares/{encoded_url}/driveItem"
        response = requests.get(share_url, headers=headers)
        item_info = response.json()

        if response.status_code != 200 or 'id' not in item_info:
            raise Exception("Failed to retrieve item info from the shared URL")

        item_id = item_info['id']
        drive_id = item_info['parentReference']['driveId']

        workbook_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{item_id}/workbook"

        range_url = f"{workbook_url}/worksheets('{sheet}')/range(address='A1:A1000')"
        response = requests.get(range_url, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to retrieve values from the worksheet")

        values = response.json().get('values', [])
        
        empty_row = 1
        for i, row in enumerate(values):
            if all(cell == "" for cell in row):
                empty_row = i + 1
                break
        else:
            empty_row = len(values) + 1

        columns = input_string.split(';')
        num_columns = len(columns)
        last_column = chr(64 + num_columns)  

        update_data = {
            "values": [columns]
        }

        update_url = f"{workbook_url}/worksheets('{sheet}')/range(address='A{empty_row}:{last_column}{empty_row}')"
        response = requests.patch(update_url, headers=headers, data=json.dumps(update_data))

        if response.status_code == 200:
            return f"Row {empty_row} updated successfully."
        else:
            raise Exception(f"Failed to update the worksheet: {response.status_code}, {response.json()}")
