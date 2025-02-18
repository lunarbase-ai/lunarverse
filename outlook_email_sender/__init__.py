import os
import requests
from typing import Optional
from msal import ConfidentialClientApplication

from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentModel
from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.datatypes import DataType

class OutlookEmailSender(
    BaseComponent,
    component_name="Outlook Email Sender",
    component_description="This component automates the process of sending emails using the Outlook API.",
    input_types={"email": DataType.TEXT, "subject": DataType.TEXT, "body": DataType.TEXT, "to_recipients": DataType.TEXT, "cc_recipients": DataType.TEXT, "bcc_recipients": DataType.TEXT},
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

    def run(self, email: str, subject: str, body: str, to_recipients: str, cc_recipients: Optional[str] = None, bcc_recipients: Optional[str] = None) -> str:
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

        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body
                },
                "toRecipients": [{"emailAddress": {"address": addr.strip()}} for addr in to_recipients.split(",")],
                "ccRecipients": [{"emailAddress": {"address": addr.strip()}} for addr in cc_recipients.split(",")] if cc_recipients else [],
                "bccRecipients": [{"emailAddress": {"address": addr.strip()}} for addr in bcc_recipients.split(",")] if bcc_recipients else []
            }
        }

        send_mail_url = f"https://graph.microsoft.com/v1.0/users/{email}/sendMail"
        response = requests.post(send_mail_url, headers=headers, json=email_data)

        if response.status_code != 202:
            raise Exception(f"Failed to send email: {response.json()}")

        return "Email sent successfully"