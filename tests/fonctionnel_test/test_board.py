from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_board():
    chrome = webdriver.Chrome()
    """
        Test fonctionnel permettant d'aller sur la page board
    """
    chrome.get('http://127.0.0.1:5000')
    chrome.find_element(By.LINK_TEXT, 'Lien vers le tableau des clubs').click()
    time.sleep(0.5)
    assert chrome.current_url == 'http://127.0.0.1:5000/board'
