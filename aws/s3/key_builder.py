from datetime import datetime
from zoneinfo import ZoneInfo


def telegram_key(event: dict, prefix: str) -> str:

    fecha = datetime.fromtimestamp(
        event["message"]["date"],
        tz=ZoneInfo("America/Bogota")
    )

    update_id = event["update_id"]

    return (
        f"{prefix.rstrip('/')}/"
        f"{fecha:%Y/%m/%d}/"
        f"{fecha:%Y%m%d_%H%M%S}_update{update_id}.json"
    )

def change_prefix(key: str, new_prefix: str) -> str:
    """
    Cambia el prefijo de una key.

    Ejemplo:
    raw/2026/08/05/file.json
    ->
    processed/2026/08/05/file.json
    """

    _, path = key.split("/", 1)

    return f"{new_prefix.rstrip('/')}/{path}"