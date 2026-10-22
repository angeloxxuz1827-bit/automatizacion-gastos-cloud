import requests

from config.settings import TELEGRAM_TOKEN, TELEGRAM_API_URL


class TelegramAPIError(RuntimeError):
    """Error de Telegram con mensaje sanitizado: nunca incluye URL ni token."""


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

    @staticmethod
    def _redact(value: str) -> str:
        """Elimina el token si Telegram llegara a devolverlo en un mensaje."""
        if TELEGRAM_TOKEN:
            return value.replace(TELEGRAM_TOKEN, "[redacted]")
        return value

    def _request(self, method: str, action: str, **kwargs) -> dict:
        """
        Ejecuta una petición HTTP y devuelve el JSON de respuesta.

        Los errores se convierten en `TelegramAPIError` con un mensaje seguro:
        no incluyen la URL, el token ni el traceback original de `requests`.
        """

        try:
            response = requests.request(
                method,
                f"{self.base_url}/{action}",
                timeout=35,
                **kwargs
            )
        except requests.RequestException as exc:
            # str(exc) puede incluir la URL con el token; solo el tipo es seguro.
            raise TelegramAPIError(
                f"Telegram {action} falló ({type(exc).__name__})"
            ) from None

        if response.status_code >= 400:
            description = ""
            try:
                payload = response.json()
                if isinstance(payload, dict):
                    description = str(payload.get("description") or "")
            except ValueError:
                pass

            detail = f"HTTP {response.status_code}"
            if description:
                detail = f"{detail}: {self._redact(description)}"

            raise TelegramAPIError(
                f"Telegram {action} falló ({detail})"
            ) from None

        try:
            return response.json()
        except ValueError:
            raise TelegramAPIError(
                f"Telegram {action} devolvió una respuesta no JSON"
            ) from None

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

        return self._request("GET", "getUpdates", params=params)

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

        return self._request("POST", "sendMessage", json=payload)

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

        return self._request("GET", "getUpdates", params=params)
