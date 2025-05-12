from telethon import events

def info_modl():
    return {
        "name": "!помощь",
        "description": "Показывает список доступных команд",
        "version": 1.0,
        "suntax": "!помощь"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!помощь$'))
    async def help_command(event):
        from main import get_commands_info  # Импортируем функцию из main.py
        commands_info = get_commands_info()
        if not commands_info:
            await event.reply("Нет доступных команд.")
            return

        # Формируем список команд
        help_text = "Доступные команды:\n\n"
        for command in commands_info:
            help_text += f"**{command['name']}** - {command['description']}\nСинтаксис: `{command['suntax']}`\n\n"

        await event.reply(help_text)