import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from Grafica_fifo import generar_fifo
from Grafica_AlgoPriori import generar_AlgoritmoPrioridad
from Grafica_SJF import generar_SJF
from Grafica_SRTF import generar_SRTF
from Grafica_RoundRobin import generar_RoundRobin
from Fifo import tabla_fifo
from AlgoPriori import tabla_AlgoPriori
from SJF import tabla_SJF
from SRTF import tabla_SRTF
from RoundRobin import tabla_RoundRobin
from Tiempos_fifo import mostrar_tabla_tiempos as tiempos_fifo
from Tiempos_prioridades import mostrar_tabla_tiempos as tiempos_prioridad
from Tiempos_SJF import mostrar_tabla_tiempos as tiempos_sjf
from Tiempos_SRTF import mostrar_tabla_tiempos as tiempos_srtf
from Tiempos_RoundRobin import mostrar_tabla_tiempos as tiempos_rr

ALGOS = {
    'FIFO': (tabla_fifo, generar_fifo, tiempos_fifo),
    'Prioridades': (tabla_AlgoPriori, generar_AlgoritmoPrioridad, tiempos_prioridad),
    'SJF': (tabla_SJF, generar_SJF, tiempos_sjf),
    'SRTF': (tabla_SRTF, generar_SRTF, tiempos_srtf),
    'Round Robin': (tabla_RoundRobin, generar_RoundRobin, tiempos_rr)
}


def comparar_algoritmos():
    root = tk.Tk()
    root.withdraw()
    opciones = list(ALGOS.keys())
    # Selección de algoritmos
    alg1 = simpledialog.askstring("Comparación", f"Seleccione el primer algoritmo: {opciones}")
    if alg1 not in opciones:
        messagebox.showerror("Error", "Algoritmo no válido.")
        return
    alg2 = simpledialog.askstring("Comparación", f"Seleccione el segundo algoritmo: {opciones}")
    if alg2 not in opciones or alg2 == alg1:
        messagebox.showerror("Error", "Algoritmo no válido o repetido.")
        return
    # Ingreso de procesos
    cantidad_procesos = simpledialog.askinteger("Entrada", "Ingrese la cantidad de procesos:")
    procesos = []
    pedir_prioridad = 'Prioridades' in [alg1, alg2]
    for i in range(cantidad_procesos):
        rafaga = simpledialog.askinteger("Entrada", f"Ráfaga del Proceso {i + 1}:")
        tiempo = simpledialog.askinteger("Entrada", f"Tiempo del Proceso {i + 1}:")
        if pedir_prioridad:
            prioridad = simpledialog.askinteger("Entrada", f"Prioridad del Proceso {i + 1}:")
            procesos.append([i + 1, rafaga, tiempo, prioridad])
        else:
            procesos.append([i + 1, rafaga, tiempo])
    # Quantum si es necesario
    quantum = None
    if 'Round Robin' in [alg1, alg2]:
        quantum = simpledialog.askinteger("Entrada", "Ingrese el quantum para Round Robin:")
    # Ejecutar ambos algoritmos
    resultados = {}
    for alg in [alg1, alg2]:
        if alg == 'Round Robin':
            resultados[alg] = {'procesos': procesos.copy(), 'quantum': quantum}
        else:
            resultados[alg] = {'procesos': procesos.copy()}
    # Mostrar gráficas y tiempos

        # Llamar a la función de comparación de gráficas externa
        from Grafica_Comparacion import mostrar_graficas_comparacion
        mostrar_graficas_comparacion(alg1, alg2, procesos, quantum)
