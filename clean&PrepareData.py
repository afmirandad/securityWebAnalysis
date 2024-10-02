import pandas as pd
import os, re

class CleanUp:

    def __init__(self):
        self.listJson = []
        self.log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(?P<date>.+?)\]\s"(?P<method>\w+)\s(?P<resource>.+?)\sHTTP\/[\d\.]+"\s(?P<error_code>\d+)\s'
)

    def cleanUpLog(self):
        for file in os.listdir():
            if file.endswith('txt'):
                filefullpath = os.path.join(file)
                with open(file, 'r', encoding='utf-8') as rawFile:
                    pass




class PrepareData:

    def __init__(self,listData):
        self.listData = listData

    def prepare(self):
        df = pd.DataFrame(self.listData, columns=[])

prueba = CleanUp()
prueba.cleanUpLog()