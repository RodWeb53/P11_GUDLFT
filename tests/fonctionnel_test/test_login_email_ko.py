from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_email_ko():
    chrome = webdriver.Chrome()
    """
        Test fonctionnel permettant de vérifier la redirection
        avec une adresse email inconnue
    """
    chrome.get('http://127.0.0.1:5000')
    email = chrome.find_element(By.ID, 'email')
    # On met une adresse email inconnue via l'ID du formulaire
    email.send_keys('test@test.com')
    time.sleep(0.5)
    # Vérification de la redirection vers la page souhaitée
    chrome.find_element(By.TAG_NAME, 'button').click()
    time.sleep(0.5)
    assert chrome.current_url == 'http://127.0.0.1:5000/'
