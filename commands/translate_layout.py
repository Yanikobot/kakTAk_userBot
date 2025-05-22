from telethon import events
from main import config

# Таблица соответствия символов (английская -> русская)
ENG_TO_RUS = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~",
    "йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"
)

def info_modl():
    return {
        "name": "!тр",
        "description": "Переводит текст по раскладке (ghbdtn → привет). Использовать ответом на сообщение.",
        "version": 1.0,
        "suntax": "!тр (ответом на сообщение)"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!тр$'))
    async def translate_layout_handler(event):
        if str(event.chat_id) not in config["ALLOWED_CHATS"]:
            await event.reply("Чат не добавлен в список исключений")
            return
        if not event.is_reply:
            await event.reply("Используйте команду ответом на сообщение!")
            return
        reply_msg = await event.get_reply_message()
        if not reply_msg or not reply_msg.text:
            await event.reply("Нет текста для перевода.")
            return
        translated = reply_msg.text.translate(ENG_TO_RUS)
        await event.reply(translated)
