import matplotlib.pyplot as plt
import numpy as np


class Viga:
    def __init__(self, longitud):
        self.longitud = longitud
        self.cargas_puntuales = []
        self.cargas_distribuidas = []

    def agregar_carga_puntual(self, magnitud, posicion):
        self.cargas_puntuales.append((magnitud, posicion))

    def eliminar_carga_puntual(self, posicion):
        self.cargas_puntuales = [
            carga for carga in self.cargas_puntuales if abs(carga[1] - posicion) > 0.1
        ]

    def calcular_momentos(self):
        x = np.linspace(0, self.longitud, 500)
        momentos = np.zeros_like(x)

        for magnitud, posicion in self.cargas_puntuales:
            reacc_a, _ = self.calcular_reacciones()
            momentos += np.where(
                x >= posicion,
                reacc_a * x - magnitud * (x - posicion),
                reacc_a * x,
            )

        return x, momentos

    def calcular_reacciones(self):
        suma_fuerzas = sum(c[0] for c in self.cargas_puntuales)
        momento_total = sum(c[0] * c[1] for c in self.cargas_puntuales)

        reacc_a = momento_total / self.longitud
        reacc_b = suma_fuerzas - reacc_a
        return reacc_a, reacc_b


class InterfazGrafica:
    def __init__(self, viga):
        self.viga = viga
        self.fig, self.ax = plt.subplots()
        self.selected_carga = None

    def iniciar(self):
        self.ax.set_xlim(0, self.viga.longitud)
        self.ax.set_ylim(-10, 10)
        self.ax.set_title("Manipulación de Cargas en la Viga")
        self.ax.set_xlabel("Longitud (m)")
        self.ax.set_ylabel("Carga / Momento")
        self.ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.dibujar_cargas()
        plt.show()

    def dibujar_cargas(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.viga.longitud)
        self.ax.set_ylim(-10, 10)
        self.ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        self.ax.set_title("Manipulación de Cargas en la Viga")
        self.ax.set_xlabel("Longitud (m)")
        self.ax.set_ylabel("Carga / Momento")

        # Dibujar cargas puntuales
        for magnitud, posicion in self.viga.cargas_puntuales:
            self.ax.scatter(posicion, magnitud, color="red", s=100, label="Carga Puntual")
            self.ax.text(
                posicion, magnitud + 0.5, f"{magnitud} kN", ha="center", fontsize=9
            )

        # Dibujar diagrama de momentos flectores
        x, momentos = self.viga.calcular_momentos()
        self.ax.plot(x, momentos, label="Momento Flector", color="blue")

        self.ax.legend()
        self.fig.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        # Detectar si se hace clic sobre una carga puntual
        for magnitud, posicion in self.viga.cargas_puntuales:
            if abs(event.xdata - posicion) < 0.2:
                self.selected_carga = (magnitud, posicion)
                return

        # Si no se selecciona una carga, agregar una nueva
        nueva_carga_magnitud = float(input("Ingrese la magnitud de la carga puntual (kN): "))
        self.viga.agregar_carga_puntual(nueva_carga_magnitud, event.xdata)
        self.dibujar_cargas()

    def on_motion(self, event):
        if self.selected_carga and event.inaxes == self.ax:
            # Mover la carga seleccionada
            magnitud, _ = self.selected_carga
            nueva_posicion = event.xdata
            self.viga.eliminar_carga_puntual(self.selected_carga[1])
            self.viga.agregar_carga_puntual(magnitud, nueva_posicion)
            self.dibujar_cargas()

    def on_release(self, event):
        if self.selected_carga:
            self.selected_carga = None


# Crear la viga e iniciar la interfaz
if __name__ == "__main__":
    longitud_viga = float(input("Ingrese la longitud de la viga (m): "))
    viga = Viga(longitud_viga)
    interfaz = InterfazGrafica(viga)
    interfaz.iniciar()
