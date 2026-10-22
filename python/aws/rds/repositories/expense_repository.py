from mysql.connector import MySQLConnection


class ExpenseRepository:
    """
    Repository responsible for managing expense persistence operations.

    This class provides methods to interact with the `gastos` table,
    including inserting expense records.
    """

    def __init__(self, connection: MySQLConnection):
        """
        Initializes the repository with an active database connection.

        Args:
            connection: Active MySQL database connection.
        """

        # Database connection used to execute SQL operations.
        self.connection = connection

    def save(self, expense) -> None:
        """
        Inserts a new expense into the database.

        Args:
            expense: Expense entity containing the information to be stored.
        """

        # Create a new cursor for the database operation.
        cursor = self.connection.cursor()

        try:
            # Insert the expense into the database.
            cursor.execute(
                """
                INSERT INTO gastos (
                    mensaje_id,
                    categoria,
                    subcategoria,
                    producto,
                    cantidad,
                    unidad,
                    lugar,
                    metodo_pago,
                    valor,
                    moneda,
                    fecha_gasto
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    expense.mensaje_id,
                    expense.categoria,
                    expense.subcategoria,
                    expense.producto,
                    expense.cantidad,
                    expense.unidad,
                    expense.lugar,
                    expense.metodo_pago,
                    expense.valor,
                    expense.moneda,
                    expense.fecha_gasto
                )
            )

        finally:
            # Ensure the cursor is always closed.
            cursor.close()