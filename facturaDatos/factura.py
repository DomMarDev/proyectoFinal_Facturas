# Creamos un script para generar un archivo json

import os
from pathlib import Path
import json

from ruta import ruta

class Abrir_archivo:
    def __init__(self):
        self.ubicacion = ruta() # Ejecuta ruta
        self.archivoFacturas = Path(f'{self.ubicacion}')
        try:
            self.facturas = self.archivoFacturas.read_text() #Lo lee/hay algo?
            print('Archivo inicializado correctamente')
            os.system('pause')
        except FileNotFoundError:
            self.facturas = []
            self.contenidoFacturas = json.dumps(self.facturas, indent= 4, sort_keys= False)
            self.archivoFacturas.write_text(self.contenidoFacturas) # Creamos el archivo con el contenido de sel.usuarios, que es una lista vacía.
            print('Archivo creado!!')
            os.system('pause')

#Prueba unitaria
if __name__ == '__main__':
    miArchivo = Abrir_archivo()