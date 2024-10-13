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


def send_image(image_path):
    token = os.getenv("TELEGRAM_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        url_req = f"https://api.telegram.org/bot{token}/sendPhoto"
        payload = {
            "chat_id": chat_id,
        }
        files = {"photo": image_file}

        # Send the request
        response = requests.post(url_req, data=payload, files=files, timeout=10)

        # Print the response from Telegram
        print(response.json())
