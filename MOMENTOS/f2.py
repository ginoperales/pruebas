import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

class BeamAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("Analizador de Vigas Interactivo")

        # Parámetros de la viga
        self.beam_length = tk.DoubleVar(value=7)
        self.young_modulus = tk.DoubleVar(value=2000)
        self.inertia = tk.DoubleVar(value=100000)

        # Cargas y apoyos
        self.loads = []
        self.supports = []

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

        # Botón para actualizar el gráfico
        tk.Button(frame_inputs, text="Actualizar Viga", command=self.update_plot).grid(row=5, columnspan=2, pady=10)

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

        # Botón para quitar carga
        tk.Button(frame_loads, text="Quitar Carga", command=self.remove_load).grid(row=6, columnspan=2, pady=5)

        # Frame para mostrar cargas
        self.loads_display = tk.Listbox(self.master, width=50, height=10)
        self.loads_display.pack(padx=10, pady=10)

        # Frame para los apoyos
        frame_supports = tk.Frame(self.master)
        frame_supports.pack(padx=10, pady=10)

        # Tipo de apoyo
        self.support_type = tk.StringVar(value="simpleSupport")
        tk.Label(frame_supports, text="Tipo de Apoyo:").grid(row=0, column=0)
        support_options = ["simpleSupport", "fixedSupport", "rollerSupport", "hingedSupport"]
        tk.OptionMenu(frame_supports, self.support_type, *support_options).grid(row=0, column=1)

        # Posición del apoyo
        self.support_position = tk.DoubleVar(value=0)
        tk.Label(frame_supports, text="Posición del Apoyo (m):").grid(row=1, column=0)
        tk.Entry(frame_supports, textvariable=self.support_position).grid(row=1, column=1)

        # Botón para añadir apoyo
        tk.Button(frame_supports, text="Añadir Apoyo", command=self.add_support).grid(row=2, columnspan=2, pady=10)

        # Botón para quitar apoyo
        tk.Button(frame_supports, text="Quitar Apoyo", command=self.remove_support).grid(row=3, columnspan=2, pady=5)

        # Botón para realizar cálculos estructurales
        tk.Button(self.master, text="Calcular Resultados", command=self.calculate_results).pack(pady=10)

        # Crear área para el gráfico
        self.figure, self.ax = plt.subplots(figsize=(10, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

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
        if position < 0 or position > self.beam_length.get():
            messagebox.showerror("Error", "La posición de la carga debe estar dentro de la longitud de la viga.")
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

        self.update_plot()  # Actualizar el gráfico en tiempo real

    def remove_load(self):
        try:
            selected_load_index = self.loads_display.curselection()[0]
            del self.loads[selected_load_index]
            self.loads_display.delete(selected_load_index)
            self.update_plot()  # Actualizar el gráfico en tiempo real
        except IndexError:
            messagebox.showerror("Error", "No se ha seleccionado ninguna carga para quitar.")

    def add_support(self):
        support_type = self.support_type.get()
        position = self.support_position.get()

        # Validación de entrada
        if position < 0 or position > self.beam_length.get():
            messagebox.showerror("Error", "La posición del apoyo debe estar dentro de la longitud de la viga.")
            return

        new_support = {
            "type": support_type,
            "position": position
        }
        self.supports.append(new_support)
        self.update_plot()  # Actualizar el gráfico en tiempo real

    def remove_support(self):
        try:
            selected_support_index = self.supports_display.curselection()[0]
            del self.supports[selected_support_index]
            self.update_plot()  # Actualizar el gráfico en tiempo real
        except IndexError:
            messagebox.showerror("Error", "No se ha seleccionado ningún apoyo para quitar.")

    def update_plot(self):
        # Limpiar gráfico actual
        self.ax.clear()

        # Crear una representación gráfica de la viga
        self.ax.plot([0, self.beam_length.get()], [0, 0], color="black", linewidth=4)

        # Dibujar los apoyos
        for support in self.supports:
            if support["type"] == "simpleSupport":
                self.ax.scatter(support["position"], 0, color="blue", s=200, zorder=5, label="Apoyo Simple")
            elif support["type"] == "fixedSupport":
                self.ax.scatter(support["position"], 0, color="red", s=200, zorder=5, label="Apoyo Fijo")
            elif support["type"] == "rollerSupport":
                self.ax.scatter(support["position"], 0, color="green", s=200, zorder=5, label="Apoyo Deslizante")
            elif support["type"] == "hingedSupport":
                self.ax.scatter(support["position"], 0, color="purple", s=200, zorder=5, label="Apoyo Articulado")

        # Dibujar las cargas
        for load in self.loads:
            if load["type"] == "pointLoad":
                self.ax.annotate(f"{load['magnitude']} N", (load["position"], 0.1),
                                 color="green", fontsize=12, ha="center", va="bottom", 
                                 arrowprops=dict(arrowstyle="->", color="green"))
            elif load["type"] == "distributedLoad":
                self.ax.plot([load["start"], load["end"]], [0.1, 0.1], color="orange", linewidth=6, label="Carga Distribuida")
            elif load["type"] == "torque":
                self.ax.annotate("Torque", (load["position"], 0.1), color="purple", fontsize=12, ha="center")

        # Actualizar el gráfico
        self.ax.set_xlim(-0.5, self.beam_length.get() + 0.5)
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_title("Gráfico de la Viga con Cargas y Apoyos")
        self.ax.legend(loc="upper left")
        self.canvas.draw()

    def calculate_results(self):
        # Realizar un cálculo estructural simple de las reacciones en los apoyos
        total_load = sum([load["magnitude"] for load in self.loads])
        left_reaction = total_load / 2
        right_reaction = total_load / 2

        # Mostrar resultados básicos
        result_message = f"Reacción en Apoyo Izquierdo: {left_reaction} N\n"
        result_message += f"Reacción en Apoyo Derecho: {right_reaction} N"

        messagebox.showinfo("Resultados del Cálculo", result_message)


# Crear la ventana principal
root = tk.Tk()
app = BeamAnalyzer(root)
root.mainloop()
