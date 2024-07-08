# Importaciones de librerías
import os                                               # Obtener rutas del sistema operativo
import json                                             # Trabajar con el archivo json
from pathlib import Path                                # Trabajar con las rutas
import tkinter as tk                                    # Interfaz gráfica
from tkinter import messagebox, filedialog as FD        # Por si queremos agregar la función de escoger el archivo json, mostrar mensajes
import sys                                              # Necesario para que no haya errores a la hora de importar módulos
from fpdf import FPDF                                   # Necesario para crear el archivo PDF
from datetime import date                               # Necesario para manejar fechas

sys.path.append('.')

from modulos.generic import centrar_ventanas as centrar # Necesario para importar la función de centrar
from modulos.leer_archivo import Lectura_archivo        # Necesario para leer el archivo json
from modulos.colores_y_rutas import *                   # Necesario para autoasignar ciertos campos de la factura
from ruta import ruta                                   # Se importa la ruta del archivo json
from pathlib import Path
import random

from modulos. creacionPDF import crear_pdf as CPDF
class ModificarFactura():

    def __init__(self, root):
        ''' Método para crear la ventana de Modificar Factura
        Se le asigna un título, unas dimensiones base, se centra en el centro de la pantalla'''        
        self.ventana_buscar_por_datos = root
        self.ventana_buscar_por_datos.title("Modificar Factura") # Título
        w, h = 500, 100  # Tamaño de la ventana
        centrar(self.ventana_buscar_por_datos, w, h) # Centrado
        # Configuración del menú superior y botón Buscar y Modificar
        self.barraMenu = tk.Menu(self.ventana_buscar_por_datos)
        self.ventana_buscar_por_datos.config(menu=self.barraMenu)
        self.ventana_buscar_por_datos.resizable(False,False)

        botonBuscarModificar= tk.Button(self.ventana_buscar_por_datos,
                                text = 'Buscar y Modificar',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.abrir_PDF)
        botonBuscarModificar.pack(fill = tk.X, padx = 20, pady = 30)

        self.menuArchivo = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Archivo", menu=self.menuArchivo)
        self.menuArchivo.add_command(label="Abrir PDF de Facturas", command=self.abrir_PDF)
        self.menuArchivo.add_separator()
        self.menuArchivo.add_command(label="Salir", command=self.ventana_buscar_por_datos.destroy)

    def abrir_PDF(self):
        ''' Método para abrir el archivo PDF manualmente:
        1) Asignamos la ruta del json (necesaria)
        2) Obtenemos la ruta absoluta del archivo PDF seleccionado
        3) Se obtiene el nombre del archivo PDF sin extensión .pdf
        4) Si existe el archivo se invoca a la clase para buscar la factura, pero la versión 2 donde no introducimos datos para buscar la factura
        '''
        self.ventana_buscar_por_datos.destroy()
        ruta_Json = 'archivoJson/facturas.json'        
        ruta_PDF   = FD.askopenfilename(title="Selecciona la factura a modificar", filetypes=[("Archivo PDF", "*.pdf"),], initialdir= 'PDF')
        nombre_PDF = Path(ruta_PDF).stem
        if ruta_Json:
            self.ventana_modificar_factura = Modificar(ruta_Json)
            self.ventana_modificar_factura.buscar_factura2(nombre_PDF)
    

