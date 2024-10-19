import random
import numpy as np
from collections import Counter
from scipy.stats import truncnorm
import matplotlib.pyplot as plt

# Variable global para el tiempo
tiempo = 0

# Definir clase Cliente
class Cliente:
    def __init__(self, id):
        self.id = id
        self.tiempo_llegada = np.random.poisson(3)  # Tiempo de llegada en base a Distribución Poisson
        self.productos = self.generar_productos()  # Llama a función que define número de productos
        self.pago_efectivo = random.random() < 0.4  # Pago en efectivo (Bernoulli con probabilidad de 0.4)
        self.tiempo_pago = 2 if self.pago_efectivo else 70 / 60  # Tiempo de pago en minutos dependiendo del método
        self.tiempo_total = self.productos + self.tiempo_pago  # Tiempo total

    # Función que define número de productos según Distribución normal con media 5 y desviación 3.
    def generar_productos(self, media=5, desviacion=3, minimo=1, maximo=10):
        a, b = (minimo - media) / desviacion, (maximo - media) / desviacion
        return int(truncnorm.rvs(a, b, loc=media, scale=desviacion))

    def __str__(self):
        tipo_pago = "Efectivo" if self.pago_efectivo else "Otro medio"
        return (
            f"Cliente {self.id}: Llegada={self.tiempo_llegada} min, "
            f"Productos={self.productos}, Pago={tipo_pago}, "
            f"Tiempo Total={self.tiempo_total:.2f} min"
        )

# Definir la clase Caja
class Caja:
    def __init__(self, id):
        self.id = id
        self.clientes_en_cola = []  # Lista de clientes en cola
        self.tiempo_total_espera = 0  # Tiempo total de espera acumulado
        self.tiempo_total_activa = 0  # Tiempo activa
        self.tiempo_inactivo = 0  # Tiempo inactivo

    # Agregar cliente a cola
    def atender_cliente(self, cliente):
        self.clientes_en_cola.append(cliente)  # Añadir cliente a la cola
        global tiempo
        tiempo += cliente.tiempo_llegada
        # El cliente es atendido después de su llegada
        self.tiempo_total_activa += cliente.tiempo_total
        self.tiempo_total_espera += len(self.clientes_en_cola) * cliente.tiempo_llegada

    def num_clientes_en_cola(self):
        return len(self.clientes_en_cola)

    def __str__(self):
        return f"Caja {self.id}: Clientes en Cola={self.num_clientes_en_cola()}"

def seleccionar_caja(cajas):
    # Seleccionar la caja con menos clientes en cola
    return min(cajas, key=lambda caja: caja.num_clientes_en_cola())

# Crear lista de cajas
num_cajas = 3
cajas = [Caja(i) for i in range(1, num_cajas + 1)]

# Crear lista de clientes y simular la atención
clientes = []
for i in range(10):
    cliente = Cliente(id=i + 1)
    clientes.append(cliente)

# Simular atención a clientes
for cliente in clientes:
    caja = seleccionar_caja(cajas)  # Seleccionar la caja con menos clientes
    caja.atender_cliente(cliente)

# Calcular tiempo inactivo para cada caja
for caja in cajas:
    caja.tiempo_inactivo = tiempo - (caja.tiempo_total_activa + caja.tiempo_total_espera)

# Datos para graficar
tiempos_activas = [caja.tiempo_total_activa for caja in cajas]
tiempos_inactivos = [caja.tiempo_inactivo for caja in cajas]
cajas_ids = [caja.id for caja in cajas]

# Graficar tiempos activos
plt.figure(figsize=(12, 5))

# Gráfica de tiempo activo
plt.subplot(1, 2, 1)
plt.bar(cajas_ids, tiempos_activas, color='blue')
plt.xlabel('Cajas')
plt.ylabel('Tiempo Activo (min)')
plt.title('Tiempo Activo de Cada Caja')
plt.xticks(cajas_ids)

# Gráfica de tiempo inactivo
plt.subplot(1, 2, 2)
plt.bar(cajas_ids, tiempos_inactivos, color='orange')
plt.xlabel('Cajas')
plt.ylabel('Tiempo Inactivo (min)')
plt.title('Tiempo Inactivo de Cada Caja')
plt.xticks(cajas_ids)

plt.tight_layout()
plt.show()