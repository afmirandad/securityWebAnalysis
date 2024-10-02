import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Cargar los datos
data = pd.read_csv('dataMalware.csv')

# Convertir fecha_evento a datetime
data['fecha_evento'] = pd.to_datetime(data['fecha_evento'])

# Convertir las IPs y el tipo de evento en variables categóricas
data['origen_ip'] = data['origen_ip'].astype('category').cat.codes
data['destino_ip'] = data['destino_ip'].astype('category').cat.codes
data['tipo_evento'] = data['tipo_evento'].astype('category').cat.codes

# Variables independientes (features) y dependientes (target)
X = data[['tipo_evento', 'severidad', 'origen_ip', 'destino_ip', 'puerto_destino', 'duración_segundos', 'cantidad_datos_mb']]
y = data['nuevos_eventos']

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo de regresión lineal
model = LinearRegression()

# Entrenar el modelo
model.fit(X_train, y_train)

# Realizar predicciones sobre el conjunto de prueba
y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Visualización de resultados
plt.scatter(y_test, y_pred, color='blue', label="Predicciones")
min_val = min(min(y_test), min(y_pred))
max_val = max(max(y_test), max(y_pred))
plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label="Línea ideal")

plt.xlabel("Valores reales")
plt.ylabel("Predicciones")
plt.title("Regresión: Valores reales vs Predicciones")
plt.legend()
plt.show()