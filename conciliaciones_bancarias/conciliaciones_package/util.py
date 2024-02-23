
import os
import pandas as pd
from sys import path
import shutil
from django.core.files.storage import default_storage
import pandas as pd


def verificar_columnas(archivo):
    try:
        # Se lee el archivo de Excel.
        df = pd.read_excel(archivo)
        # Se verifica la cantidad de columnas.
        if len(df.columns) != 4:
          return False, "El archivo debe tener solo 4 columnas  ---- fecha ---- descripcion ---- valor ---- tipo --- "

        # Se verifica el nombre de las columnas.
        for i, columna in enumerate(["fecha", "descripcion", "valor", "tipo"]):
          if df.columns[i] != columna:
            return False, f"El archivo {archivo} debe tener solo 4 columnas  ---- fecha ---- descripcion ---- valor ---- tipo --- "

        # Se verifica el formato de la columna fecha.
        columnas_incorrectas = []
        for i, fecha in enumerate(df["fecha"]):
            try:
                # Se intenta convertir la fecha a formato datetime.
                # datetime.strptime(fecha, "%d/%m/%Y")
                pd.to_datetime(fecha)
            except ValueError:
                # La fecha no tiene el formato correcto.
                columnas_incorrectas.append(f"fecha (fila {i + 2})")

        if columnas_incorrectas:
            return False, f"La columna fecha del archivo {archivo} no tiene el formato DD/MM/AAAA {columnas_incorrectas}"

    except Exception as e:
        # Se produce una excepción si hay un error al leer el archivo.
        print(f"Error al leer el archivo: {e}")
        #break
        return False, f"Error al leer el archivo: {e}"

    return True, True


def copiar_archivo(file, carpeta_destino, token):
    # Obtener el nombre del archivo
    nombre_archivo = file.name

    # Construir la ruta completa de la carpeta destino
    ruta_carpeta_destino = os.path.join(os.path.abspath(carpeta_destino), '')

    # Construir la ruta completa del archivo en la carpeta destino
    ruta_archivo_destino = os.path.join(ruta_carpeta_destino, token+"."+nombre_archivo)

    # Guardar el archivo en la carpeta destino
    with default_storage.open(ruta_archivo_destino, 'wb') as destino:
        # Leer y escribir en bloques para archivos grandes
        for chunk in file.chunks():
            destino.write(chunk)

    return ruta_archivo_destino
