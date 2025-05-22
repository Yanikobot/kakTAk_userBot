from telethon import events
from main import config
def info_modl():
    return {
        "name": "!гитхаб",
        "description": "Отправляет ссылку на GitHub проекта",
        "version": 1.1,
        "suntax": "!гитхаб"
    }


       
        # Ссылка на GitHub проекта
       


try:
    def register(client, allowed_chats):
      @client.on(events.NewMessage(pattern=r'^!гитхаб$'))
      async def github_command(event):
           print(event.chat_id)
           if str(event.chat_id) in config["ALLOWED_CHATS"]:
               await event.reply(f"[гитхаб](https://github.com/Yanikobot/kakTAk_userBot.git)", link_preview=False)
               return
           
    print(f"модуль: {info_modl()["name"]} загружен.")

except:
    print(f"модуль: {info_modl()["name"]} не загружен.")
