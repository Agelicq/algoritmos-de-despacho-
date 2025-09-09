import matplotlib.pyplot as plt

def mostrar_tabla_tiempos(procesos):
    if not procesos:
        print("Error: No hay datos de procesos disponibles.")
        return
    procesos.sort(key=lambda x: x[2])
    tiempo_actual = 0
    lista_listos = []
    pendientes = procesos.copy()
    rafagas_restantes = {p[0]: p[1] for p in procesos}
    tiempos_espera = {p[0]: 0 for p in procesos}
    tiempos_sistema = {p[0]: 0 for p in procesos}
    tiempos_inicio = {}
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
            if pid not in tiempos_inicio:
                tiempos_inicio[pid] = tiempo_actual if tiempo_actual >= llegada else llegada
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
