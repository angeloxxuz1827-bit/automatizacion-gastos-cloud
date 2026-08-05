import os
import mysql.connector


class DatabaseConnection:
    """
    Factory class responsible for creating MySQL database connections.

    Connection parameters are loaded from environment variables,
    allowing the application to connect to different environments
    (e.g., local development, testing, or Amazon RDS).
    """

    @staticmethod
    def get_connection():
        """
        Creates and returns a new MySQL database connection.

        Environment Variables:
            DB_HOST: Database host.
            DB_PORT: Database port (defaults to 3306 if not provided).
            DB_NAME: Database name.
            DB_USER: Database username.
            DB_PASSWORD: Database password.

        Returns:
            mysql.connector.MySQLConnection: Active MySQL database connection.
        """

        # Create a new connection using the configured environment variables.
        connection = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            port=int(os.environ.get("DB_PORT", 3306)),
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            autocommit=False
        )

        # Return the active database connection.
        return connection