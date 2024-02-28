from proyecto_parte_1 import ExtractorArchivoCsvUrl
from proyecto_parte_2 import AnalizadorDatosArchivoCsv
from proyecto_parte_3 import AnalizadorDatosArchivoTxt

def main():
    # Parámetros de la primera clase
    usuario = "9511839"
    
    contraseña = "K67Z"
    archivo_csv = 'Proyecto 3.csv'
    directorio_destino = r'C:\Users\Dell\Desktop\PROYECTO CURSO PYTHON.1.2'

    # Instancia de la primera clase
    extractor_csv = ExtractorArchivoCsvUrl(usuario, contraseña, archivo_csv, directorio_destino)

    # Llamada a los métodos de la primera clase
    extractor_csv.iniciar_sesion()
    extractor_csv.descargar_y_descomprimir_archivo_zip()
    extractor_csv.cerrar_sesion()
    

    # Parámetros de la segunda clase
    archivo_csv = 'Proyecto 3.csv'
    archivo_txt = 'archivo.txt'

    # Instancia de la segunda clase
    analizador_csv = AnalizadorDatosArchivoCsv(archivo_csv, archivo_txt)

    # Llamada a los métodos de la segunda clase
    analizador_csv.guardar_txt()
    analizador_csv.mostrar_contenido_txt()
    analizador_csv.menu()

    # Parámetro de la tercera clase
    archivo_txt = 'archivo.txt'

    # Instancia de la tercera clase
    analizador_txt = AnalizadorDatosArchivoTxt(archivo_txt)

    # Llamada a los métodos de la tercera clase
    analizador_txt.cargar_datos()
    analizador_txt.menu()

if __name__ == "__main__":
    main()
