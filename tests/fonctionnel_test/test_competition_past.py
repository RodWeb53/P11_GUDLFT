from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_competition_past():
    chrome = webdriver.Chrome()
    """
        Test fonctionnel permettant de vérifier l'acces
        a une competition dans le passé avec une redirection
        sur la page des compétitions
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
    # Vérification de la redirection apres un clique sur 'book places' pour aller dans la compétition
    chrome.find_element(By.LINK_TEXT, 'Book Places').click()
    time.sleep(0.5)
    assert chrome.current_url == 'http://127.0.0.1:5000/book/Spring%20Festival/Simply%20Lift'
    time.sleep(0.5)
