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

from typing import Any, Dict, List, Optional

from lunarcore.core.component import BaseComponent
from lunarcore.core.typings.components import ComponentGroup
from lunarcore.core.data_models import ComponentInput, ComponentModel
from lunarcore.core.typings.datatypes import DataType
import smtplib
import dns.resolver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_an_email(email_dst: str, sender: str, html: str, subject: str):
    """
    Sends an email to a specified recipient with HTML content.

    This function takes the recipient's email address, the sender's email address, and the HTML content to be sent. It determines the recipient's email server by querying DNS for MX records of the domain part of the recipient's email address. Then, it connects to the email server and sends an email with the specified HTML content as the body. The subject of the email is set to "Automatically generated report".

    Args:
        email_dst (str): The email address of the recipient. Must be a valid email format (e.g., "user@example.com").
        sender (str): The email address of the sender. Must be a valid email format and authorized to send emails through the identified SMTP server.
        html (str): The HTML content to be sent in the email body.
        subject (str): The subject of the email.

    Example:
        send_an_email("recipient@example.com", "sender@example.com", "<h1>This is a Test Email</h1>", "hello")

    """
    domain = email_dst.split("@")[-1]
    records = dns.resolver.resolve(domain, "MX")
    mx_record = str(records[0].exchange)
    server = smtplib.SMTP(mx_record, 25)
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = email_dst

    part1 = MIMEText(html, "html")
    message.attach(part1)

    server.sendmail(sender, email_dst, message.as_string())

    server.quit()


class EmailsSender(
    BaseComponent,
    component_name="Emails Sender",
    #  The ability to use the module __doc__ would have been more elegant
    #  But the parser crash if you try
    #  component_description=__doc__,
    component_description="""Sends emails.
Inputs:
  emails_input (Dict[Dict[str, str]]): A dictionary with the receiver email adresses (str) as keys, each mapped to a dictionary with the keys `html` (str) mapped to a string `<b>body of the email</b>` with the email content, and `subject` mapped to a string of the email subject.
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
):
    def __init__(
        self,
        model: Optional[ComponentModel] = None,
        **kwargs: Any,
    ):
        super().__init__(model=model, configuration=kwargs)

    def run(
        self,
        emails_input: Dict,
        sender: str,
        subject: str = "Email from Lunar without a particular subject",
    ) -> Dict[str, Dict[str, str]]:
        for email, subdict in emails_input.items():
            if isinstance(subdict, dict):
                html = subdict["html"]
                subject = subdict["subject"]
            else:
                html = subdict
            send_an_email(email, sender, html, subject)
        return "emails sent"
