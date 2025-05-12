from telethon import events

def info_modl():
    return {
        "name": "!гитхаб",
        "description": "Отправляет ссылку на GitHub проекта",
        "version": 1.1,
        "suntax": "!гитхаб"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!гитхаб$'))
    async def github_command(event):
        # Ссылка на GitHub проекта
         await event.reply(f"[гитхаб](https://github.com/Yanikobot/kakTAk_userBot.git)", link_preview=False)

