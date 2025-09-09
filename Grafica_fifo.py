"""Dibuja el diagrama de Gantt para el algoritmo FIFO.

La función `generar_fifo` acepta una lista de procesos o la solicita
mediante `Fifo.tabla_fifo` si no se le pasa. Dibuja barras horizontales
que representan la ejecución de cada proceso en el tiempo y añade un
botón para calcular y mostrar los tiempos (espera y sistema) usando
`Tiempos_fifo.mostrar_tabla_tiempos`.
"""

import matplotlib.pyplot as plt  # Importar la librería para gráficos
import numpy as np  # Manejo de arrays numéricos
from Fifo import tabla_fifo  # Importar la función que obtiene los datos
from matplotlib.widgets import Button
from Tiempos_fifo import mostrar_tabla_tiempos


def generar_fifo(procesos=None):
    """Genera el diagrama de Gantt para FIFO.

    Args:
        procesos (list, optional): Lista de tuplas (pid, rafaga, tiempo_llegada).
    Returns:
        list: Lista de tareas (pid_str, inicio, fin) dibujadas.
    """
    # Obtener los datos desde tabla_fifo() en Fifo.py
    if procesos is None:
        procesos = tabla_fifo()

    if not procesos:
        print("No hay procesos para mostrar.")
        return

    # Listas para almacenar los datos procesados
    tareas = []
    total_tiempo = 0  # El primer proceso inicia en 0

    # Procesar los datos obtenidos
    for i, proceso in enumerate(procesos):
        pid, rafaga, tiempo = proceso  # Extraer datos

        if i == 0:
            # El primer proceso inicia en 0, ignorando su tiempo de llegada
            inicio = 0
        else:
            # El siguiente proceso empieza donde terminó el anterior o cuando llega, lo que sea mayor
            inicio = max(total_tiempo, tiempo)

        fin = inicio + rafaga
        tareas.append((f"Proceso {pid}", inicio, fin))

        # Actualizar el tiempo total acumulado
        total_tiempo = fin

    # Crear el diagrama de Gantt
    import matplotlib.pyplot as plt
    if 'ax' in locals() and ax is not None:
        _ax = ax
        own_fig = False
    else:
        fig, _ax = plt.subplots(figsize=(10, 5))
        own_fig = True

    for tarea, inicio, fin in tareas:
        _ax.barh(tarea, fin - inicio, left=inicio, color="mediumpurple", edgecolor="black")

    _ax.set_xticks(np.arange(0, total_tiempo + 1, 1))  # Ajustar el eje X
    _ax.set_xlim(0, total_tiempo)  # Ajustar el límite del eje X
    _ax.set_xlabel("Tiempo")  # Etiqueta del eje X
    _ax.set_ylabel("Procesos")  # Etiqueta del eje Y
    _ax.set_title("Planificación FIFO")  # Título del gráfico
    _ax.grid(axis="x", linestyle="--", alpha=0.7)  # Cuadrícula en el eje X

        # Crear el botón en la parte inferior de la figura
    ax_button = fig.add_axes([0.4, 0, 0.2, 0.06])  # [left, bottom, width, height]
    button = Button(ax_button, 'Cálculo de Tiempos')
    button.on_clicked(lambda event: mostrar_tabla_tiempos(procesos))

    plt.show()