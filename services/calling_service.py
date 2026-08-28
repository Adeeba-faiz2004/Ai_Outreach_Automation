import os
import requests
import json
from logs.log import log_info, log_error

class CallingService:
    """
    AI Voice Calling Integration (Bland AI / Retell AI / Vapi AI).
    Allows launching autonomous AI phone agents to call leads,
    pitch agency services, answer objections, and book meetings.
    """

    def __init__(self):
        self.bland_api_key = os.getenv("BLAND_API_KEY", "")
        self.bland_api_url = "https://api.bland.ai/v1/calls"

    def trigger_ai_call(
        self,
        phone_number: str,
        lead_name: str,
        company_name: str,
        industry: str,
        objective: str = "Book a 15-minute discovery call for AI automation services"
    ) -> tuple[bool, str]:
        if not phone_number:
            return False, "No phone number provided for lead."

        if self.bland_api_key:
            headers = {
                "authorization": self.bland_api_key,
                "Content-Type": "application/json"
            }

            prompt = f"""
            You are Alex, an AI Outreach Specialist calling on behalf of Adeeba's AI Agency.
            You are speaking with {lead_name}, who is a leader at {company_name} in the {industry} industry.

            Goal:
            - Introduce yourself politely.
            - Mention you sent an email regarding workflow automation for {company_name}.
            - Objective: {objective}.
            - If they sound interested, ask if Tuesday at 3 PM or Wednesday at 11 AM works for a brief Zoom meeting.
            - Keep answers concise and human-like.
            """

            payload = {
                "phone_number": phone_number,
                "task": prompt,
                "model": "enhanced",
                "voice": "nat",
                "first_sentence": f"Hi {lead_name}, this is Alex following up on the email we sent regarding {company_name}'s AI automation. Do you have 60 seconds?",
                "wait_for_greeting": True,
                "record": True,
                "max_duration": 5
            }

            try:
                response = requests.post(self.bland_api_url, json=payload, headers=headers, timeout=10)
                res_data = response.json()

                if response.status_code == 200 and res_data.get("status") == "success":
                    call_id = res_data.get("call_id")
                    log_info(f"AI Call initiated for {lead_name} ({phone_number}). Call ID: {call_id}")
                    return True, f"AI Call Dispatched successfully! Call ID: {call_id}"
                else:
                    err_msg = res_data.get("message", "API Request Failed")
                    log_error(f"AI Call failed for {lead_name}: {err_msg}")
                    return False, f"Call Failed: {err_msg}"

            except Exception as e:
                log_error(f"Calling Service Error: {e}")
                return False, f"Connection Error: {str(e)}"

        log_info(f"[SIMULATION] AI Call triggered for {lead_name} at {phone_number}")
        return True, f"Simulated AI Call triggered for {lead_name} ({phone_number}). (Set BLAND_API_KEY in .env for live calls)"