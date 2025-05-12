from telethon import events

def info_modl():
    return {
        "name": "!айди",
        "description": "Получает ID текущего чата",
        "version": 1.0,
        "suntax": "!айди"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!айди$'))
    async def get_chat_id(event):
        chat = await event.get_chat()
        await event.reply(f"ID этого чата: `{chat.id}`")