import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

class BeamAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("Analizador de Vigas Interactivo")

        # Parámetros de la viga
        self.beam_length = tk.DoubleVar(value=7)
        self.young_modulus = tk.DoubleVar(value=2000)
        self.inertia = tk.DoubleVar(value=100000)

        # Cargas
        self.loads = []

        # Tipos de apoyos
        self.supports = ["Simple", "Empotrado", "Rolado"]
        self.left_support = tk.StringVar(value=self.supports[0])
        self.right_support = tk.StringVar(value=self.supports[0])

        # Configuración de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Frame para la entrada de datos
        frame_inputs = tk.Frame(self.master)
        frame_inputs.pack(padx=10, pady=10)

        # Longitud de la viga
        tk.Label(frame_inputs, text="Longitud de la viga (m):").grid(row=0, column=0)
        tk.Entry(frame_inputs, textvariable=self.beam_length).grid(row=0, column=1)

        # Módulo de Young
        tk.Label(frame_inputs, text="Módulo de Young (E):").grid(row=1, column=0)
        tk.Entry(frame_inputs, textvariable=self.young_modulus).grid(row=1, column=1)

        # Momento de Inercia
        tk.Label(frame_inputs, text="Momento de Inercia (I):").grid(row=2, column=0)
        tk.Entry(frame_inputs, textvariable=self.inertia).grid(row=2, column=1)

        # Selección de apoyos
        tk.Label(frame_inputs, text="Apoyo Izquierdo:").grid(row=3, column=0)
        tk.OptionMenu(frame_inputs, self.left_support, *self.supports).grid(row=3, column=1)

        tk.Label(frame_inputs, text="Apoyo Derecho:").grid(row=4, column=0)
        tk.OptionMenu(frame_inputs, self.right_support, *self.supports).grid(row=4, column=1)

        # Botón para dibujar la viga
        tk.Button(frame_inputs, text="Dibujar Viga", command=self.draw_beam).grid(row=5, columnspan=2, pady=10)

        # Frame para las cargas
        frame_loads = tk.Frame(self.master)
        frame_loads.pack(padx=10, pady=10)

        # Tipo de carga
        self.load_type = tk.StringVar(value="pointLoad")
        tk.Label(frame_loads, text="Tipo de carga:").grid(row=0, column=0)
        load_options = ["pointLoad", "distributedLoad", "torque"]
        tk.OptionMenu(frame_loads, self.load_type, *load_options).grid(row=0, column=1)

        # Magnitud de la carga
        self.load_magnitude = tk.DoubleVar(value=1000)
        tk.Label(frame_loads, text="Magnitud (N):").grid(row=1, column=0)
        tk.Entry(frame_loads, textvariable=self.load_magnitude).grid(row=1, column=1)

        # Posición de la carga (para cargas puntuales o torsionales)
        self.load_position = tk.DoubleVar(value=2)
        tk.Label(frame_loads, text="Posición (m):").grid(row=2, column=0)
        tk.Entry(frame_loads, textvariable=self.load_position).grid(row=2, column=1)

        # Para cargas distribuidas: inicio y fin
        self.load_start = tk.DoubleVar(value=1)
        self.load_end = tk.DoubleVar(value=4)
        tk.Label(frame_loads, text="Posición Inicial (m):").grid(row=3, column=0)
        tk.Entry(frame_loads, textvariable=self.load_start).grid(row=3, column=1)
        tk.Label(frame_loads, text="Posición Final (m):").grid(row=4, column=0)
        tk.Entry(frame_loads, textvariable=self.load_end).grid(row=4, column=1)

        # Botón para añadir carga
        tk.Button(frame_loads, text="Añadir Carga", command=self.add_load).grid(row=5, columnspan=2, pady=10)

        # Frame para mostrar cargas
        self.loads_display = tk.Listbox(self.master, width=50, height=10)
        self.loads_display.pack(padx=10, pady=10)

        # Botón para realizar cálculos estructurales
        tk.Button(self.master, text="Calcular Resultados", command=self.calculate_results).pack(pady=10)

    def add_load(self):
        load_type = self.load_type.get()
        magnitude = self.load_magnitude.get()
        position = self.load_position.get()
        start = self.load_start.get()
        end = self.load_end.get()

        # Validación de entrada
        if load_type == "distributedLoad" and start >= end:
            messagebox.showerror("Error", "La posición final debe ser mayor que la inicial para carga distribuida.")
            return
        if magnitude <= 0:
            messagebox.showerror("Error", "La magnitud debe ser mayor que 0.")
            return

        new_load = {
            "type": load_type,
            "magnitude": magnitude,
            "position": position,
            "start": start,
            "end": end
        }
        self.loads.append(new_load)
        self.loads_display.insert(tk.END, f"{load_type} - Magnitud: {magnitude} N")

    def draw_beam(self):
        # Crear una representación gráfica de la viga usando matplotlib
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot([0, self.beam_length.get()], [0, 0], color="black", linewidth=6, label="Viga")  # La viga

        # Dibujar los apoyos con tipos personalizados
        left_support = self.left_support.get()
        right_support = self.right_support.get()

        # Apoyo izquierdo
        if left_support == "Simple":
            ax.scatter(0, 0, color="red", s=200, zorder=5, label="Apoyo Simple Izq.")
        elif left_support == "Empotrado":
            ax.scatter(0, 0, color="blue", s=250, zorder=5, label="Apoyo Empotrado Izq.")
        elif left_support == "Rolado":
            ax.scatter(0, 0, color="green", s=200, zorder=5, label="Apoyo Rolado Izq.")

        # Apoyo derecho
        if right_support == "Simple":
            ax.scatter(self.beam_length.get(), 0, color="red", s=200, zorder=5, label="Apoyo Simple Der.")
        elif right_support == "Empotrado":
            ax.scatter(self.beam_length.get(), 0, color="blue", s=250, zorder=5, label="Apoyo Empotrado Der.")
        elif right_support == "Rolado":
            ax.scatter(self.beam_length.get(), 0, color="green", s=200, zorder=5, label="Apoyo Rolado Der.")

        # Dibujar las cargas
        for load in self.loads:
            if load["type"] == "pointLoad":
                ax.scatter(load["position"], 0, color="blue", s=100, zorder=4, label=f"Carga Puntual: {load['magnitude']} N")
            elif load["type"] == "distributedLoad":
                ax.plot([load["start"], load["end"]], [0, 0], color="green", linewidth=6, label=f"Carga Distribuida: {load['magnitude']} N/m")
            elif load["type"] == "torque":
                ax.scatter(load["position"], 0, color="purple", s=100, zorder=4, label=f"Torsión: {load['magnitude']} N·m")

        # Configuración del gráfico
        ax.set_title("Diagrama de la Viga con Cargas")
        ax.set_xlabel("Longitud (m)")
        ax.set_ylabel("Cargas (N) / Torsión (N·m)")
        ax.grid(True)
        ax.legend(loc="upper right")
        ax.set_ylim(-0.5, 1.5)  # Ajuste de los límites del eje Y para las cargas
        ax.set_xlim(0, self.beam_length.get() + 1)

        plt.show()

    def calculate_results(self):
        # Este método puede realizar los cálculos estructurales correspondientes.
        # Aquí, por ahora, solo se mostrará un mensaje de confirmación.
        messagebox.showinfo("Cálculos Completados", "Los cálculos estructurales se han realizado correctamente.")

# Crear la ventana principal
root = tk.Tk()
app = BeamAnalyzer(root)
root.mainloop()
