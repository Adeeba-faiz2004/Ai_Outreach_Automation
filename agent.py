from datetime import datetime


import json
from prompts import (
    SOFTWARE_PROMPT,
    HEALTHCARE_PROMPT,
    GENERAL_PROMPT,
    
)
from gemini_service import GeminiService
from logs.log import log_error
from models.lead import Lead


PROMPTS = {
    "Software": SOFTWARE_PROMPT,
    "Healthcare": HEALTHCARE_PROMPT,
}
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
       
    # -------------------------------------

    
    def choose_prompt(self, lead:Lead) -> str:
        """
      Select and personalize the prompt
      based on the given industry.
      """
        base_prompt = PROMPTS.get(lead.industry, GENERAL_PROMPT)

        return f"""
     You are an expert sales copywriter.

     Your task is to write ONLY ONE personalized cold outreach email.

     Company Name: {self.company}
     Sender Name: {self.sender_name}
     Recipient Name: {lead.name}

     Recipient Company: {lead.company}

     Recipient Position: {lead.position}
     Industry: {lead.industry}
     Writing Tone:{self.tone}
     Email Length:{self.email_length}

     Requirements:
     - Generate only ONE email.
     - Do NOT generate multiple versions.
     - Do NOT include explanations, notes, or headings.
       IMPORTANT:

     -IMPORTANT:

     -Return your response in this exact format:

      Subject:
      <email subject>

      Email:
      <complete email>

     -Do not include explanations.
     - Do not use markdown.
     - Return only the subject and email.

    -The email must start directly with the greeting.
     - Address the recipient by name.

     - Mention the recipient company naturally.

     - Write as if the email is specifically written for this person.
     - If recipient name is unknown, use "Dear Sir/Madam,".
     - Never use placeholders like [Recipient Name] or [Company Name].
     - Mention the company name naturally.
     - Keep the email between 120–180 words.
    
     - Do not use markdown formatting.
        Return plain text only.
     -  Write the email using the requested tone.
     - Keep the email according to the requested length.
     - End the email with:

     Best regards,
     {self.sender_name}

     Base Instructions:
     {base_prompt}

     Return ONLY the final email.
     
    -Generate a DIFFERENT version from any previous email.
    -Use different wording, opening, CTA, and sentence structure.
    -Do not repeat the previous email.
     """
    
    # ------------------------------------------------
    def generate_outreach(self, lead: Lead) -> tuple[str | None, str | None]:
        """
        Generate subject and email using Google Gemini AI.
        """

        print(f"Generating outreach for {lead.company}")

        prompt = self.choose_prompt(lead)

        # -----------------------------
        # GENERATE USING GEMINI
        # -----------------------------
        response = self.gemini.generate(prompt)

        if response == "QUOTA_EXCEEDED":
            return "QUOTA_EXCEEDED", "QUOTA_EXCEEDED"

        if response == "GENERATION_FAILED":
            return "GENERATION_FAILED", "GENERATION_FAILED"

        if not response:
            log_error("Outreach generation failed.")
            return None, None

    # -----------------------------
    # PARSE RESPONSE
    # -----------------------------
        try:

            subject = (
                response.split("Email:")[0]
                .replace("Subject:", "")
                .strip()
        )

            email = response.split("Email:")[1].strip()

            return subject, email

        except Exception:

            log_error("Response parsing failed.")

            return None, None
    #--------------------------------------------------
    def save_email(self, subject: str, email: str, lead: Lead) -> None:
        """
        Save the generated subject and email to a JSON file.
        """

        email_data = {
        "company": self.company,
        "sender": self.sender_name,

        "recipient_name": lead.name,
        "recipient_company": lead.company,
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

            emails.append(email_data)

            with open("data/sent_emails.json", "w") as file:
                json.dump(emails, file, indent=4)

            print("Email saved successfully")

        except Exception as e:
            log_error(f"Save Error: {e}")
        

    # -------------------------------------

    def load_email(self) -> list | None:
        """
    Load all previously saved emails.
        """
        try:

            with open("data/sent_emails.json", "r") as file:

                 return json.load(file)
        except Exception as e:
             log_error(f"Load Error: {e}")

             return None
        