from telethon import events
from main import config

def info_modl():
    return {
        "name": "!айди",
        "description": "Получает ID текущего чата",
        "version": 1.0,
        "suntax": "!айди"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!чатинфо$'))
    async def get_chat_info(event):
        if str(event.chat_id) in config["ALLOWED_CHATS"]:
            chat = await event.get_chat()
            chat_info = (
                f"**Информация о чате:**\n"
                f"ID: `{chat.id}`\n"
                f"Название: `{chat.title}`\n"
                f"Тип: `{chat.__class__.__name__}`\n"
                f"Участники: `{getattr(chat, 'participants_count', 'Неизвестно')}`\n"
                f"Ссылка: `{getattr(chat, 'username', 'Нет')}`\n"
                f"Описание: `{getattr(chat, 'about', 'Нет')}`\n"
                f"Дата создания: `{getattr(chat, 'date', 'Неизвестно')}`\n"
                f"Создатель: `{getattr(chat, 'creator', 'Неизвестно')}`\n"
            )
            await event.reply(chat_info)
        else:
            await event.reply("Чат не добавлен в список исключений")


def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!чатади$'))
    async def get_chat_info(event):
        if str(event.chat_id) in config["ALLOWED_CHATS"]:
          chat = await event.get_chat()
          chat_info = (
              f"ID: `{chat.id}`\n"
          )
          await event.reply(chat_info)


