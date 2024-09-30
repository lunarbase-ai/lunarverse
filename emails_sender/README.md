# Emails Sender Component

## Description

The **Emails Sender** component is designed to facilitate the sending of emails. It takes in a structured input of email details, including the recipient addresses, email content, and subject, and sends out the emails. Upon successful completion, it outputs a confirmation string.

## Inputs

### emails_input (Dict[Dict[str, str]])

A JSON dictionary where the keys are the receiver email addresses (strings). Each email address maps to another dictionary containing:

- `html` (str): The HTML content of the email body, enclosed in `<b>` tags. For example, `<b>body of the email</b>`.
- `subject` (str): The subject of the email.

### sender (str)

A string representing the sender's email address. For instance, `no-reply@lunarbase.ch`.

### subject (str) (Optional)

A global subject string that will overwrite the individual subjects provided in the `emails_input` dictionary. For example, `newsletter for you!`.

## Output

### (str)

A string with the text `emails sent` if the emails were sent successfully.

## Input Types

- `emails_input`: JSON
- `sender`: TEXT
- `subject`: TEXT

## Output Type

- TEXT

## Configuration Parameters

This component does not require any additional configuration parameters.

---

This documentation provides an overview of the **Emails Sender** component, detailing its inputs, outputs, and types. This component is essential for automating the process of sending emails with specified content and subject lines.