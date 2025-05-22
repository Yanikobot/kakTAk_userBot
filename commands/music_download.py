import os
import subprocess
import sys
from telethon import events
import json
from main import config



def info_modl():
    return {
        "name": "!гитхаб",
        "description": "Отправляет ссылку на GitHub проекта",
        "version": 1.1,
        "suntax": "!гитхаб"
    }




# Папка для сохранения загруженной музыки
MUSIC_DIRECTORY = "music_files"

# Если папки ещё нет, создаём её
if not os.path.exists(MUSIC_DIRECTORY):
    os.makedirs(MUSIC_DIRECTORY)

# Добавляем список чатов, в которых бот будет отвечать


def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'(?i)^!музыка\s+(.+)'))
    async def music_handler(event):
        if str(event.chat_id) in config["ALLOWED_CHATS"]:
            """
            Обрабатывает команду !музыка <поисковый запрос>.
            Находит видео на YouTube по запросу и скачивает аудиодорожку в формате MP3.

            Если MP3-файл уже существует, отправляет его в чат.
            """
            search_query = event.pattern_match.group(1).strip()  # Извлекаем поисковый запрос
            file_name = f"{search_query}.mp3"
            file_path = os.path.join(MUSIC_DIRECTORY, file_name)

            # Если файл уже скачан, отправляем его
            if os.path.exists(file_path):
                await event.reply("Такая музыка уже скачана. Вот она:", file=file_path)
                return

            try:
                # Информируем пользователя о начале загрузки
                await event.reply("Ищем музыку на YouTube и загружаем, пожалуйста подождите... 🎶")

                # Получаем информацию о видео, чтобы проверить длительность
                info_command = [
                    sys.executable,
                    "-m",
                    "yt_dlp",
                    "--print-json",
                    "--default-search", "ytsearch",
                    search_query
                ]

                # Добавляем cookies для авторизации
                info_command.extend(["--cookies-from-browser", "firefox"])

                result = subprocess.run(info_command, capture_output=True, text=True)

                if result.returncode != 0:
                    await event.reply(f"Ошибка при получении информации о видео: {result.stderr}")
                    return

                try:
                    video_info = json.loads(result.stdout.splitlines()[0])
                except json.JSONDecodeError:
                    await event.reply("Не удалось обработать информацию о видео. Попробуйте другой запрос.")
                    return

                # Проверяем длительность видео
                duration = video_info.get("duration", 0)
                if duration > 600:  # 600 секунд = 10 минут
                    await event.reply("Видео слишком длинное. Пожалуйста, выберите видео короче 10 минут.")
                    return

                # Формируем команду для загрузки
                command = [
                    sys.executable,
                    "-m",
                    "yt_dlp",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--cookies-from-browser", "firefox", 
                    "--ffmpeg-location", "C:\\fmpeg\\bin",  # Укажите правильный путь
                    "--default-search", "ytsearch",
                    "--output", os.path.join(MUSIC_DIRECTORY, f"{search_query}.%(ext)s"),
                    "--verbose",
                    search_query
                ]

                # Запускаем процесс (это может занять некоторое время)
                subprocess.run(command, check=True)

                if os.path.exists(file_path):
                    await event.reply("Музыка успешно загружена 🎵", file=file_path)
                else:
                    await event.reply("Не удалось скачать музыку. Попробуйте позже.")
            except subprocess.CalledProcessError as e:
                await event.reply(f"Ошибка при загрузке музыки: {e}")
            except Exception as e:
                await event.reply(f"Произошла ошибка: {e}")
        else:
            await event.reply("Чат не добавлен в список исключений")