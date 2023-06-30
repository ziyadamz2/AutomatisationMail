from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def connection(nom,prenom):
    url="https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="+nom+"+"+prenom+"&ou=&univers=pagesblanches&idOu="
    print(url)
    driver = webdriver.Firefox()
    driver.get(url)   
    driver.find_element(By.ID,"didomi-notice-agree-button").click()
    offers = driver.find_elements(By.CSS_SELECTOR,".bi.bi-generic")
    for offer in offers:
        print(offer.text)
        

    driver.quit()
    return

connection('Amzil','Fatima')
    
