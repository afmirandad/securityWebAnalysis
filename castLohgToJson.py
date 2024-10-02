import re
from datetime import datetime

# Log de Apache como cadena
log_data = """
85.115.32.180 - - [01/Jan/2017:04:05:20 -0800] "GET /favicon.ico HTTP/1.1" 200 212 "http://www.secrepo.com/" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
144.32.170.29 - - [01/Jan/2017:04:05:20 -0800] "GET /twitter-icon.png HTTP/1.1" 200 27787 "http://www.secrepo.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
144.32.170.29 - - [01/Jan/2017:04:05:20 -0800] "GET /GitHub-Mark.png HTTP/1.1" 200 7428 "http://www.secrepo.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
144.32.170.29 - - [01/Jan/2017:04:05:21 -0800] "GET /bootstrap/img/favicon.ico HTTP/1.1" 200 589 "http://www.secrepo.com/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
195.154.191.64 - - [01/Jan/2017:04:08:07 -0800] "GET /udd.php HTTP/1.0" 404 295 "-" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
195.154.191.64 - - [01/Jan/2017:04:08:07 -0800] "GET /udd.php HTTP/1.0" 404 295 "-" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
95.28.180.251 - - [01/Jan/2017:04:17:12 -0800] "GET /honeypot/BSidesDFW%20-%202014.ipynb HTTP/1.1" 200 930799 "http://yandex.ru/clck/jsredir?from=yandex.ru%3Bsearch%3Bweb%3B%3B&text=&etext=1288.NcizpTYIrIKFVmv2WIJv1tqWRuOQHAauX4lDzDRsw1aHrjkujLYUt5anLdIneu0M.50c617e90d6577492401070ac76cbb8ec49f3dbb&uuid=&state=_BLhILn4SxNIvvL0W45KSic66uCIg23qh8iRG98qeIXmeppkgUc0YCYBcIrWNUha-mUlBiA3OhY&data=UlNrNmk5WktYejR0eWJFYk1LdmtxdFVvX2JPZzkyaEU2WFNsdVNGUmVZbHU3ZjQwYnJsWFQzaTk3eklSTnotZ1h4SW1DUmpSY1JVWlAxT212aTdGbmljek9uMzIxTElNRnUyZGR2aTVBa0llUnpQQl9ka3A0QVVIRG80MGhhdUhtd3lndk9vOXNJNXNEQ2FNNWJFc2ROa2VSTlRCMkVtVA&b64e=2&sign=70f0f6ac4b8f81fd73c613c07fa8df7e&keyno=0&cst=AiuY0DBWFJ7IXge4WdYJQYuwSQLovbTTryfMjxprCVs7vnZTjjpMFM_dv67elkC4YlgJtET6dSPLJf5Bu7hH4tFNqQyXuItq48tXlD6EUvlEXq9TiwoFLvrv4PVC5Lkmdlv2OSq5CKFxVzxJpwGeCA"
166.88.123.66 - - [01/Jan/2017:04:18:54 -0800] "GET / HTTP/1.1" 200 10230 "https://www.google.com/" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
"""

# Expresión regular para capturar los elementos clave del log
log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s-\s-\s\[(?P<date>.+?)\]\s"(?P<method>\w+)\s(?P<resource>.+?)\sHTTP\/[\d\.]+"\s(?P<error_code>\d+)\s'
)

# Convertir el log en una lista de entradas JSON
logs_json = []
for match in re.finditer(log_pattern, log_data):
    ip = match.group('ip')
    date_str = match.group('date')
    method = match.group('method')
    resource = match.group('resource')
    error_code = match.group('error_code')

    # Convertir la fecha al formato deseado
    date_time = datetime.strptime(date_str.split()[0], "%d/%b/%Y:%H:%M:%S")

    # Crear el diccionario para cada entrada
    json_data = {
        'date': date_time.strftime('%Y-%m-%d'),
        'ip': ip,
        'method': method,
        'resource': resource,
        'errorCode': error_code
    }

    # Añadir la entrada JSON a la lista
    logs_json.append(json_data)

# Mostrar los resultados
for entry in logs_json:
    print(entry)
