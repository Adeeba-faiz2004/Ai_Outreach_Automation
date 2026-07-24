import requests

from config import OPENROUTER_API_KEY


class OpenRouterService:

    def generate_email(self, prompt):

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI Outreach Agent",
        }

        payload = {
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]
        print(payload)