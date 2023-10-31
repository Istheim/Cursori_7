import requests

from django.conf import settings

token = settings.TOKEN
chat_id = settings.CHAT_ID


def handle(message):  # функция отправки собщения в чат
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()  # Эта строка отсылает сообщение
