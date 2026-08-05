from llm.client import GroqCloudClient
from llm.models import LLAMA_70B
from llm.request_builder import build_request_body
from llm.prompts.extract_prompts import system_prompt_structure_data
from llm.response_parser import get_json


class LLM:
    """
    Service responsible for interacting with the configured
    Large Language Model (LLM).

    This class builds the request payload, invokes the Groq Cloud API,
    and returns the model response.
    """

    def __init__(self):
        """
        Initializes the LLM service.
        """

        # Initialize the Groq Cloud client.
        self.groq_client = GroqCloudClient()

    def call_service(self, user_prompt: str) -> dict:
        """
        Sends a user prompt to the configured language model.

        Args:
            user_prompt: User input to be processed by the LLM.

        Returns:
            A dictionary containing the response returned by the Groq API.
        """

        # Build the request payload using the configured prompt template
        # and model parameters.
        groq_request_body = build_request_body(
            system_prompt=system_prompt_structure_data,
            user_prompt=user_prompt,
            model=LLAMA_70B,
            temperature=0.3
        )

        # Send the request to the Groq Cloud API.
        response = self.groq_client.groq_services(groq_request_body)

        # Return the raw response from the language model.
        return response