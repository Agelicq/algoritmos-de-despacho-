"""Cálculo y visualización de tiempos para FIFO.

Contiene `mostrar_tabla_tiempos` que recibe la lista de procesos
[[id, rafaga, tiempo], ...] y muestra una tabla con Tiempo de Espera
y Tiempo en el Sistema para cada proceso, además de los promedios.
"""

import matplotlib.pyplot as plt
import numpy as np
from Fifo import tabla_fifo  # Importamos la función para obtener los datos


def mostrar_tabla_tiempos(procesos):
    """Calcula y muestra los tiempos de espera y sistema para FIFO.

    Args:
        procesos (list): Lista de procesos [[pid, rafaga, tiempo], ...]
    """
    if not procesos:
        print("Error: No hay datos de procesos disponibles.")
        return

    tiempos_espera = []
    nombres_procesos = []
    tiempo_acumulado = 0
    tiempos_sistema = []
    rafagas = [p[1] for p in procesos]

    for i, proceso in enumerate(procesos):
        pid, rafaga, tiempo = proceso
        if i == 0:
            espera = 0 - tiempo
        else:
            espera = tiempo_acumulado - tiempo

        tiempo_acumulado += rafaga
        nombres_procesos.append(f"P{pid}")
        tiempos_espera.append(espera)

    tiempoE_promedio = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0

    for i, proceso in enumerate(procesos):
        pid, rafaga, tiempo = proceso
        sistema = sum(rafagas[:i+1]) - tiempo
        tiempos_sistema.append(sistema)

    tiempoS_promedio = sum(tiempos_sistema) / len(tiempos_sistema) if tiempos_sistema else 0

    datos_tabla = list(zip(nombres_procesos, tiempos_espera, tiempos_sistema))
    datos_tabla.append(["Promedio", round(tiempoE_promedio, 2), round(tiempoS_promedio, 2)])

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=datos_tabla, 
                      colLabels=["Proceso", "Tiempo de Espera", "Tiempo en el Sistema"],
                      cellLoc='center', loc='center')

    plt.show()

