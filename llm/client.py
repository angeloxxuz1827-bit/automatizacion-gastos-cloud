import requests

from config.settings import GROQ_API_KEY, GROQ_API_URL

class GroqCloudClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.base_url = GROQ_API_URL

        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

    def groq_services(self, body: dict):

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=body,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
