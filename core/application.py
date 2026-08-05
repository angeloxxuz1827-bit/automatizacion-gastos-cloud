import json
from pydoc import text
from urllib import response

from datetime import datetime
from zoneinfo import ZoneInfo

from ingestion.telegram.service import TelegramService
from llm.llm_service import LLM







class Aplication:
    def __init__(self):
        self.telegram_service = TelegramService()
        self.llm_service = LLM()

    def run(self,response:dict):

        #Descomponer la respuesta de Telegram para obtener el chat_id y el texto del mensaje

        chat_id = response["message"]["chat"]["id"]
        text = response['message']['text']

        
        timestamp = response["message"]["date"]

        date = datetime.fromtimestamp(
            timestamp,
            tz=ZoneInfo("America/Bogota")
        ).strftime("%Y-%m-%d %H:%M:%S")

        #Construir el prompt para enviar a la API de GroqCloud
        system_prompt =f"Fecha: {date} \n Mensaje: {text}"
        print (f"response: {json.dumps(response, indent=4, ensure_ascii=False)}")
        print (f"System Prompt: {system_prompt}")
        
        responseLLM = self.llm_service.call_service(system_prompt)

        #responseLLM = self.groq.call_llm(llm_input)

        print(f"Response LLM: {json.dumps(responseLLM, indent=4, ensure_ascii=False)}")

        text =responseLLM["choices"][0]["message"]["content"]
        
        text_json = json.loads(text)
        estado = text_json.get("Estado")
        print (f"Estado: {estado}")

        

        self.telegram_service.send_message(chat_id, text)


        #self.telegram_service.get_updates_update_id(update_id)

    


