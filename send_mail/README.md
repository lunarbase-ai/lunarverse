# Send Email Component

## Description

The **Send Email** component sends plain-text emails using an SMTP server. It allows specifying the SMTP server and port, the sender and recipient addresses, as well as the email subject and body. The component also supports sending to multiple recipients separated by semicolons.

## Inputs

- **smtp_server** (str): The SMTP server address used to send the email. Example: `smtp.gmail.com`.
- **smtp_port** (str): The port number used for SMTP. Typically `587` for TLS. Example: `"587"`.
- **email_sender** (str): The email address of the sender. Example: `no-reply@example.com`.
- **password** (str): The password or app-specific password for the sender's email account.
- **recipient** (str): The recipient's email address. You can specify multiple addresses separated by semicolons. Example: `user1@example.com;user2@example.com`.
- **subject** (str): The subject line of the email.
- **body** (str): The plain text content of the email message.

## Outputs

- **result** (str): Returns a confirmation message `"Emails sent successfully"` if all emails were sent without errors. If there are any issues (like missing recipient or empty body), the component returns an appropriate error message.

## Usage

To use the **Send Email** component, provide the required SMTP settings, the sender’s email and credentials, and the email content. The component will send the email(s) using the SMTP protocol with TLS encryption.


## Example

If your inputs are:


"smtp_server": "smtp.gmail.com",
"smtp_port": "587",
"email_sender": "no-reply@example.com",
"password": "examplepassword",
"recipient": "user1@example.com;user2@example.com",
"subject": "Test Email",
"body": "This is a test email sent using the Send Email component."

The output will be:

Emails sent successfully

This confirms the emails were sent to both recipients without errors.
