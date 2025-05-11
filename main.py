import json
import os
from telethon import TelegramClient, events
from importlib import import_module

# Загружаем данные из JSON файла
with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

# Инициализация клиента
client = TelegramClient(
    config['session_name'],
    config['api_id'],
    config['api_hash'],
    device_model=config['device_model'],
    system_version=config['system_version'],
    app_version=config['app_version']
)


# Список разрешенных чатов (заполняется ID чатов)
allowed_chats = [5656356344]  # Добавьте сюда ID чатов, из которых бот принимает сообщения

# Глобальный фильтр для сообщений
@client.on(events.NewMessage)
async def filter_messages(event):
    if event.chat_id not in allowed_chats:
        return  # Игнорируем сообщения из запрещенных чатов
    

# Функция для загрузки всех модулей команд
def load_modules():
    commands_dir = 'commands'
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module = import_module(f'{commands_dir}.{module_name}')
            module.register(client, allowed_chats)

# Функция для загрузки информации о модулях
def get_commands_info():
    commands_dir = 'commands'
    commands_info = []
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module = import_module(f'{commands_dir}.{module_name}')
            if hasattr(module, 'info_modl'):
                commands_info.append(module.info_modl())
    return commands_info

# Команда для получения ID чатов
@client.on(events.NewMessage(pattern=r'^!айди$'))
async def get_chat_id(event):
    chat = await event.get_chat()
    await event.reply(f"ID этого чата: `{chat.id}`")

# Команда "помощь"
@client.on(events.NewMessage(pattern=r'^!помощь$'))
async def help_command(event):
    commands_info = get_commands_info()
    if not commands_info:
        await event.reply("Нет доступных команд.")
        return

    # Формируем список команд
    help_text = "Доступные команды:\n\n"
    for command in commands_info:
        help_text += f"**{command['name']}** - {command['description']}\nСинтаксис: `{command['suntax']}`\n\n"

    await event.reply(help_text)

# Запускаем бота
async def main():
    print("Бот запущен...")
    load_modules()
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())    # Список разрешенных чатов (заполняется ID чатов)
    allowed_chats = []  # Добавьте сюда ID чатов, из которых бот принимает сообщения
    
    # Глобальный фильтр для сообщений
    @client.on(events.NewMessage)
    async def filter_messages(event):
        if event.chat_id not in allowed_chats:
            return  # Игнорируем сообщения из запрещенных чатов