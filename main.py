import json

from ingestion.telegram.service import TelegramService
from core.application import Aplication 

from aws.s3.put_object_read_json import save_json_s3

def main():

    telegram = TelegramService()
    app = Aplication()

    responses = telegram.get_updates()

    for response in responses["result"]:

        # Guardar el JSON en S3
        archivo =save_json_s3(response)
        print(f"Archivo guardado en S3: {archivo}")

        app.run(response)



    



if __name__ == "__main__":
    main()