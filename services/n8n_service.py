import os
import requests
import json
from logs.log import log_info, log_error

class N8NService:
    """
    Service to trigger n8n Webhook workflows for:
    - Lead Processing & Enrichment
    - Email Delivery & Follow-up Scheduling
    - AI Sentiment Analysis
    - AI Voice Calling Dispatch
    """

    def __init__(self):
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL", "")

    def trigger_lead_workflow(self, lead_item: dict, event_type: str = "EMAIL_SENT") -> tuple[bool, str]:
        """
        Sends lead event data to n8n Webhook matching the exact JSON keys
        expected by the 'Validate Payload' node in n8n:
        - recipient_email
        - subject
        - email_body
        - recipient_name
        - recipient_company
        - recipient_phone
        """
        if not self.webhook_url:
            log_info(f"[n8n Service] Webhook URL not configured. Event '{event_type}' logged locally.")
            return True, "n8n Webhook logged locally (Set N8N_WEBHOOK_URL in .env to activate live automation)"

        lead = lead_item.get("lead") if "lead" in lead_item else lead_item

        payload = {
            "recipient_email": getattr(lead, "email", lead_item.get("email", "faizadiba2004@gmail.com")),
            "subject": lead_item.get("subject", "Exclusive AI Outreach Strategy"),
            "email_body": lead_item.get("email", lead_item.get("email_body", "Hi, let's connect!")),
            "recipient_name": getattr(lead, "name", lead_item.get("name", "Adeeba Faiz")),
            "recipient_company": getattr(lead, "company", lead_item.get("company", "AI Outreach Automation")),
            "recipient_phone": getattr(lead, "phone", lead_item.get("phone", "+923494638576")),
            "event": event_type
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )

            if response.status_code in (200, 201):
                log_info(f"n8n Webhook triggered successfully for event: {event_type}")
                return True, "n8n Automation Triggered Successfully"
            else:
                log_error(f"n8n Webhook returned status code {response.status_code}")
                return False, f"n8n Response Code: {response.status_code}"

        except Exception as e:
            log_error(f"Failed to connect to n8n Webhook: {e}")
            return False, f"n8n Connection Error: {str(e)}"
