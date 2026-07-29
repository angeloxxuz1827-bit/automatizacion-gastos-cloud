import json

from ingestion.telegram.service import TelegramService

telegram = TelegramService()

def lambda_handler(event, context):

    body = json.loads(event["body"])
    #telegram.process_update(body)
    
    chat_id = body["message"]["chat"]["id"]
    text = "Enviando mensaje desde lambda"

    telegram.send_message(chat_id, text)

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok"})
    }