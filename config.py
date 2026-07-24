
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
print("OpenRouter Key:", OPENROUTER_API_KEY)