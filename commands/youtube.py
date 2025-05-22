from googleapiclient.discovery import build
from telethon import events
from main import config
# Укажите ваш YouTube API Key
YOUTUBE_API_KEY = "AIzaSyAX075NxWYBL40YahJjS_4z4gfbGFYy72Y"

def info_modl():
    return {
        "name": "!последние видео",
        "description": "Получает название, дату и обложку последнего видео с YouTube канала",
        "version": 1.3,
        "suntax": "!последние видео <название канала>"
    }



def register(client, allowed_chats):
    @client.on(events.NewMessage(pattern=r'^!последние видео (.+)$'))
    async def get_latest_video(event):
        if str(event.chat_id) in config["ALLOWED_CHATS"]:
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
                thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]  # URL обложки видео

                def format_number(number):
                    if number >= 1_000_000:
                        return f"{number // 1_000_000}м"
                    elif number >= 1_000:
                        return f"{number // 1_000}к"
                    return str(number)

                # Получаем статистику видео (просмотры и лайки)
                video_id = video['id']['videoId']
                video_stats = youtube.videos().list(
                    id=video_id,
                    part="statistics"
                ).execute()

                view_count = int(video_stats['items'][0]['statistics'].get('viewCount', 0))
                like_count = int(video_stats['items'][0]['statistics'].get('likeCount', 0))

                formatted_views = format_number(view_count)
                formatted_likes = format_number(like_count)

                # Сокращаем название видео, если оно слишком длинное
                max_title_length = 50
                if len(video_title) > max_title_length:
                    video_title = video_title[:max_title_length].strip() + '...'

                # Формируем текст с использованием смайликов
                caption = (f"Последнее видео канала '{channel_name}':\n\n"
                           f"🎥: `{video_title}`\n"
                           f"🗓️: `{video_date}`\n"
                           f"👁️: `{formatted_views}` ❤️: `{formatted_likes}`\n"
                           f" [🔗ссылка🔗]({video_url})\n\n")
                # Отправляем текст и обложку в одном сообщении
                await client.send_file(event.chat_id, thumbnail_url, caption=caption, parse_mode="markdown")
            except Exception as e:
                await event.reply(f"Произошла ошибка при получении данных: {e}")
        else:
            await event.reply("Чат не добавлен в список исключений")