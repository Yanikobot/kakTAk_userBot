from telethon import events, functions
import time
import random
from main import config
# Словарь для отслеживания времени последнего использования команды
last_used = {}


def info_modl():
    return {
        "name": "!описание",
        "description": "Изменяет описание профиля (можно использовать раз в 20 минут, шанс 50%)",
        "version": 1.2,
        "suntax": "!описание [текст] или ответом на сообщение"
    }



def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!описание(?: (.+))?$'))
    async def change_description(event):
        if str(event.chat_id) in config["ALLOWED_CHATS"]:
            user_id = event.sender_id
            current_time = time.time()

        # Проверяем, прошло ли 20 минут с последнего использования
            if user_id in last_used and current_time - last_used[user_id] < 1200:  # 1200 секунд = 20 минут
                remaining_time = int(1200 - (current_time - last_used[user_id]))
                await event.reply(f"Вы можете использовать эту команду снова через {remaining_time // 60} минут.")
                return

        # Обновляем время последнего использования
            last_used[user_id] = current_time

        # Проверяем, есть ли текст после команды
            if event.pattern_match.group(1):  # Если пользователь указал текст после команды
                new_description = event.pattern_match.group(1)
            elif event.is_reply:  # Если текст после команды отсутствует, но сообщение отправлено в ответ
                reply_message = await event.get_reply_message()
                new_description = reply_message.text
            else:  # Если ни текста, ни ответа нет
                 await event.reply("Пожалуйста, укажите описание или ответьте на сообщение с текстом.")
                 return
        
        # Проверяем длину описания
            if len(new_description) > 100:
                await event.reply("Описание слишком длинное. Максимум 100 символов.")
                return
            

      
              # 50% шанс на успешное изменение описания
            if str(user_id) != "5656356344":
                if   random.random() > 0.5:
                    await event.reply("Не повезло Попробуйте снова позже.")
                    return
            

      
        # Меняем описание профиля
            try:
                await client(functions.account.UpdateProfileRequest(about=new_description))
                await event.reply("Описание профиля успешно обновлено!")
            except Exception as e:
                await event.reply(f"Произошла ошибка: {e}")
        else:
            await event.reply("Чат не добавлен в список исключений")



