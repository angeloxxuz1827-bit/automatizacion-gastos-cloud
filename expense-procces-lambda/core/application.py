import json

from datetime import datetime
from zoneinfo import ZoneInfo


from llm.llm_service import LLM


class Aplication:
    """
    Servicio principal que orquesta el flujo de Telegram y el LLM.

    Prepara el mensaje para el modelo, invoca la extracción de datos y
    construye la respuesta que se envía al usuario.
    """

    def __init__(self):
        """
        Inicializa los servicios de la aplicación.
        """

        # Servicio responsable de interactuar con el LLM.
        self.llm_service = LLM()

    def llm_run(self, response: dict) -> dict:
        """
        Procesa un mensaje de Telegram y lo envía al modelo.

        Args:
            response: Update de Telegram recibido por la aplicación.

        Returns:
            Diccionario con la respuesta cruda del LLM.
        """

        # Extraer identificadores y contenido del mensaje.
        chat_id = response["message"]["chat"]["id"]
        message_id = response["message"]["message_id"]
        text = response["message"]["text"]

        # Convertir la fecha Unix de Telegram a hora local de Bogotá.
        timestamp = response["message"]["date"]
        date = datetime.fromtimestamp(
            timestamp,
            tz=ZoneInfo("America/Bogota")
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Construir el payload estructurado para el modelo.
        input_data = {
            "ChatId": chat_id,
            "MessageId": message_id,
            "Fecha": date,
            "Mensaje": text
        }

        # Serializar el payload como JSON.
        user_prompt = json.dumps(
            input_data,
            ensure_ascii=False,
            indent=2
        )

        # Invocar el modelo.
        response_llm = self.llm_service.call_service(user_prompt)

        # Los IDs y la fecha son datos conocidos por Telegram. Se sobrescriben
        # en la respuesta para que el contrato con store no dependa del LLM.
        content_response_llm = json.loads(
            response_llm["choices"][0]["message"]["content"]
        )
        content_response_llm["ChatId"] = chat_id
        content_response_llm["MessageId"] = message_id
        content_response_llm["Fecha"] = date

        response_llm["choices"][0]["message"]["content"] = json.dumps(
            content_response_llm,
            ensure_ascii=False
        )

        return response_llm

    def build_expense_message(self, expense: dict) -> str:
        """
        Construye la confirmación que se envía por Telegram.

        Args:
            expense: Datos del gasto extraídos por el LLM.

        Returns:
            Mensaje listo para enviar al usuario.
        """

        cantidad = expense.get("Cantidad")
        if isinstance(cantidad, (int, float)):
            cantidad = f"{cantidad:g}"
        else:
            cantidad = cantidad or "-"

        unidad = expense.get("Unidad") or ""
        unidad = f" {unidad}".rstrip()

        categoria = expense.get("Categoria") or "No especificada"
        producto = expense.get("Producto") or "No especificado"
        valor = expense.get("Valor")
        valor = valor if valor is not None else "No especificado"
        lugar = expense.get("Lugar") or "No especificado"
        metodo_pago = expense.get("MetodoPago") or "No especificado"

        return f"""✅ Gasto registrado

📂 Categoría: {categoria}
🛒 Producto: {producto}
📦 Cantidad: {cantidad}{unidad}
💰 Valor: {valor}
📍 Lugar: {lugar}
💳 Método de pago: {metodo_pago}
"""
