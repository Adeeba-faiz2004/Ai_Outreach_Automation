import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (
    SENDER_EMAIL,
    APP_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
)


class EmailSender:

    def send(
    self,
    recipient,
    subject,
    body,
):

        try:

            message = MIMEMultipart()

            message["From"] = SENDER_EMAIL
            message["To"] = recipient
            message["Subject"] = subject

            message.attach(
                MIMEText(
                    body,
                    "plain",
                )
        )

            server = smtplib.SMTP(
                SMTP_SERVER,
                SMTP_PORT,
            )

            server.starttls()

            server.login(
                SENDER_EMAIL,
                APP_PASSWORD,
            )

            server.sendmail(
                SENDER_EMAIL,
                recipient,
                message.as_string(),
            )

            server.quit()

            return True, "Email accepted by the SMTP server."

        except smtplib.SMTPRecipientsRefused:

            return False, "❌ Recipient email address rejected."

        except smtplib.SMTPAuthenticationError:

            return False, "❌ SMTP Authentication Failed."

        except smtplib.SMTPException as e:

            return False, f"❌ SMTP Error: {e}"

        except Exception as e:

            return False, f"❌ {e}"