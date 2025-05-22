from telethon import events
from main import config
from deep_translator import GoogleTranslator

def info_modl():
    return {
        "name": "!перевод",
        "description": "Переводит текст на русский язык, автоматически определяя исходный язык. Использовать ответом на сообщение.",
        "version": 1.0,
        "suntax": "!перевод (ответом на сообщение)"
    }




def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!перевод$'))
    async def translate_text_handler(event):
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
        try:
            translated = GoogleTranslator(source='auto', target='ru').translate(reply_msg.text)
            entities = reply_msg.entities if hasattr(reply_msg, 'entities') else None
            if entities:
                await client.send_message(
                    event.chat_id,
                    translated,
                    entities=entities,
                    reply_to=reply_msg.id
                )
            else:
                await event.reply(translated)
        except Exception as e:
            await event.reply(f"Ошибка перевода: {e}")


