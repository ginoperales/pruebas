import ipywidgets as widgets
import matplotlib.pyplot as plt
from indeterminatebeam import Beam, Support, PointLoadV, DistributedLoadV, PointTorque

# Crear la viga
beam = Beam(7)  # Longitud de la viga

# Soportes y cargas iniciales
a = Support(5, (1, 1, 0))  # Soporte tipo pin en x=5 m
b = Support(0, (0, 1, 0))  # Soporte tipo rodillo en x=0 m
c = Support(7, (1, 1, 1))  # Soporte fijo en x=7 m
beam.add_supports(a, b, c)

# Funciones para actualizar las cargas y la viga interactivamente
def update_beam(length=7, point_load_mag=1000, point_load_pos=2, udl_mag=2000, udl_start=1, udl_end=4, torque_mag=2000, torque_pos=3.5):
    # Limpiar los elementos actuales
    beam.clear_loads()
    beam.clear_supports()

    # Actualizar la longitud de la viga
    beam = Beam(length)

    # Agregar los soportes
    a = Support(5, (1, 1, 0))
    b = Support(0, (0, 1, 0))
    c = Support(length, (1, 1, 1))  # Soporte fijo en el final
    beam.add_supports(a, b, c)

    # Agregar las cargas
    load_1 = PointLoadV(point_load_mag, point_load_pos)  # Carga puntual
    load_2 = DistributedLoadV(udl_mag, (udl_start, udl_end))  # Carga distribuida
    load_3 = PointTorque(torque_mag, torque_pos)  # Torque puntual
    beam.add_loads(load_1, load_2, load_3)

    # Analizar la viga
    beam.analyse()

    # Graficar los resultados
    fig_1 = beam.plot_beam_external()
    fig_2 = beam.plot_beam_internal()

    fig_1.show()
    fig_2.show()

# Crear widgets interactivos para los parámetros
length_slider = widgets.FloatSlider(value=7, min=5, max=10, step=0.1, description='Longitud de la viga (m):')
point_load_slider = widgets.FloatSlider(value=1000, min=0, max=5000, step=100, description='Magnitud carga puntual (N):')
point_load_pos_slider = widgets.FloatSlider(value=2, min=0, max=length_slider.value, step=0.1, description='Posición carga puntual (m):')
udl_mag_slider = widgets.FloatSlider(value=2000, min=0, max=5000, step=100, description='Magnitud UDL (N/m):')
udl_start_slider = widgets.FloatSlider(value=1, min=0, max=length_slider.value, step=0.1, description='Inicio UDL (m):')
udl_end_slider = widgets.FloatSlider(value=4, min=0, max=length_slider.value, step=0.1, description='Fin UDL (m):')
torque_mag_slider = widgets.FloatSlider(value=2000, min=0, max=5000, step=100, description='Magnitud torque (N.m):')
torque_pos_slider = widgets.FloatSlider(value=3.5, min=0, max=length_slider.value, step=0.1, description='Posición torque (m):')

# Enlazar los widgets con la función de actualización
widgets.interactive(update_beam,
                    length=length_slider,
                    point_load_mag=point_load_slider,
                    point_load_pos=point_load_pos_slider,
                    udl_mag=udl_mag_slider,
                    udl_start=udl_start_slider,
                    udl_end=udl_end_slider,
                    torque_mag=torque_mag_slider,
                    torque_pos=torque_pos_slider)
