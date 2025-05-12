import json
import time
from telethon import events

# ID администратора, который может использовать команды бана
ADMIN_USER_ID = 5656356344

# Файл для хранения забаненных пользователей
BANNED_USERS_FILE = "banned_users.json"

# Загружаем забаненных пользователей из файла
def load_banned_users():
    try:
        with open(BANNED_USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Сохраняем забаненных пользователей в файл
def save_banned_users(banned_users):
    with open(BANNED_USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(banned_users, file, ensure_ascii=False, indent=4)

# Инициализация списка забаненных пользователей
banned_users = load_banned_users()

def info_modl():
    return {
        "name": "Управление банами",
        "description": "Команды для бана, разбана и просмотра списка забаненных пользователей",
        "version": 1.0,
        "suntax": "!бан <причина> <минуты>, !бан лист, !разбан"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage)
    async def filter_banned_users(event):
        # Игнорируем сообщения от забаненных пользователей
        if str(event.sender_id) in banned_users:
            # Проверяем, истек ли бан
            if time.time() > banned_users[str(event.sender_id)]["unban_time"]:
                del banned_users[str(event.sender_id)]  # Убираем из списка забаненных
                save_banned_users(banned_users)
            else:
                return

    @client.on(events.NewMessage(pattern=r'^!бан (.+) (\d+)$'))
    async def ban_user(event):
        # Проверяем, что команду использует администратор
        if event.sender_id != ADMIN_USER_ID:
            await event.reply("У вас нет прав использовать эту команду.")
            return

        # Получаем причину и время бана
        reason = event.pattern_match.group(1)
        ban_minutes = int(event.pattern_match.group(2))

        # Проверяем, что команда отправлена в ответ на сообщение
        if not event.is_reply:
            await event.reply("Пожалуйста, используйте эту команду в ответ на сообщение пользователя.")
            return

        # Получаем ID пользователя, которого нужно забанить
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id

        # Добавляем пользователя в список забаненных
        banned_users[str(user_id)] = {
            "reason": reason,
            "unban_time": time.time() + ban_minutes * 60
        }
        save_banned_users(banned_users)
        await event.reply(f"Пользователь с ID `{user_id}` забанен на {ban_minutes} минут. Причина: {reason}")

    @client.on(events.NewMessage(pattern=r'^!бан лист$'))
    async def ban_list(event):
        # Проверяем, что команду использует администратор
        if event.sender_id != ADMIN_USER_ID:
            await event.reply("У вас нет прав использовать эту команду.")
            return

        if not banned_users:
            await event.reply("Список забаненных пользователей пуст.")
            return

        # Формируем список забаненных пользователей
        ban_list_text = "Забаненные пользователи:\n\n"
        for user_id, info in banned_users.items():
            remaining_time = int((info["unban_time"] - time.time()) / 60)
            ban_list_text += f"ID: `{user_id}`, Причина: {info['reason']}, Осталось: {remaining_time} минут\n"

        await event.reply(ban_list_text)

    @client.on(events.NewMessage(pattern=r'^!разбан$'))
    async def unban_user(event):
        # Проверяем, что команду использует администратор
        if event.sender_id != ADMIN_USER_ID:
            await event.reply("У вас нет прав использовать эту команду.")
            return

        # Проверяем, что команда отправлена в ответ на сообщение
        if not event.is_reply:
            await event.reply("Пожалуйста, используйте эту команду в ответ на сообщение пользователя.")
            return

        # Получаем ID пользователя, которого нужно разбанить
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id

        # Убираем пользователя из списка забаненных
        if str(user_id) in banned_users:
            del banned_users[str(user_id)]
            save_banned_users(banned_users)
            await event.reply(f"Пользователь с ID `{user_id}` разбанен.")
        else:
            await event.reply(f"Пользователь с ID `{user_id}` не находится в списке забаненных.")