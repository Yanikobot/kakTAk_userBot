import asyncio
from telethon import events

def info_modl():
    return {
        "name": "Анимации",
        "description": "Команды для текстовых анимаций",
        "version": 1.3,
        "suntax": "!анимация <тип> <текст>"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!а (\w+)\s*(.+)?$'))
    async def handle_animation(event):
        animation_type = event.pattern_match.group(1)
        user_text = event.pattern_match.group(2)

        if not user_text:
            await event.reply("Пожалуйста, укажите текст для анимации.")
            return

        # Преобразуем текст в нижний регистр
        user_text = user_text.lower()

        if animation_type == "постепенно":
            await gradual_animation(event, user_text)
        elif animation_type == "обратная":
            await reverse_animation(event, user_text)
        elif animation_type == "мигание":
            await blinking_animation(event, user_text)
        else:
            await event.reply("Неизвестный тип анимации. Доступные типы: `постепенно`, `обратная`, `мигание`.")

async def gradual_animation(event, text):
    """Анимация: текст появляется по одному символу."""
    await event.delete()  # Удаляем сообщение пользователя
    message = await event.reply("...")
    animated_text = ""
    for char in text:
        animated_text += char
        await asyncio.sleep(0.3)  # Задержка между символами
        await message.edit(animated_text)

async def reverse_animation(event, text):
    """Анимация: текст исчезает по одному символу с конца."""
    await event.delete()  # Удаляем сообщение пользователя
    message = await event.reply(text)
    for i in range(len(text), 0, -1):
        await asyncio.sleep(0.3)  # Задержка между символами
        await message.edit(text[:i])

async def blinking_animation(event, text):
    """Анимация: текст мигает (появляется и исчезает)."""
    await event.delete()  # Удаляем сообщение пользователя
    message = await event.reply(text)
    for _ in range(5):  # Количество миганий
        await asyncio.sleep(0.5)  # Задержка между состояниями
        await message.edit("")
        await asyncio.sleep(0.5)
        await message.edit(text)