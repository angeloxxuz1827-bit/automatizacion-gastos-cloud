import json

from aws.s3.client import S3Client
from aws.s3.events import get_bucket_and_key
from aws.s3.key_builder import change_prefix
from database.supabase_client import SupabaseClient

from core.application import Application


# Clientes y servicio reutilizados entre invocaciones de la Lambda.
s3 = S3Client()
supabase = SupabaseClient()
application = Application(supabase)


def lambda_handler(event, context):
    """
    Entry point de la Lambda que persiste el gasto en Supabase.

    Se dispara con un evento `ObjectCreated` sobre `processed/`. Lee la
    respuesta del LLM, recupera el update original de Telegram para obtener
    los datos reales del cliente y del mensaje, y ejecuta la función RPC
    transaccional de Supabase.
    """

    # Extraer el bucket y la key del objeto procesado.
    bucket, processed_key = get_bucket_and_key(event)

    # Leer la respuesta cruda del LLM.
    response_llm = s3.get_json(
        bucket=bucket,
        key=processed_key
    )

    # Deserializar el JSON estructurado del gasto.
    content_response_llm = json.loads(
        response_llm["choices"][0]["message"]["content"]
    )

    # El update original conserva texto, usuario y fecha de Telegram.
    raw_key = change_prefix(processed_key, "raw")
    raw_update = s3.get_json(
        bucket=bucket,
        key=raw_key
    )

    # Guardar cliente, mensaje y gasto en una sola transacción.
    result = application.save_expense(
        raw_update=raw_update,
        content=content_response_llm,
        s3_key_processed=processed_key
    )

    # Devolver el resultado de la función RPC.
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "status": "ok",
                "result": result
            },
            ensure_ascii=False
        )
    }
