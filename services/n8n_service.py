"""
N8NService
----------
Bridges the AI Outreach Agent with an n8n automation workflow.

Instead of sending emails directly through Python's smtplib, this service
sends the generated lead + email data to an n8n Webhook node. n8n then
handles validation, sending (via its Gmail node), and logging — turning
"send an email" into a proper automated workflow that can later be
extended (delays, retries, CRM updates, Slack notifications, etc.)
without touching the Python codebase at all.

Setup:
1. Import n8n_workflows/outreach_automation.json into your n8n instance.
2. Add your Gmail OAuth2 credential to the "Send Email (Gmail)" node.
3. Activate the workflow and copy its Production Webhook URL.
4. Put that URL in your .env file as N8N_WEBHOOK_URL.
"""

import requests
from logs.log import log_info, log_error
from config import N8N_WEBHOOK_URL


class N8NService:
    """
    Service responsible for triggering the n8n outreach automation workflow.
    """

    def __init__(self):
        self.webhook_url = N8N_WEBHOOK_URL

    def is_configured(self) -> bool:
        """Return True if an n8n webhook URL has been set."""
        return bool(self.webhook_url)

    def trigger_send(
        self,
        lead_name: str,
        recipient_email: str,
        sender_name: str,
        subject: str,
        email_body: str,
        timeout: int = 15,
    ) -> tuple[bool, str]:
        """
        Trigger the n8n workflow to send one outreach email.

        Returns:
            (success, message)
        """
        if not self.is_configured():
            log_error("N8N Error: N8N_WEBHOOK_URL is not set in .env")
            return False, "n8n webhook URL is not configured."

        payload = {
            "lead_name": lead_name,
            "recipient_email": recipient_email,
            "sender_name": sender_name,
            "subject": subject,
            "email_body": email_body,
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=timeout,
            )

            if response.status_code == 200:
                log_info(f"n8n workflow triggered successfully for {lead_name}")
                return True, "Email queued through n8n workflow."

            log_error(
                f"n8n Error: status={response.status_code} body={response.text}"
            )
            return False, f"n8n responded with status {response.status_code}."

        except requests.exceptions.Timeout:
            log_error("N8N Error: Request timed out")
            return False, "n8n workflow request timed out."

        except requests.exceptions.RequestException as e:
            log_error(f"N8N Error: {e}")
            return False, f"Could not reach n8n webhook: {e}"

    def trigger_bulk_send(self, outreach_items: list[dict]) -> dict:
        """
        Trigger the n8n workflow for a batch of generated emails.

        outreach_items: list of dicts, each containing
            lead_name, recipient_email, sender_name, subject, email_body

        Returns a summary dict: {"sent": int, "failed": int, "errors": list}
        """
        summary = {"sent": 0, "failed": 0, "errors": []}

        for item in outreach_items:
            success, message = self.trigger_send(
                lead_name=item.get("lead_name", ""),
                recipient_email=item.get("recipient_email", ""),
                sender_name=item.get("sender_name", ""),
                subject=item.get("subject", ""),
                email_body=item.get("email_body", ""),
            )
            if success:
                summary["sent"] += 1
            else:
                summary["failed"] += 1
                summary["errors"].append(
                    {"lead_name": item.get("lead_name", ""), "reason": message}
                )

        return summary
