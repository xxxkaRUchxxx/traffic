import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_database():
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

def main():
    create_database()

    # Вставить учетные данные в базу данных (выполняется один раз)
    # insert_credentials("ваш_логин", "ваш_пароль")

    # Получить учетные данные из базы данных
    credentials = get_credentials()

    # Если учетные данные не найдены, вы можете их вставить (раскомментировать строку выше)
    if credentials:
        # Запуск браузера и открытие страницы YouTube
        driver = webdriver.Firefox()
        driver.get("https://www.youtube.com")

        # Вход в аккаунт
        login(driver, credentials[0], credentials[1])

        # Загрузка видео и добавление описания
        upload_video(driver, "ваше_описание", "ваш_комментарий")

        # Закрытие браузера
        driver.quit()
    else:
        print("Учетные данные не найдены. Пожалуйста, вставьте их в базу данных.")

if __name__ == "__main__":
    main()
