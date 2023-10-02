from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_index():
    chrome = webdriver.Chrome()
    """
        Test fonctionnel permettant de vérifier la page d'accueil
    """
    chrome.get('http://127.0.0.1:5000')
    title = chrome.find_element(By.TAG_NAME, 'h1').text
    assert 'Registration Portal' in title
    assert chrome.current_url == 'http://127.0.0.1:5000/'
    time.sleep(0.5)
