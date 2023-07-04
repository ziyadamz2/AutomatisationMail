from time import sleep
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
import numpy as np

def proxy1():
    response = requests.get("https://free-proxy-list.net/")
    proxy_list = pd.read_html(response.text)[0]
    proxy_list["url"] = "http://" + proxy_list["IP Address"] + ":" + proxy_list["Port"].astype(str)
    proxy_list.head()
    https_proxies = proxy_list[proxy_list["Https"] == "yes"]
    return https_proxies
    
    
def create_safe_proxy(https_proxies):
    url = "https://httpbin.org/ip"
    for proxy_url in https_proxies["url"]:
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }          
        try:
            response = requests.get(url, proxies=proxies, timeout=2)
            good_proxies= proxy_url.replace("http://", "")
            return good_proxies
        except Exception:
            pass



def connection(nom,prenom,departement):
    driver = webdriver.Firefox()    
    urlf="https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="+nom+"+"+prenom+"&ou=&univers=pagesblanches&idOu="
    url="https://www.google.com/"
    driver.get(urlf)  
    driver.find_element(By.ID,"didomi-notice-agree-button").click()
    contacts = driver.find_elements(By.CSS_SELECTOR,".bi-generic")
    sleep(20)
    client=[]
    for contact in contacts:
        try: 
            id=contact.find_element(By.TAG_NAME,"h3").text
            adress=contact.find_element(By.CSS_SELECTOR,".bi-address").text.replace(" Voir le plan", "")
            contact.find_element(By.TAG_NAME,"button").click()
            numero= contact.find_element(By.CSS_SELECTOR,".number-contact").text.replace("Tél : ","")
            tel=numero.replace("Tél :\nOpposé aux opérations de marketing\n", "")
            client.append((id,adress,tel))
        except:
            pass
        
    print(client)
    driver.quit()
    return
connection('Fatima','Chaouki',91)
proxy_temprar=create_safe_proxy(proxy1())

