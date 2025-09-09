"""Generación de diagrama Gantt para SJF.

Provee `generar_SJF` que acepta una lista de procesos o solicita los datos
mediante `SJF.tabla_SJF`. Dibuja el ordenamiento por ráfaga y añade un botón
para mostrar los tiempos calculados en `Tiempos_SJF`.
"""

import matplotlib.pyplot as plt
import numpy as np
from SJF import tabla_SJF  # Obtener los datos
from matplotlib.widgets import Button
from Tiempos_SJF import mostrar_tabla_tiempos

def generar_SJF(procesos=None):
    """Genera el diagrama de Gantt para SJF.

    Args:
        procesos (list, optional): Lista de procesos [[id, rafaga, llegada], ...]
    """
    # Obtener procesos [pid, rafaga, tiempo_llegada]
    if procesos is None:
        procesos = tabla_SJF()

    if not procesos:
        print("No hay procesos para mostrar.")
        return

    # Ordenar inicialmente por tiempo de llegada
    procesos.sort(key=lambda x: x[2])

    tiempo_actual = 0
    tareas = []
    lista_listos = []
    pendientes = procesos.copy()

    while pendientes or lista_listos:
        # Mover a la lista de listos los procesos que ya llegaron
        lista_listos.extend([p for p in pendientes if p[2] <= tiempo_actual])
        pendientes = [p for p in pendientes if p[2] > tiempo_actual]

        if lista_listos:
            # Elegir el proceso con la ráfaga más corta
            lista_listos.sort(key=lambda x: x[1])
            pid, rafaga, llegada = lista_listos.pop(0)

            inicio = max(tiempo_actual, llegada)
            fin = inicio + rafaga
            tareas.append((f"P{pid}", inicio, fin))

            tiempo_actual = fin  # Avanzar el tiempo
        else:
            # Si no hay procesos listos, avanzar al siguiente tiempo de llegada
            tiempo_actual = pendientes[0][2]

    # Crear el diagrama de Gantt
    import matplotlib.pyplot as plt
    if 'ax' in locals() and ax is not None:
        _ax = ax
        own_fig = False
    else:
        fig, _ax = plt.subplots(figsize=(10, 5))
        own_fig = True


    # Ordenar las tareas por el número de proceso (extraído del nombre)
    tareas.sort(key=lambda x: int(x[0].replace('P','')))
    for tarea, inicio, fin in tareas:
        _ax.barh(tarea, fin - inicio, left=inicio, color="seagreen", edgecolor="black")

    _ax.set_xticks(np.arange(0, tiempo_actual + 1, 1))
    _ax.set_xlim(0, tiempo_actual)
    _ax.set_xlabel("Tiempo")
    _ax.set_ylabel("Procesos")
    _ax.set_title("SJF")
    _ax.grid(axis="x", linestyle="--", alpha=0.7)

    # Crear el botón en la parte inferior de la figura
    ax_button = fig.add_axes([0.4, 0, 0.2, 0.06])  # [left, bottom, width, height]
    button = Button(ax_button, 'Cálculo de Tiempos')
    button.on_clicked(lambda event: mostrar_tabla_tiempos(procesos))

    plt.show()