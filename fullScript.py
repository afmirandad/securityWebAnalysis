import pandas as pd
import numpy as np

# Configurar la semilla para reproducibilidad
np.random.seed(42)

# Número de muestras
n_samples = 1000

# Generar fechas desde el 1 de enero de 2024, una por día
fechas = pd.date_range(start='2024-01-01', periods=n_samples, freq='D')

# Posibles tipos de eventos
tipos_evento = ['malware', 'phishing', 'DDoS', 'ransomware', 'spyware']

# Generar datos sintéticos
data = pd.DataFrame({
    'fecha_evento': fechas,
    'tipo_evento': np.random.choice(tipos_evento, n_samples),
    'severidad': np.random.randint(1, 11, n_samples),
    'origen_ip': ['192.168.1.' + str(np.random.randint(1, 255)) for _ in range(n_samples)],
    'destino_ip': ['172.16.0.' + str(np.random.randint(1, 255)) for _ in range(n_samples)],
    'puerto_destino': np.random.choice([21, 22, 80, 443, 8080], n_samples),
    'duración_segundos': np.random.exponential(scale=300, size=n_samples).astype(int),
    'cantidad_datos_mb': np.random.exponential(scale=100, size=n_samples).astype(int),
})

# Generar la variable 'nuevos_eventos' con alguna relación con las otras variables
# Por ejemplo, supongamos que los eventos más severos y de mayor duración tienden a preceder más eventos nuevos
data['nuevos_eventos'] = (data['severidad'] * 0.5 + data['duración_segundos'] * 0.01 + np.random.normal(0, 5, n_samples)).astype(int)
# Asegurarse de que no haya valores negativos
data['nuevos_eventos'] = data['nuevos_eventos'].clip(lower=0)

# Guardar el dataset en un archivo CSV
data.to_csv('dataMalware.csv', index=False)
