from mysql.connector import MySQLConnection


class ClientRepository:
    """
    Repository responsible for managing client persistence operations.

    This class provides methods to interact with the `clientes` table,
    including checking if a client exists and registering new clients.
    """

    def __init__(self, connection: MySQLConnection):
        """
        Initializes the repository with an active database connection.

        Args:
            connection: Active MySQL database connection.
        """

        # Database connection used to execute SQL operations.
        self.connection = connection

    def exists(self, chat_id: int) -> bool:
        """
        Checks whether a client already exists in the database.

        Args:
            chat_id: Unique Telegram chat identifier.

        Returns:
            True if the client exists; otherwise, False.
        """

        # Create a new cursor for the database operation.
        cursor = self.connection.cursor()

        try:
            # Search for the client using the Telegram chat ID.
            cursor.execute(
                """
                SELECT 1
                FROM clientes
                WHERE chat_id = %s
                LIMIT 1
                """,
                (chat_id,)
            )

            # Returns True if at least one record is found.
            return cursor.fetchone() is not None

        finally:
            # Ensure the cursor is always closed.
            cursor.close()

    def save(self, client):
        """
        Inserts a new client into the database.

        Args:
            client: Client entity containing the information to be stored.
        """

        # Create a new cursor for the database operation.
        cursor = self.connection.cursor()

        try:
            # Insert the client into the database.
            cursor.execute(
                """
                INSERT INTO clientes (
                    chat_id,
                    nombre,
                    username
                )
                VALUES (%s, %s, %s)
                """,
                (
                    client.chat_id,
                    client.nombre,
                    client.username
                )
            )

        finally:
            # Ensure the cursor is always closed.
            cursor.close()