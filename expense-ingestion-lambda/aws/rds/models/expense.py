class Expense:
    """
    Represents an expense record extracted from a user message.

    Attributes:
        id: Unique identifier of the expense record.
        mensaje_id: Identifier of the Telegram message associated with the expense.
        categoria: Main expense category.
        subcategoria: Expense subcategory.
        producto: Name or description of the purchased product or service.
        cantidad: Quantity of the product or service.
        unidad: Unit of measurement associated with the quantity.
        lugar: Location where the expense occurred.
        metodo_pago: Payment method used for the expense.
        valor: Monetary value of the expense.
        moneda: Currency in which the expense was recorded.
        fecha_gasto: Date and time when the expense occurred.
        fecha_registro: Date and time when the expense was stored in the system.
    """

    def __init__(
        self,
        mensaje_id: int,
        categoria: str,
        subcategoria: str,
        producto: str,
        cantidad: float,
        unidad: str,
        lugar: str,
        metodo_pago: str,
        valor: float,
        moneda: str,
        fecha_gasto,
        id: int = None,
        fecha_registro=None
    ):
        # Unique identifier of the expense record.
        self.id = id

        # Identifier of the Telegram message associated with the expense.
        self.mensaje_id = mensaje_id

        # Expense classification.
        self.categoria = categoria
        self.subcategoria = subcategoria

        # Purchased product or service.
        self.producto = producto

        # Quantity and measurement unit.
        self.cantidad = cantidad
        self.unidad = unidad

        # Location and payment information.
        self.lugar = lugar
        self.metodo_pago = metodo_pago

        # Monetary information.
        self.valor = valor
        self.moneda = moneda

        # Expense date and registration timestamp.
        self.fecha_gasto = fecha_gasto
        self.fecha_registro = fecha_registro