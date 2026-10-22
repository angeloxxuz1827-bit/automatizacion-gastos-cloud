from mysql.connector import MySQLConnection


class MessageRepository:
    """
    Repository responsible for managing message persistence operations.

    This class provides methods to interact with the `mensajes` table,
    including inserting and retrieving message records.
    """

    def __init__(self, connection: MySQLConnection):
        """
        Initializes the repository with an active database connection.

        Args:
            connection: Active MySQL database connection.
        """

        # Database connection used to execute SQL operations.
        self.connection = connection

    def save(self, message) -> int:
        """
        Inserts a new message into the database.

        Args:
            message: Message entity containing the information to be stored.

        Returns:
            The auto-generated primary key (`id`) assigned to the inserted
            message record.
        """

        # Create a new cursor for the database operation.
        cursor = self.connection.cursor()

        try:
            # Insert the message into the database.
            cursor.execute(
                """
                INSERT INTO mensajes (
                    chat_id,
                    message_id,
                    tipo,
                    mensaje_original,
                    estado,
                    s3_key_processed,
                    fecha_mensaje
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    message.chat_id,
                    message.message_id,
                    message.tipo,
                    message.mensaje_original,
                    message.estado,
                    message.s3_key_processed,
                    message.fecha_mensaje
                )
            )

            # Return the auto-generated primary key assigned by MySQL.
            return cursor.lastrowid

        finally:
            # Ensure the cursor is always closed.
            cursor.close()