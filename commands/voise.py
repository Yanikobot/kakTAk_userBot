import os
import logging
import speech_recognition as sr
import requests
from telethon import events
from main import config

# Папка для временных файлов
VOICE_DIR = 'voice_tmp'
os.makedirs(VOICE_DIR, exist_ok=True)

def info_modl():
    return {
        "name": "Голос в текст (авто)",
        "description": "Автоматически распознаёт голосовые сообщения и присылает их текст.",
        "version": 1.0,
        "suntax": "(автоматически на голосовые сообщения)"
    }

def autopunctuate(text):
    """
    Простая автопунктуация: добавляет точку в конце, делает первую букву заглавной,
    заменяет многоточия и двойные пробелы, добавляет запятые перед союзами (и, а, но, чтобы, как, если).
    """
    import re
    text = text.strip()
    if not text:
        return ""
    # Первая буква заглавная
    text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
    # Добавить точку, если нет знака в конце
    if text[-1] not in ".!?":
        text += "."
    # Заменить многоточия
    text = text.replace("...", "…")
    # Добавить запятые перед союзами (очень простое правило)
    text = re.sub(r"\s(и|а|но|чтобы|как|если)\s", r", \1 ", text)
    # Убрать двойные пробелы
    text = re.sub(r"\s+", " ", text)
    return text

def autopunctuate_api(text):
    """
    Автопунктуация через публичный API Lindat (работает для русского и английского).
    """
    url = "https://lindat.mff.cuni.cz/services/punct/api/process"
    try:
        resp = requests.post(url, data={"text": text, "lang": "ru"}, timeout=10)
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            return text  # если сервис недоступен, возвращаем исходный текст
    except Exception:
        return text

def yandex_speller_punctuate(text):
    """
    Использует Яндекс.Спеллер для исправления опечаток и пунктуации.
    """
    import requests
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    try:
        resp = requests.post(url, data={"text": text, "lang": "ru"}, timeout=10)
        if resp.status_code == 200:
            result = resp.json()
            # Исправляем ошибки в тексте
            for err in reversed(result):
                s, l, repls = err['pos'], err['len'], err['s']
                if err['s']:
                    text = text[:s] + err['s'][0] + text[s+l:]
            return text
        else:
            return text
    except Exception:
        return text

def register(client, allowed_chats):
    @client.on(events.NewMessage())
    async def voice_to_text_handler(event):
        file_path = None
        wav_path = None
        try:
            chat_id = str(event.chat_id)
            if chat_id not in config["ALLOWED_CHATS"]:
                return
            msg = event.message
            # Проверяем, что это именно голосовое сообщение (audio/ogg и duration < 180 сек)
            if not (msg and msg.media and getattr(msg.media, 'document', None)):
                return
            doc = msg.media.document
            mime = getattr(doc, 'mime_type', '')
            # Проверяем, что это голосовое (audio/ogg) и есть duration (обычно у voice)
            if mime != 'audio/ogg' or not hasattr(doc, 'attributes'):
                return
            # Проверяем, что это не музыка/файл, а именно voice message
            is_voice = any(getattr(attr, 'voice', False) for attr in doc.attributes)
            if not is_voice:
                return
            file_id = str(event.id)
            file_path = os.path.join(VOICE_DIR, f"{file_id}.ogg")
            wav_path = os.path.join(VOICE_DIR, f"{file_id}.wav")
            await event.download_media(file_path)
            if os.system(f'ffmpeg -y -i "{file_path}" "{wav_path}"') != 0:
                await event.reply("Ошибка при конвертации аудио.")
                return
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ru-RU')
            punctuated = yandex_speller_punctuate(text)
            await event.reply(f"Текст голосового:\n{punctuated}")
        except sr.UnknownValueError:
            await event.reply("Не удалось распознать речь.")
        except Exception as e:
            logging.exception("Ошибка при обработке голосового:")
            await event.reply(f"Ошибка распознавания: {e}")
        finally:
            for path in (file_path, wav_path):
                if path and os.path.exists(path):
                    os.remove(path)
