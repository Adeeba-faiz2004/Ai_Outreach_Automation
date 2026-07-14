from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiService:

    def __init__(self):

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(self, prompt: str) -> str | None:
        """
        Generate content using Gemini AI.
        """

        print("Inside Gemini Service...")

        try:

            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            print("Gemini Response Received.")

            return response.text

        except Exception as e:

            print(f"Gemini Error: {e}")

            return None
