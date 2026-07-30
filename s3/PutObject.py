import json
#import boto3
from datetime import datetime
from zoneinfo import ZoneInfo

# s3 = boto3.client("s3")

BUCKET_NAME = "telegram-raw-messages-angel-610433739351-us-east-2-an"


def save_json_s3(event):
    """
    Guarda el JSON recibido desde API Gateway en un archivo de S3.
    """

    timestamp = event["message"]["date"]

    ahora = datetime.fromtimestamp(
        timestamp,
        tz=ZoneInfo("America/Bogota")
    )

    # Estructura de carpetas
    carpeta = ahora.strftime("%Y/%m/%d")

    # Intentamos obtener el update_id de Telegram
    update_id = event.get("update_id", "sin_update")

    # Nombre del archivo
    nombre_archivo = f"{carpeta}/{ahora.strftime('%Y%m%d_%H%M%S')}_update{update_id}.json"

    # s3.put_object(
    #     Bucket=BUCKET_NAME,
    #     Key=nombre_archivo,
    #     Body=json.dumps(event, ensure_ascii=False),
    #     ContentType="application/json"
    # )

    return nombre_archivo