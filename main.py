import json

from ingestion.telegram.service import TelegramService


def main():

    telegram = TelegramService()

    updates = telegram.get_updates()

    for update in updates["result"]:
        chat_id = update["message"]["chat"]["id"]

        text = "Enviando mensaje desde python"
        telegram.send_message(chat_id, text)

    print(json.dumps(updates, indent=4, ensure_ascii=False))



if __name__ == "__main__":
    main()