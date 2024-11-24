import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

class Viga:
    def __init__(self, longitud):
        self.longitud = longitud
        self.cargas_puntuales = []
        self.cargas_distribuidas = []

    def agregar_carga_puntual(self, magnitud, posicion):
        self.cargas_puntuales.append((magnitud, posicion))
    
    def agregar_carga_distribuida(self, magnitud, inicio, fin):
        self.cargas_distribuidas.append((magnitud, inicio, fin))
    
    def calcular_momentos(self):
        x = np.linspace(0, self.longitud, 500)
        momentos = np.zeros_like(x)

        for magnitud, posicion in self.cargas_puntuales:
            reacc_a, reacc_b = self.calcular_reacciones()
            momentos += np.where(
                x >= posicion,
                reacc_a * x - magnitud * (x - posicion),
                reacc_a * x
            )
        
        for magnitud, inicio, fin in self.cargas_distribuidas:
            reacc_a, reacc_b = self.calcular_reacciones()
            momentos += np.where(
                x >= inicio,
                reacc_a * x - magnitud * ((x - inicio)**2) / 2,
                reacc_a * x
            )
        
        return x, momentos
    
    def calcular_reacciones(self):
        # Calcular reacciones en apoyos para cargas puntuales
        suma_fuerzas = sum(c[0] for c in self.cargas_puntuales)
        momento_total = sum(c[0] * c[1] for c in self.cargas_puntuales)

        reacc_a = momento_total / self.longitud
        reacc_b = suma_fuerzas - reacc_a
        return reacc_a, reacc_b
    
    def graficar_momentos(self):
        x, momentos = self.calcular_momentos()
        plt.plot(x, momentos, label='Momento Flector')
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.title("Diagrama de Momentos Flectores")
        plt.xlabel("Longitud (m)")
        plt.ylabel("Momento Flector (kNm)")
        plt.legend()
        plt.grid()
        plt.show()

# Interfaz gráfica con Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Momentos Flectores")
        self.viga = None

        # Widgets
        tk.Label(root, text="Longitud de la viga (m):").grid(row=0, column=0)
        self.longitud_entry = tk.Entry(root)
        self.longitud_entry.grid(row=0, column=1)
        tk.Button(root, text="Crear Viga", command=self.crear_viga).grid(row=0, column=2)

        tk.Label(root, text="Carga Puntual: Magnitud (kN), Posición (m):").grid(row=1, column=0)
        self.carga_puntual_entry = tk.Entry(root)
        self.carga_puntual_entry.grid(row=1, column=1)
        tk.Button(root, text="Agregar Carga Puntual", command=self.agregar_carga_puntual).grid(row=1, column=2)

        tk.Label(root, text="Carga Distribuida: Magnitud (kN/m), Inicio (m), Fin (m):").grid(row=2, column=0)
        self.carga_distribuida_entry = tk.Entry(root)
        self.carga_distribuida_entry.grid(row=2, column=1)
        tk.Button(root, text="Agregar Carga Distribuida", command=self.agregar_carga_distribuida).grid(row=2, column=2)

        tk.Button(root, text="Calcular y Graficar", command=self.graficar_momentos).grid(row=3, column=1)

    def crear_viga(self):
        try:
            longitud = float(self.longitud_entry.get())
            self.viga = Viga(longitud=longitud)
            messagebox.showinfo("Éxito", f"Viga creada con longitud {longitud} m.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor numérico válido para la longitud.")

    def agregar_carga_puntual(self):
        if not self.viga:
            messagebox.showerror("Error", "Primero debe crear la viga.")
            return
        try:
            magnitud, posicion = map(float, self.carga_puntual_entry.get().split(","))
            self.viga.agregar_carga_puntual(magnitud, posicion)
            messagebox.showinfo("Éxito", f"Carga puntual de {magnitud} kN agregada en {posicion} m.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese los datos en el formato correcto (magnitud, posición).")

    def agregar_carga_distribuida(self):
        if not self.viga:
            messagebox.showerror("Error", "Primero debe crear la viga.")
            return
        try:
            magnitud, inicio, fin = map(float, self.carga_distribuida_entry.get().split(","))
            self.viga.agregar_carga_distribuida(magnitud, inicio, fin)
            messagebox.showinfo("Éxito", f"Carga distribuida de {magnitud} kN/m agregada desde {inicio} m hasta {fin} m.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese los datos en el formato correcto (magnitud, inicio, fin).")

    def graficar_momentos(self):
        if not self.viga:
            messagebox.showerror("Error", "Primero debe crear la viga y agregar cargas.")
            return
        self.viga.graficar_momentos()

# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
