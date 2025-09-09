
"""Generación de diagrama Gantt para SRTF.

Provee `generar_SRTF` que acepta una lista de procesos o solicita los datos
mediante `SRTF.tabla_SRTF`. Dibuja segmentos preemptivos según tiempo restante
y añade un botón para mostrar los tiempos calculados.
"""

import matplotlib.pyplot as plt
import numpy as np
from SRTF import tabla_SRTF
from matplotlib.widgets import Button
from Tiempos_SRTF import mostrar_tabla_tiempos


def generar_SRTF(procesos=None, ax=None):
    if procesos is None:
        procesos = tabla_SRTF()
    if not procesos:
        print("No hay procesos para mostrar.")
        return
    procesos.sort(key=lambda x: x[2])
    tiempo_actual = 0
    tareas = []
    pendientes = procesos.copy()
    lista_listos = []
    rafagas_restantes = {p[0]: p[1] for p in procesos}
    en_ejecucion = None
    while pendientes or lista_listos or en_ejecucion:
        lista_listos.extend([p for p in pendientes if p[2] <= tiempo_actual])
        pendientes = [p for p in pendientes if p[2] > tiempo_actual]
        if en_ejecucion:
            lista_listos.append(en_ejecucion)
            en_ejecucion = None
        if lista_listos:
            lista_listos.sort(key=lambda x: rafagas_restantes[x[0]])
            pid, rafaga, llegada = lista_listos.pop(0)
            inicio = tiempo_actual
            rafaga_restante = rafagas_restantes[pid]
            siguiente_llegada = min([p[2] for p in pendientes], default=None)
            if siguiente_llegada is not None and inicio + rafaga_restante > siguiente_llegada:
                ejecucion = siguiente_llegada - inicio
                rafagas_restantes[pid] -= ejecucion
                tareas.append((f"P{pid}", inicio, inicio + ejecucion))
                tiempo_actual = siguiente_llegada
                en_ejecucion = (pid, rafagas_restantes[pid], llegada)
            else:
                tareas.append((f"P{pid}", inicio, inicio + rafaga_restante))
                tiempo_actual = inicio + rafaga_restante
                rafagas_restantes[pid] = 0
        else:
            tiempo_actual = pendientes[0][2]
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
        own_fig = True
    else:
        own_fig = False

    # Ordenar las tareas por el número de proceso (extraído del nombre)
    tareas.sort(key=lambda x: int(x[0].replace('P','')))
    for tarea, inicio, fin in tareas:
        ax.barh(tarea, fin - inicio, left=inicio, color="orchid", edgecolor="black")
    ax.set_xticks(np.arange(0, tiempo_actual + 1, 1))
    ax.set_xlim(0, tiempo_actual)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Procesos")
    ax.set_title("SRTF")
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    # Crear el botón en la parte inferior de la figura
    ax_button = fig.add_axes([0.4, 0, 0.2, 0.06])  # [left, bottom, width, height]
    button = Button(ax_button, 'Cálculo de Tiempos')
    button.on_clicked(lambda event: mostrar_tabla_tiempos(procesos))

    plt.show()
