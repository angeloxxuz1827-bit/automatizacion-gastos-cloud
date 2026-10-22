import requests

from config.settings import GROQ_API_KEY, GROQ_API_URL


class GroqCloudClient:
    """
    Client responsible for interacting with the Groq Cloud API.

    This class provides methods to send requests to Groq-hosted
    language models and retrieve their responses.
    """

    def __init__(self):
        """
        Initializes the Groq Cloud client.
        """

        # API authentication credentials.
        self.api_key = GROQ_API_KEY

        # Base URL of the Groq API endpoint.
        self.base_url = GROQ_API_URL

        # Default HTTP headers used for all requests.
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def groq_services(self, body: dict) -> dict:
        """
        Sends a request to the Groq API.

        Args:
            body: Request payload containing the model configuration
                and conversation messages.

        Returns:
            A dictionary containing the response returned by the Groq API.
        """

        # Send the request to the Groq API.
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=body,
            timeout=30
        )

        # Raise an exception if the request failed.
        response.raise_for_status()

        # Return the response as a Python dictionary.
        return response.json()