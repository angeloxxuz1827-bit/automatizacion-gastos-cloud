class Message:
    """
    Represents a message received from a user and its processing status.

    Attributes:
        id: Unique identifier of the message record.
        chat_id: Identifier of the Telegram chat.
        message_id: Identifier of the Telegram message.
        tipo: Type of the received message (e.g., text, image, audio).
        mensaje_original: Original content of the message.
        fecha_mensaje: Date and time when the message was sent.
        s3_key_processed: S3 object key of the processed message.
        estado: Current processing status of the message.
        fecha_registro: Date and time when the message was stored in the system.
    """

    def __init__(
        self,
        chat_id: int,
        message_id: int,
        tipo: str,
        mensaje_original: str,
        fecha_mensaje,
        s3_key_processed: str = None,
        estado: str = "PENDIENTE",
        id: int = None,
        fecha_registro=None
    ):
        # Unique identifier of the message record.
        self.id = id

        # Telegram identifiers.
        self.chat_id = chat_id
        self.message_id = message_id

        # Message metadata.
        self.tipo = tipo
        self.mensaje_original = mensaje_original

        # Current processing status.
        self.estado = estado

        # S3 object key where the processed message is stored.
        self.s3_key_processed = s3_key_processed

        # Message and registration timestamps.
        self.fecha_mensaje = fecha_mensaje
        self.fecha_registro = fecha_registro