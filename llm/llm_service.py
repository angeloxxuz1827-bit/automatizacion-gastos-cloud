



from llm.client import GroqCloudClient

from llm.models import LLAMA_70B

from llm.request_builder import build_request_body

from llm.prompts.extract_prompts import system_prompt_structure_data

from llm.response_parser import get_json



class LLM:
    def __init__(self):
        self.groq_client = GroqCloudClient()



    def call_service(self, user_prompt):
        # Construir el cuerpo de la solicitud para enviar a la API de GroqCloud
        groq_request_body = build_request_body(
            system_prompt=system_prompt_structure_data,
            user_prompt=user_prompt,
            model=LLAMA_70B,
            temperature=0.3
        )

        # Llamar a la API de GroqCloud
        response = self.groq_client.groq_services(groq_request_body)

        return response