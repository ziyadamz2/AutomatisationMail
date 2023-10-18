from time import sleep
import datetime
import csv
import re
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def similarity_percentage(s1, s2):
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    similarity = 1 - (distance / max_len)
    return similarity * 100

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
    return


def connection(nom,prenom,cp):
    L=None
    while(L==None):
        L=create_safe_proxy(proxy1())
    chrome_options = Options()
    x=L.index(":")
    port_du_proxy=L[x+1:]
    ip_du_proxy=L.replace(L[x:],"")
    
    nom_departements= {"01": "Ain",     "02": "Aisne",     "03": "Allier",     "04": "Alpes-de-Haute-Provence",     "05": "Hautes-Alpes",    
                       "06": "Alpes-Maritimes",     "07": "Ardèche",     "08": "Ardennes",     "09": "Ariège",     "10": "Aube",     "11": "Aude",     
                       "12": "Aveyron",     "13": "Bouches-du-Rhône",     "14": "Calvados",     "15": "Cantal",     "16": "Charente",     
                       "17": "Charente-Maritime",     "18": "Cher",     "19": "Corrèze",     "21": "Côte-d'Or",     "22": "Côtes-d'Armor",    
                       "23": "Creuse",     "24": "Dordogne",     "25": "Doubs",     "26": "Drôme",     "27": "Eure",     "28": "Eure-et-Loir",    
                       "29": "Finistère",     "2A": "Corse-du-Sud",     "2B": "Haute-Corse",     "30": "Gard",     "31": "Haute-Garonne",     
                       "32": "Gers",     "33": "Gironde",     "34": "Hérault",     "35": "Ille-et-Vilaine",     "36": "Indre",     "37": "Indre-et-Loire",    
                       "38": "Isère",     "39": "Jura",     "40": "Landes",     "41": "Loir-et-Cher",     "42": "Loire",     "43": "Haute-Loire",     
                       "44": "Loire-Atlantique",     "45": "Loiret",     "46": "Lot",     "47": "Lot-et-Garonne",     "48": "Lozère",     "49": "Maine-et-Loire",   
                       "50": "Manche",     "51": "Marne",     "52": "Haute-Marne",     "53": "Mayenne",     "54": "Meurthe-et-Moselle",     "55": "Meuse",   
                       "56": "Morbihan",     "57": "Moselle",     "58": "Nièvre",     "59": "Nord",     "60": "Oise",     "61": "Orne",     "62": "Pas-de-Calais",  
                       "63": "Puy-de-Dôme",     "64": "Pyrénées-Atlantiques",     "65": "Hautes-Pyrénées",     "66": "Pyrénées-Orientales",     "67": "Bas-Rhin",  
                       "68": "Haut-Rhin",     "69": "Rhône",     "70": "Haute-Saône",     "71": "Saône-et-Loire",     "72": "Sarthe",     "73": "Savoie", 
                       "74": "Haute-Savoie",     "75": "Paris",     "76": "Seine-Maritime",     "77": "Seine-et-Marne",     "78": "Yvelines",   
                       "79": "Deux-Sèvres",     "80": "Somme",     "81": "Tarn",     "82": "Tarn-et-Garonne",     "83": "Var",     "84": "Vaucluse",    
                       "85": "Vendée",     "86": "Vienne",     "87": "Haute-Vienne",     "88": "Vosges",     "89": "Yonne",     "90": "Territoire de Belfort",    
                       "91": "Essonne",     "92": "Hauts-de-Seine",     "93": "Seine-Saint-Denis",     "94": "Val-de-Marne",     "95": "Val-d'Oise",   
                       "971": "Guadeloupe",     "972": "Martinique",     "973": "Guyane",     "974": "La Réunion",     "976": "Mayotte"
    }
    chrome_options.add_argument("--headless")
    # Changer le proxy
    chrome_options.set_preference("network.proxy.type", 1)
    chrome_options.set_preference("network.proxy.http", ip_du_proxy)
    chrome_options.set_preference("network.proxy.http_port", port_du_proxy)
    driver = webdriver.Firefox(options = chrome_options)
    urlf="https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui="+prenom+"+"+nom+"&ou="+nom_departements[cp]+"+("+cp+")&univers=pagesblanches&idOu="
    driver.get(urlf)
    
    sleep(30)
    driver.find_element(By.ID,"didomi-notice-agree-button").click()
    contacts = driver.find_elements(By.CSS_SELECTOR, ".bi-generic")
    print(contacts)
    client = []
 
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
    driver.close()
    print(client)
    return client


def numero():
    date = datetime.datetime.now()
    tim=date.strftime("%Y-%m-%d")
    filename="/home/ziyad/projetinformatique/AutomatisationMail/resultat/"+tim+".csv"
    df = pd.read_csv(filename)
    taille_tableau=df.shape   
    b=0 
    for i in range(taille_tableau[0]):
        
        fprenom=df['prenomUsuelUniteLegale'][i]
        fnom=df['nomUniteLegale'][i]
        f2cp=str(df['CodePostal'][i])[0:2]                     #code postal à 4 chiffre
        adresse=df['Adresse'][i]+" "+df['Commune'][i]+" "+str(df['CodePostal'][i])
        if int(f2cp)>95:
            f2cp=str(df['CodePostal'][i])[0:3]
        sresultat=connection(fnom,fprenom,f2cp)
        fid=(fnom+" "+fprenom).lower()
        if(sresultat!=[]):
            indice=[]
            h=[]
            for element in sresultat:
                sid=element[0].lower()
                sadresse=element[1].lower()
                h=h+[element[2]]
                i=similarity_percentage(sadresse,adresse)
                if (fid==sid ):         #obtention du code postale 5 chiffres identiques
                    indice=indice+[i]                                            
                else:
                    indice=indice+[0]
            if (max(indice)==0):
                numero_exact=h
                df.at[b,'NuméroC1']=str(numero_exact)
            else:  
                numero_exact=sresultat[indice.index(max(indice))][2]
                df.at[b,'NuméroC1']=str(numero_exact)
        else:
            numero_exact=[]
            df.at[b,'NuméroC1']=str(numero_exact)
        df.to_csv(filename, index=False)
        b=b+1
    return 

