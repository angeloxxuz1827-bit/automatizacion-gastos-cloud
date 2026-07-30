import requests

from config.settings import TELEGRAM_TOKEN, TELEGRAM_API_URL


class TelegramClient:

    def __init__(self):
    
        self.base_url = f"{TELEGRAM_API_URL}/bot{TELEGRAM_TOKEN}"

    def get_updates(self, offset: int | None = None) -> dict:


        params = {
            "timeout": 30
        }

        if offset is not None:
            params["offset"] = offset

        response = requests.get(
            f"{self.base_url}/getUpdates",
            params=params,
            timeout=30 + 5
        )

        response.raise_for_status()

        return response.json()


    def send_message(self, chat_id: int, text: str) -> dict:
        payload = {
            "chat_id": chat_id,
            "text": text
        }

        response = requests.post(
            url = f"{self.base_url}/sendMessage",
            json=payload,
            timeout=30 + 5
        )

        response.raise_for_status()

        return response.json()
    

    def get_updates_update_id(self, update_id: int) -> dict:
        params = {
            "timeout": 30,
            "offset": update_id + 1
        }

        response = requests.get(
            f"{self.base_url}/getUpdates",
            params=params,
    
        )

        response.raise_for_status()

        return response.json()