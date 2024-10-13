import requests
import os


def send_msg(text):

    token = os.getenv("TELEGRAM_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    url_req = (
        "https://api.telegram.org/bot"
        + token
        + "/sendMessage"
        + "?chat_id="
        + chat_id
        + "&text="
        + text
        + "&parse_mode=markdown"
    )
    results = requests.get(url_req, timeout=10)
    print(results.json())
