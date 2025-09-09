"""Entradas para el algoritmo FIFO.

Este módulo contiene la función `tabla_fifo` que solicita al usuario
la lista de procesos (con ráfaga y tiempo de llegada) mediante diálogos
de Tkinter y presenta los datos en una tabla con Matplotlib.

La función retorna una lista de filas con la forma [pid, rafaga, tiempo].
"""

import matplotlib.pyplot as plt  # Para generar gráficos y tablas
import tkinter as tk  # Para crear cuadros de diálogo e interfaces gráficas
from tkinter import simpledialog  # Para capturar datos de entrada del usuario
from matplotlib.widgets import Button  # Para agregar botones a la interfaz de Matplotlib


def tabla_fifo():
    """Pide procesos al usuario y muestra una tabla para FIFO.

    Returns:
        list: Lista de procesos [[id, rafaga, tiempo], ...]

    Notas:
        - Usa diálogos de Tkinter para pedir cantidad, ráfagas y tiempos.
        - Muestra una tabla en Matplotlib y permite cerrarla con un botón.
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
        """Cierra la ventana de Matplotlib que contiene la tabla."""
        plt.close(fig)

    button.on_clicked(cerrar_ventana)

    plt.show()

    return filas
