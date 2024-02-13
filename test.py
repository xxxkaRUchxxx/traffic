import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get('http://youtube.com')
assert 'Войти' in browser.title

elem = browser.find_element(By.NAME, 'span')  # Find the search box
print(1)
elem.send_keys('seleniumhq' + Keys.RETURN)
print(2)
time.sleep(10)

browser.quit()