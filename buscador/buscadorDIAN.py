import os
from sys import path

path.append("../")

import time
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By


class buscadorDIAN:
    def __init__(self, valoresBuscados):
        self.valoresBuscados = valoresBuscados
        self.DATA = []
        self.avance = 0
        self.driver = None
        self.url = "https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces"
        self.archivo = os.getcwd().split('buscador')[0]

    def iniciar_navegador(self):
        # Configurar las opciones del controlador de ChromeDriver
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Habilitar el modo headless para que se oculte el navegador
        # Configurar el controlador de ChromeDriver (asegúrate de tenerlo instalado y en el PATH)
        self.driver = webdriver.Chrome()  # options=chrome_options
        # Abrir la página web en el controlador del navegador
        self.driver.get(self.url)
        # Pausa de 2 segundos
        time.sleep(2)

    def cerrar_navegador(self):
        if self.driver:
            self.driver.quit()

    def unaBusqueda(self, valor):
        # Encontrar el elemento de entrada por su ID y asignarle el número
        input_element = self.driver.find_element("id", "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit")
        input_element.clear()  # Limpiar cualquier valor previo
        input_element.send_keys(valor)

        # Encontrar el botón de búsqueda y hacer clic en él
        button_element = self.driver.find_element("id", "vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar")
        button_element.click()

        # Esperar algunos segundos para que la página se cargue después de hacer clic
        self.driver.implicitly_wait(3)

        try:
            # Encontrar el elemento span por su ID y obtener su contenido
            span_primer_apellido = self.driver.find_element("id",
                                                            "vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerApellido")
            span_segundo_apellido = self.driver.find_element("id",
                                                             "vistaConsultaEstadoRUT:formConsultaEstadoRUT:segundoApellido")
            span_primer_nombre = self.driver.find_element("id",
                                                          "vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerNombre")
            span_segundo_nombre = self.driver.find_element("id",
                                                           "vistaConsultaEstadoRUT:formConsultaEstadoRUT:otrosNombres")
            span_estado_rut = self.driver.find_element("id", "vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado")

            pA = span_primer_apellido.text
            sA = span_segundo_apellido.text
            pN = span_primer_nombre.text
            sN = span_segundo_nombre.text
            eR = span_estado_rut.text

            fila = [valor, pA, sA, pN, sN, eR]
            self.DATA.append(fila)

            #print(pA, sA, pN, sN, eR)
        except:
            #print("No existe registro")
            fila = [valor, "", "", "", "", "No Registrado"]
            self.DATA.append(fila)



    def multiples_busquedas(self):
        self.iniciar_navegador()

        for nit_busqueda in self.valoresBuscados:
            self.unaBusqueda(nit_busqueda)


        self.cerrar_navegador()




    def archivo_excel(self):
        workbook = Workbook()
        hoja_activa = workbook.active

        encabezados = ['NIT', 'APELLIDO 1', 'APELLIDO 2', 'NOMBRE 1', 'NOMBRE 2', 'ESTADO']
        hoja_activa.append(encabezados)
        datos = self.DATA

        for fila in datos:
            hoja_activa.append(fila)

        workbook.save(self.archivo+'/Busqueda.xlsx')