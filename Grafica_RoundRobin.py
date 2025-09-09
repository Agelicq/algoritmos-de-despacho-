"""Generación de diagrama Gantt para Round Robin.

La función `generar_RoundRobin` solicita procesos y quantum si no se pasan
como argumentos. Dibuja las ejecuciones en segmentos según el quantum y
añade un botón para calcular los tiempos mediante `Tiempos_RoundRobin`.
"""

import matplotlib.pyplot as plt
import numpy as np
from RoundRobin import tabla_RoundRobin
from matplotlib.widgets import Button
from Tiempos_RoundRobin import mostrar_tabla_tiempos

def generar_RoundRobin(procesos=None, quantum=None, ax=None):
    """Genera el diagrama de Gantt para Round Robin.

    Args:
        procesos (list, optional): Lista de procesos [[id, rafaga, llegada], ...]
        quantum (int, optional): Quantum del algoritmo.
        ax (matplotlib.axes.Axes, optional): Eje para dibujar.
    """
    if procesos is None or quantum is None:
        resultado = tabla_RoundRobin()
        if not resultado:
            print("No hay procesos para mostrar.")
            return
        procesos, quantum = resultado
        if not procesos or not quantum:
            print("Datos insuficientes.")
            return
    procesos.sort(key=lambda x: x[2])
    tiempo_actual = 0
    pendientes = procesos.copy()
    cola = []
    rafagas_restantes = {p[0]: p[1] for p in procesos}
    tareas = []
    completados = set()
    while pendientes or cola:
        cola.extend([p for p in pendientes if p[2] <= tiempo_actual and p[0] not in completados and p not in cola])
        pendientes = [p for p in pendientes if p[2] > tiempo_actual]
        if cola:
            pid, rafaga, llegada = cola.pop(0)
            inicio = max(tiempo_actual, llegada)
            ejecucion = min(quantum, rafagas_restantes[pid])
            tareas.append((f"P{pid}", inicio, inicio + ejecucion))
            rafagas_restantes[pid] -= ejecucion
            tiempo_actual = inicio + ejecucion
            if rafagas_restantes[pid] > 0:
                # Reinsertar si quedan ráfagas
                cola.extend([p for p in pendientes if p[2] <= tiempo_actual and p[0] not in completados and p not in cola])
                cola.append((pid, rafagas_restantes[pid], llegada))
            else:
                completados.add(pid)
        else:
            if pendientes:
                tiempo_actual = pendientes[0][2]
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
        own_fig = True
    else:
        own_fig = False

    # Ordenar las tareas por el número de proceso (extraído del nombre)
    tareas.sort(key=lambda x: int(x[0].replace('P','')))    
    for tarea, inicio, fin in tareas:
        ax.barh(tarea, fin - inicio, left=inicio, color="gold", edgecolor="black")
    ax.set_xticks(np.arange(0, tiempo_actual + 1, 1))
    ax.set_xlim(0, tiempo_actual)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Procesos")
    ax.set_title("Round Robin")
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    # Crear el botón en la parte inferior de la figura
    ax_button = fig.add_axes([0.4, 0, 0.2, 0.06])  # [left, bottom, width, height]
    button = Button(ax_button, 'Cálculo de Tiempos')
    button.on_clicked(lambda event: mostrar_tabla_tiempos(procesos, quantum))

    plt.show()