class Modificar:

    def __init__(self, ruta):
        ''' Se rescata la ruta del archivo json "facturas.json" y se carga para editarlo.'''
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)

    # def modificar_factura(self):
    #     ''' Método para modificar los datos de una factura:
    #     Al usuario se le pide:
    #         -1) Número de la Factura
    #         -2) Cliente de la Factura
    #         -3) DNI/CIF del cliente
    #         -4) Unidades/Concepto(s)/Precio Unidad        
    #     '''
    #     # / Genero una ventana por encima de la del menú principal.         
    #     self.ventana_ModificarFactura = tk.Toplevel() # Uso la clase Toplevel de tkinter
    #     self.ventana_ModificarFactura.title("Modificar Factura") # Asigno el título Modificar factura a esta ventana
    #     w, h = 500, 300  # Tamaño de la ventana
    #     centrar(self.ventana_ModificarFactura, w, h) # Llamo a la función centrar para que me centre la ventana en el centro de la pantalla

    #     # / Pido la entrada de datos
    #     self.numeroFactura = self.entradaDatos(self.ventana_ModificarFactura, "Introduce número de factura: ")
    #     self.fecha = self.entradaDatos(self.ventana_ModificarFactura, "Introduce la fecha (dd/mm/yyyy): ")
    #             # /// Se hace un botón para los buscar facturas, se le asigna el comando buscar_factura y se empaqueta luego   
    #     self.botonBuscar = tk.Button(self.ventana_ModificarFactura, text="Buscar Factura", command=self.buscar_factura)
    #     self.botonBuscar.pack(pady=10)
        
    def entradaDatos(self, ventana_ModificarFactura, texto):
        ''' Método para hacer la entrada de datos:
        1) Se crea el frame dentro de la ventana_ModificarFactura y se empaqueta
        2) Se crea la etigueta del dato pedido que se obtiene gracias a que se lo pasamos por los parámetros y se empaqueta
        3) Se crea la entrada para el dato y se empaqueta
        
        Se devuelve la entrada 
        '''        
        frame = tk.Frame(ventana_ModificarFactura)
        frame.pack(pady=5)
        label = tk.Label(frame, text=texto)
        label.pack(side=tk.LEFT)
        entrada = tk.Entry(frame, width=50)
        entrada.pack(side=tk.LEFT)
        return entrada

    # def buscar_factura(self):
    #     ''' Método 1 para buscar una factura introduciendo los datos de búsqueda de la factura:
    #     Se importan los datos introducidos en método de modificar_factura:
    #         1) Número de la factura
    #         2) Fecha de la factura
    #     Se recorre la lista de diccionarios de las facturas creadas y si coincide el número de la factura y la fecha:
    #         1) Se asigna a la variable facturaEncontrada el diccionario correspondiente a la factura
    #         2) Se invoca al método para modificar los datos y elementos de la factura (formulario_edicion)
    #     Si no coincide alguno de los datos va a decir que no se pudo encontrar la factura con los datos proporcionados
    #     Además se borra el PDF antiguo y el diccionario antiguo para volver a introducirlos posteriormente modificados
    #     '''
        
    #     numeroFactura = self.numeroFactura.get().lower().strip()
    #     fecha = self.fecha.get().lower().strip()
        
    #     facturaEncontrada = None

    #     for factura in self.listaFacturas:
    #         if factura['numeroFactura'] == numeroFactura and factura['fecha'] == fecha:
    #             facturaEncontrada = factura
    #             self.listaFacturas.remove(factura) 
    #             break

    #     if facturaEncontrada:
    #         self.formulario_edicion(facturaEncontrada)

    #         fechaCorregida = fecha.replace('/', '_') 

    #         ruta_pdf = f"PDF/{fechaCorregida}_{numeroFactura}.pdf" 

    #         if os.path.exists(ruta_pdf):
    #             os.remove(ruta_pdf)
                
    #     else:
    #         messagebox.showerror("Error", "No se encontró una factura con los datos proporcionados")
    #     self.ventana_ModificarFactura.destroy()
        
    # def formulario_edicion(self, factura):
    #     ''' Método para editar los campos de la factura seleccionada manualmente:
    #     Se van a mostrar todas los campos de la factura original y se podrán editar
    #     Cuando se acabe se pulsa el botón de editar factura y se invoca el método de guardar_cambios2
    #     '''
    #     self.ventana_ModificarFactura.destroy()
    #     self.ventana_EditarFactura = tk.Toplevel()
    #     self.ventana_EditarFactura.title("Editar Factura")
    #     w, h = 500, 500  # Tamaño de la ventana
    #     centrar(self.ventana_EditarFactura, w, h)

    #     self.numeroFactura = self.entradaDatos(self.ventana_EditarFactura, "Número de Factura: ")
    #     self.numeroFactura.insert(0, factura['numeroFactura'])
    #     self.fecha = self.entradaDatos(self.ventana_EditarFactura, "Fecha: ")
    #     self.fecha.insert(0, factura['fecha'])
    #     self.cliente = self.entradaDatos(self.ventana_EditarFactura, "Cliente: ")
    #     self.cliente.insert(0, factura['cliente'])
    #     self.dni = self.entradaDatos(self.ventana_EditarFactura, "DNI: ")
    #     self.dni.insert(0, factura['dni'])

    #     self.listaElementos = []
    #     self.elementos_frame = tk.Frame(self.ventana_EditarFactura)
    #     self.elementos_frame.pack(pady=10)

    #     for elem in factura['listaElementos']:
    #         self.anadir_elemento(elem[0], elem[1], elem[2])

 

    #     self.botonGuardar = tk.Button(self.ventana_EditarFactura, text="Guardar Cambios", command=lambda: self.guardar_cambios(factura))
    #     self.botonGuardar.pack(pady=10)


    # def anadir_elemento(self, unidades="", elemento="", precio=""):
    #     ''' Método para generar los frames y entradas de los elementos'''
    #     frame = tk.Frame(self.elementos_frame)
    #     frame.pack(pady=5)

    #     etiquetaUnidades = tk.Label(frame, text="Unidades:")
    #     etiquetaUnidades.pack(side=tk.LEFT)
    #     entradaUnidades = tk.Entry(frame, width=5)
    #     entradaUnidades.pack(side=tk.LEFT)
    #     entradaUnidades.insert(0, unidades)

    #     etiquetaElemento = tk.Label(frame, text="Elemento:")
    #     etiquetaElemento.pack(side=tk.LEFT)
    #     entradaElemento = tk.Entry(frame, width=20)
    #     entradaElemento.pack(side=tk.LEFT)
    #     entradaElemento.insert(0, elemento)

    #     etiquetaPrecio = tk.Label(frame, text="Precio:")
    #     etiquetaPrecio.pack(side=tk.LEFT)
    #     entradaPrecio = tk.Entry(frame, width=10)
    #     entradaPrecio.pack(side=tk.LEFT)
    #     entradaPrecio.insert(0, precio)

    #     self.listaElementos.append((entradaUnidades, entradaElemento, entradaPrecio))

    # def guardar_cambios(self, factura):
    #     ''' Método para guardar los cambios realizados en la factura:
    #     Se asignan los valores introducios en el formulario de edición al diccionario de la factura seleccionada (datos_factura)
    #     Se realiza un append de este diccionario a la lista de diccionarios
    #     Se pasa a formato json y se sobreescribe al anterior
    #     Se muestra un mensaje conforme la factura ha sido guardada
    #     La diferencia aqui se destruye la ventana de modificar factura previamente generada
    #     Se invoca al método de crear_pdf
    #     '''
    #     listaFinalElementos = []
    #     for unidad, elemento, precio in self.listaElementos:
    #         unidad = str(unidad.get().lower().strip())
    #         elemento= str(elemento.get().lower().strip())
    #         precio= str(precio.get().lower().strip())
    #         listaFinalElementos.append([unidad, elemento, precio])

    #     self.datos_factura = {
    #         'numeroFactura': str(self.numeroFactura.get().lower().strip()),
    #         'fecha': self.fecha.get().lower().strip(),
    #         'cliente': str(self.cliente.get().lower().strip()),
    #         'dni': str(self.dni.get().lower().strip()),
    #         'listaElementos': listaFinalElementos 
    #     }
    #     if self.datos_factura['numeroFactura'] == '':
    #         self.datos_factura['numeroFactura'] = 'sn'

    #     for factura in self.listaFacturas:
    #         if factura['numeroFactura'] == self.datos_factura['numeroFactura']:
    #             self.datos_factura['numeroFactura'] = f"copia - {self.datos_factura['numeroFactura']}" #{random.randint(0, 1000)}
       
    #     for elemento1 in self.datos_factura['listaElementos']:
    #         if elemento1[0].isdigit():
    #             elemento1[0] = elemento1[0]
    #         else:
    #             elemento1[0] = '0'                
        
    #     for elemento2 in self.datos_factura['listaElementos']:
    #         if elemento2[2].isdigit():
    #             elemento2[2] = elemento2[2]
    #         else:
    #             elemento2[2] = '0'

    #     self.listaFacturas.append(self.datos_factura)
    #     contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
    #     self.path.write_text(contenido)
    #     messagebox.showinfo("Éxito", "Factura guardada")
    #     self.ventana_EditarFactura.destroy()
    #     CPDF(self.datos_factura)

        ###############################################
        # Necesario para que haya dos maneras de proceder a la hora de gestionar las ventanas de modificar facturas
    def buscar_factura2(self, nombrePDF):
        ''' Método 2 para buscar una factura sin introducir los datos de búsqueda de la factura:
        1) Se importa el nombre del archivo PDF seleccionado tal que fecha_numeroFactura:
        2) Se convierte en string el nombre y se separan los elementos de fecha y numeroFactura
        3) Se adapta la fecha para que pueda buscarla en la lista de diccionarios de facturas

        Se recorre la lista de diccionarios de las facturas creadas y si coincide el número de la factura y la fecha:
            1) Se asigna a la variable facturaEncontrada el diccionario correspondiente ala factura
            2) Se invoca al método para modificar los datos y elementos de la factura (formulario_edicion2)
        Si no coincide alguno de los datos va a decir que no se pudo encontrar la factura con los datos proporcionados (no pasa nunca)
        Además se borra el PDF antiguo y el diccionario antiguo para volver a introducirlos posteriormente modificados
        '''
        # numeroFactura = self.numeroFactura.get().lower().strip()
        # fecha = self.fecha.get().lower().strip()    


        self.nombrePDF = str(nombrePDF)
        numFactura0= self.nombrePDF[11:]
        fecha1= self.nombrePDF[0:10]
        fecha0 = fecha1.replace('_', '/')
        self.numeroFacturaZ = numFactura0.lower().strip()
        self.fechaZ = fecha0.lower().strip()

        facturaEncontrada = None
        
        for factura in self.listaFacturas:
            if factura['numeroFactura'] == self.numeroFacturaZ and factura['fecha'] == self.fechaZ:
                facturaEncontrada = factura
                self.listaFacturas.remove(factura)
                break
            
        if facturaEncontrada:
            self.formulario_edicion2(facturaEncontrada)

            # fechaCorregida = fecha2.replace('/', '_') # Prueba2

            # ruta_pdf = f"PDF/{fechaCorregida}_{numeroFactura}.pdf" # Prueba2

            # if os.path.exists(ruta_pdf): # Prueba2
            #     os.remove(ruta_pdf)
  
        else:
            messagebox.showerror("Error", "No se encontró una factura con los datos proporcionados")

    def formulario_edicion2(self, factura):
        ''' Método para editar los campos de la factura seleccionada manualmente:
        Se van a mostrar todas los campos de la factura original y se podrán editar
        Cuando se acabe se pulsa el botón de editar factura y se invoca el método de guardar_cambios2
        '''
        self.ventana_EditarFactura = tk.Toplevel()
        self.ventana_EditarFactura.title("Editar Factura")
        w, h = 500, 500  # Tamaño de la ventana
        centrar(self.ventana_EditarFactura, w, h)

        self.numeroFactura = self.entradaDatos(self.ventana_EditarFactura, "Número de Factura: ")
        self.numeroFactura.insert(0, factura['numeroFactura'])
        self.fecha = self.entradaDatos(self.ventana_EditarFactura, "Fecha: ")
        self.fecha.insert(0, factura['fecha'])
        self.cliente = self.entradaDatos(self.ventana_EditarFactura, "Cliente: ")
        self.cliente.insert(0, factura['cliente'])
        self.dni = self.entradaDatos(self.ventana_EditarFactura, "DNI: ")
        self.dni.insert(0, factura['dni'])

        self.listaElementos = []
        self.elementos_frame = tk.Frame(self.ventana_EditarFactura)
        self.elementos_frame.pack(pady=10)

        for elem in factura['listaElementos']:
            self.anadir_elemento2(elem[0], elem[1], elem[2])
            
                    # /// Se hace un botón para los elementos, se le asigna el comando anadir_elemento y se empaqueta luego        
        self.botonElemento = tk.Button(self.ventana_EditarFactura, text="Añadir Elemento", command=self.anadir_elemento2) 
        self.botonElemento.pack(pady = 5)  

        self.botonGuardar = tk.Button(self.ventana_EditarFactura, text="Guardar Cambios", command=lambda: self.guardar_cambios2(factura))
        self.botonGuardar.pack(pady=10)


       

    def anadir_elemento2(self, unidades="", elemento="", precio=""):
        ''' Método para generar los frames y entradas de los elementos'''
        
        frame = tk.Frame(self.elementos_frame)
        frame.pack(pady=5)

        etiquetaUnidades = tk.Label(frame, text="Unidades:")
        etiquetaUnidades.pack(side=tk.LEFT)
        entradaUnidades = tk.Entry(frame, width=5)
        entradaUnidades.pack(side=tk.LEFT)
        entradaUnidades.insert(0, unidades)

        etiquetaElemento = tk.Label(frame, text="Elemento:")
        etiquetaElemento.pack(side=tk.LEFT)
        entradaElemento = tk.Entry(frame, width=20)
        entradaElemento.pack(side=tk.LEFT)
        entradaElemento.insert(0, elemento)

        etiquetaPrecio = tk.Label(frame, text="Precio:")
        etiquetaPrecio.pack(side=tk.LEFT)
        entradaPrecio = tk.Entry(frame, width=10)
        entradaPrecio.pack(side=tk.LEFT)
        entradaPrecio.insert(0, precio)

        self.listaElementos.append((entradaUnidades, entradaElemento, entradaPrecio))

        #         # Controles de entrada, de partida le pone un 0 a unidades y precio################### falta esto
        # if entradaUnidades.get().isdigit() and entradaUnidades.get() == '' :
        #     pass
        # else:
        #     entradaUnidades.delete(0, tk.END)
        #     entradaUnidades.insert(0, '0')
        
        # if entradaPrecio.get().isdigit() and entradaUnidades.get() == '' :
        #     pass
        # else:
        #     entradaPrecio.delete(0, tk.END)
        #     entradaPrecio.insert(0, '0')
        
    def guardar_cambios2(self, factura):
        ''' Método para guardar los cambios realizados en la factura:
        Se asignan los valores introducios en el formulario de edición al diccionario de la factura seleccionada (datos_factura)
        Se realiza un append de este diccionario a la lista de diccionarios
        Se pasa a formato json y se sobreescribe al anterior
        Se muestra un mensaje conforme la factura ha sido guardada
        La diferencia aqui no se destruye la ventana de modificar factura porque nunca se generó (si no, peta)
        Se invoca al método de crear_pdf
        '''
        

        fechaCorregidaZ = self.fechaZ.replace('/', '_') # Prueba2

        ruta_pdf = f"PDF/{fechaCorregidaZ}_{self.numeroFacturaZ}.pdf" # Prueba2

        if os.path.exists(ruta_pdf): # Prueba2
            os.remove(ruta_pdf)

        listaFinalElementos = []
        for unidad, elemento, precio in self.listaElementos:
            unidad = str(unidad.get().lower().strip())
            elemento= str(elemento.get().lower().strip())
            precio= str(precio.get().lower().strip())
            listaFinalElementos.append([unidad, elemento, precio])

        self.datos_factura = {
            'numeroFactura': str(self.numeroFactura.get().lower().strip()),
            'fecha': self.fecha.get().lower().strip(),
            'cliente': str(self.cliente.get().lower().strip()),
            'dni': str(self.dni.get().lower().strip()),
            'listaElementos': listaFinalElementos 
        }
        if self.datos_factura['numeroFactura'] == '':
            self.datos_factura['numeroFactura'] = 'sn'

        for factura in self.listaFacturas:
            if factura['numeroFactura'] == self.datos_factura['numeroFactura']:
                self.datos_factura['numeroFactura'] = f"copia - {self.datos_factura['numeroFactura']}" #{random.randint(0, 1000)}
       
        for elemento1 in self.datos_factura['listaElementos']:
            if elemento1[0].isdigit():
                elemento1[0] = elemento1[0]
            else:
                elemento1[0] = '0'                
        
        for elemento2 in self.datos_factura['listaElementos']:
            if elemento2[2].isdigit():
                elemento2[2] = elemento2[2]
            else:
                elemento2[2] = '0'

        self.listaFacturas.append(self.datos_factura)
        contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
        self.path.write_text(contenido)
        messagebox.showinfo("Éxito", "Factura guardada")
        self.ventana_EditarFactura.destroy()
        CPDF(self.datos_factura)
        ###############################################