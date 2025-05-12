import json
import os
import traceback
import logging
from telethon import TelegramClient, events
from importlib import import_module
import time

# Настройка логирования
logging.basicConfig(
    filename='bot_errors.log',  # Имя файла для сохранения ошибок
    level=logging.ERROR,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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


def load_modules():
    commands_dir = 'commands'
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                module_name = filename[:-3]
                module = import_module(f'{commands_dir}.{module_name}')
                module.register(client, None)  # Передаем None вместо allowed_chats
            except Exception as e:
                error_message = f"Ошибка при загрузке модуля {filename}: {e}"
                print(error_message)
                logging.error(error_message, exc_info=True)  # Логируем ошибку
                time.sleep(5)

# Функция для загрузки информации о модулях
def get_commands_info():
    commands_dir = 'commands'
    commands_info = []
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                module_name = filename[:-3]
                module = import_module(f'{commands_dir}.{module_name}')
                if hasattr(module, 'info_modl'):
                    commands_info.append(module.info_modl())
            except Exception as e:
                error_message = f"Ошибка при получении информации из модуля {filename}: {e}"
                print(error_message)
                logging.error(error_message, exc_info=True)  # Логируем ошибку
    return commands_info

# Запускаем бота
async def main():
    await client.start()
    load_modules()
    print("Успешное подключение!")
    await client.run_until_disconnected()  # Убираем disconnect, чтобы бот продолжал работать

import asyncio
asyncio.run(main())