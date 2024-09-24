import requests, json
from pymongo import MongoClient
from config import config
from urllib.parse import urlparse

#Cadena de conexión a Mongo atlas
connectionURI = MongoClient(config['uri'])
databaseMongo = connectionURI[config['database']]
collectionMongo = databaseMongo[config['collection']]


#Definición de clase
class logicData:

    def __init__(self,domain):
        self.domain = domain

    def getIpAddressFromDomain(self):
        domainResponse = requests.get(str("https://networkcalc.com/api/dns/lookup/"+self.domain))
        if domainResponse.json()['records'] != None:
            for ip in range(len(domainResponse.json()['records']['A'])):
                print("Dominio -> "+self.domain+" : "+str(domainResponse.json()['records']['A'][ip]['address']))
                address = str(domainResponse.json()['records']['A'][ip]['address'])
                self.getLocationByIpAddress(address)

    def getLocationByIpAddress(self,address):
        responseIP = requests.get("https://ipinfo.io/"+str(address)+"/json")
        print("Region: "+str(responseIP.json()['region']))



domainsColombia = requests.get("https://raw.githubusercontent.com/carloslfu/Startup-Colombia-Empresas/master/datos.json")
for i in range(len(domainsColombia.json())):
    if 'webpage' in domainsColombia.json()[i]:
        parsedDomain = urlparse(domainsColombia.json()[i]['webpage'])
        domainClean =  parsedDomain.netloc
        result = logicData(domainClean)
        result.getIpAddressFromDomain()





