import time
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import sqlite3
import cv2
import os
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser



cursor_credentials.execute('''
    CREATE TABLE IF NOT EXISTS credentials (
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
cursor_videos.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        video_id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT
    )
''')
conn_channels.commit()
conn_credentials.commit()
conn_videos.commit()

def create_database_for_second_program():
    connection = sqlite3.connect("credentials.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials
                      (username TEXT NOT NULL, password TEXT NOT NULL)''')
    connection.commit()
    connection.close()

def insert_credentials(username, password):
    connection = sqlite3.connect("credentials.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO credentials VALUES (?, ?)", (username, password))
    connection.commit()
    connection.close()

def get_credentials():
    connection = sqlite3.connect("credentials.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM credentials")
    result = cursor.fetchone()
    connection.close()
    return result

def login(driver, username, password):
    login_link = driver.find_element_by_link_text("Войти")
    login_link.click()

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    )
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)

    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

def upload_video(driver, video_description, comment):
    driver.get("https://www.youtube.com/upload")

    description_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "description"))
    )
    description_field.send_keys(video_description)

    comment_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "comment"))
    )
    comment_field.send_keys(comment)

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "save"))
    )
    save_button.click()

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

def change_metadata(video_path, new_metadata):
    # Создаем парсер для видео файла
    parser = createParser(video_path)
    metadata = extractMetadata(parser)

    # Извлекаем текущие метаданные
    current_metadata = metadata.exportDictionary()

    # Обновляем метаданные новыми значениями
    current_metadata.update(new_metadata)

    # Записываем обновленные метаданные обратно в видеофайл
    parser = createParser(video_path)
    metadata = extractMetadata(parser)
    metadata.update(current_metadata)
    metadata.exportToXML(filename=video_path + '.temp.xml')

    # Переименовываем временный файл с обновленными метаданными
    os.rename(video_path + '.temp.xml', video_path)

def add_watermark(video_path, output_path, text):
    # Загрузка видео
    cap = cv2.VideoCapture(video_path)

    # Получение размеров видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Создание видеопотока для записи
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Выбор кодека для сохранения
    out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (width, height))

    # Настройка параметров текста
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (255, 255, 255)  # Белый цвет текста
    position = (10, height - 10)  # Позиция текста (нижний левый угол)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Добавление текстового водяного знака на каждый кадр
        cv2.putText(frame, text, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

        # Запись измененного кадра в выходное видео
        out.write(frame)

    # Закрытие видеофайлов
    cap.release()
    out.release()

def color_correction(video_path, output_path):
    # Загрузка видео
    cap = cv2.VideoCapture(video_path)

    # Получение размеров видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Создание видеопотока для записи
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Выбор кодека для сохранения
    out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Применение цветокоррекции
        corrected_frame = apply_color_correction(frame, brightness_factor=1.2, contrast_factor=1.2)

        # Запись измененного кадра в выходное видео
        out.write(corrected_frame)

    # Закрытие видеофайлов
    cap.release()
    out.release()

def apply_color_correction(frame, brightness_factor, contrast_factor):
    # Коррекция яркости и контраста
    corrected_frame = cv2.convertScaleAbs(frame, alpha=contrast_factor, beta=brightness_factor)

    return corrected_frame

def change_codec(video_path, output_path, new_codec='h264'):
    # Загрузка видео
    cap = cv2.VideoCapture(video_path)

    # Получение размеров видео
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Создание объекта для записи видео с новым кодеком
    fourcc = cv2.VideoWriter_fourcc(*new_codec)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Запись кадра с новым кодеком
        out.write(frame)

    # Закрытие видеофайлов
    cap.release()
    out.release()

if __name__ == "__main__":
    # Получаем учетные данные из базы данных
    credentials = get_credentials()

    # Если учетные данные не найдены, вы можете их вставить (раскомментировать строку ниже)
    if not credentials:
        # insert_credentials("ваш_логин", "ваш_пароль")
        print("Учетные данные не найдены. Пожалуйста, вставьте их в базу данных.")

    cursor_channels.execute("SELECT * FROM channels")
    channels = cursor_channels.fetchall()

    for channel in channels:
        CHANNEL_URL = channel[1]

        print(f"Начинаем обработку канала: {CHANNEL_URL}")

        # Очищаем таблицу videos перед каждым обновлением данных
        cursor_videos.execute("DELETE FROM videos")
        conn_videos.commit()

        try:
            response = requests.get(CHANNEL_URL)
            soup = BeautifulSoup(response.text, 'html.parser')

            shorts = soup.find_all('a', {'class': 'style-scope ytd-grid-video-renderer'})

            for short in shorts:
                video_url = f"https://www.youtube.com{short['href']}"
                video_id, title, description = get_video_data(video_url)

                print(f"Обработка видео: {video_id}")

                save_to_database(video_id, title, description)
                download_video(video_id)

                # Пример использования для изменения метаданных и добавления водяного знака
                video_path = f"{video_id}.mp4"
                output_path = f"{video_id}_processed.mp4"
                new_metadata = {"Camera": "NewCamera", "Date": "2024-02-10"}

                print(f"Изменение метаданных для {video_id}")
                change_metadata(video_path, new_metadata)

                print(f"Добавление водяного знака для {video_id}")
                add_watermark(video_path, output_path, "Your Watermark Text")

                print(f"Цветокоррекция для {video_id}")
                color_correction(video_path, output_path)

                print(f"Изменение кодека для {video_id}")
                change_codec(video_path, output_path, "h264")

                os.remove(video_path)

            print(f"Обработка канала {CHANNEL_URL} завершена")
            time.sleep(30)  # Проверка каждый час
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print("Пауза перед повторной попыткой...")
            time.sleep(300)  # Подождать 5 минут перед повторной попыткой

    # Закрываем соединения с базами данных
    conn_channels.close()
    conn_credentials.close()
    conn_videos.close()