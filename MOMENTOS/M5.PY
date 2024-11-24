import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons
import numpy as np


class Viga:
    def __init__(self, longitud):
        self.longitud = longitud
        self.cargas_puntuales = []
        self.cargas_distribuidas = []
        self.momentos_concentrados = []

    def agregar_carga_puntual(self, magnitud, posicion):
        self.cargas_puntuales.append((magnitud, posicion))

    def agregar_carga_distribuida(self, tipo, intensidad_inicio, intensidad_fin, inicio, fin):
        self.cargas_distribuidas.append((tipo, intensidad_inicio, intensidad_fin, inicio, fin))

    def agregar_momento_concentrado(self, magnitud, posicion):
        self.momentos_concentrados.append((magnitud, posicion))

    def calcular_momentos(self):
        x = np.linspace(0, self.longitud, 500)
        momentos = np.zeros_like(x)

        # Cargas puntuales
        for magnitud, posicion in self.cargas_puntuales:
            momentos += np.where(
                x >= posicion,
                magnitud * (x - posicion),
                0,
            )

        # Cargas distribuidas
        for tipo, intensidad_inicio, intensidad_fin, inicio, fin in self.cargas_distribuidas:
            if tipo == "Uniforme":
                q_prom = (intensidad_inicio + intensidad_fin) / 2
                momentos += np.where(
                    (x >= inicio) & (x <= fin),
                    q_prom * (fin - inicio) * (x - inicio),
                    0,
                )
            elif tipo == "Triangular":
                # Simplificación de una carga distribuida triangular
                momentos += np.where(
                    (x >= inicio) & (x <= fin),
                    (intensidad_inicio * (fin - x) + intensidad_fin * (x - inicio)) / (fin - inicio),
                    0,
                )

        return x, momentos


