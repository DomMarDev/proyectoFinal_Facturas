# Importaciones

import os
from ruta import ruta
from facturaDatos.factura import Abrir_archivo

from funciones_json.anadir_factura import Add_factura

class Menu:
    def __init__(self):
        os.system('cls')
        self.menu = ''' 
        Agenda personal
        1) Crear factura
        2) Salir de crear factura 
        '''
        print(self.menu)

        self.opcion = input('Introduzca una opción: ')

        match(self.opcion):
            case '1':
                Add_factura(ruta())
                Add_factura.add_factura()
            case '2':
                print('Saliendo de la agenda.')
                exit() # Te cierra la terminal de Python
            case _:
                print('Opción no contemplada')
    
        os.system('pause')
        self.__init__() # Función recursiva para que te vaya imprimiendo el método de __init__

miArchivo = Abrir_archivo()
miMenu = Menu()