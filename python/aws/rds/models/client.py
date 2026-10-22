from datetime import datetime


class Client:
    """
    Represents a Telegram user interacting with the application.

    Attributes:
        chat_id: Unique Telegram chat identifier.
        nombre: User's display name.
        username: Telegram username.
        fecha_registro: Date and time when the user was registered.
    """

    def __init__(
        self,
        chat_id: int,
        nombre: str | None = None,
        username: str | None = None,
        fecha_registro: datetime | None = None,
    ):
        self.chat_id = chat_id
        self.nombre = nombre
        self.username = username
        self.fecha_registro = fecha_registro