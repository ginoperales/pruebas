from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import yes_no_dialog, input_dialog
from prompt_toolkit.styles import Style
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

# Interfaz interactiva
def main():
    style = Style.from_dict({
        'dialog': 'bg:#88ff88',
        'input': 'bg:#f5f5f5',
    })

    print("Bienvenido a la Calculadora de Momentos Flectores")
    longitud = float(input_dialog(
        title="Longitud de la Viga",
        text="Ingrese la longitud de la viga (m):",
        style=style,
    ).run())
    viga = Viga(longitud)

    while True:
        opcion = prompt(
            "¿Qué desea hacer?\n"
            "1. Agregar carga puntual\n"
            "2. Agregar carga distribuida\n"
            "3. Calcular y graficar momentos\n"
            "4. Salir\n"
            "Seleccione una opción: ",
            style=style,
        )

        if opcion == "1":
            carga = input_dialog(
                title="Agregar Carga Puntual",
                text="Ingrese la magnitud y posición de la carga puntual (kN, m):",
                style=style,
            ).run()
            try:
                magnitud, posicion = map(float, carga.split(","))
                viga.agregar_carga_puntual(magnitud, posicion)
                print(f"Carga puntual de {magnitud} kN agregada en {posicion} m.")
            except ValueError:
                print("Error: Entrada no válida. Intente de nuevo.")
        elif opcion == "2":
            carga = input_dialog(
                title="Agregar Carga Distribuida",
                text="Ingrese la magnitud, inicio y fin de la carga distribuida (kN/m, inicio m, fin m):",
                style=style,
            ).run()
            try:
                magnitud, inicio, fin = map(float, carga.split(","))
                viga.agregar_carga_distribuida(magnitud, inicio, fin)
                print(f"Carga distribuida de {magnitud} kN/m agregada desde {inicio} m hasta {fin} m.")
            except ValueError:
                print("Error: Entrada no válida. Intente de nuevo.")
        elif opcion == "3":
            print("Generando diagrama de momentos flectores...")
            viga.graficar_momentos()
        elif opcion == "4":
            if yes_no_dialog(
                title="Salir",
                text="¿Está seguro de que desea salir?",
                style=style,
            ).run():
                print("Gracias por usar la calculadora. ¡Hasta luego!")
                break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
