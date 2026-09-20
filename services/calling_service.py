import requests

from logs.log import log_info, log_error
from config import VAPI_API_KEY, VAPI_PHONE_NUMBER_ID, VAPI_VOICE_MODEL


class CallingService:
    """
    AI Voice Calling Integration — Vapi.

    This is the ONLY voice-calling provider used in this project. It
    powers both:
    1. The manual "Dispatch AI Voice Call" button in the dashboard
       (this file), for on-demand calls a user triggers themselves.
    2. The automated "Trigger Vapi AI Call" step in the n8n workflow
       (n8n_workflows/outreach_automation.json), which fires
       automatically 3 days after an email if no reply is detected.

    Both paths use the same Vapi account/model (gpt-4o-mini) so the
    project has one consistent, documented voice-calling system
    instead of two different providers.
    """

    def __init__(self):
        self.api_key = VAPI_API_KEY
        self.phone_number_id = VAPI_PHONE_NUMBER_ID
        self.api_url = "https://api.vapi.ai/call"

    def trigger_ai_call(
        self,
        phone_number: str,
        lead_name: str,
        company_name: str,
        industry: str,
        objective: str = "Book a 15-minute discovery call for AI automation services",
    ) -> tuple[bool, str]:
        """
        Trigger an outbound Vapi AI voice call to a lead.

        Returns (success, message). Never falls back to a hardcoded
        phone number — if no phone_number is supplied, it fails safely
        instead of guessing or defaulting to anyone's personal number.
        """
        if not phone_number:
            return False, "No phone number provided for this lead."

        if not self.api_key or not self.phone_number_id:
            log_info(
                f"[SIMULATION] Vapi call would be triggered for {lead_name} "
                f"at {phone_number}. (Set VAPI_API_KEY and "
                f"VAPI_PHONE_NUMBER_ID in .env for live calls.)"
            )
            return True, (
                f"Simulated AI call for {lead_name} ({phone_number}). "
                f"Set VAPI_API_KEY and VAPI_PHONE_NUMBER_ID in .env to "
                f"make this a real call."
            )

        system_prompt = (
            f"You are an AI outreach assistant calling on behalf of an "
            f"AI automation agency. You are speaking with {lead_name}, "
            f"who works at {company_name} in the {industry} industry. "
            f"Goal: introduce yourself briefly, mention the follow-up "
            f"email sent about workflow automation for {company_name}, "
            f"and work toward this objective: {objective}. If they "
            f"sound interested, offer two specific time options for a "
            f"short call. Keep responses concise and natural."
        )

        first_message = (
            f"Hi {lead_name}, this is an AI assistant following up on "
            f"the email we sent about {company_name}'s automation. Do "
            f"you have a minute?"
        )

        payload = {
            "phoneNumberId": self.phone_number_id,
            "customer": {
                "number": phone_number,
                "name": lead_name,
            },
            "assistant": {
                "model": {
                    "provider": "openai",
                    "model": VAPI_VOICE_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt}
                    ],
                },
                "voice": {
                    "provider": "vapi",
                    "voiceId": "Elliot",
                },
                "firstMessage": first_message,
            },
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=10,
            )

            if response.status_code in (200, 201):
                call_id = response.json().get("id", "unknown")
                log_info(
                    f"Vapi call initiated for {lead_name} ({phone_number}). "
                    f"Call ID: {call_id}"
                )
                return True, f"AI call dispatched successfully! Call ID: {call_id}"

            err_msg = response.text[:200]
            log_error(f"Vapi call failed for {lead_name}: {err_msg}")
            return False, f"Call failed (status {response.status_code}): {err_msg}"

        except requests.exceptions.Timeout:
            log_error("Vapi call request timed out")
            return False, "Vapi request timed out."

        except Exception as e:
            log_error(f"Calling Service Error: {e}")
            return False, f"Connection error: {str(e)}"
