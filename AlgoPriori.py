# Archivo: AlgoPriori.py
# Descripción: Solicita datos de procesos con prioridad, muestra una tabla y permite ver el diagrama de Gantt.


import matplotlib.pyplot as plt  # Para generar gráficos y tablas
import tkinter as tk  # Para crear cuadros de diálogo e interfaces gráficas
from tkinter import simpledialog  # Para capturar datos de entrada del usuario
from matplotlib.widgets import Button  # Para agregar botones a la interfaz de Matplotlib
import numpy as np
from Tiempos_prioridades import mostrar_tabla_tiempos

# Definimos la función tabla_AlgoPriori, que solicita datos y muestra una tabla de procesos con prioridad
def tabla_AlgoPriori():
    """
    Solicita al usuario los datos de procesos (ráfaga, tiempo de llegada y prioridad),
    muestra una tabla con los datos y permite cerrar la ventana con un botón.
    Devuelve la lista de procesos ingresados.
    """
    root = tk.Tk()  # Creamos una ventana de Tkinter
    root.withdraw()  # Ocultamos la ventana principal, solo usaremos los cuadros de diálogo

    # Solicitamos al usuario la cantidad de procesos a ingresar
    cantidad_procesos = simpledialog.askinteger("Entrada", "Ingrese la cantidad de procesos:")

    # Definimos las columnas de la tabla
    columnas = ["Proceso", "Ráfaga", "Tiempo", "Prioridad"]
    filas = []  # Lista para almacenar los datos de cada proceso

    # Bucle para solicitar los datos de cada proceso
    for i in range(cantidad_procesos):
        rafaga = simpledialog.askinteger("Entrada", f"Ráfaga del Proceso {i + 1}:")  # Duración del proceso
        tiempo = simpledialog.askinteger("Entrada", f"Tiempo del Proceso {i + 1}:")  # Cuándo inicia el proceso
        prioridad = simpledialog.askinteger("Entrada", f"Prioridad del Proceso {i + 1}:")  # Prioridad del proceso
        filas.append([i + 1, rafaga, tiempo, prioridad])  # Guardamos los datos en la lista

    # Crear una figura y un eje para mostrar la tabla
    fig, ax = plt.subplots(figsize=(6, 3))  # Define el tamaño de la tabla
    ax.axis('tight')  # Ajusta la tabla al espacio disponible
    ax.axis('off')  # Oculta los ejes para que solo se vea la tabla
    ax.table(cellText=filas, colLabels=columnas, cellLoc='center', loc='center')  # Crea la tabla con los datos
    
    # Crear un botón en la interfaz para cerrar la ventana
    ax_button = plt.axes([0.4, 0.02, 0.2, 0.075])
    button = Button(ax_button, 'Ver Gantt')
    
    def cerrar_ventana(event):
        """Cierra la ventana de la tabla al hacer clic en el botón."""
        plt.close(fig)

    button.on_clicked(cerrar_ventana)
    plt.show()

    return filas