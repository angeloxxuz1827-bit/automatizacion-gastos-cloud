from datetime import datetime
from zoneinfo import ZoneInfo


def telegram_key(event: dict, prefix: str) -> str:
    """
    Builds an S3 object key for storing a Telegram message.

    The generated key follows the structure:

        <prefix>/YYYY/MM/DD/YYYYMMDD_HHMMSS_update<update_id>.json

    Args:
        event: Telegram update received by the application.
        prefix: Root folder (e.g., "raw", "processed", "failed").

    Returns:
        A formatted S3 object key.
    """

    # Convert the Telegram Unix timestamp to the local timezone.
    fecha = datetime.fromtimestamp(
        event["message"]["date"],
        tz=ZoneInfo("America/Bogota")
    )

    # Retrieve the Telegram update identifier.
    update_id = event["update_id"]

    # Build and return the S3 object key.
    return (
        f"{prefix.rstrip('/')}/"
        f"{fecha:%Y/%m/%d}/"
        f"{fecha:%Y%m%d_%H%M%S}_update{update_id}.json"
    )


def change_prefix(key: str, new_prefix: str) -> str:
    """
    Replaces the root prefix of an S3 object key.

    Example:
        raw/2026/08/05/file.json
        ->
        processed/2026/08/05/file.json

    Args:
        key: Original S3 object key.
        new_prefix: New root prefix for the object.

    Returns:
        The updated S3 object key with the new prefix.
    """

    # Remove the current prefix while preserving the remaining path.
    _, path = key.split("/", 1)

    # Build and return the new key.
    return f"{new_prefix.rstrip('/')}/{path}"