from datetime import datetime
import json
from prompts import (
    SOFTWARE_PROMPT,
    HEALTHCARE_PROMPT,
    TECHNOLOGY_PROMPT,
    RETAIL_PROMPT,
    FINANCE_PROMPT,
    GENERAL_PROMPT,
)
from gemini_service import GeminiService
from logs.log import log_error
from models.lead import Lead


PROMPTS = {
    "Software": SOFTWARE_PROMPT,
    "Healthcare": HEALTHCARE_PROMPT,
    "Technology": TECHNOLOGY_PROMPT,
    "Retail": RETAIL_PROMPT,
    "Finance": FINANCE_PROMPT,
}


def load_email_history() -> list | None:
    """
    Load all previously saved emails from disk.
    """
    try:
        with open("data/sent_emails.json", "r") as file:
            return json.load(file)
    except Exception as e:
        log_error(f"Load Error: {e}")
        return None


class OutreachAgent:

    def __init__(
        self,
        sender_name: str,
        company: str,
        tone: str,
        email_length: str,
    ):
        """
        Initialize the Outreach Agent.
        """
        self.sender_name = sender_name
        self.company = company
        self.tone = tone
        self.email_length = email_length
        self.gemini = GeminiService()

    def choose_prompt(self, lead: Lead) -> str:
        """
        Select and personalize the prompt based on the given industry.
        Uses intelligent matching to select the exact domain prompt.
        """
        industry_raw = lead.industry.strip()
        industry_lower = industry_raw.lower()

        # Intelligent matching for prompt selection
        if "soft" in industry_lower or "dev" in industry_lower:
            base_prompt = SOFTWARE_PROMPT
        elif "health" in industry_lower or "med" in industry_lower or "clinic" in industry_lower:
            base_prompt = HEALTHCARE_PROMPT
        elif "tech" in industry_lower or "cloud" in industry_lower or "ai" in industry_lower or "it" == industry_lower:
            base_prompt = TECHNOLOGY_PROMPT
        elif "retail" in industry_lower or "e-com" in industry_lower or "store" in industry_lower or "shop" in industry_lower:
            base_prompt = RETAIL_PROMPT
        elif "fin" in industry_lower or "bank" in industry_lower or "invest" in industry_lower:
            base_prompt = FINANCE_PROMPT
        else:
            base_prompt = PROMPTS.get(industry_raw, GENERAL_PROMPT)

        return f"""
You are an expert sales copywriter.

Your task is to write ONLY ONE personalized cold outreach email.

Sender Details:
- Company Name: {self.company}
- Sender Name: {self.sender_name}

Recipient Details:
- Name: {lead.name}
- Position: {lead.position}
- Company: {lead.company}
- Industry: {lead.industry}

Writing Style:
- Tone: {self.tone}
- Target Length: {self.email_length}

Industry Specific Guidance:
{base_prompt}

Strict Rules:
- Return response in this EXACT format:

Subject:
<email subject>

Email:
<complete email text>

- Address the recipient naturally by name.
- Mention their company ({lead.company}) naturally in the email.
- Highlight specific benefits relevant to {lead.industry}.
- Do NOT use markdown formatting (* or #). Return plain text only.
- Do NOT include any explanations, notes, or meta text.
- The email must end with:

Best regards,
{self.sender_name}
"""

    def generate_outreach(self, lead: Lead) -> tuple[str | None, str | None]:
        """
        Generate subject and email using Google Gemini AI.
        """
        print(f"Generating outreach for {lead.company} ({lead.industry})")

        prompt = self.choose_prompt(lead)

        response = self.gemini.generate(prompt)

        if response == "QUOTA_EXCEEDED":
            return "QUOTA_EXCEEDED", "QUOTA_EXCEEDED"

        if response == "GENERATION_FAILED":
            return "GENERATION_FAILED", "GENERATION_FAILED"

        if not response:
            log_error("Outreach generation failed.")
            return None, None

        # Parse Subject and Email Body
        try:
            subject = (
                response.split("Email:")[0]
                .replace("Subject:", "")
                .strip()
            )
            email = response.split("Email:")[1].strip()
            return subject, email

        except Exception as e:
            log_error(f"Response parsing failed: {e}")
            return None, None

    def save_email(self, subject: str, email: str, lead: Lead) -> None:
        """
        Save or update generated email in history.
        """
        email_data = {
            "company": self.company,
            "sender": self.sender_name,
            "recipient_name": lead.name,
            "recipient_company": lead.company,
            "recipient_email": lead.email,
            "recipient_phone": getattr(lead, "phone", ""),
            "recipient_position": lead.position,
            "industry": lead.industry,
            "tone": self.tone,
            "email_length": self.email_length,
            "subject": subject,
            "email": email,
            "date": datetime.now().strftime("%d %B %Y"),
        }

        try:
            try:
                with open("data/sent_emails.json", "r") as file:
                    emails = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                emails = []

            updated = False
            for i, existing in enumerate(emails):
                if existing.get("recipient_email") == lead.email:
                    emails[i] = email_data
                    updated = True
                    break

            if not updated:
                emails.append(email_data)

            with open("data/sent_emails.json", "w") as file:
                json.dump(emails, file, indent=4)

            print("Email history updated successfully.")

        except Exception as e:
            log_error(f"Save Error: {e}")

    def load_email(self) -> list | None:
        """
        Load all previously saved emails.
        """
        return load_email_history()
