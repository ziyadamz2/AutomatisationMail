import requests
import datetime
import csv
import os

def utilisation_donnees():
    
    date = datetime.datetime.now()
    tim=date.strftime("%Y-%m-%d")
    headers={"Authorization": "Bearer a176ce4c-cea1-391b-ad25-7f85c0f9aba5"}
    response=requests.get("https://api.insee.fr/entreprises/sirene/V3/siren?q=dateCreationUniteLegale%3A"+str(tim)+"&champs=siren%2CactivitePrincipaleUniteLegale%2CprenomUsuelUniteLegale%2CnomUniteLegale",headers=headers)
    data = response.json()
    nb=data['header']['total']
    response=requests.get("https://api.insee.fr/entreprises/sirene/V3/siren?q=dateCreationUniteLegale%3A"+str(tim)+"&champs=siren%2CactivitePrincipaleUniteLegale%2CnomUniteLegale%2CprenomUsuelUniteLegale&nombre="+str(nb),headers=headers)
    data = response.json()
    test=data
    cles=[]
    
    
    del test['header']
    x=[]
    for i in range(0,len(test['unitesLegales'])-1):
        value=[]
        if 'dateFin' in test['unitesLegales'][i]['periodesUniteLegale'][0]:
            test['unitesLegales'][i]['periodesUniteLegale'][0].pop('dateFin')    
        for valeur in test['unitesLegales'][i].values():  
            if valeur==test['unitesLegales'][i]['periodesUniteLegale']:
                for valeur1 in test['unitesLegales'][i]['periodesUniteLegale'][0].values():
                    value=value+[valeur1]
            else:
                value=value+[valeur]
        for element in value:
            if element=='None':
                del value
        x=x+[value]
    
    for key  in test['unitesLegales'][0]:
        cles= cles+[key]
    for key in test['unitesLegales'][0]['periodesUniteLegale'][0]:
        cles= cles+[key]
    cles.remove('periodesUniteLegale')  
    return x,cles

def enregistrement():
    x=utilisation_donnees()
    filename="infoclients.csv"
    f=open(filename, 'a',newline='')
    writer = csv.writer(f)
    file_size = os.path.getsize(filename)
    if (file_size<100):
        writer.writerow(x[1])
        writer.writerows(x[0])
    else:
        f=open(filename, 'a',newline='')
        writer.writerows(x[0])
    return 
enregistrement()
