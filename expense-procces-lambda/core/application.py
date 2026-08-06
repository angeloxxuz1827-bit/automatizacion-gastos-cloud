import json
from datetime import datetime
from zoneinfo import ZoneInfo


from llm.llm_service import LLM


class Aplication:
    """
    Main application service responsible for orchestrating the
    Telegram and LLM workflows.

    This class prepares Telegram messages for the language model,
    invokes the LLM service, and formats responses returned to users.
    """

    def __init__(self):
        """
        Initializes the application services.
        """

        

        # Service responsible for interacting with the LLM.
        self.llm_service = LLM()

    def llm_run(self, response: dict) -> dict:
        """
        Processes a Telegram message and sends it to the language model.

        The Telegram payload is transformed into a structured prompt
        before being submitted to the LLM.

        Args:
            response: Telegram update received by the application.

        Returns:
            A dictionary containing the response returned by the LLM.
        """

        # Extract Telegram identifiers and message content.
        chat_id = response["message"]["chat"]["id"]
        message_id = response["message"]["message_id"]
        text = response["message"]["text"]

        # Convert the Telegram Unix timestamp to a formatted date.
        timestamp = response["message"]["date"]

        date = datetime.fromtimestamp(
            timestamp,
            tz=ZoneInfo("America/Bogota")
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Build the structured payload sent to the language model.
        input_data = {
            "ChatId": chat_id,
            "MessageId": message_id,
            "Fecha": date,
            "Mensaje": text
        }

        # Serialize the payload as JSON.
        user_prompt = json.dumps(
            input_data,
            ensure_ascii=False,
            indent=2
        )

        # Invoke the language model.
        response_llm = self.llm_service.call_service(user_prompt)

        # Return the raw LLM response.
        return response_llm

    def build_expense_message(self, expense: dict) -> str:
        """
        Builds a user-friendly confirmation message from the
        structured expense information.

        Args:
            expense: Dictionary containing the expense extracted by the LLM.

        Returns:
            A formatted message ready to be sent through Telegram.
        """

        # Build and return the confirmation message.
        return f"""✅ Gasto registrado

📂 Categoría: {expense.get("Categoria", "No especificada")}
🛒 Producto: {expense.get("Producto", "No especificado")}
📦 Cantidad: {expense.get("Cantidad", "-")} {expense.get("Unidad", "")}
💰 Valor: {expense.get("Valor") or "No especificado"}
📍 Lugar: {expense.get("Lugar", "No especificado")}
💳 Método de pago: {expense.get("MetodoPago", "No especificado")}
"""