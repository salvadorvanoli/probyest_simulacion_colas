import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli, norm, poisson

# Parámetros iniciales
n = 100  # Número de clientes
k = 3    # Número de cajas
mu_llegadas = 3  # Media de la distribución Poisson para tiempo entre llegadas
mu_productos = 5  # Media de la distribución normal para cantidad de productos
sigma_productos = 3  # Desviación estándar para cantidad de productos
p_pago_efectivo = 0.4  # Probabilidad de pagar en efectivo
tiempo_efectivo = 2  # Tiempo en minutos si paga en efectivo
tiempo_otro_medio = 70 / 60  # Tiempo en minutos si paga con otro medio

# Simular los tiempos entre llegadas (Poisson)
tiempos_llegada = np.cumsum(poisson(mu_llegadas).rvs(n))

# Simular el número de productos de cada cliente (Normal)
productos = np.maximum(0, norm(mu_productos, sigma_productos).rvs(n))  # Asegurar que sea mayor que 0

# Simular si pagan en efectivo o no (Bernoulli)
pago_efectivo = bernoulli(p_pago_efectivo).rvs(n)

# Asignar tiempos de pago
tiempos_pago = np.where(pago_efectivo == 1, tiempo_efectivo, tiempo_otro_medio)

# Tiempo total que pasa cada cliente en la caja
tiempos_en_caja = productos + tiempos_pago

def simular_fila_unica(n, k, tiempos_llegada, tiempos_en_caja):
    # Inicializar las cajas (tiempo disponible)
    tiempo_cajas = np.zeros(k)
    tiempos_espera = np.zeros(n)

    for i in range(n):
        # Encontrar la primera caja que esté disponible
        caja = np.argmin(tiempo_cajas)
        
        if tiempo_cajas[caja] > tiempos_llegada[i]:
            tiempos_espera[i] = tiempo_cajas[caja] - tiempos_llegada[i]
        
        # Asignar al cliente a la caja y actualizar el tiempo
        tiempo_cajas[caja] = max(tiempos_llegada[i], tiempo_cajas[caja]) + tiempos_en_caja[i]

    return tiempo_cajas, tiempos_espera

def simular_filas_separadas(n, k, tiempos_llegada, tiempos_en_caja):
    tiempo_cajas = np.zeros(k)
    tiempos_espera = np.zeros(n)

    for i in range(n):
        # Encontrar la caja con menos personas en la fila
        caja = np.argmin(tiempo_cajas)
        
        if tiempo_cajas[caja] > tiempos_llegada[i]:
            tiempos_espera[i] = tiempo_cajas[caja] - tiempos_llegada[i]

        # Asignar al cliente a la caja y actualizar el tiempo
        tiempo_cajas[caja] = max(tiempos_llegada[i], tiempo_cajas[caja]) + tiempos_en_caja[i]

    return tiempo_cajas, tiempos_espera

# Simulación fila única
tiempo_cajas_unica, tiempos_espera_unica = simular_fila_unica(n, k, tiempos_llegada, tiempos_en_caja)

# Simulación filas separadas
tiempo_cajas_separadas, tiempos_espera_separadas = simular_filas_separadas(n, k, tiempos_llegada, tiempos_en_caja)

# Graficar tiempo de uso de cada caja
plt.figure(figsize=(10, 6))
plt.bar(range(k), tiempo_cajas_unica, color='blue', alpha=0.6, label='Fila Única')
plt.bar(range(k), tiempo_cajas_separadas, color='green', alpha=0.6, label='Filas Separadas')
plt.title('Tiempo de uso de cada caja')
plt.xlabel('Caja')
plt.ylabel('Tiempo (min)')
plt.legend()
plt.show()

# Graficar tiempo de espera
plt.figure(figsize=(10, 6))
plt.hist(tiempos_espera_unica, bins=30, alpha=0.6, color='blue', label='Fila Única')
plt.hist(tiempos_espera_separadas, bins=30, alpha=0.6, color='green', label='Filas Separadas')
plt.title('Tiempo de espera en la fila')
plt.xlabel('Tiempo de espera (min)')
plt.ylabel('Frecuencia')
plt.legend()
plt.show()

# Promedio y desviación estándar de tiempo de uso de cada caja
media_uso_unica = np.mean(tiempo_cajas_unica)
desviacion_uso_unica = np.std(tiempo_cajas_unica)

media_uso_separadas = np.mean(tiempo_cajas_separadas)
desviacion_uso_separadas = np.std(tiempo_cajas_separadas)

# Promedio y desviación estándar de tiempo de espera
media_espera_unica = np.mean(tiempos_espera_unica)
desviacion_espera_unica = np.std(tiempos_espera_unica)

media_espera_separadas = np.mean(tiempos_espera_separadas)
desviacion_espera_separadas = np.std(tiempos_espera_separadas)

# Tiempo libre de las cajas (tiempo total menos tiempo usado)
tiempo_libre_unica = max(tiempo_cajas_unica) - tiempo_cajas_unica
tiempo_libre_separadas = max(tiempo_cajas_separadas) - tiempo_cajas_separadas

print(f'Tiempo libre de las cajas - Fila única: {tiempo_libre_unica}')
print(f'Tiempo libre de las cajas - Filas separadas: {tiempo_libre_separadas}')
