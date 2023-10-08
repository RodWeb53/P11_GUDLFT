from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_email_ok():
    chrome = webdriver.Chrome()
    """
        Test fonctionnel permettant de vérifier la connexion
        avec une adresse email connue
    """
    chrome.get('http://127.0.0.1:5000')
    email = chrome.find_element(By.ID, 'email')
    # On met une adresse email connue via l'ID du formuaire
    email.send_keys('john@simplylift.co')
    time.sleep(0.5)
    # Vérification de la redirection vers la page souhaitée
    chrome.find_element(By.TAG_NAME, 'button').click()
    time.sleep(0.5)
    assert chrome.current_url == 'http://127.0.0.1:5000/showSummary'