class InterfazGrafica:
    def __init__(self, viga):
        self.viga = viga
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.subplots_adjust(left=0.3, bottom=0.3)  # Espacio para widgets
        self.zoom_factor = 1.0
        self.init_grafico()
        self.crear_widgets()

        # Conectar evento de scroll del mouse
        self.fig.canvas.mpl_connect("scroll_event", self.zoom_dinamico)

    def init_grafico(self):
        self.ax.set_xlim(0, self.viga.longitud)
        self.ax.set_ylim(-10, 10)
        self.ax.set_title("Manipulación Gráfica de Cargas en la Viga")
        self.ax.set_xlabel("Longitud (m)")
        self.ax.set_ylabel("Momento Flector (kNm)")
        self.ax.axhline(0, color="black", linewidth=0.8, linestyle="--")

    def ajustar_vista(self):
        posiciones = [c[1] for c in self.viga.cargas_puntuales]
        momentos = [c[0] for c in self.viga.cargas_puntuales]
        if not posiciones:
            return

        min_x, max_x = min(posiciones), max(posiciones)
        min_y, max_y = min(momentos), max(momentos)

        margen_x = (max_x - min_x) * 0.1 if max_x != min_x else 1
        margen_y = (max_y - min_y) * 0.1 if max_y != min_y else 1

        self.ax.set_xlim(max(0, min_x - margen_x), min(self.viga.longitud, max_x + margen_x))
        self.ax.set_ylim(min_y - margen_y, max_y + margen_y)

    def dibujar_cargas(self):
        self.ax.clear()
        self.init_grafico()

        # Dibujar cargas puntuales
        for magnitud, posicion in self.viga.cargas_puntuales:
            self.ax.scatter(posicion, magnitud, color="red", s=100)
            self.ax.text(posicion, magnitud + 0.5, f"{magnitud} kN", ha="center", fontsize=9)

        # Dibujar diagrama de momentos
        x, momentos = self.viga.calcular_momentos()
        self.ax.plot(x, momentos, label="Momento Flector", color="blue")

        self.ax.legend()
        self.fig.canvas.draw()

    def crear_widgets(self):
        # Widget para ingresar longitud de la viga
        self.ax_longitud = self.fig.add_axes([0.05, 0.85, 0.2, 0.05])
        self.caja_longitud = TextBox(self.ax_longitud, "Longitud Viga (m)", initial=str(self.viga.longitud))
        self.caja_longitud.on_submit(self.cambiar_longitud)

        # Widgets para agregar carga
        self.ax_radio = self.fig.add_axes([0.05, 0.7, 0.2, 0.2])
        self.radio_tipo_carga = RadioButtons(self.ax_radio, ("Puntual", "Distribuida", "Momento"))
        self.radio_tipo_carga.on_clicked(self.actualizar_widgets_carga)

        # Widgets de carga distribuida (inicialmente ocultos)
        self.ax_tipo_dist = self.fig.add_axes([0.05, 0.55, 0.2, 0.05])
        self.caja_tipo_dist = TextBox(self.ax_tipo_dist, "Tipo de Carga (Uniforme/Triangular)", initial="")
        self.ax_pos_ini = self.fig.add_axes([0.05, 0.48, 0.2, 0.05])
        self.caja_pos_ini = TextBox(self.ax_pos_ini, "Inicio", initial="0")
        self.ax_pos_fin = self.fig.add_axes([0.05, 0.41, 0.2, 0.05])
        self.caja_pos_fin = TextBox(self.ax_pos_fin, "Fin", initial="2")

        # Carga puntual
        self.ax_caja_pos = self.fig.add_axes([0.05, 0.35, 0.2, 0.05])
        self.caja_posicion = TextBox(self.ax_caja_pos, "Posición", initial="0")
        self.ax_caja_magnitud = self.fig.add_axes([0.05, 0.28, 0.2, 0.05])
        self.caja_magnitud = TextBox(self.ax_caja_magnitud, "Magnitud", initial="0")

        self.ax_agregar = self.fig.add_axes([0.05, 0.2, 0.2, 0.05])
        self.boton_agregar = Button(self.ax_agregar, "Agregar Carga")
        self.boton_agregar.on_clicked(self.agregar_carga)

        # Botón para limpiar el gráfico
        self.ax_limpiar = self.fig.add_axes([0.05, 0.1, 0.2, 0.05])
        self.boton_limpiar = Button(self.ax_limpiar, "Limpiar")
        self.boton_limpiar.on_clicked(self.limpiar)

        # Botón para ajustar vista automáticamente
        self.ax_auto_ajuste = self.fig.add_axes([0.05, 0.05, 0.2, 0.05])
        self.boton_auto_ajuste = Button(self.ax_auto_ajuste, "Autoajustar")
        self.boton_auto_ajuste.on_clicked(self.auto_ajustar)

        # Botones de Zoom
        self.ax_zoom_in = self.fig.add_axes([0.05, 0.0, 0.09, 0.05])
        self.boton_zoom_in = Button(self.ax_zoom_in, "Zoom In")
        self.boton_zoom_in.on_clicked(self.zoom_in)

        self.ax_zoom_out = self.fig.add_axes([0.16, 0.0, 0.09, 0.05])
        self.boton_zoom_out = Button(self.ax_zoom_out, "Zoom Out")
        self.boton_zoom_out.on_clicked(self.zoom_out)

    def actualizar_widgets_carga(self, label):
        if label == "Distribuida":
            # Mostrar las opciones de tipo de carga y posiciones
            self.ax_tipo_dist.set_visible(True)
            self.ax_pos_ini.set_visible(True)
            self.ax_pos_fin.set_visible(True)
        else:
            # Ocultar las opciones si no es una carga distribuida
            self.ax_tipo_dist.set_visible(False)
            self.ax_pos_ini.set_visible(False)
            self.ax_pos_fin.set_visible(False)

        self.fig.canvas.draw()

    def agregar_carga(self, event):
        tipo_carga = self.radio_tipo_carga.value_selected
        if tipo_carga == "Puntual":
            posicion = float(self.caja_posicion.text)
            magnitud = float(self.caja_magnitud.text)
            self.viga.agregar_carga_puntual(magnitud, posicion)
        elif tipo_carga == "Distribuida":
            tipo = self.caja_tipo_dist.text
            inicio = float(self.caja_pos_ini.text)
            fin = float(self.caja_pos_fin.text)
            intensidad_inicio = float(self.caja_magnitud.text.split()[0])  # Suposición: valor único para la carga
            intensidad_fin = intensidad_inicio
            self.viga.agregar_carga_distribuida(tipo, intensidad_inicio, intensidad_fin, inicio, fin)
        self.dibujar_cargas()

    def limpiar(self, event):
        self.viga = Viga(self.viga.longitud)
        self.dibujar_cargas()

    def cambiar_longitud(self, longitud):
        self.viga.longitud = float(longitud)
        self.dibujar_cargas()

    def auto_ajustar(self, event):
        self.ajustar_vista()
        self.dibujar_cargas()

    def zoom_in(self, event):
        self.zoom_factor *= 1.2
        self.ax.set_xlim(self.ax.get_xlim()[0] * 1.2, self.ax.get_xlim()[1] * 1.2)
        self.ax.set_ylim(self.ax.get_ylim()[0] * 1.2, self.ax.get_ylim()[1] * 1.2)
        self.fig.canvas.draw()

    def zoom_out(self, event):
        self.zoom_factor /= 1.2
        self.ax.set_xlim(self.ax.get_xlim()[0] * 0.8, self.ax.get_xlim()[1] * 0.8)
        self.ax.set_ylim(self.ax.get_ylim()[0] * 0.8, self.ax.get_ylim()[1] * 0.8)
        self.fig.canvas.draw()

    def zoom_dinamico(self, event):
        factor_zoom = 1.1 if event.button == 'up' else 0.9
        self.zoom_factor *= factor_zoom
        self.ax.set_xlim(self.ax.get_xlim()[0] * factor_zoom, self.ax.get_xlim()[1] * factor_zoom)
        self.ax.set_ylim(self.ax.get_ylim()[0] * factor_zoom, self.ax.get_ylim()[1] * factor_zoom)
        self.fig.canvas.draw()


if __name__ == "__main__":
    viga = Viga(10)  # Longitud inicial de la viga
    app = InterfazGrafica(viga)
    plt.show()
