import time
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import sqlite3

# Ваши данные
CHANNEL_URL = "https://www.youtube.com/c/ВашКанал"
# Подключение к базе данных
conn = sqlite3.connect('video_database.db')
cursor = conn.cursor()

# Создание таблицы, если её ещё нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        video_id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT
    )
''')
conn.commit()


def get_video_data(video_url):
    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    video_id = video_url.split("v=")[1]
    title = soup.find('span', {'class': 'watch-title'}).text.strip()
    description = soup.find('meta', {'name': 'description'})['content'].strip()

    return video_id, title, description


def save_to_database(video_id, title, description):
    cursor.execute('''
        INSERT OR IGNORE INTO videos (video_id, title, description) 
        VALUES (?, ?, ?)
    ''', (video_id, title, description))
    conn.commit()


def download_video(video_id):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    yt = YouTube(video_url)
    yt.streams.filter(file_extension='mp4', res='360p').first().download()


if __name__ == "__main__":
    while True:
        try:
            response = requests.get(CHANNEL_URL)
            soup = BeautifulSoup(response.text, 'html.parser')

            shorts = soup.find_all('a', {'class': 'style-scope ytd-grid-video-renderer'})

            for short in shorts:
                video_url = f"https://www.youtube.com{short['href']}"
                video_id, title, description = get_video_data(video_url)

                save_to_database(video_id, title, description)
                download_video(video_id)

            time.sleep(3600)  # Проверка каждый час
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(300)  # Подождать 5 минут перед повторной попыткой
