import base64
import os
import requests
from typing import List, Optional, Dict
from msal import ConfidentialClientApplication

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType, File

class OutlookAttachment(
    BaseComponent,
    component_name="Outlook Attachment",
    component_description="This component automates the process of retrieving email attachments from unread messages in an Outlook inbox. It scans for unread emails, downloads all available attachments, and marks the emails as read once processed.",
    input_types={"email": DataType.TEXT, "count": DataType.TEXT, "expand": DataType.TEXT, "filter": DataType.TEXT, "format": DataType.TEXT, "orderby": DataType.TEXT, "search": DataType.TEXT, "select":DataType.TEXT, "skip": DataType.TEXT, "top": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.DATA_EXTRACTION,
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

    def build_query_string(self, **kwargs) -> str:
        query_parts = []
        for key, value in kwargs.items():
            if value is not None and value.strip():
                query_parts.append(f"${key}={value}")
        return "&".join(query_parts)

    def run(self, email: str, count: Optional[str] = None, expand: Optional[str] = None, filter: Optional[str] = None, \
            format: Optional[str] = None, orderby: Optional[str] = None, search: Optional[str] = None, \
            select: Optional[str] = None, skip: Optional[str] = None, top: Optional[str] = None) -> str:
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        scopes = ["https://graph.microsoft.com/.default"]

        app = ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret,
        )

        token_response = app.acquire_token_for_client(scopes=scopes)
        access_token = token_response.get("access_token")

        if not access_token:
            raise Exception("Failed to acquire access token")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        query_string = self.build_query_string(
            count=count, expand=expand, filter=filter, format=format,
            orderby=orderby, search=search, select=select, skip=skip, top=top
        )
        graph_url = f"https://graph.microsoft.com/v1.0/users/{email}/messages?{query_string}"
        response = requests.get(graph_url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch messages: {response.json()}")

        messages = response.json().get("value", [])
        output_files = []

        for message in messages:
            message_id = message["id"]
            attachments_url = f"https://graph.microsoft.com/v1.0/users/{email}/messages/{message_id}/attachments"

            attachments_response = requests.get(attachments_url, headers=headers)

            if attachments_response.status_code == 200:
                attachments = attachments_response.json().get("value", [])
                for attachment in attachments:
                    if "contentBytes" in attachment:
                        content = base64.b64decode(attachment["contentBytes"])
                        file_name = attachment["name"]

                        with open(file_name, "wb") as file:
                            file.write(content)

                        output_files.append(os.path.abspath(file_name))
            
            mark_as_read_url = f"https://graph.microsoft.com/v1.0/users/{email}/messages/{message_id}"
            mark_as_read_body = {"isRead": True}
            requests.patch(mark_as_read_url, headers=headers, json=mark_as_read_body)

        if not output_files:
            raise Exception("No attachments found in unread messages.")

        return output_files
