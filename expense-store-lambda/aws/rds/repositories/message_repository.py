from mysql.connector import MySQLConnection


class MessageRepository:
    """
    Repository responsible for managing message persistence operations.

    This class provides methods to interact with the `mensajes` table,
    including creating, updating, retrieving, and deleting message records.
    """

    def __init__(self, connection: MySQLConnection):
        """
        Initializes the repository with an active database connection.

        Args:
            connection: Active MySQL database connection.
        """

        # Database connection used to execute SQL operations.
        self.connection = connection