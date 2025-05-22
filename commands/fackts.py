from telethon import events, functions
import random
from main import config


def info_modl():
    return {
        "name": "Факты",
        "description": "Дает рандомный не тупой фатк",
        "version": 1.0,
        "suntax": "!факт",
        "prefix": "!факт"
    }


def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!факт$'))
    async def fackts(event):
        await event.reply(f"{config["fckt"][random.randint(0, len(config["fckt"]))]}")


print(f"модуль: {info_modl()["name"]} загружен.")


