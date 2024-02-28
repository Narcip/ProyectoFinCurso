import csv
import json
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd

class AnalizadorDatosArchivoCsv:
    def __init__(self, archivo_csv='Proyecto 3.csv', archivo_txt='archivo.txt'):
        # Constructor de la clase, establece los nombres de los archivos y obtiene datos agrupados
        self.archivo_csv = archivo_csv
        self.archivo_txt = archivo_txt
        self.datos_agrupados = self.filtrar_agrupar_datos()

    def cargar_datos_desde_csv(self):
        # Método para cargar datos desde un archivo CSV y manejar excepciones
        resultado = []
        try:
            with open(self.archivo_csv, encoding='utf-8') as archivo:
                lectura = csv.DictReader(archivo)
                for fila in lectura:
                    resultado.append(fila)
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo '{self.archivo_csv}'.")
            exit()
        except Exception as e:
            print(f"Error al leer el archivo CSV: {type(e).__name__} - {e}")
            exit()

        return resultado

    def filtrar_agrupar_datos(self):
        # Método para filtrar y agrupar datos desde el archivo CSV
        datos = self.cargar_datos_desde_csv()
        datos_agrupados = defaultdict(lambda: defaultdict(lambda: {'Defunciones': 0, 'Nuevos Casos Covid': 0, 'Hospitalizaciones': 0, 'Hospitalizados UCI': 0}))

        for fila in datos:
            try:
                # Extraer información relevante de cada fila
                fecha_str = fila['date']
                provincia = fila['province']

                # Convertir la fecha a un objeto datetime y obtener el día de la semana
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
                dia_semana = fecha_obj.strftime('%A')

                # Actualizar los datos agrupados con la información de la fila
                datos_agrupados[provincia][dia_semana]['Defunciones'] += int(fila['num_def'])
                datos_agrupados[provincia][dia_semana]['Nuevos Casos Covid'] += int(fila['new_cases'])
                datos_agrupados[provincia][dia_semana]['Hospitalizaciones'] += int(fila['num_hosp'])
                datos_agrupados[provincia][dia_semana]['Hospitalizados UCI'] += int(fila['num_uci'])
            except (KeyError, ValueError) as e:
                # Manejar errores si alguna clave no está presente o si hay un problema con la conversión a entero
                print(f"Error procesando fila: {fila}. Motivo: {type(e).__name__} - {e}")

        return datos_agrupados

    def guardar_txt(self):
        # Método para guardar los datos agrupados en un archivo de texto en formato JSON
        with open(self.archivo_txt, 'w', encoding='utf-8') as txt:
            json.dump(self.datos_agrupados, txt, indent=2, ensure_ascii=False)

    def mostrar_contenido_txt(self):
        # Método para mostrar el contenido del archivo de texto JSON
        with open(self.archivo_txt, 'r', encoding='utf-8') as txt:
            contenido = txt.read()
            df = pd.read_json(contenido)

            for day, row in df.iterrows():
                print(f"Día: {day}")
                print()

                for column, dictionary in row.items():
                    print(f"  Provincia: {column}")

                    for key, value in dictionary.items():
                        print(f"     {key}: {value}")
                    print()

    def mostrar_grafica(self, opcion):
        # Método para mostrar una gráfica según la opción seleccionada
        provincias = list(self.datos_agrupados.keys())
        provincia = input('Dime de qué provincia quieres la gráfica: ').capitalize()
        dias = list(next(iter(self.datos_agrupados.values())).keys())

        for i in provincias:
            if i == provincia:
                valores = [self.datos_agrupados[provincia][dia][opcion] for dia in dias]
                
                plt.figure(figsize=(12, 6))
                plt.plot(dias, valores, marker='o', linestyle='-', label=provincia)

                plt.title(f"Acumulado de {opcion.replace('_', ' ')} en {provincia}")
                plt.xlabel("Días")
                plt.ylabel(f"Acumulado de {opcion.replace('_', ' ')}")
                plt.legend()
                plt.grid(True)

        plt.show()

    def menu(self):
        while True:
            try:
                opcion = int(input("""\n
                    ¿Qué gráfica quieres visualizar?
                    1. Acumulado de Fallecimientos
                    2. Acumulado de Nuevos Casos de COVID-19
                    3. Acumulado de Hospitalizados
                    4. Acumulado de Hospitalizados en UCI
                    5. Salir
                    """))

                if opcion == 5:
                    break
                elif opcion in range(1, 5):
                    variables = ['Defunciones', 'Nuevos Casos Covid', 'Hospitalizaciones', 'Hospitalizados UCI']
                    variable = variables[opcion - 1]
                    self.mostrar_grafica(variable)
                else:
                    print("Opción no válida. Intente de nuevo.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

#Descomentar y ejecutar el bloque siguiente si se desea utilizar la clase directamente
# try:
#     analizador = AnalizadorDatosArchivoCsv()
#     analizador.guardar_txt()
#     analizador.mostrar_contenido_txt()
#     analizador.menu()
# except Exception as e:
#     print(f"Error inesperado: {type(e).__name__} - {e}")
