# Gmail Attachment Component

## Description

The **Gmail Attachment** component automates the process of retrieving email attachments from unread or filtered messages in a Gmail inbox. It uses IMAP to authenticate with a Gmail account, scan for messages based on given filters (such as sender, subject, date, and body content), download attachments to a local directory, and mark the emails as read once processed.

## Inputs

- **username** (str): Gmail address used to authenticate and access the inbox. Example: `myemail@gmail.com`.
- **password** (str): App-specific password for Gmail IMAP access. Example: `my-app-password`.
- **status_filter** (str): IMAP status filter such as `UNSEEN` or `SEEN`.
- **start_date** (str): Filter to retrieve emails received since this date. Format example: `01-Jan-2024`.
- **sender** (str): Filter to include only emails sent by this address. Example: `sender@example.com`.
- **recipient** (str): Filter to include only emails sent to this address. Example: `myemail@gmail.com`.
- **subject** (str): Filter emails with matching subject. Example: `Invoice`.
- **content** (str): Filter emails that contain this text in the body. Example: `Payment`.

## Outputs

The component returns a list of strings with the absolute paths of all attachments found in the filtered emails.

- **result** (List[str]): Example: `["/full/path/to/attachments/file1.pdf"]`.

## Usage

To use the **Gmail Attachment** component, provide your Gmail address and app-specific password, along with optional filters such as status, date, sender, subject, or content. The component connects to the Gmail inbox via IMAP, applies the filters, downloads attachments to a local folder named `attachments`, and returns the file paths.


## Example

If your inputs are:

{
  "username": "myemail@gmail.com",
  "password": "my-app-password",
  "status_filter": "UNSEEN",
  "start_date": "01-Jan-2024",
  "sender": "billing@example.com",
  "subject": "Invoice"
}

The output might be:

[
  "/home/user/attachments/invoice_jan.pdf",
  "/home/user/attachments/invoice_feb.pdf"
]

This indicates the component successfully retrieved and saved the attachments locally.
