import requests
import sys

def send_telegram_alarm(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.text}")

if __name__ == "__main__":
    bot_token = sys.argv[1]
    chat_id = sys.argv[2]
    message = sys.argv[3]
    send_telegram_alarm(message, bot_token, chat_id)
