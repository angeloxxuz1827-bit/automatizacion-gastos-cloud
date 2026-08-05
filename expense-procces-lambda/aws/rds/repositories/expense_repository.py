from mysql.connector import MySQLConnection


class ExpenseRepository:
    """
    Repository responsible for managing expense persistence operations.

    This class provides methods to interact with the `gastos` table,
    including creating, updating, retrieving, and deleting expense records.
    """

    def __init__(self, connection: MySQLConnection):
        """
        Initializes the repository with an active database connection.

        Args:
            connection: Active MySQL database connection.
        """

        # Database connection used to execute SQL operations.
        self.connection = connection