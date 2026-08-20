
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