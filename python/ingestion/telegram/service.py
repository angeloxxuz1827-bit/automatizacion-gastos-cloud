from ingestion.telegram.client import TelegramClient


class TelegramService:
    """
    Service layer responsible for handling Telegram operations.

    This class acts as an intermediary between the application
    and the Telegram client, delegating requests to the Telegram Bot API.
    """

    def __init__(self):
        """
        Initializes the Telegram service.
        """

        # Initialize the Telegram API client.
        self.client = TelegramClient()

    def get_updates(self, offset=None):
        """
        Retrieves pending updates from Telegram.

        Args:
            offset: Identifier of the first update to retrieve.

        Returns:
            A dictionary containing the updates returned by Telegram.
        """

        # Delegate the request to the Telegram client.
        return self.client.get_updates(offset)

    def send_message(self, chat_id: int, text: str):
        """
        Sends a text message to a Telegram chat.

        Args:
            chat_id: Unique identifier of the destination chat.
            text: Message text to send.

        Returns:
            A dictionary containing the Telegram API response.
        """

        # Delegate the request to the Telegram client.
        return self.client.send_message(chat_id, text)

    def get_updates_update_id(self, update_id):
        """
        Retrieves updates received after a specific update identifier.

        Args:
            update_id: Last processed Telegram update identifier.

        Returns:
            A dictionary containing the updates returned by Telegram.
        """

        # Delegate the request to the Telegram client.
        return self.client.get_updates_update_id(update_id)