from telethon import events
from main import config
def info_modl():
    return {
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!тест$'))
    async def test_command(event):
        if str(event.chat_id) in config["ALLOWED_CHATS"]:
            print(event.chat_id)
            await event.reply("Все работает!")
        else:
            await event.reply("чат не дабавлен в список исключений")





