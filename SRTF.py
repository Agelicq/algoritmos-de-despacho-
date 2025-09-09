# Archivo: SRTF.py
# Descripción: Solicita datos de procesos para el algoritmo SRTF, muestra una tabla y permite ver el diagrama de Gantt.


import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from matplotlib.widgets import Button

# Definimos la función tabla_SRTF, que solicita datos y muestra una tabla de procesos SRTF
"""Entradas para SRTF (Shortest Remaining Time First).

Contiene `tabla_SRTF` que solicita al usuario ráfagas y tiempos de llegada
y muestra la tabla resultante. Retorna la lista de procesos.
"""

import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from matplotlib.widgets import Button


def tabla_SRTF():
    """Solicita procesos para SRTF y los muestra en una tabla.

    Returns:
        list: Lista de procesos [[id, rafaga, tiempo], ...]
    """
    root = tk.Tk()
    root.withdraw()

    cantidad_procesos = simpledialog.askinteger("Entrada", "Ingrese la cantidad de procesos:")
    columnas = ["Proceso", "Ráfaga", "Tiempo"]
    filas = []

    for i in range(cantidad_procesos):
        rafaga = simpledialog.askinteger("Entrada", f"Ráfaga del Proceso {i + 1}:")
        tiempo = simpledialog.askinteger("Entrada", f"Tiempo del Proceso {i + 1}:")
        filas.append([i + 1, rafaga, tiempo])

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=filas, colLabels=columnas, cellLoc='center', loc='center')

    ax_button = plt.axes([0.4, 0.02, 0.2, 0.075])
    button = Button(ax_button, 'Ver Gantt')

    def cerrar_ventana(event):
        """Cierra la figura que contiene la tabla de procesos."""
        plt.close(fig)

    button.on_clicked(cerrar_ventana)

    plt.show()
    return filas
