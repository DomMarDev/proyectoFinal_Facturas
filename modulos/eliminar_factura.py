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

class Eliminar:

    def __init__(self, ruta):
        ''' Se rescata la ruta del archivo json "facturas.json" y se carga para editarlo.'''
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)

    def eliminar_factura(self):
        ''' Método para eliminar los datos de una factura:
        Al usuario se le pide:
            -1) Número de la Factura
            -2) Cliente de la Factura
            -3) DNI/CIF del cliente
            -4) Unidades/Concepto(s)/Precio Unidad   
        Cuando se acabe se pulsa el botón de Eliminar factura y se invoca el método de borrado_factura     
        '''
        # / Genero una ventana por encima de la del menú principal.          
        self.ventanaEliminarFactura = tk.Toplevel() # Uso la clase Toplevel de tkinter
        self.ventanaEliminarFactura.title("Eliminar Factura") # Asigno el título Eliminar factura a esta ventana
        w, h = 500, 100  # Tamaño de la ventana
        centrar(self.ventanaEliminarFactura, w, h)  # Llamo a la función centrar para que me centre la ventana en el centro de la pantalla
        
        # / Pido la entrada de datos
        self.numeroFacturaEliminar = self.entradaDatos(self.ventanaEliminarFactura, "Introduce el Nº de la factura a eliminar: ")
        self.fechaEliminar = self.entradaDatos(self.ventanaEliminarFactura, "Introduce la fecha de la factura (dd/mm/yyyy): ")

        self.botonEliminar = tk.Button(self.ventanaEliminarFactura, text="Eliminar Factura", command=self.borrado_factura)
        self.botonEliminar.pack(pady=10)
    
    def entradaDatos(self, ventana_facturas, texto):
        ''' Método para hacer la entrada de datos:
        1) Se crea el frame dentro de la ventana_EliminarFactura y se empaqueta
        2) Se crea la etigueta del dato pedido que se obtiene gracias a que se lo pasamos por los parámetros y se empaqueta
        3) Se crea la entrada para el dato y se empaqueta
        
        Se devuelve la entrada 
        '''
        frame = tk.Frame(ventana_facturas)
        frame.pack(pady=5)
        label = tk.Label(frame, text=texto)
        label.pack(side=tk.LEFT)
        entrada = tk.Entry(frame, width=50)
        entrada.pack(side=tk.LEFT)
        return entrada

    def borrado_factura(self):
        ''' Método 1 para borrar una factura introduciendo los datos de búsqueda de la factura:
        Se importan los datos introducidos en método de eliminar_factura:
            1) Número de la factura
            2) Fecha de la factura
        Se recorre la lista de diccionarios de las facturas creadas y si coincide el número de la factura y la fecha:
            1) Se asigna a la variable facturaEncontrada el valor booleando de True
            2) Se elimina el diccionario correspondiente a la factura que coincida con las credenciales dadas
            3) la lista de diccionarios de facturas se pasa a json y se sobreescribe
            4) Se rescata la fecha y el numeroFactura para poder eliminar el PDF gracias a la clase os con .path.exists()
        '''           
        numeroFactura = str(self.numeroFacturaEliminar.get().lower().strip())
        fechaFactura = self.fechaEliminar.get().strip()

        factura_encontrada = False

        for factura in self.listaFacturas:
            if factura['numeroFactura'] == numeroFactura and factura['fecha'] == fechaFactura:
                self.listaFacturas.remove(factura)
                factura_encontrada = True
                break

        if factura_encontrada:
            contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
            self.path.write_text(contenido)

            fechaCorregida = fechaFactura.replace('/', '_')

            ruta_pdf = f"PDF/{fechaCorregida}_{numeroFactura}.pdf"

            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)

            messagebox.showinfo("Éxito", "Factura eliminada correctamente")
            self.ventanaEliminarFactura.destroy()
        else:
            messagebox.showerror("Error", "Factura no encontrada")
        self.ventanaEliminarFactura.destroy()
    ###################################################
    def borrado_factura2(self, nombrePDF):
        ''' Método 2 para eliminar una factura sin introducir los datos de búsqueda de la factura:
        1) Se importa el nombre del archivo PDF seleccionado tal que fecha_numeroFactura:
        2) Se convierte en string el nombre y se separan los elementos de fecha y numeroFactura
        3) Se adapta la fecha para que pueda buscarla en la lista de diccionarios de facturas

        Se recorre la lista de diccionarios de las facturas creadas y si coincide el número de la factura y la fecha:
            1) Se asigna a la variable facturaEncontrada el valor booleando de True
            2) Se elimina el diccionario correspondiente a la factura que coincida con las credenciales dadas
            3) La lista de diccionarios de facturas se pasa a json y se sobreescribe
            4) Se rescata la fecha y el numeroFactura para poder eliminar el PDF gracias a la clase os con .path.exists()
        Si no coincide alguno de los datos va a decir que no se pudo encontrar la factura (no pasa nunca)
        '''           
        self.nombrePDF = str(nombrePDF)

        numFactura0= self.nombrePDF[11:]
        fecha1= self.nombrePDF[0:10]
        fecha0 = fecha1.replace('_', '/')
        numeroFactura = numFactura0
        fecha = fecha0

        facturaEncontrada = False

        for factura in self.listaFacturas:
            if factura['numeroFactura'] == numeroFactura and factura['fecha'] == fecha:
                self.listaFacturas.remove(factura)
                facturaEncontrada = True
                break

        if facturaEncontrada:
            contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
            self.path.write_text(contenido)

            fechaCorregida = fecha.replace('/', '_')

            ruta_pdf = f"PDF/{fechaCorregida}_{numeroFactura}.pdf"

            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)

            messagebox.showinfo("Éxito", "Factura eliminada correctamente")
        else:
            messagebox.showerror("Error", "Factura no encontrada")
    ###############################################

