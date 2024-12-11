# Emails Sender Component

## Description

The **Emails Sender** component is designed to facilitate the sending of emails through a specified SMTP server. It takes in a structured input of email details, including the recipient addresses, email content, and subject, and sends out the emails. Upon successful completion, it outputs a confirmation string.



## Inputs

### `emails_input` (Dict[Dict[str, str]])

A JSON dictionary where the keys are the recipient email addresses (strings). Each email address maps to another dictionary containing:

- `html` (str): The HTML content of the email body. For example, `<b>Welcome to our service!</b>`.
- `subject` (str): The subject of the email.

**Example:**
```json
{
    "user1@domain.com": {
        "html": "<b>Welcome to Our Service!</b>",
        "subject": "Hello User1"
    },
    "user2@domain.com": {
        "html": "<b>Don't miss our updates.</b>",
        "subject": "Greetings User2"
    }
}
```
### sender (str)

A string representing the sender's email address. For instance, `no-reply@lunarbase.ch`.

### subject (str) (Optional)

A global subject string that will overwrite the individual subjects provided in the `emails_input` dictionary. For example, `Monthly Newsletter`.


## Output

### (str)

A string with the text `emails sent` if the emails were sent successfully. In case of failure, it returns an error message detailing the reason.


## Input Types

- `emails_input`: JSON
- `sender`: TEXT
- `subject`: TEXT

## Output Type

- TEXT

## Configuration Parameters

The Emails Sender component relies on the following environment variables for SMTP configuration. Ensure these are set in your environment:

- **SMTP_SERVER**: Your SMTP server address (e.g., smtp.gmail.com).
- **SMTP_PORT**: SMTP server port (e.g., 587 for TLS).
- **SMTP_USERNAME**: Username for SMTP authentication.
- **SMTP_PASSWORD**: Password for SMTP authentication.

