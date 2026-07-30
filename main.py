import json

from ingestion.telegram.service import TelegramService
from core.application import Aplication 

from s3.PutObject import save_json_s3

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