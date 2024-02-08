import requests
from bs4 import BeautifulSoup
import sqlite3


# Функция для получения данных о видео и добавления их в базу данных
def parse_youtube_shorts():
    url = "https://www.youtube.com/c/your_channel/shorts"  # Замените "your_channel" на ваш канал
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    videos = soup.find_all("a", {"id": "video-title"})

    conn = sqlite3.connect('youtube_shorts.db')
    c = conn.cursor()

    for video in videos:
        video_title = video.get_text()
        video_link = "https://www.youtube.com" + video["href"]

        # Добавляем данные в базу данных
        c.execute("INSERT INTO videos (title, link) VALUES (?, ?)", (video_title, video_link))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    parse_youtube_shorts()
