from telethon import events

# ID пользователя, чьи сообщения нужно обрабатывать
USER_ID = 5656356344  # Замените на ваш ID

def info_modl():
    return {
        "name": "Фильтр капса",
        "description": "Автоматически убирает капс из сообщений пользователя",
        "version": 1.0,
        "suntax": "Автоматическая обработка"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(outgoing=True))  # Отслеживаем только исходящие сообщения
    async def remove_caps(event):
        # Проверяем, что сообщение отправлено указанным пользователем
        if event.sender_id == USER_ID:
            message_text = event.raw_text

            # Проверяем длину сообщения и наличие капса
            if len(message_text) > 10 and message_text.isupper():
                # Преобразуем текст в нижний регистр
                new_text = message_text.lower()

                # Редактируем сообщение
                await event.edit(new_text)