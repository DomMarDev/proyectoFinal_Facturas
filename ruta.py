# Creando ruta absoluta, la carpeta datos será archivoJson 
import os

def ruta():
    ruta_relativa = 'archivoJson/facturas.json'

    ruta_absoluta = os.path.abspath(ruta_relativa)

    return f'{ruta_absoluta}'