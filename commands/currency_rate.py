import requests
from telethon import events
from main import config

def info_modl():
    return {
        "name": "!курс <валюта>",
        "description": "Показывает курс валюты к рублю (пример: !курс usd)",
        "version": 1.0,
        "suntax": "!курс <валюта>"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!курс\s+(\w+)$'))
    async def currency_handler(event):
        if str(event.chat_id) not in config["ALLOWED_CHATS"]:
            await event.reply("Чат не добавлен в список исключений")
            return
        code = event.pattern_match.group(1).upper()
        if code == 'RUB':
            await event.reply("1 RUB = 1 RUB")
            return
        try:
            url = f"https://api.exchangerate.host/latest?base={code}&symbols=RUB"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            if 'rates' in data and 'RUB' in data['rates']:
                rate = data['rates']['RUB']
                await event.reply(f"1 {code} = {rate:.2f} RUB")
            else:
                await event.reply("Не удалось получить курс для этой валюты.")
        except Exception as e:
            await event.reply(f"Ошибка получения курса: {e}")
