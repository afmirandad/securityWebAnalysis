import json
import threading

import pandas as pd
import os, re
from datetime import datetime

import requests
from tqdm import tqdm

class CleanUp:

    def __init__(self):
        self.listJson = []
        self.log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(?P<date>.+?)\]\s"(?P<method>\w+)\s(?P<resource>.+?)\sHTTP\/[\d\.]+"\s(?P<error_code>\d+)\s'
)
        self.storedFile = os.path.join(os.getcwd(),'dataCollected.json')
        self.thread = threading.Thread(target=self.cleanUpLog)

    def cleanUpLog(self):
        pathRoute = os.getcwd()
        files = [file for file in os.listdir(pathRoute) if file.endswith('txt')]
        for file in tqdm(files, desc="Procesando archivos"):
            fullPath = os.path.join(pathRoute,file)
            with open(fullPath, 'r', encoding='utf-8') as rawFile:
                for line in rawFile:
                    self.listJson.append(self.regexClean(line))
            with open(self.storedFile,'w',encoding='utf-8') as storeJson:
                json.dump(self.listJson,storeJson,ensure_ascii=False,indent=4)

    def launchThread(self):
        self.thread.start()

    def regexClean(self,file):
        logs_json = []
        for match in re.finditer(self.log_pattern, file):
            ip = match.group('ip')
            date_str = match.group('date')
            method = match.group('method')
            resource = match.group('resource')
            error_code = match.group('error_code')

            date_time = datetime.strptime(date_str.split()[0], "%d/%b/%Y:%H:%M:%S")

            json_data = {
                'date': date_time.strftime('%Y-%m-%d'),
                'ip': ip,
                'method': method,
                'resource': resource,
                'errorCode': error_code
            }

            logs_json.append(json_data)
        return logs_json

    def getRegionByIP(self):
        with open('dataCollectedSummary.json','r') as file:
            data = json.load(file)

        for item in data:
            url = f"https://ipinfo.io/{item[0]['ip']}?token="
            response = requests.get(url)
            print(f"La región de la ip {item[0]['ip']} es {response.json()['region']}")
            item[0]['region'] = response.json()['region']

        with open('dataCollectedSummary.json','w') as file:
            json.dump(data,file,indent=4)



class PrepareData:

    def __init__(self,listData):
        self.listData = listData

    def prepare(self):
        df = pd.DataFrame(self.listData, columns=[])

prueba = CleanUp()
prueba.getRegionByIP()