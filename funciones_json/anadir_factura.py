import os
import json
from pathlib import Path

from funciones_json.leer_archivo import Lectura_archivo

class Add_factura:

    @classmethod #metiodo estatico
    def __init__(cls, ruta):
        os.system('cls')
        cls.path = Path(ruta)
        cls.facturas = Lectura_archivo.lee_archivo(ruta)
        cls.listaFacturas = json.loads(cls.facturas) # rescatando el archivo y lo tenemos en memoria
        # print(cls.listaUsuarios)
    
    @classmethod
    def add_factura(cls):
        cls.nombreEmpresa = input('Introduce el nombre de la empresa: ').lower().strip() # strip elimina espacios a izq y derecha, lstrip para izq, rstrip a derecha sólo
        cls.fecha = input('Introduce fecha de hoy: ').lower().strip()
        cls.cliente = input('Introduce el cliente: ').lower().strip()
        cls.dni= input('Introduce el DNI del cliente: ').lower().strip()
        cls.localizacion = input('Introduce la localización de la empresa: ').lower().strip() # strip elimina espacios a izq y derecha, lstrip para izq, rstrip a derecha sólo
        indice= 0
        cls.listaElementos = []

        while True:
            indice += 1
            opcion= input('¿Quieres añadir un elemento a la factura?\n 1)Si 2)NO')
            if opcion == '1':
                cls.unidades = input(f'Introduce el número de unidades del elemento {indice} : ').lower().strip()
                cls.elementos = input(f'Introduce el elemento {indice} : ').lower().strip()
                cls.precio = input(f'Introduce el precio del elemento {indice} : ').lower().strip()
                cls.listaElementos.append((cls.unidades, cls.elementos, cls.precio))
            else:
                break

        


        cls.datoFactura = {
            'nombreEmpresa': cls.nombreEmpresa,
            'fecha': cls.fecha,
            'cliente': cls.dni,
            'dni': cls.dni,
            'localizacion': cls.localizacion,
            'listaElementos': cls.listaElementos
        }
        cls.listaFacturas.append(cls.datoFactura) 
        cls.contenido = json.dumps(cls.listaFacturas, indent = 4, sort_keys = False)
        cls.path.write_text(cls.contenido)