class EliminarFactura():

    def __init__(self, root):
        ''' Método para crear la ventana de Eliminar Factura
        Se le asigna un título, unas dimensiones base, se centra en el centro de la pantalla'''
        self.ventana_eliminar_por_datos = root
        self.ventana_eliminar_por_datos.title("Eliminar Factura") # Título
        w, h = 500, 200  # Tamaño de la ventana
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
                                command = self.abrir_json)
        botonCrear.pack(fill = tk.X, padx = 20, pady = 30)

        botonBuscarEliminar= tk.Button(self.ventana_eliminar_por_datos,
                                text = 'Buscar y Eliminar',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.abrir_PDF)
        botonBuscarEliminar.pack(fill = tk.X, padx = 20, pady = 30)

        #Por si queremos que el usuario escoja el json
        # self.menuArchivo = tk.Menu(self.barraMenu, tearoff=0)
        # self.barraMenu.add_cascade(label="Archivo", menu=self.menuArchivo)
        # self.menuArchivo.add_command(label="Abrir JSON de Facturas", command=self.abrir_json)
        # self.menuArchivo.add_separator()
        # self.menuArchivo.add_command(label="Salir", command=self.root.quit)

        self.menuArchivo = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Archivo", menu=self.menuArchivo)
        self.menuArchivo.add_command(label="Abrir PDF de Facturas", command=self.abrir_PDF)
        self.menuArchivo.add_separator()
        self.menuArchivo.add_command(label="Salir", command=self.ventana_eliminar_por_datos.destroy)


        self.menuFactura = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Facturas", menu=self.menuFactura)
        self.menuFactura.add_command(label="Eliminar Factura", command=self.abrir_json) # Si se quiere abrir Json, cambiar abrir_json por eliminar_factura
    
    #Por si queremos que el usuario escoja el json
    # def abrir_json(self):
    #     ruta_Json = FD.askopenfilename(title="Selecciona el archivo de facturas", filetypes=[("Archivo JSON", "*.json"),], initialdir= 'archivoJson')
    #     if ruta_Json:
    #         self.ventana_anadir_factura = Eliminar(ruta_Json)
    #         self.ventana_anadir_factura.eliminar_factura()

    def abrir_json(self):
        ''' Método para abrir el archivo json automáticamente:
        1) Asignamos la ruta
        2) Si existe el archivo se invoca a la clase para introducir los datos de eliminar de factura
        '''
        self.ventana_eliminar_por_datos.destroy()        
        ruta_Json = 'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_anadir_factura = Eliminar(ruta_Json)
            self.ventana_anadir_factura.eliminar_factura()

    def abrir_PDF(self):
        ''' Método para abrir el archivo PDF manualmente:
        1) Asignamos la ruta del json (necesaria)
        2) Obtenemos la ruta absoluta del archivo PDF seleccionado
        3) Se obtiene el nombre del archivo PDF sin extensión .pdf
        4) Si existe el archivo se invoca a la clase para eliminar la factura, pero la versión 2 donde no introducimos datos para eliminar la factura
        '''
        self.ventana_eliminar_por_datos.destroy()
        ruta_PDF   = FD.askopenfilename(title="Selecciona la factura a modificar", filetypes=[("Archivo PDF", "*.pdf"),], initialdir= 'PDF')
        nombre_PDF = Path(ruta_PDF).stem

        ruta_Json  = 'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_modificar_factura = Eliminar(ruta_Json)
            self.ventana_modificar_factura.borrado_factura2(nombre_PDF)
    
    #Por si queremos que el usuario escoja el json
    # def eliminar_factura(self):
    #     if hasattr(self, 'Ventana de Añadir Factura'):
    #         self.ventana_anadir_factura.eliminar_factura()
    #     else:
    #         messagebox.showwarning("Archivo no seleccionado", "Primero seleccione un archivo JSON de facturas desde el menú Archivo -> Abrir JSON de Facturas.")