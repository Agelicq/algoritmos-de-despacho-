import matplotlib.pyplot as plt

def mostrar_tabla_tiempos(procesos):
    if not procesos:
        print("Error: No hay datos de procesos disponibles.")
        return

    # Ordenar inicialmente por tiempo de llegada
    procesos.sort(key=lambda x: x[2])

    tiempo_actual = 0
    lista_listos = []
    pendientes = procesos.copy()
    tiempos_espera = {}
    tiempos_sistema = {}
    orden_ejecucion = []

    while pendientes or lista_listos:
        # Mover a la lista de listos los procesos que ya llegaron
        lista_listos.extend([p for p in pendientes if p[2] <= tiempo_actual])
        pendientes = [p for p in pendientes if p[2] > tiempo_actual]

        if lista_listos:
            # Escoger el proceso con menor ráfaga
            lista_listos.sort(key=lambda x: x[1])
            pid, rafaga, llegada = lista_listos.pop(0)

            inicio = max(tiempo_actual, llegada)
            fin = inicio + rafaga

            # Guardar tiempos
            espera = inicio - llegada
            sistema = fin - llegada

            tiempos_espera[pid] = espera
            tiempos_sistema[pid] = sistema
            orden_ejecucion.append((pid, espera, sistema))

            tiempo_actual = fin
        else:
            # Avanzar al siguiente proceso si no hay listos
            tiempo_actual = pendientes[0][2]

    # Calcular promedios
    tiempoE_promedio = sum(tiempos_espera.values()) / len(tiempos_espera)
    tiempoS_promedio = sum(tiempos_sistema.values()) / len(tiempos_sistema)

    # Preparar datos para la tabla
    datos_tabla = [(f"P{pid}", espera, sistema) for pid, espera, sistema in orden_ejecucion]
    datos_tabla.append(("Promedio", round(tiempoE_promedio, 2), round(tiempoS_promedio, 2)))

    # Crear tabla
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=datos_tabla,
                     colLabels=["Proceso", "Tiempo de Espera", "Tiempo en el Sistema"],
                     cellLoc='center', loc='center')

    plt.show()
