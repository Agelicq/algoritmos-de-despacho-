import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_tabla_tiempos(procesos):

    if not procesos:
        print("Error: No hay datos de procesos disponibles.")
        return

    # Ordenar procesos por prioridad (menor número = mayor prioridad)
    procesos.sort(key=lambda x: x[3])

    tiempos_espera = []
    nombres_procesos = []
    tiempo_acumulado = 0
    tiempos_sistema = []
    tiempo_actual = 0

    for i, proceso in enumerate(procesos):
        pid, rafaga, tiempo_llegada, prioridad = proceso
        if i == 0:
            espera = 0
        else:
            espera = max(0, tiempo_acumulado - tiempo_llegada)
        tiempo_acumulado += rafaga
        nombres_procesos.append(f"P{pid}")
        tiempos_espera.append(espera)

    tiempoE_promedio = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0

    for proceso in procesos:
        pid, rafaga, tiempo_llegada, prioridad = proceso
        inicio = max(tiempo_actual, tiempo_llegada)
        fin = inicio + rafaga
        sistema = fin - tiempo_llegada
        tiempo_actual = fin
        tiempos_sistema.append(sistema)

    tiempoS_promedio = sum(tiempos_sistema) / len(tiempos_sistema) if tiempos_sistema else 0

    datos_tabla = list(zip(nombres_procesos, tiempos_espera, tiempos_sistema))
    datos_tabla.append(["Promedio", round(tiempoE_promedio, 2), round(tiempoS_promedio, 2)])

    ventana = tk.Toplevel()
    ventana.title("Tiempos de Prioridades")
    ventana.geometry("800x400")

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=datos_tabla,
                     colLabels=["Procesos", "Tiempo de Espera", "Tiempo del sistema"],
                     cellLoc='center', loc='center')

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    ventana.mainloop()
