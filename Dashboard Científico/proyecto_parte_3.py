import pandas as pd
import matplotlib.pyplot as plt

class AnalizadorDatosArchivoTxt:
    def __init__(self, archivo):
        # Constructor de la clase, inicializa el nombre del archivo y los datos
        self.archivo = archivo
        self.datos = None

    def cargar_datos(self):
        # Método para cargar datos desde el archivo JSON
        with open(self.archivo, 'r', encoding='utf-8') as file:
            self.datos = pd.read_json(file)

    def obtener_ciudades_con_mas_estadisticas(self, tipo_estadistica):
        # Método para calcular la ciudad con más y menos estadísticas
        suma_por_ciudad = {}
        total_casos_todas_ciudades = 0  
    
        for ciudad, datos_ciudad in self.datos.items():
            suma_por_ciudad[ciudad] = 0
        
            for dia, estadisticas_dia in datos_ciudad.items():
                # Obtener el valor de la estadística para el día, o 0 si no está presente
                valor_estadistica = estadisticas_dia.get(tipo_estadistica, 0)
                suma_por_ciudad[ciudad] += valor_estadistica
                total_casos_todas_ciudades += valor_estadistica

        # Encontrar la ciudad con más y menos casos
        ciudad_con_mas_casos = max(suma_por_ciudad, key=suma_por_ciudad.get)        
        ciudad_con_menos_casos = min(suma_por_ciudad, key=suma_por_ciudad.get)
        
        casos_ciudad_con_mas_casos = suma_por_ciudad[ciudad_con_mas_casos]
        casos_ciudad_con_menos_casos = suma_por_ciudad[ciudad_con_menos_casos]
    
        # Imprimir resultados
        print(f"Ciudad con más {tipo_estadistica}: {ciudad_con_mas_casos} ({casos_ciudad_con_mas_casos} casos)")
        print(f"Total acumulado para todas las ciudades: {total_casos_todas_ciudades}")
    
        return casos_ciudad_con_mas_casos, casos_ciudad_con_menos_casos, ciudad_con_mas_casos, ciudad_con_menos_casos, total_casos_todas_ciudades

    def visualizar_datos_en_pastel(self, casos_ciudad, ciudad, ciudad_con_menos_casos, total_todas_ciudades, etiquetas, estadistica):
        # Método para visualizar datos en un gráfico de pastel
        valores = [casos_ciudad, (total_todas_ciudades - casos_ciudad)]
    
        plt.figure(figsize=(10, 6))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title(f'Comparacion de {estadistica} Entre la Ciudad con mas Casos y el Total de Casos')
        plt.show()
    
        print(f"Ciudad con más {estadistica}: {ciudad}")
        print(f"Ciudad con menos {estadistica}: {ciudad_con_menos_casos}")

    def menu(self):
        # Método para mostrar un menú de opciones y realizar análisis
        while True:
            print("""\n¿Qué gráfica quieres visualizar?
                1. Más Fallecimientos
                2. Más Nuevos Casos de COVID-19
                3. Más Hospitalizados
                4. Más Hospitalizados en UCI
                5. Salir""")
            
            try:
                opcion = int(input("Ingrese el número de la opción deseada: "))
            except ValueError:
                print("Error: Ingrese un número válido.")
                continue

            if opcion == 5:
                break
            elif opcion in range(1, 5):
                variables = ['Defunciones', 'Nuevos Casos Covid', 'Hospitalizaciones', 'Hospitalizados UCI']
                tipo_estadistica = variables[opcion - 1]
                casos_ciudad, _, ciudad_con_mas_casos, ciudad_con_menos_casos, total_casos_todas_ciudades = self.obtener_ciudades_con_mas_estadisticas(tipo_estadistica)
                etiquetas = [ciudad_con_mas_casos, 'Resto De Provincias']
                self.visualizar_datos_en_pastel(casos_ciudad, ciudad_con_mas_casos, ciudad_con_menos_casos, total_casos_todas_ciudades, etiquetas, tipo_estadistica)
            else:
                print("Opción no válida. Intente de nuevo")

# if __name__ == "__main__":
#     try:
#         analisis_ciudades = AnalizadorDatosArchivoTxt('archivo.txt')
#         analisis_ciudades.cargar_datos()
#         analisis_ciudades.menu()
#     except Exception as e:
#         print(f"Error inesperado: {e}")
