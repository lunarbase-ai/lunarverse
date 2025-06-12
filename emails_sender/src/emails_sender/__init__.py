# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: William Droz <william.droz@idiap.ch>
#
# SPDX-License-Identifier: LicenseRef-lunarbase
"""Component to send emails
Need two inputs:
  `emails_input` (Dict[Dict[str, str]]): e.g {"william.droz@idiap.ch": {"html": "<b>body of the email</b>", "subject": "hello"}}
  `sender` (str): e.g "no-reply@lunarbase.ch"
  `subject` (str): Optionnal global subject, will overwrite the subject. e.g "newsletter for you!"
"""

from typing import Any, Dict, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from emails_sender.models import EmailsInputModel

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType

class EmailsSender(
    LunarComponent,
    component_name="Emails Sender",
    component_description="""Sends emails based on user-defined inputs, including recipients, subject lines, and message content. .
Inputs:
  emails_input (Dict[Dict[str, Optional]]): A dictionary with the receiver email adresses (str) as keys, each mapped to a dictionary with the keys `html` (str) mapped to a string `<b>body of the email</b>` with the email content, and `subject` mapped to a string of the email subject.
  sender (str): A string of the sender email, e.g `no-reply@lunarbase.ch`.
  subject (str): Optional global subject, will overwrite the subject. e.g `newsletter for you!`.
Output (str): A string of the text `emails sent` if the emails were sent successfully.""",
    input_types={
        "emails_input": DataType.JSON,
        "sender": DataType.TEXT,
        "subject": DataType.TEXT,
    },
    output_type=DataType.TEXT,
    component_group=ComponentGroup.UTILS,
    smtp_server="$LUNARENV::SMTP_SERVER",
    smtp_port="$LUNARENV::SMTP_PORT",
    smtp_username="$LUNARENV::SMTP_USERNAME",
    smtp_password="$LUNARENV::SMTP_PASSWORD",
):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(configuration=kwargs)

    def run(
        self,
        emails_input: EmailsInputModel,
        sender: str,
        subject: Optional[str] = None,
    ) -> str:
        try:
            with smtplib.SMTP(self.configuration['smtp_server'], self.configuration['smtp_port']) as server:
                server.login(self.configuration['smtp_username'], self.configuration['smtp_password'])

                for receiver, content in emails_input.items():
                    msg = MIMEMultipart()

                    msg['From'] = sender
                    msg['To'] = receiver
                    msg['Subject'] = subject if subject else content.get('subject', '')

                    msg.attach(MIMEText(content.get('html', ''), 'html'))

                    server.sendmail(sender, receiver, msg.as_string())
            return "emails sent"
        except smtplib.SMTPException as e:
            return f"failed to send emails: {str(e)}"
        except Exception as e:
            return f"failed to send emails: {str(e)}"
