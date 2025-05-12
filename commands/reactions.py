import random
from telethon import events

# ID пользователя, которого нужно исключить
EXCLUDED_USER_ID = 5656356344

# Словарь с ключевыми словами и списками ответов
RESPONSES = {
    "доброе утро": [
        "Доброе утро! ☀️",
        "Привет! Как спалось? 😊",
        "Доброе утро, хорошего дня! 🌞",
        "Утро доброе! 🌅"
    ],
    "привет": [
        "Привет! 👋",
        "Здравствуй! 😊",
        "Привет-привет! 😄",
        "Приветствую! 🙌"
    ]
}

def info_modl():
    return {
        "name": "Реакции на ключевые слова",
        "description": "Бот реагирует на определенные ключевые слова в сообщениях",
        "version": 1.0,
        "suntax": "Автоматическая реакция"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage)
    async def respond_to_keywords(event):
        # Исключаем сообщения от указанного пользователя
        if event.sender_id == EXCLUDED_USER_ID:
            return

        # Проверяем текст сообщения
        message_text = event.raw_text.lower()
        for keyword, responses in RESPONSES.items():
            if keyword in message_text:
                # Отправляем случайный ответ
                await event.reply(random.choice(responses))
                break