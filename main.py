import json, asyncio
import os
import traceback
import logging
from telethon import TelegramClient, events
from importlib import import_module
import time
import datetime
from telethon import types, events
from telethon.extensions import markdown
from telethon.tl.custom import Message
from telethon.tl.types import InputPeerUser, MessageEntityCustomEmoji
from telethon.tl.types import InputDocument









# Определяем наш кастомный Markdown-парсер
class CustomMarkdown:
    @staticmethod
    def parse(text):
        text, entities = markdown.parse(text)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == 'spoiler':
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith('emoji/'):
                    try:
                        document_id = int(e.url.split('/')[1])
                        entities[i] = types.MessageEntityCustomEmoji(e.offset, e.length, document_id)
                    except (IndexError, ValueError):
                        continue
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, f'emoji/{e.document_id}')
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, 'spoiler')
        return markdown.unparse(text, entities)

# Назначаем кастомный парсер клиенту




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


# Устанавливаем кастомный парсер Markdown для клиента
# Назначаем наш кастомный парсер клиенту:
client.parse_mode = CustomMarkdown()

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



# Функция для регистрации команд
async def log_command(user_id, command):
    log_entry = {
        "user_id": user_id,
        "command": command,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Сохраняем данные в файл commands_log.json
    log_file = 'commands_log.json'
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as file:
            logs = json.load(file)
    else:
        logs = []

    logs.append(log_entry)

    with open(log_file, 'w', encoding='utf-8') as file:
        json.dump(logs, file, ensure_ascii=False, indent=4)






@client.on(events.NewMessage(pattern=r'^!помощь$'))
async def help_command(event):
    try:
        commands_info = get_commands_info()
        if not commands_info:
            await event.reply("Нет доступных команд.")
            return

        # Формируем список команд
        help_text = "Доступные команды:\n\n"
        for command in commands_info:
            help_text += f"**{command['name']}** - {command['description']}\nСинтаксис: `{command['suntax']}`\n\n"

        await event.reply(help_text)
    except Exception as e:
        error_message = f"Ошибка в команде !помощь: {e}"
        print(error_message)
        logging.error(error_message, exc_info=True)
        await event.reply("Произошла ошибка при выполнении команды !помощь.")

# Подключаем новый модуль typing_action


@client.on(events.NewMessage(pattern=r'^!\+чат$'))
async def add_chat(event):
    chat_id = str(event.chat_id)
    if chat_id not in config["ALLOWED_CHATS"]:
        config["ALLOWED_CHATS"].append(chat_id)
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=False, indent=4)
        await client.delete_messages(event.chat_id, 1)
    else:
        await event.reply("Чат уже находится в списке исключений")



@client.on(events.NewMessage(pattern=r'^!поискэмодзи$'))
async def find_emoji_in_saved(event):
    try:
        async for msg in client.iter_messages('me', limit=50):
            if msg.entities:
                for entity in msg.entities:
                    if isinstance(entity, MessageEntityCustomEmoji):
                        emoji_id = entity.document_id
                        if hasattr(msg.media, 'document'):
                            doc = msg.media.document
                            await client.send_message(
                                'me',
                                f"🔍 Найден кастомный эмодзи:\n\nID: `{emoji_id}`\nAccess Hash: `{doc.access_hash}`"
                            )
                        else:
                            await client.send_message(
                                'me',
                                f"🔍 Найден эмодзи без media.document:\nID: `{emoji_id}`"
                            )

    except Exception as e:
        import traceback
        error_text = traceback.format_exc()
        await client.send_message(
            'me',
            f"💥 Ошибка при поиске эмодзи:\n\n```\n{error_text}\n```",
            parse_mode='markdown'
        )









# Type for 2 seconds, then send a message
chat_ids = [
          # пользователь
]

async def fake_voice_loop():
    while True:
        tasks = []
        for chat in chat_ids:
            # "record-audio" будет действовать 5 секунд, потом исчезнет — надо повторять
            tasks.append(client.action(chat, 'record-audio'))

        # Запускаем статус в каждом чате одновременно
        contexts = [action.__aenter__() for action in tasks]
        entered = await asyncio.gather(*contexts)

        # Ждём 5 секунд — в это время статус активен
        await asyncio.sleep(6)

        # Закрываем контекстные менеджеры
        exits = [action.__aexit__(None, None, None) for action in tasks]
        await asyncio.gather(*exits)

        # Небольшая пауза перед повтором (чтобы Telegram не забанил)
        await asyncio.sleep(1)

@client.on(events.NewMessage(pattern=r'^!стоп$'))
async def stop_command(event):
    await event.reply("🛑 Остановить через Ctrl+C в консоли.")  # можно доработать на отключение вручную

    










# Запускаем бота
async def main():



    # Получаем список последних сообщений самого себя
   

    print(config['ALLOWED_CHATS'])
    await client.start()
    load_modules()
    print("Успешное подключение!")
    await client.run_until_disconnected()  # Убираем disconnect, чтобы бот продолжал работать

if __name__ == '__main__':
    asyncio.run(main())


