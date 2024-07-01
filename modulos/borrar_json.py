# Importaciones de librerías
import os                                               # Obtener rutas del sistema operativo
import json                                             # Trabajar con el archivo json
from pathlib import Path                                # Trabajar con las rutas
import tkinter as tk                                    # Interfaz gráfica
from tkinter import messagebox, filedialog as FD        # Por si queremos agregar la función de escoger el archivo json, mostrar mensajes
import sys                                              # Necesario para que no haya errores a la hora de importar módulos

sys.path.append('.')

from modulos.leer_archivo import Lectura_archivo        # Necesario para leer el archivo json
from modulos.generic import centrar_ventanas as centrar # Necesario para importar la función de centrar

class EliminarJson_PDF():

    def __init__(self, root):
        ''' Método para crear la ventana de Eliminar Factura
        Se le asigna un título, unas dimensiones base, se centra en el centro de la pantalla'''
        self.ventana_eliminar_por_datos = root
        self.ventana_eliminar_por_datos.title("Eliminar JSON y PDFs") # Título
        w, h = 500, 30  # Tamaño de la ventana
        centrar(self.ventana_eliminar_por_datos, w, h) # Centrado
        # Configuración del menú superior y botón Eliminar / Buscar y Eliminar       
        self.barraMenu = tk.Menu(self.ventana_eliminar_por_datos) 
        self.ventana_eliminar_por_datos.config(menu=self.barraMenu)
        self.ventana_eliminar_por_datos.resizable(False, False)

        botonCrear= tk.Button(self.ventana_eliminar_por_datos,
                                text = 'Eliminar',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.pregunta_definitiva)
        botonCrear.pack(fill = tk.X, padx = 5, pady = 5)
    
    def pregunta_definitiva(self):
        resultado = messagebox.askyesno('Cuidado!', '(¿Quieres borrarlo todo?')
        if resultado:
            self.abrir_json()

    def abrir_json(self):
        ''' Método para abrir el archivo json automáticamente:
        1) Asignamos la ruta
        2) Si existe el archivo se invoca a la clase para introducir los datos de eliminar de factura
        '''
        self.ventana_eliminar_por_datos.destroy()        
        ruta_Json = 'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_anadir_factura = Eliminar(ruta_Json)
            self.ventana_anadir_factura.eliminar_json()
class Eliminar:
    def __init__(self, ruta):
        ''' Se rescata la ruta del archivo json "facturas.json" y se carga para editarlo.'''
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)
    
    def eliminar_json(self):    
        
        contador = 0
        contadorMax = len(self.listaFacturas)
        control = True

        while control:
            if contador == contadorMax:
                contenido = json.dumps(self.listaFacturas)
                self.path.write_text(contenido)
                if contadorMax == 0:
                    messagebox.showinfo("Éxito", f"No había datos ni PDF a borrar.")
                else:
                    messagebox.showinfo("Éxito", f"Archivos (PDF y diccionarios asociados) borrados correctamente.")
                control = False

            for factura in self.listaFacturas:                         

                contador = contador + 1

                a, b = factura['numeroFactura'], factura['fecha']
                if  factura['numeroFactura'] == a and factura['fecha'] == b:
                    
                    fechaCorregida = b.replace('/', '_')
                    ruta_pdf = f"PDF/{fechaCorregida}_{a}.pdf"
                    if os.path.exists(ruta_pdf):
                        os.remove(ruta_pdf)
                        # messagebox.showinfo("Éxito", f"Archivo PDF {b}{a} borrado correctamente.")

                    self.listaFacturas.remove(factura)
                    contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
                    self.path.write_text(contenido)
                    # messagebox.showinfo("Éxito", f"Archivo diccionario del archivo json de la factura {b}{a} se ha borrado correctamente.")
