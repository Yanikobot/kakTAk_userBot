from datetime import datetime
import pytz
from telethon import events
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from main import config


geolocator = Nominatim(user_agent="time_bot")
tf = TimezoneFinder()

def info_modl():
    return {
        "name": "!время <город>",
        "description": "Показывает текущее время в указанном городе (пример: !время Москва)",
        "version": 1.1,
        "syntax": "!время <город> (или просто !время)"
    }

def find_timezone(city_name):
    try:
        location = geolocator.geocode(city_name)
        if not location:
            return None, f"Не удалось найти координаты для '{city_name}'."
        timezone = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        if not timezone:
            return None, f"Не удалось определить часовой пояс для '{city_name}'."
        return timezone, None
    except Exception as e:
        return None, f"Ошибка при определении часового пояса: {e}"

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!время(?:\s+(.*))?$'))
    async def time_handler(event):
        if str(event.chat_id) not in config["ALLOWED_CHATS"]:
            await event.reply("Чат не добавлен в список разрешенных.")
            return

        city = event.pattern_match.group(1)
        if not city or not city.strip():
            tz = 'Europe/Moscow'
            city_disp = 'Москва'
        else:
            city = city.strip()
            tz, error = find_timezone(city)
            if not tz:
                await event.reply(error)
                return
            city_disp = city.title()

        now = datetime.now(pytz.timezone(tz))
        await event.reply(f"Время в {city_disp}: {now.strftime('%H:%M:%S, %d %B %Y')}")
