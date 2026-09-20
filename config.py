
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


GEMINI_MODEL = "gemini-2.5-flash"


SENDER_EMAIL = os.getenv("SENDER_EMAIL")

APP_PASSWORD = os.getenv("APP_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 587

# n8n workflow automation (see n8n_workflows/outreach_automation.json)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# Vapi AI voice calling (used by services/calling_service.py AND by the
# "Trigger Vapi AI Call" node in n8n_workflows/outreach_automation.json).
# This is the single voice-calling provider across the whole project —
# do not add a second provider (e.g. Bland.ai) without updating both
# places and the README.
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")
VAPI_VOICE_MODEL = "gpt-4o-mini"
