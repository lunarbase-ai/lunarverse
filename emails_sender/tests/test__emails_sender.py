# test__emails_sender.py

import pytest
from unittest.mock import patch
import smtplib
from emails_sender import EmailsSender

class TestEmailsSender:

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        monkeypatch.setenv('SMTP_SERVER', 'smtp.test.com')
        monkeypatch.setenv('SMTP_PORT', '587')
        monkeypatch.setenv('SMTP_USERNAME', 'user@test.com')
        monkeypatch.setenv('SMTP_PASSWORD', 'password')

        self.emails_sender = EmailsSender()

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.sendmail.return_value = {}

        emails_input = {
            "test@domain.com": {"html": "<b>Test Body</b>", "subject": "Test Subject"}
        }
        sender = "no-reply@lunarbase.ch"
        subject = "Global Subject"

        result = self.emails_sender.run(emails_input, sender, subject)

        assert result == "emails sent"

    @patch('smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.sendmail.side_effect = smtplib.SMTPException("Connection failed")

        emails_input = {
            "test@domain.com": {"html": "<b>Test Body</b>", "subject": "Test Subject"}
        }
        sender = "no-reply@lunarbase.ch"
        subject = "Global Subject"

        result = self.emails_sender.run(emails_input, sender, subject)

        assert result == "failed to send emails: Connection failed"

    @patch('smtplib.SMTP')
    def test_send_multiple_emails_success(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.sendmail.return_value = {}
    
        emails_input = {
            "user1@domain.com": {"html": "<b>Body 1</b>", "subject": "Subject 1"},
            "user2@domain.com": {"html": "<b>Body 2</b>", "subject": "Subject 2"}
        }
        sender = "no-reply@lunarbase.ch"
        subject = "Global Subject"
    
        result = self.emails_sender.run(emails_input, sender, subject)
    
        assert result == "emails sent"
        assert mock_smtp_instance.sendmail.call_count == 2

    @patch('smtplib.SMTP')
    def test_send_empty_emails_input(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
    
        emails_input = {}
        sender = "no-reply@lunarbase.ch"
        subject = "Global Subject"
    
        result = self.emails_sender.run(emails_input, sender, subject)
    
        assert result == "emails sent"
        mock_smtp_instance.sendmail.assert_not_called()

    @patch('smtplib.SMTP')
    def test_send_email_without_subject(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.sendmail.return_value = {}
    
        emails_input = {
            "test@domain.com": {"html": "<b>Test Body</b>"}
        }
        sender = "no-reply@lunarbase.ch"
        subject = None
    
        result = self.emails_sender.run(emails_input, sender, subject)
    
        assert result == "emails sent"
        mock_smtp_instance.sendmail.assert_called_once()

    @patch('smtplib.SMTP')
    def test_smtp_login_failure(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.login.side_effect = smtplib.SMTPAuthenticationError(535, b'Authentication failed')
    
        emails_input = {
            "test@domain.com": {"html": "<b>Test Body</b>", "subject": "Test Subject"}
        }
        sender = "no-reply@lunarbase.ch"
        subject = "Global Subject"
    
        result = self.emails_sender.run(emails_input, sender, subject)
    
        assert "failed to send emails: " in result


    @patch('smtplib.SMTP')
    def test_generic_exception(self, mock_smtp):
        mock_smtp_instance = mock_smtp.return_value.__enter__.return_value
        mock_smtp_instance.sendmail.side_effect = Exception("Unexpected error")
    
        emails_input = {
            "test@domain.com": {"html": "<b>Test Body</b>", "subject": "Test Subject"}
        }
        sender = "no-reply@lunarbase.ch"
        subject = "Global Subject"
    
        result = self.emails_sender.run(emails_input, sender, subject)
    
        assert "failed to send emails: Unexpected error" == result