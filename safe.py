import re
import requests
from pytube import YouTube


def get_video_id(url, platform):
    if platform == 'tiktok':
        match = re.search(r'/video/(\d+)', url)
        if match:
            return match.group(1)
    elif platform == 'youtube':
        yt = YouTube(url)
        return yt.video_id


def download_video(url, output_path='.'):
    try:
        platform = detect_platform(url)

        video_id = get_video_id(url, platform)
        print(f"Detected platform: {platform}")

        if platform == 'tiktok':
            tiktok_download(video_id)
        elif platform == 'youtube':
            youtube_download(url, output_path)

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


def detect_platform(url):
    if 'tiktok' in url:
        return 'tiktok'
    elif 'youtube' in url:
        return 'youtube'
    else:
        raise ValueError("Неподдерживаемая платформа")


def tiktok_download(video_id):
    response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')

    if response.status_code == 200:
        print("Success! Video downloaded.")
        with open(f"{video_id}.mp4", "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download video. Status code: {response.status_code}")
        return None


def youtube_download(url, output_path):
    yt = YouTube(url)
    video_stream = yt.streams.get_highest_resolution()

    print(f"Скачиваем видео: {yt.title}...")
    video_stream.download(output_path)
    print("Видео успешно скачано!")


if __name__ == "__main__":
    video_url = input("Введите URL видео: ")
    output_path = input(
        "Введите путь для сохранения видео (нажмите Enter для использования текущей директории): ") or '.'

    download_video(video_url, output_path)
