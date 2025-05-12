import random
from telethon import events

def info_modl():
    return {
        "name": "!рандом",
        "description": "Генерирует случайное число",
        "version": 1.0,
        "suntax": "!рандом <минимум> <максимум>"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!рандом (\d+) (\d+)$'))
    async def random_command(event):
        try:
            min_val = int(event.pattern_match.group(1))
            max_val = int(event.pattern_match.group(2))
            random_number = random.randint(min_val, max_val)
            await event.reply(f"Случайное число: {random_number}")
        except Exception as e:
            await event.reply(f"Ошибка: {e}")