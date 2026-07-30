from ingestion.telegram.client import TelegramClient



class TelegramService:


    def __init__(self):
        self.client = TelegramClient()
       

    def get_updates(self, offset=None):

        return self.client.get_updates(offset)
    
    def send_message(self, chat_id: int, text: str):

        return self.client.send_message(chat_id, text)
    
    def get_updates_update_id(self, update_id):

        return self.client.get_updates_update_id(update_id)

