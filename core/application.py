from ingestion.telegram.service import TelegramService

class Aplication:
    def __init__(self):
        self.telegram_service = TelegramService()

    def run(self,response:dict):

        chat_id = response["message"]["chat"]["id"]
        text = "Enviando mensaje desde algun lugar"

        self.telegram_service.send_message(chat_id, text)

