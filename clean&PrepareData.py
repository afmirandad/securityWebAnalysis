import json
import threading
import random

import pandas as pd
import os, re
from datetime import datetime

import requests
from requests.exceptions import ContentDecodingError
from tqdm import tqdm

class CleanUp:

    def __init__(self):
        self.listJson = []
        self.log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(?P<date>.+?)\]\s"(?P<method>\w+)\s(?P<resource>.+?)\sHTTP\/[\d\.]+"\s(?P<error_code>\d+)\s'
)
        self.storedFile = os.path.join(os.getcwd(),'dataCollected.json')
        #self.thread = threading.Thread(target=self.cleanUpLog)
        #self.thread = threading.Thread(target=self.getRegionByIP())

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

        for item in tqdm(data, desc="Procesando items"):
            if 'region' not in item[0]:
                ip_region_dict = {}
                if item[0]['ip'] not in ip_region_dict:
                    #url = f"https://ipinfo.io/{item[0]['ip']}?token=f18cd1e491bd68"
                    url = f"https://ipinfo.io/{item[0]['ip']}/json"
                    response = requests.get(url)
                    try:
                        item[0]['region'] = response.json()['region']
                        ip_region_dict[item[0]['ip']] = response.json()['region']
                    except KeyError:
                        print(f"Error generado {response.json()}")
                    except ContentDecodingError:
                        print(f"Error generado {response.json()}")
                else:
                    item[0]['region'] = ip_region_dict[item[0]['ip']]

        with open('dataCollected.json','w') as file:
            json.dump(data,file,indent=4)


    def proxiesToCheck(self):
        import ast
        with open('http.txt', 'r') as file:
            content = file.read()
        proxy_list = ast.literal_eval(content)
        return random.choice(proxy_list)

    def getRegionByIPAlternative(self,max_retries=5):
        ip_region_dict = {}
        chunk_size = 100000

        with open('dataCollected.json', 'r') as f:
            data = json.load(f)

            num_chunks = len(data) // chunk_size + 1

            for i in tqdm(range(num_chunks), desc="Procesando chunks"):
                chunk = data[i * chunk_size:(i + 1) * chunk_size]

                valid_records = [record[0] for record in chunk if len(record) > 0]

                if valid_records:
                    chunk_df = pd.DataFrame(valid_records)

                    for index, row in chunk_df.iterrows():
                        ip = row['ip']
                        if ip not in ip_region_dict:
                            attempts = 0
                            while attempts < max_retries:
                                proxy = self.proxiesToCheck()
                                proxies = {
                                    "http":proxy,
                                    "https":proxy
                                }
                                try:
                                    url = f"https://ipinfo.io/{ip}/json"
                                    response = requests.get(url,proxies=proxies, timeout=5, verify=False)
                                    if response.status_code == 200 and 'region' in response.json():
                                        ip_region_dict[ip] = response.json()['region']
                                    else:
                                        print(f"Non-200 status code with proxy {proxy}: {response.status_code}")
                                except requests.exceptions.RequestException as e:
                                    print(f"Error with proxy {proxy}: {e}")
                                attempts += 1
                else:
                    print("Chunk vacío o sin registros válidos.")
        print(ip_region_dict)

    def getStatusAttack(self):
        with open('big.txt','r',encoding='iso-8859-1') as file:
            possible_attacks = [line.strip() for line in file]

        with open('dataCollectedSummary.json', 'r') as file:
            data = json.load(file)

        for item in data:
            resource = item[0]['resource']
            print(resource)
            error_code = item[0]['errorCode']
            print(error_code)

            if resource in possible_attacks:
                if error_code == "200" or error_code == "500":
                    item[0]['statusAttack'] = True
                else:
                    item[0]['statusAttack'] = False

        with open('dataCollectedSummary.json','w') as file:
            json.dump(data,file,indent=4)


class PrepareData:

    def __init__(self,listData):
        self.listData = listData

    def prepare(self):
        df = pd.DataFrame(self.listData, columns=[])

#prueba = CleanUp()
#prueba.getRegionByIP()
#prueba.launchThread()
#prueba.getRegionByIPAlternative()
#prueba.getStatusAttack()

if __name__ == "__main__":
    prueba = CleanUp()
    #prueba.getRegionByIPAlternative()
    prueba.getRegionByIP()