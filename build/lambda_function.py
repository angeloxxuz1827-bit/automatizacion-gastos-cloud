import json

from ingestion.telegram.service import TelegramService
from core.application import Aplication

telegram = TelegramService()
app = Aplication()

def lambda_handler(event, context):

    body = json.loads(event["body"])
    #telegram.process_update(body)

    app.run(body)
    

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok"})
    }