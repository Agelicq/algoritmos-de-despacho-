# Autor: Juan Jose ,Maria Angelica Alvarez
# Fecha: 09/09/2025

"""Interfaz principal para la demo de algoritmos de planificación.

Este módulo construye la ventana principal con botones para abrir
las ventanas/diágramas/tablas asociadas con cada algoritmo de despacho.
"""

from comparacion import comparar_algoritmos
import tkinter as tk  
from PIL import Image, ImageTk
from Grafica_fifo import generar_fifo
from Grafica_AlgoPriori import generar_AlgoritmoPrioridad
from Grafica_SJF import generar_SJF
from Grafica_SRTF import generar_SRTF
from Grafica_RoundRobin import generar_RoundRobin


def ocultar_ventana():
    """Oculta la ventana principal (la deja disponible para remostrarse).

    Usada antes de abrir ventanas secundarias para mantener la app en memoria.
    """
    root.withdraw()


def salir():
    """Cierra la aplicación principal y termina el bucle de eventos."""
    root.destroy()

root = tk.Tk()
root.title("Algoritmos de despacho")
root.geometry("800x500")  
root.resizable(False, False)

try:
    imagen_pil = Image.open("imagen1.jpg")
    fondo = ImageTk.PhotoImage(imagen_pil)
    background_label = tk.Label(root, image=fondo)
    background_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Error cargando imagen: {e}")
    root.configure(bg="#DED3EA")

frame = tk.Frame(root, bg="#FFFFFF", bd=5)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


btn_prioridad = tk.Button(frame, text="Algoritmo Prioridades", 
                          command=lambda: [ocultar_ventana(), generar_AlgoritmoPrioridad()],
                          font=("Arial", 12), bg="#2196F3", fg="white", width=20)

btn_fifo = tk.Button(frame, text="FIFO", 
                     command=lambda: [ocultar_ventana(), generar_fifo()],
                     font=("Arial", 12), bg="#2196F3", fg="white", width=20)

btn_sjf = tk.Button(frame, text="SJF", 
                    command=lambda: [ocultar_ventana(), generar_SJF()],
                    font=("Arial", 12), bg="#2196F3", fg="white", width=20)

btn_srtf = tk.Button(frame, text="SRTF", 
                    command=lambda: [ocultar_ventana(), generar_SRTF()],
                    font=("Arial", 12), bg="#2196F3", fg="white", width=20)

btn_rr = tk.Button(frame, text="Round Robin", 
                   command=lambda: [ocultar_ventana(), generar_RoundRobin()],
                   font=("Arial", 12), bg="#2196F3", fg="white", width=20)

btn_comparar = tk.Button(frame, text="Comparar Algoritmos", 
                         command=lambda: [ocultar_ventana(), comparar_algoritmos()],
                         font=("Arial", 12), bg="#4CAF50", fg="white", width=20)


btn_salir = tk.Button(frame, text="Salir", command=salir, 
                      font=("Arial", 12), bg="#F44336", fg="white", width=20)



btn_prioridad.pack(pady=5)
btn_fifo.pack(pady=5)
btn_sjf.pack(pady=5)
btn_srtf.pack(pady=5)
btn_rr.pack(pady=5)
btn_comparar.pack(pady=5)
btn_salir.pack(pady=5)


root.mainloop()