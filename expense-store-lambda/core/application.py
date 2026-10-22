import re

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


# Zona horaria usada por el bot para interpretar las fechas del LLM.
BOGOTA = ZoneInfo("America/Bogota")


def _clean_text(value):
    """
    Normaliza un valor de texto opcional.
    """

    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _build_name(sender: dict) -> str:
    """
    Construye el nombre visible del usuario de Telegram.
    """

    first_name = _clean_text(sender.get("first_name"))
    last_name = _clean_text(sender.get("last_name"))

    parts = [part for part in (first_name, last_name) if part]
    if parts:
        return " ".join(parts)

    return _clean_text(sender.get("username")) or "Usuario"


def _parse_cantidad(value):
    """
    Convierte la cantidad del LLM en número y unidad separada.

    El prompt devuelve un número y `Unidad` por separado, pero se acepta texto
    como "2 kilos" por si el modelo responde con el formato anterior.
    """

    if value is None or isinstance(value, bool):
        return None, None

    if isinstance(value, (int, float)):
        return float(value), None

    text = str(value).strip()
    if not text:
        return None, None

    lower = text.lower()

    # Expresiones cualitativas frecuentes en español.
    if lower.startswith("media "):
        return 0.5, _clean_text(text[6:])

    if lower in {"un", "una", "uno"}:
        return 1.0, None

    # Formato "2 kilos", "3 botellas", "2,5 libras".
    match = re.match(r"^\s*(\d+(?:[.,]\d+)?)\s*(.*)$", text)
    if not match:
        return None, _clean_text(text)

    number = float(match.group(1).replace(",", "."))
    unit = _clean_text(match.group(2))
    return number, unit


def _parse_valor(value):
    """
    Convierte el valor monetario del LLM en un número.
    """

    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    lower = text.lower()

    # Interpretar expresiones como "15k", "15 mil" o "3 millones".
    multiplier = 1.0
    if "millon" in lower:
        multiplier = 1_000_000.0
    elif re.search(r"\d\s*(k|mil|lucas?|lukas?)\b", lower):
        multiplier = 1_000.0

    # Quitar símbolos de moneda, espacios y letras.
    text = re.sub(r"[^\d,.-]", "", text)
    if not text or text in {"-", ".", ","}:
        return None

    # Normalizar separadores decimales y de miles.
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(".", "").replace(",", ".")
    elif text.count(".") > 1:
        text = text.replace(".", "")
    elif "." in text:
        integer, decimal = text.rsplit(".", 1)
        if len(decimal) == 3 and integer.isdigit():
            text = integer + decimal

    try:
        return float(text) * multiplier
    except ValueError:
        return None


def _parse_fecha(value):
    """
    Convierte una fecha del LLM a ISO 8601 con zona horaria.

    Acepta el formato ISO que envía process y el formato `dd/mm/yyyy` de
    versiones anteriores. Si no trae zona horaria, asume America/Bogota.
    """

    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    parsed = None

    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        for date_format in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y"):
            try:
                parsed = datetime.strptime(text, date_format)
                break
            except ValueError:
                continue

    if parsed is None:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=BOGOTA)

    return parsed.isoformat()


def _message_date(message: dict):
    """
    Convierte la fecha Unix de Telegram a ISO 8601 en UTC.
    """

    timestamp = message.get("date")
    if timestamp is None:
        return None

    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


class Application:
    """
    Orquesta la persistencia de cliente, mensaje y gasto en Supabase.
    """

    def __init__(self, supabase_client):
        """
        Inicializa el servicio con el cliente REST de Supabase.
        """

        self.supabase_client = supabase_client

    def save_expense(
        self,
        raw_update: dict,
        content: dict,
        s3_key_processed: str
    ) -> dict:
        """
        Construye el payload y ejecuta la transacción en Supabase.

        Args:
            raw_update: Update original de Telegram almacenado en S3.
            content: JSON estructurado devuelto por el LLM.
            s3_key_processed: Key del objeto `processed/...` en S3.

        Returns:
            Diccionario con los IDs de mensaje y gasto.
        """

        message = raw_update.get("message") or {}
        sender = message.get("from") or {}
        chat = message.get("chat") or {}

        # Los IDs se toman del update original; el LLM solo es respaldo.
        chat_id = chat.get("id")
        if chat_id is None:
            chat_id = content.get("ChatId")

        message_id = message.get("message_id")
        if message_id is None:
            message_id = content.get("MessageId")

        if chat_id is None or message_id is None:
            raise ValueError(
                "El update no contiene chat_id o message_id."
            )

        message_date = _message_date(message)
        fecha_gasto = _parse_fecha(content.get("Fecha")) or message_date

        cantidad, unidad_cantidad = _parse_cantidad(content.get("Cantidad"))
        unidad = _clean_text(content.get("Unidad")) or unidad_cantidad

        payload = {
            "p_chat_id": chat_id,
            "p_message_id": message_id,
            "p_name": _build_name(sender),
            "p_username": _clean_text(sender.get("username")),
            "p_tipo": "texto",
            "p_original_message": message.get("text") or "",
            "p_state": _clean_text(content.get("Estado")) or "PENDIENTE",
            "p_s3_key_processed": s3_key_processed,
            "p_message_date": message_date,
            "p_categoria": _clean_text(content.get("Categoria")),
            "p_subcategoria": _clean_text(content.get("Subcategoria")),
            "p_producto": _clean_text(content.get("Producto")),
            "p_cantidad": cantidad,
            "p_unidad": unidad,
            "p_lugar": _clean_text(content.get("Lugar")),
            "p_metodo_pago": _clean_text(content.get("MetodoPago")),
            "p_valor": _parse_valor(content.get("Valor")),
            "p_moneda": _clean_text(content.get("Moneda")) or "COP",
            "p_fecha_gasto": fecha_gasto
        }

        return self.supabase_client.registrar_gasto(payload)
