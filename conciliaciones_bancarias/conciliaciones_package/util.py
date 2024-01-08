
import os
import pandas as pd
from sys import path
import shutil
from django.core.files.storage import default_storage


def verificar_columnas(archivo):
    df = pd.read_excel(archivo)
    return (
        len(df.columns) == 4
        and df.columns[0] == "fecha"
        and df.columns[1] == "descripcion"
        and df.columns[2] == "valor"
        and df.columns[3] == "tipo"
    )


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
