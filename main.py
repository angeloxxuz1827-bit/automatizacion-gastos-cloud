import json

from ingestion.telegram.service import TelegramService
from core.application import Aplication 



def main():

    telegram = TelegramService()
    app = Aplication()

    responses = telegram.get_updates()

    for response in responses["result"]:

        app.run(response)



    



if __name__ == "__main__":
    main()