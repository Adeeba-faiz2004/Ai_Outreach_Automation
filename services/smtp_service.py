
import smtplib

from email.message import EmailMessage

from config import (
    SENDER_EMAIL,
    APP_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
)


class SMTPService:
    """
    Service responsible for sending emails.
    """

    def __init__(self):

        self.sender_email = SENDER_EMAIL
        self.app_password = APP_PASSWORD
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
    ) -> bool:
        """
        Send an email using Gmail SMTP.
        """

        message = EmailMessage()

        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        message.set_content(body)

        try:

            with smtplib.SMTP(
                self.smtp_server,
                self.smtp_port,
            ) as server:

                server.starttls()

                server.login(
                    self.sender_email,
                    self.app_password,
                )

                server.send_message(message)

            print("Email sent successfully.")
            return True

        except Exception as e:

            print(f"SMTP Error: {e}")
            return False