# Archivo: RoundRobin.py
# Descripción: Solicita datos de procesos para el algoritmo Round Robin, muestra una tabla y permite ver el diagrama de Gantt.


import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog
from matplotlib.widgets import Button
# Definimos la función tabla_RoundRobin, que solicita datos y muestra una tabla de procesos Round Robin
def tabla_RoundRobin():
    """Entradas para Round Robin.

    Proporciona `tabla_RoundRobin` que solicita al usuario la lista de procesos
    con ráfagas, tiempos de llegada y el quantum. Presenta los datos en una tabla
    y devuelve (procesos, quantum).
    """
    root = tk.Tk()
    root.withdraw()

    cantidad_procesos = simpledialog.askinteger("Entrada", "Ingrese la cantidad de procesos:")
    quantum = simpledialog.askinteger("Entrada", "Ingrese el quantum:")
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

    # Crear un botón en la interfaz para cerrar la ventana
    ax_button = plt.axes([0.4, 0.02, 0.2, 0.075])
    button = Button(ax_button, 'Ver Gantt')
    
    
    def cerrar_ventana(event):
        """Cierra la figura de Matplotlib con la tabla."""
        plt.close(fig)
    def cerrar_ventana(event):
        """Cierra la ventana de la tabla al hacer clic en el botón."""
        plt.close(fig)

    button.on_clicked(cerrar_ventana)

    plt.show()
    return filas, quantum
