"""Generación de diagrama Gantt para el algoritmo por prioridades.

Define `generar_AlgoritmoPrioridad` que solicita procesos si no se le pasan,
ordena por prioridad y dibuja el Gantt. Añade un botón para mostrar tiempos
usando `Tiempos_prioridades.mostrar_tabla_tiempos`.
"""

import matplotlib.pyplot as plt  # Importar la librería para gráficos
import numpy as np  # Manejo de arrays numéricos
from AlgoPriori import tabla_AlgoPriori  # Obtener los datos
from matplotlib.widgets import Button
from Tiempos_prioridades import mostrar_tabla_tiempos

def generar_AlgoritmoPrioridad(procesos=None):
    # Si no se pasan procesos, pedirlos normalmente
    if procesos is None:
        procesos = tabla_AlgoPriori()

    if not procesos:
        print("No hay procesos para mostrar.")
        return
    
    # Separar el proceso 1 y los demás
    proceso_1 = next((p for p in procesos if p[0] == 1), None)
    otros_procesos = [p for p in procesos if p[0] != 1]
    
    # Ordenar los demás procesos por prioridad (menor número = mayor prioridad)
    otros_procesos.sort(key=lambda x: x[3])
    
    # Reconstruir la lista de procesos asegurando que "1" vaya primero
    procesos_ordenados = [proceso_1] + otros_procesos if proceso_1 else otros_procesos
    
    tareas = []
    tiempo_actual = 0  # Tiempo acumulado en la ejecución

    for i, proceso in enumerate(procesos_ordenados):
        pid, rafaga, tiempo_llegada, prioridad = proceso  # Extraer datos
        
        # Si es el primer proceso (Proceso 1), debe comenzar en 0
        if i == 0:
            inicio = 0
        else:
            inicio = max(tiempo_actual, tiempo_llegada)
        
        fin = inicio + rafaga
        tareas.append((f"Proceso {pid}", inicio, fin))
        
        # Actualizar el tiempo actual
        tiempo_actual = fin
    
    # Crear el diagrama de Gantt
    import matplotlib.pyplot as plt
    if 'ax' in locals() and ax is not None:
        _ax = ax
        own_fig = False
    else:
        fig, _ax = plt.subplots(figsize=(10, 5))
        own_fig = True

    # Ordenar las tareas por el número de proceso (extraído del nombre)
    tareas.sort(key=lambda x: int(x[0].split()[-1]))
    for tarea, inicio, fin in tareas:
        _ax.barh(tarea, fin - inicio, left=inicio, color="royalblue", edgecolor="black")

    _ax.set_xticks(np.arange(0, tiempo_actual + 1, 1))  # Ajustar el eje X
    _ax.set_xlim(0, tiempo_actual)  # Límite del eje X
    _ax.set_xlabel("Tiempo")
    _ax.set_ylabel("Procesos")
    _ax.set_title("Algoritmo de prioridad")
    _ax.grid(axis="x", linestyle="--", alpha=0.7)

    # Crear el botón en la parte inferior de la figura
    ax_button = fig.add_axes([0.4, 0, 0.2, 0.06])  # [left, bottom, width, height]
    button = Button(ax_button, 'Cálculo de Tiempos')
    button.on_clicked(lambda event: mostrar_tabla_tiempos(procesos_ordenados))

    plt.show()