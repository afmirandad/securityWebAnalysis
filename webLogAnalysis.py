#Usamos gzip para descomprimir el archivo .gz y requests para realizar la descarga del archivo
import gzip, requests, os

#Url de archivo de log comprimido

class classifiedData:

    def __init__(self):
        self.directory = 'logsDownloaded'
        self.url = "http://www.secrepo.com/self.logs/access.log.2017-01-01.gz" #Url de archivo de log comprimido
        self.local_file_gz = os.path.join(self.directory,'access.log.2017-01-01.gz')
        self.validateFolder()

    def downloadFile(self):
        responseData = requests.get(self.url, stream=True, verify=False)
        with open(self.local_file_gz,'wb') as file:
            for chunk in responseData.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    def decompressFile(self):
        with gzip.open(self.local_file_gz, 'rt') as file:
            file_content = file.read()
            print(file_content)

    def validateFolder(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

prueba = classifiedData()
prueba.downloadFile()
prueba.decompressFile()