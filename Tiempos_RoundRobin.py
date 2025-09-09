import matplotlib.pyplot as plt

def mostrar_tabla_tiempos(procesos, quantum):
    if not procesos or not quantum:
        print("Error: No hay datos de procesos o quantum disponible.")
        return
    procesos.sort(key=lambda x: x[2])
    tiempo_actual = 0
    pendientes = procesos.copy()
    cola = []
    rafagas_restantes = {p[0]: p[1] for p in procesos}
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
    for pid, rafaga, llegada in procesos:
        tiempos_espera[pid] = tiempos_final[pid] - llegada - rafaga
        tiempos_sistema[pid] = tiempos_final[pid] - llegada
    tiempoE_promedio = sum(tiempos_espera.values()) / len(tiempos_espera)
    tiempoS_promedio = sum(tiempos_sistema.values()) / len(tiempos_sistema)
    datos_tabla = [(f"P{pid}", tiempos_espera[pid], tiempos_sistema[pid]) for pid, _, _ in procesos]
    datos_tabla.append(("Promedio", round(tiempoE_promedio, 2), round(tiempoS_promedio, 2)))
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=datos_tabla,
                     colLabels=["Proceso", "Tiempo de Espera", "Tiempo en el Sistema"],
                     cellLoc='center', loc='center')
    plt.show()
