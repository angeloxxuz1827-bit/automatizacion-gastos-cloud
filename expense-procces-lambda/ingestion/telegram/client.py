import requests

from config.settings import TELEGRAM_TOKEN, TELEGRAM_API_URL


class TelegramClient:
    """
    Client responsible for interacting with the Telegram Bot API.

    This class provides methods to receive updates from Telegram
    and send messages to users.
    """

    def __init__(self):
        """
        Initializes the Telegram Bot API client.
        """

        # Base URL used for all Telegram Bot API requests.
        self.base_url = f"{TELEGRAM_API_URL}/bot{TELEGRAM_TOKEN}"

    def get_updates(self, offset: int | None = None) -> dict:
        """
        Retrieves pending updates from the Telegram Bot API.

        Args:
            offset: Identifier of the first update to retrieve.
                If provided, updates with a lower identifier are ignored.

        Returns:
            A dictionary containing the updates returned by Telegram.
        """

        # Request parameters.
        params = {
            "timeout": 30
        }

        # Include the offset when provided.
        if offset is not None:
            params["offset"] = offset

        # Send the request to Telegram.
        response = requests.get(
            f"{self.base_url}/getUpdates",
            params=params,
            timeout=35
        )

        # Raise an exception if the request failed.
        response.raise_for_status()

        # Return the response as a Python dictionary.
        return response.json()

    def send_message(self, chat_id: int, text: str) -> dict:
        """
        Sends a text message to a Telegram chat.

        Args:
            chat_id: Unique identifier of the destination chat.
            text: Message text to send.

        Returns:
            A dictionary containing the Telegram API response.
        """

        # Request payload.
        payload = {
            "chat_id": chat_id,
            "text": text
        }

        # Send the message.
        response = requests.post(
            url=f"{self.base_url}/sendMessage",
            json=payload,
            timeout=35
        )

        # Raise an exception if the request failed.
        response.raise_for_status()

        # Return the response as a Python dictionary.
        return response.json()

    def get_updates_update_id(self, update_id: int) -> dict:
        """
        Retrieves updates received after a specific update identifier.

        Args:
            update_id: Last processed Telegram update identifier.

        Returns:
            A dictionary containing the updates returned by Telegram.
        """

        # Request parameters.
        params = {
            "timeout": 30,
            "offset": update_id + 1
        }

        # Send the request to Telegram.
        response = requests.get(
            f"{self.base_url}/getUpdates",
            params=params,
        )

        # Raise an exception if the request failed.
        response.raise_for_status()

        # Return the response as a Python dictionary.
        return response.json()