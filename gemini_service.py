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
            print("Response:", response.text)
            return response.text

        except Exception as e:

            import traceback

            print("=" * 50)
            print("GEMINI ERROR")
            print(e)
            traceback.print_exc()
            print("=" * 50)
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                return "QUOTA_EXCEEDED"

            return "GENERATION_FAILED"