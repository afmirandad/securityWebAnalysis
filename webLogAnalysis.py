#Usamos gzip para descomprimir el archivo .gz y requests para realizar la descarga del archivo
import gzip, requests, os, re, shutil
from bs4 import BeautifulSoup

#Url de archivo de log comprimido

class classifiedData:

    # Función constructor: se construye la clase a partir de los datos entregados por el usuario. Para este caso la lista de URLs a descargar.
    def __init__(self,listUrls):
        self.directory = 'logsDownloaded'
        self.file_content = ''
        self.ipAddress = []
        self.listUrls = listUrls
        # Valida que la carpeta donde se va a descargar los archivos exista
        self.validateFolder()

    # Función toma la lista de URLs y una por una va a consumirla, descargar el archivo, descomprimirlo y almacenarlo como un archivo.txt.
    def downloadFile(self):
        for url in self.listUrls:
            responseData = requests.get(url, stream=True, verify=False)
            self.local_file_gz = os.path.join(self.directory, url.split("/")[-1])
            with open(self.local_file_gz,'wb') as file:
                for chunk in responseData.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            self.output_file = url.split("/")[-1].replace('.gz', '.txt')
            with gzip.open(self.local_file_gz, 'rb') as gz_file:
                with open(self.output_file, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file)
            os.remove(self.local_file_gz)
            print(f"Archivo descomprimido guardado como {self.output_file}.")

    # Función para validar si la carpeta existe o no, y en caso dado la va a crear.
    def validateFolder(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

class PrepareSources:

    @staticmethod
    def returnSources():
        listUrls = []
        url = "http://www.secrepo.com/self.logs/"
        body = requests.get(url)
        file_pattern = re.compile(r'access\.log\..*\.gz')
        soup = BeautifulSoup(body.text, 'html.parser')
        files_to_download = [a['href'] for a in soup.find_all('a', href=True) if file_pattern.match(a['href'])]
        for i in files_to_download:
            listUrls.append(url+i)
        return listUrls


prueba = classifiedData(PrepareSources().returnSources())
prueba.downloadFile()