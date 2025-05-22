from telethon import events
from main import config
def info_modl():
    return {
        "name": "!тгк",
        "description": "Отправляет ссылку на тгк участников чата",
        "version": 1.1,
        "suntax": "!тгк"
    }


text = ""

for i in config["tgk"]:
    text += f"[{i['name']}]({i['sorse']})\n"
    


def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!тгк$'))
    async def github_command(event):
         print(event.chat_id)
         if str(event.chat_id) in config["ALLOWED_CHATS"]:
             await event.reply(f"Список тгк участнков группы: \n {text}", link_preview=False)
             return
           
print(f"модуль: {info_modl()["name"]} загружен.")

