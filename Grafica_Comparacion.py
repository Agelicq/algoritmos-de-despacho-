"""Módulo para mostrar gráficas Gantt comparativas de dos algoritmos.

Proporciona `mostrar_graficas_comparacion` que dibuja dos diagramas
de Gantt en una ventana Tkinter y permite calcular/mostrar los tiempos
promedio de espera y sistema para cada algoritmo comparado.
"""

import matplotlib.pyplot as plt
from Grafica_fifo import generar_fifo
from Grafica_AlgoPriori import generar_AlgoritmoPrioridad
from Grafica_SJF import generar_SJF
from Grafica_SRTF import generar_SRTF
from Grafica_RoundRobin import generar_RoundRobin
import tkinter as tk
from matplotlib.widgets import Button
from Tiempos_Comparacion import mostrar_tiempos_comparacion
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def mostrar_graficas_comparacion(alg1, alg2, procesos, quantum=None):
    import matplotlib.pyplot as plt
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    ventana = tk.Toplevel()
    ventana.title("Comparación de Algoritmos - Gantt")
    ventana.geometry("1200x600")


    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    nombres = [alg1, alg2]
    for idx, alg in enumerate([alg1, alg2]):
        if alg == 'Prioridades':
            datos = sorted(procesos, key=lambda x: x[3])
            tareas = []
            tiempo_actual = 0
            for i, proceso in enumerate(datos):
                pid, rafaga, tiempo_llegada, prioridad = proceso
                inicio = max(tiempo_actual, tiempo_llegada)
                fin = inicio + rafaga
                tareas.append((f"P{pid}", inicio, fin))
                tiempo_actual = fin
        elif alg == 'FIFO':
            datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
            tareas = []
            tiempo_actual = 0
            for i, proceso in enumerate(datos):
                pid, rafaga, tiempo = proceso
                inicio = max(tiempo_actual, tiempo)
                fin = inicio + rafaga
                tareas.append((f"P{pid}", inicio, fin))
                tiempo_actual = fin
        elif alg == 'SJF':
            datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
            tareas = []
            tiempo_actual = 0
            pendientes = datos.copy()
            lista_listos = []
            while pendientes or lista_listos:
                lista_listos.extend([p for p in pendientes if p[2] <= tiempo_actual])
                pendientes = [p for p in pendientes if p[2] > tiempo_actual]
                if lista_listos:
                    lista_listos.sort(key=lambda x: x[1])
                    pid, rafaga, llegada = lista_listos.pop(0)
                    inicio = max(tiempo_actual, llegada)
                    fin = inicio + rafaga
                    tareas.append((f"P{pid}", inicio, fin))
                    tiempo_actual = fin
                else:
                    tiempo_actual = pendientes[0][2]
        elif alg == 'SRTF':
            datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
            tareas = []
            tiempo_actual = 0
            pendientes = datos.copy()
            lista_listos = []
            rafagas_restantes = {p[0]: p[1] for p in datos}
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
        elif alg == 'Round Robin':
            datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
            tareas = []
            tiempo_actual = 0
            pendientes = datos.copy()
            cola = []
            rafagas_restantes = {p[0]: p[1] for p in datos}
            completados = set()
            while pendientes or cola:
                cola.extend([p for p in pendientes if p[2] <= tiempo_actual and p[0] not in completados and p not in cola])
                pendientes = [p for p in pendientes if p[2] > tiempo_actual]
                if cola:
                    pid, rafaga, llegada = cola.pop(0)
                    inicio = max(tiempo_actual, llegada)
                    ejecucion = min(quantum, rafagas_restantes[pid])
                    tareas.append((f"P{pid}", inicio, inicio + ejecucion))
                    rafagas_restantes[pid] -= ejecucion
                    tiempo_actual = inicio + ejecucion
                    if rafagas_restantes[pid] > 0:
                        cola.extend([p for p in pendientes if p[2] <= tiempo_actual and p[0] not in completados and p not in cola])
                        cola.append((pid, rafagas_restantes[pid], llegada))
                    else:
                        completados.add(pid)
                else:
                    if pendientes:
                        tiempo_actual = pendientes[0][2]
        # Ordenar tareas por nombre de proceso ascendente (P1, P2, ...)
        tareas.sort(key=lambda x: int(x[0].replace('P','')))
        for tarea, inicio, fin in tareas:
            axs[idx].barh(tarea, fin - inicio, left=inicio, color="red", edgecolor="black")
        axs[idx].set_xlabel("Tiempo")
        axs[idx].set_ylabel("Procesos")
        axs[idx].set_title(f"Gantt {alg}")
        axs[idx].grid(axis="x", linestyle="--", alpha=0.7)
        # Escala de enteros en el eje X
        import numpy as np
        max_tiempo = max([fin for _, _, fin in tareas]) if tareas else 0
        axs[idx].set_xticks(np.arange(0, max_tiempo + 1, 1))
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Botón para mostrar comparación de tiempos
    boton_ax = fig.add_axes([0.4, 0.01, 0.2, 0.05])
    boton = Button(boton_ax, 'Comparar Tiempos')

    def on_click(event):
        resultados = []
        # Importar aquí para evitar ciclos de importación
        from Tiempos_fifo import mostrar_tabla_tiempos as tiempos_fifo
        from Tiempos_prioridades import mostrar_tabla_tiempos as tiempos_prioridades
        from Tiempos_SJF import mostrar_tabla_tiempos as tiempos_sjf
        from Tiempos_SRTF import mostrar_tabla_tiempos as tiempos_srtf
        # Round Robin requiere quantum, se asume que hay un archivo Tiempos_RoundRobin.py
        try:
            from Tiempos_RoundRobin import mostrar_tabla_tiempos as tiempos_rr
        except ImportError:
            tiempos_rr = None

        for alg in [alg1, alg2]:
            if alg == 'FIFO':
                # Calcular promedios FIFO
                datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
                tiempos_espera = []
                tiempo_acumulado = 0
                for i, proceso in enumerate(datos):
                    pid, rafaga, tiempo = proceso
                    if i == 0:
                        espera = 0 - tiempo
                    else:
                        espera = tiempo_acumulado - tiempo
                    tiempo_acumulado += rafaga
                    tiempos_espera.append(espera)
                tiempoE_promedio = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0
                rafagas = [p[1] for p in datos]
                tiempos_sistema = []
                for i, proceso in enumerate(datos):
                    pid, rafaga, tiempo = proceso
                    sistema = sum(rafagas[:i+1]) - tiempo
                    tiempos_sistema.append(sistema)
                tiempoS_promedio = sum(tiempos_sistema) / len(tiempos_sistema) if tiempos_sistema else 0
                resultados.append((alg, round(tiempoE_promedio,2), round(tiempoS_promedio,2)))
            elif alg == 'Prioridades':
                datos = sorted(procesos, key=lambda x: x[3])
                tiempos_espera = []
                tiempo_acumulado = 0
                for i, proceso in enumerate(datos):
                    pid, rafaga, tiempo_llegada, prioridad = proceso
                    if i == 0:
                        espera = 0
                    else:
                        espera = max(0, tiempo_acumulado - tiempo_llegada)
                    tiempo_acumulado += rafaga
                    tiempos_espera.append(espera)
                tiempoE_promedio = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0
                tiempo_actual = 0
                tiempos_sistema = []
                for proceso in datos:
                    pid, rafaga, tiempo_llegada, prioridad = proceso
                    inicio = max(tiempo_actual, tiempo_llegada)
                    fin = inicio + rafaga
                    sistema = fin - tiempo_llegada
                    tiempo_actual = fin
                    tiempos_sistema.append(sistema)
                tiempoS_promedio = sum(tiempos_sistema) / len(tiempos_sistema) if tiempos_sistema else 0
                resultados.append((alg, round(tiempoE_promedio,2), round(tiempoS_promedio,2)))
            elif alg == 'SJF':
                datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
                datos = sorted(datos, key=lambda x: x[2])
                tiempo_actual = 0
                lista_listos = []
                pendientes = datos.copy()
                tiempos_espera = {}
                tiempos_sistema = {}
                while pendientes or lista_listos:
                    lista_listos.extend([p for p in pendientes if p[2] <= tiempo_actual])
                    pendientes = [p for p in pendientes if p[2] > tiempo_actual]
                    if lista_listos:
                        lista_listos.sort(key=lambda x: x[1])
                        pid, rafaga, llegada = lista_listos.pop(0)
                        inicio = max(tiempo_actual, llegada)
                        fin = inicio + rafaga
                        espera = inicio - llegada
                        sistema = fin - llegada
                        tiempos_espera[pid] = espera
                        tiempos_sistema[pid] = sistema
                        tiempo_actual = fin
                    else:
                        tiempo_actual = pendientes[0][2]
                tiempoE_promedio = sum(tiempos_espera.values()) / len(tiempos_espera)
                tiempoS_promedio = sum(tiempos_sistema.values()) / len(tiempos_sistema)
                resultados.append((alg, round(tiempoE_promedio,2), round(tiempoS_promedio,2)))
            elif alg == 'SRTF':
                datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
                datos = sorted(datos, key=lambda x: x[2])
                tiempo_actual = 0
                lista_listos = []
                pendientes = datos.copy()
                rafagas_restantes = {p[0]: p[1] for p in datos}
                tiempos_espera = {p[0]: 0 for p in datos}
                tiempos_sistema = {p[0]: 0 for p in datos}
                tiempos_final = {}
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
                        inicio = max(tiempo_actual, llegada)
                        rafaga_restante = rafagas_restantes[pid]
                        siguiente_llegada = min([p[2] for p in pendientes], default=None)
                        if siguiente_llegada is not None and inicio + rafaga_restante > siguiente_llegada:
                            ejecucion = siguiente_llegada - inicio
                            rafagas_restantes[pid] -= ejecucion
                            tiempo_actual = siguiente_llegada
                            en_ejecucion = (pid, rafagas_restantes[pid], llegada)
                        else:
                            tiempo_actual = inicio + rafaga_restante
                            rafagas_restantes[pid] = 0
                            tiempos_final[pid] = tiempo_actual
                    else:
                        tiempo_actual = pendientes[0][2]
                for pid, rafaga, llegada in datos:
                    tiempos_espera[pid] = tiempos_final[pid] - llegada - rafaga
                    tiempos_sistema[pid] = tiempos_final[pid] - llegada
                tiempoE_promedio = sum(tiempos_espera.values()) / len(tiempos_espera)
                tiempoS_promedio = sum(tiempos_sistema.values()) / len(tiempos_sistema)
                resultados.append((alg, round(tiempoE_promedio,2), round(tiempoS_promedio,2)))
            elif alg == 'Round Robin' and tiempos_rr is not None and quantum is not None:
                datos = procesos if len(procesos[0]) == 3 else [p[:3] for p in procesos]
                datos.sort(key=lambda x: x[2])
                tiempo_actual = 0
                pendientes = datos.copy()
                cola = []
                rafagas_restantes = {p[0]: p[1] for p in datos}
                tiempos_inicio = {}
                tiempos_final = {}
                completados = set()
                while pendientes or cola:
                    cola.extend([p for p in pendientes if p[2] <= tiempo_actual and p[0] not in completados and p not in cola])
                    pendientes = [p for p in pendientes if p[2] > tiempo_actual]
                    if cola:
                        pid, rafaga, llegada = cola.pop(0)
                        if pid not in tiempos_inicio:
                            tiempos_inicio[pid] = max(tiempo_actual, llegada)
                        inicio = max(tiempo_actual, llegada)
                        ejecucion = min(quantum, rafagas_restantes[pid])
                        rafagas_restantes[pid] -= ejecucion
                        tiempo_actual = inicio + ejecucion
                        if rafagas_restantes[pid] > 0:
                            cola.extend([p for p in pendientes if p[2] <= tiempo_actual and p[0] not in completados and p not in cola])
                            cola.append((pid, rafagas_restantes[pid], llegada))
                        else:
                            tiempos_final[pid] = tiempo_actual
                            completados.add(pid)
                    else:
                        if pendientes:
                            tiempo_actual = pendientes[0][2]
                tiempos_espera = {}
                tiempos_sistema = {}
                for pid, rafaga, llegada in datos:
                    tiempos_espera[pid] = tiempos_final[pid] - llegada - rafaga
                    tiempos_sistema[pid] = tiempos_final[pid] - llegada
                tiempoE_promedio = sum(tiempos_espera.values()) / len(tiempos_espera)
                tiempoS_promedio = sum(tiempos_sistema.values()) / len(tiempos_sistema)
                resultados.append((alg, round(tiempoE_promedio,2), round(tiempoS_promedio,2)))
            else:
                resultados.append((alg, 0, 0))
        mostrar_tiempos_comparacion(resultados)
    boton.on_clicked(on_click)

    ventana.mainloop()
