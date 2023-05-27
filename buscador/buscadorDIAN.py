import os
from sys import path

from selenium.webdriver.chrome.options import Options

path.append("../")

import time
from openpyxl import Workbook
from selenium import webdriver
import random
from .models import Cliente
from selenium.webdriver.common.by import By


class buscadorDIAN:
    def __init__(self, valoresBuscados, nombre_archivo):
        self.valoresBuscados = valoresBuscados
        #self.DATA = []
        self.nombre_archivo = nombre_archivo
        self.avance = 0
        self.driver = None
        self.url = "https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces"
        self.archivo = os.getcwd().split('buscador')[0]
        self.iniciar_navegador()

    def iniciar_navegador(self):
        # Configurar las opciones del controlador de ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Habilitar el modo headless para que se oculte el navegador
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
            span_dv = self.driver.find_element("id", "vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv")



            pA = span_primer_apellido.text
            sA = span_segundo_apellido.text
            pN = span_primer_nombre.text
            sN = span_segundo_nombre.text
            eR = span_estado_rut.text
            dV = span_dv.text

            fila = [valor,dV, pA, sA, pN, sN, "", eR]

            cliente = Cliente(
                nit=valor,
                dv=dV,
                apellido1=pA,
                apellido2=sA,
                nombre1=pN,
                nombre2=sN,
                razon_social='',
                estado=eR
            )
            cliente.save()

            return fila
        except:
            try:
                span_razon_zocial_rut = self.driver.find_element("id", "vistaConsultaEstadoRUT:formConsultaEstadoRUT:razonSocial")
                span_estado_rut_raz = self.driver.find_element("id", "vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado")
                span_dv_emp = self.driver.find_element("id", "vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv")

                rZ = span_razon_zocial_rut.text
                eRR = span_estado_rut_raz.text
                dvEm = span_dv_emp.text

                fila = [valor,dvEm, "", "", "", "",rZ, eRR]


                cliente = Cliente(
                    nit=valor,
                    dv=dvEm,
                    apellido1='',
                    apellido2='',
                    nombre1='',
                    nombre2='',
                    razon_social=rZ,
                    estado=eRR
                )
                cliente.save()
                return fila
            except:
                fila = [valor, "", "", "", "", "", "No Registrado"]
                return fila



    def archivo_excel(self, datos):
        workbook = Workbook()
        hoja_activa = workbook.active
        encabezados = ['NIT', 'DV', 'APELLIDO 1', 'APELLIDO 2', 'NOMBRE 1', 'NOMBRE 2', 'RAZON SOCIAL', 'ESTADO']
        hoja_activa.append(encabezados)
        #datos = self.DATA
        for fila in datos:
            hoja_activa.append(fila)

        carpeta_delos_archivos = self.archivo+'/archivos/'
        nombre_del_archivo_generado = self.nombre_archivo

        ruta_archivo = os.path.join(carpeta_delos_archivos, nombre_del_archivo_generado)
        #if os.path.exists(ruta_archivo):
        numero_aleatorio = random.randint(1000000, 9999999)
        workbook.save(ruta_archivo+str(numero_aleatorio)+'.xlsx')

        return nombre_del_archivo_generado+str(numero_aleatorio)+'.xlsx'



