import cv2
import os
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

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

# Пример использования
video_path = "input_video.mp4"
output_path = "output_video.mp4"
watermark_path = "watermark.png"
new_metadata = {"Camera": "NewCamera", "Date": "2024-02-10"}

change_metadata(video_path, new_metadata)
add_watermark(video_path, output_path, "Your Watermark Text")
color_correction(video_path, output_path)
change_codec(video_path, output_path, "h264")
os.remove(video_path)