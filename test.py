import requests
from pytube import YouTube


def get_tiktok_video_urls_by_topic(topic, count):
    api_url = f'https://open.tiktokapis.com/v2/challenge/search/?challengeName={topic}&count={count}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Проверяем, что запрос успешен
        trending_posts = response.json()

        video_urls = []
        for post in trending_posts:
            video_url = post['itemInfos']['video']['urls'][0]
            video_urls.append(video_url)

        return video_urls
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса к TikTok API: {e}")
        return []


def download_tiktok_videos(video_urls, output_path="."):
    downloaded_videos = []
    for video_url in video_urls:
        try:
            yt = YouTube(video_url)
            video_title = yt.title

            # Скачивание видео
            stream = yt.streams.filter(file_extension="mp4").first()
            stream.download(output_path)

            downloaded_videos.append(video_title)
            print(f"Видео успешно скачано: {video_title}")
        except Exception as e:
            print(f"Произошла ошибка при скачивании видео: {e}")

    return downloaded_videos


if __name__ == "__main__":
    topic = input("Введите название тренда или темы: ")
    count = int(input("Введите количество видео для скачивания: "))
    download_path = input("Введите путь для сохранения видео (по умолчанию - текущая директория): ")

    if not download_path:
        download_path = "."

    video_urls = get_tiktok_video_urls_by_topic(topic, count)
    if video_urls:
        downloaded = download_tiktok_videos(video_urls, download_path)
        print(f"Скачано {len(downloaded)} видео по теме {topic}.")
    else:
        print("Не удалось получить видео по указанной теме.")
