import random
import numpy as np
from collections import Counter
from scipy.stats import truncnorm
import matplotlib.pyplot as plt

# Variable global para el tiempo
tiempo = 0

# Definir clase Cliente
class Cliente:
    def __init__(self, id, tiempo_llegada, tiempo_llegada_acumulado):
        self.id = id
        self.tiempo_llegada = tiempo_llegada  # Tiempo de llegada predefinido según Poisson
        self.tiempo_llegada_acumulado = tiempo_llegada_acumulado
        self.productos = self.generar_productos()  # Llama a función que define número de productos
        self.pago_efectivo = random.random() < 0.4  # Pago en efectivo (Bernoulli con probabilidad de 0.4)
        self.tiempo_pago = 2 if self.pago_efectivo else 70 / 60  # Tiempo de pago en minutos dependiendo del método
        self.tiempo_total = self.productos + self.tiempo_pago  # Tiempo total en la caja
        self.tiempo_espera = 0  # Tiempo de espera en la fila

    # Función que define número de productos según Distribución normal truncada
    def generar_productos(self, media=5, desviacion=3, minimo=1, maximo=10):
        a, b = (minimo - media) / desviacion, (maximo - media) / desviacion 
        return int(truncnorm.rvs(a, b, loc=media, scale=desviacion))

    def __str__(self):
        tipo_pago = "Efectivo" if self.pago_efectivo else "Otro medio"
        return (
            f"Cliente {self.id}: Llegada={self.tiempo_llegada} min, "
            f"Productos={self.productos}, Pago={tipo_pago}, "
            f"Tiempo Total={self.tiempo_total:.2f} min, "
            f"Tiempo de Espera={self.tiempo_espera:.2f} min"
        )

# Definir la clase Caja
class Caja:
    def __init__(self, id):
        self.id = id
        self.clientes_en_cola = []
        self.tiempo_total_espera = 0
        self.tiempo_total_activa = 0
        self.tiempo_inactivo = 0

    # Agregar cliente a cola
    def atender_cliente(self, cliente):
        global tiempo
        if self.clientes_en_cola:
            tiempo_disponible = self.clientes_en_cola[-1].tiempo_llegada_acumulado + self.clientes_en_cola[-1].tiempo_total
        else:
            tiempo_disponible = tiempo

        cliente.tiempo_espera = max(0, tiempo_disponible - cliente.tiempo_llegada)
        self.tiempo_total_espera += cliente.tiempo_espera
        tiempo_fin = cliente.tiempo_llegada + cliente.tiempo_espera + cliente.tiempo_total
        self.tiempo_total_activa += cliente.tiempo_total
        self.clientes_en_cola.append(cliente)

    def num_clientes_en_cola(self):
        return len(self.clientes_en_cola)

    def __str__(self):
        return f"Caja {self.id}: Clientes en Cola={self.num_clientes_en_cola()}"

# Seleccionar caja con menos clientes en cola
def seleccionar_caja(cajas):
    return min(cajas, key=lambda caja: caja.num_clientes_en_cola())

opcion = ""
num_cajas = 3
num_clientes = 100

while opcion not in ['1', '2']:
    opcion = input("Por favor, elige una opción:\n1 - Fila única para todas las cajas\n2 - Fila distinta por cada caja\nOpción: ")
    if opcion not in ['1', '2']:
        print("\nError: opción inválida\n")

# Crear lista de cajas

cajas = [Caja(i) for i in range(1, num_cajas + 1)]

# Generar tiempos de llegada según distribución de Poisson
clientes = []
llegada_acumulada = 0
for i in range(num_clientes):
    variable_poisson = np.random.poisson(1)
    if i != 0:
        llegada_acumulada += variable_poisson  # El tiempo de llegada está dado por una Poisson con media 3
        llegada = variable_poisson
    else:
        llegada = 0
    
    cliente = Cliente(id=i + 1, tiempo_llegada=llegada, tiempo_llegada_acumulado=llegada_acumulada)
    clientes.append(cliente)

    # Aumentamos el tiempo
    tiempo = llegada_acumulada
    if i == num_clientes:
        tiempo += cliente.tiempo_total


# Atender clientes
for cliente in clientes:
    caja = seleccionar_caja(cajas)
    caja.atender_cliente(cliente)

# Calcular tiempo inactivo para cada caja
for caja in cajas:
    print(f"\nCaja {caja.id}")
    print(f"Tiempo: {tiempo}")
    print(f"tiempo_total_activa: {caja.tiempo_total_activa}\n")
    caja.tiempo_inactivo = tiempo - caja.tiempo_total_activa

# Gráfica de tiempo de uso de cada caja
tiempos_activas = [caja.tiempo_total_activa for caja in cajas]
tiempos_inactivos = [caja.tiempo_inactivo for caja in cajas]
cajas_ids = [caja.id for caja in cajas]

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.bar(cajas_ids, tiempos_activas, color='blue')
plt.xlabel('Cajas')
plt.ylabel('Tiempo Activo (min)')
plt.title('Tiempo Activo de Cada Caja')
plt.xticks(cajas_ids)

# Gráfica de tiempos de espera de cada cliente (scatter plot)
tiempos_espera_clientes = [cliente.tiempo_espera for cliente in clientes]
ids_clientes = [cliente.id for cliente in clientes]

plt.subplot(1, 3, 2)
plt.scatter(ids_clientes, tiempos_espera_clientes, color='green', edgecolor='black')
plt.xlabel('ID Cliente')
plt.ylabel('Tiempo de Espera (min)')
plt.title('Tiempo de Espera de los Clientes')
plt.xticks(range(0, len(clientes) + 1, 10))  # Ajuste del eje X

# Grafica de tiempos de llegada de cada cliente (scatter plot)
tiempos_llegada_clientes = [cliente.tiempo_llegada for cliente in clientes]
plt.subplot(1, 3, 3)
plt.scatter(ids_clientes, tiempos_llegada_clientes, color='green', edgecolor='black')
plt.xlabel('ID Cliente')
plt.ylabel('Tiempo de Llegada (min)')
plt.title('Tiempo de Llegada de los Clientes')
plt.xticks(range(0, len(clientes) + 1, 10))  # Ajuste del eje X

plt.tight_layout()
plt.show()

# Valor medio y desviación estándar de tiempo de uso de cada caja
media_uso_cajas = np.mean(tiempos_activas)
desviacion_uso_cajas = np.std(tiempos_activas)
print(f"Valor medio del tiempo de uso de las cajas: {media_uso_cajas:.2f} min")
print(f"Desviación estándar del tiempo de uso de las cajas: {desviacion_uso_cajas:.2f} min")

# Valor medio y desviación estándar de tiempo de espera de los clientes
media_espera_clientes = np.mean(tiempos_espera_clientes)
desviacion_espera_clientes = np.std(tiempos_espera_clientes)
print(f"Valor medio del tiempo de espera de los clientes: {media_espera_clientes:.2f} min")
print(f"Desviación estándar del tiempo de espera de los clientes: {desviacion_espera_clientes:.2f} min")

# Tiempo libre de cada caja
for caja in cajas:
    print(f"Caja {caja.id}: Tiempo libre = {caja.tiempo_inactivo:.2f} min")