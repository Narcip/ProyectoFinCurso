# proyecto_parte_1.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import zipfile
import io
import requests
import os

class ExtractorArchivoCsvUrl:
    def __init__(self, usuario, contraseña, archivo_csv, directorio_destino):
        # Constructor para inicializar atributos de la clase
        self.usuario = usuario
        self.contraseña = contraseña
        self.archivo_csv = archivo_csv
        self.directorio_destino = directorio_destino
        self.drive = None  # El navegador se inicializará en iniciar_sesion()

    def iniciar_sesion(self):
        # Método para iniciar sesión en el sitio web
        self.drive = webdriver.Chrome()
        self.drive.get('https://campus.deustoformacion.com/Inicio.aspx')
        time.sleep(2)

        # Encontrar el campo de entrada de usuario y escribir el usuario
        buscador_usuario = self.drive.find_element(By.XPATH, '//*[@id="dnn_ctr498_Login_Login_DNN_txtUsername"]')
        buscador_usuario.send_keys(self.usuario)

        # Encontrar el campo de entrada de contraseña y escribir la contraseña
        buscador_contraseña = self.drive.find_element(By.XPATH, '//*[@id="dnn_ctr498_Login_Login_DNN_txtPassword"]')
        buscador_contraseña.send_keys(self.contraseña)

        # Hacer clic en el botón de inicio de sesión
        self.drive.find_element(By.XPATH, '//*[@id="dnn_ctr498_Login_Login_DNN_cmdLogin"]').click()
        time.sleep(5)

    def descargar_y_descomprimir_archivo_zip(self):
        # Método para descargar y descomprimir el archivo ZIP
        self.drive.find_element(By.XPATH, '//*[@id="sticky-wrapper"]/div/div/nav/div/ul/li[3]/a/span').click()
        time.sleep(5)

        self.drive.find_element(By.XPATH, '//*[@id="dnn_ctr6538_HtmlModule_lblContent"]/div/div/a').click()
        time.sleep(5)

        url_archivo_zip = self.drive.find_element(By.XPATH, '//*[@id="dnn_ctr12045_HtmlModule_lblContent"]/p[2]/span/a').get_attribute('href')

        response = requests.get(url_archivo_zip)
        zip_content = response.content

        zip_in_memory = io.BytesIO(zip_content)

        if not os.path.exists(self.directorio_destino):
            os.makedirs(self.directorio_destino)

        with zipfile.ZipFile(zip_in_memory, 'r') as zip_ref:
            zip_ref.extract(self.archivo_csv, self.directorio_destino)

        print(f'Archivo CSV destino: {self.directorio_destino}')

    def cerrar_sesion(self):
        # Método para cerrar sesión y cerrar el navegador
        if self.drive:
            self.drive.quit()

# Ejemplo de uso
if __name__ == "__main__":
    usuario = "9511839"
    contraseña = "K67Z"
    archivo_csv = 'Proyecto 3.csv'
    directorio_destino = r'C:\Users\Dell\Desktop\PROYECTO CURSO PYTHON.1.2'

    # Crear una instancia de la clase
    #campus_deusto_automation = ExtractorArchivoCsvUrl(usuario, contraseña, archivo_csv, directorio_destino)

    # Iniciar sesión
    #campus_deusto_automation.iniciar_sesion()

    # Descargar el archivo ZIP y extraerlo
    #campus_deusto_automation.descargar_y_descomprimir_archivo_zip()

    # Cerrar sesión
    #campus_deusto_automation.cerrar_sesion()
