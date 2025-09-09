import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_tiempos_comparacion(resultados):
    '''
    resultados: lista de tuplas (nombre_algoritmo, tiempo_espera_prom, tiempo_sistema_prom)
    '''
    ventana = tk.Toplevel()
    ventana.title("Comparación de Tiempos de Algoritmos")
    ventana.geometry("1200x600")

    # Preparar datos para la tabla
    datos_tabla = [(nombre, round(te, 2), round(ts, 2)) for nombre, te, ts in resultados]
    # Calcular promedios generales
    if resultados:
        prom_te = round(sum([te for _, te, _ in resultados]) / len(resultados), 2)
        prom_ts = round(sum([ts for _, _, ts in resultados]) / len(resultados), 2)

    fig, ax = plt.subplots(figsize=(6, 2 + len(datos_tabla)*0.3))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=datos_tabla,
                     colLabels=["Algoritmo", "Tiempo de Espera Promedio", "Tiempo en el Sistema Promedio"],
                     cellLoc='center', loc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    ventana.mainloop()
