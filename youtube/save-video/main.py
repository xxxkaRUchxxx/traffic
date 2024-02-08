import pytube

# ссылка на видео
youtube_link = "https://youtube.com/shorts/7wze4BkkLGQ?si=81Qsqi329-3xj6OD"

# механика кнопки Скачать
def download(ytlink):
    # пробуем скачать видео по ссылке
    try:
        # переводим его в нужный формат
        youtubelink = pytube.YouTube(ytlink)
        # получаем ссылку на видео с самым высоким качеством
        video = youtubelink.streams.get_highest_resolution()
        # скачиваем видео
        video.download()
        print("Загрузка завершена")
    except pytube.exceptions.RegexMatchError:
        print("Неверная ссылка на видео")

# Вызываем функцию с использованием переменной
download(youtube_link)