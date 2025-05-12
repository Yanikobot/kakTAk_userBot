from googleapiclient.discovery import build
from telethon import events

# Укажите ваш YouTube API Key
YOUTUBE_API_KEY = "AIzaSyAX075NxWYBL40YahJjS_4z4gfbGFYy72Y"

def info_modl():
    return {
        "name": "!последние видео",
        "description": "Получает название и дату последнего видео с YouTube канала",
        "version": 1.1,
        "suntax": "!последние видео <название канала>"
    }

def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!последние видео (.+)$'))
    async def get_latest_video(event):
        channel_name = event.pattern_match.group(1)
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        try:
            # Ищем канал по названию
            search_response = youtube.search().list(
                q=channel_name,
                type="channel",
                part="id,snippet",
                maxResults=1
            ).execute()

            if not search_response["items"]:
                await event.reply(f"Канал с названием '{channel_name}' не найден.")
                return

            channel_id = search_response["items"][0]["id"]["channelId"]

            # Получаем последнее видео канала
            videos_response = youtube.search().list(
                channelId=channel_id,
                type="video",
                part="id,snippet",
                order="date",
                maxResults=1
            ).execute()

            if not videos_response["items"]:
                await event.reply(f"У канала '{channel_name}' нет опубликованных видео.")
                return

            video = videos_response["items"][0]
            video_title = video["snippet"]["title"]
            video_date = video["snippet"]["publishedAt"]
            video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"

            # Отправляем информацию о видео
            await event.reply(f"Последнее видео канала '{channel_name}':\n\n"
                              f"Название: `{video_title}`\n"
                              f"Дата публикации: `{video_date}`\n"
                              f"**Ссылка:** [клик]({video_url})", link_preview=False)
        except Exception as e:
            await event.reply(f"Произошла ошибка при получении данных: {e}")