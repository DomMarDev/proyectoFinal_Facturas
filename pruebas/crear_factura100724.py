# Importaciones de librerías
from tkinter import *
import json                                             # Trabajar con el archivo json
from pathlib import Path                                # Trabajar con las rutas
import tkinter as tk                                    # Interfaz gráfica
from tkinter import messagebox, filedialog as FD        # Por si queremos agregar la función de escoger el archivo json, mostrar mensajes
import sys                                              # Necesario para que no haya errores a la hora de importar módulos
from datetime import date                               # Necesario para manejar fechas

sys.path.append('.')

from modulos.generic import centrar_ventanas as centrar # Necesario para importar la función de centrar
from modulos.leer_archivo import Lectura_archivo        # Necesario para leer el archivo json
from modulos.colores_y_rutas import *                   # Necesario para autoasignar ciertos campos de la factura
from ruta import ruta                                   # Se importa la ruta del archivo json
from modulos. creacionPDF import crear_pdf as CPDF      # Necesario para llamar al módulo de creación del PDF (crear_pdf)


class CrearFactura():

    def __init__(self, root):
        ''' Método para crear la ventana de Crear Factura
        Se le asigna un título, unas dimensiones base, se centra en el centro de la pantalla
        Tiene un menú superior con la función de crear factura o salir
        En el centro de la ventana podrá dar a un botón que le llevará al menú para crear la factura
        '''
        self.ventana_crear = root
        self.ventana_crear.title("Crear Factura") # Título
        w, h = 500, 100  # Tamaño de la ventana
        centrar(self.ventana_crear, w, h) # Centrado
        # Configuración del menú superior y botón Crear
        self.barraMenu = tk.Menu(self.ventana_crear) 
        self.ventana_crear.config(menu=self.barraMenu)
        self.ventana_crear.resizable(False,False)
    
        botonCrear= tk.Button(self.ventana_crear,
                                text = 'Crear',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command =  self.abrir_json)
        botonCrear.pack(fill = tk.X, padx = 20, pady = 30)
       
        self.menuFactura = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Facturas", menu=self.menuFactura)
        self.menuFactura.add_command(label="Añadir Factura", command=self.abrir_json)
        self.menuFactura.add_separator()
        self.menuFactura.add_command(label="Salir", command=self.ventana_crear.destroy)

    def abrir_json(self):
        ''' Método para abrir el archivo json automáticamente:
        Destruimos la ventana ventana_crear
        1) Asignamos la ruta
        2) Si existe el archivo se invoca a la clase para introducir los datos de la factura.
        Se ejecuta el método add_factura
        '''
        self.ventana_crear.destroy()
        ruta_Json = ruta() #'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_anadir_factura = Datos_Factura(ruta_Json)
            self.ventana_anadir_factura.add_factura()
    

class Datos_Factura:

    def __init__(self, ruta):
        ''' Se rescata la ruta del archivo json "facturas.json" y se carga para editarlo.'''
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)

    def add_factura(self):
        ''' Método para añadir los datos de una factura:
        Al usuario se le pide:
            -1) Número de la Factura
            -2) Cliente de la Factura
            -3) DNI/CIF del cliente
            -4) Unidades/Concepto(s)/Precio Unidad        
        '''
        # / Genero una ventana por encima de la del menú principal.        
        self.ventana_CrearFactura = tk.Toplevel() # Uso la clase Toplevel de tkinter
        self.ventana_CrearFactura.title("Añadir Factura") # Asigno el título Añadir factura a esta ventana
        w, h = 500, 500  # Tamaño de la ventana
        centrar(self.ventana_CrearFactura, w, h) # Llamo a la función centrar para que me centre la ventana en el centro de la pantalla

        # / Pido la entrada de datos
        self.numeroFactura = self.entradaDatos(self.ventana_CrearFactura, "Introduce el Nº de la factura: ")
            # // Para hacerlo más cómodo ya asigno yo la fecha del día en que se hace la factura
        fecha = date.today() # Uso la librería date para obtener cual es el día en el que estamos
        self.fecha = fecha.strftime("%d/%m/%Y") # No me gustan las fechas inglesa, por ello uso el método strftime para que me lo ponga como en España
        self.cliente = self.entradaDatos(self.ventana_CrearFactura, "Introduce el cliente: ")
        self.dni = self.entradaDatos(self.ventana_CrearFactura, "Introduce el DNI del cliente: ")
            # // Declaro la lista de elementos que corresponden a todos los elementos de la factura (4))
        
        
        # frame = tk.Frame(self.frameElementos)
        # frame.pack(pady=5)

        # self.listaElementos.append((entradaUnidades, entradaElemento, entradaPrecio))

                # /// Se hace un botón para los elementos, se le asigna el comando anadir_elemento y se empaqueta luego        
        self.botonElemento = tk.Button(self.ventana_CrearFactura, text="Añadir Elemento", command=self.anadir_elemento) 
        self.botonElemento.pack(pady = 5)
        
                # /// Se hace un botón para los Guardar la factura, se le asigna el comando guardar_factura y se empaqueta luego    
        self.botonGuardar = tk.Button(self.ventana_CrearFactura, text="Guardar Factura", command=self.guardar_factura)
        self.botonGuardar.pack(pady = 10)
        
        self.listaElementos = []
                # /// Se hace un frame para los elementos y se empaqueta luego
        self.frameElementos = tk.Frame(self.ventana_CrearFactura) 
        self.frameElementos.pack(pady = 10)


    def entradaDatos(self, ventana_CrearFactura, texto):
        ''' Método para hacer la entrada de datos:
        1) Se crea el frame dentro de la ventana_CrearFactura y se empaqueta
        2) Se crea la etigueta del dato pedido que se obtiene gracias a que se lo pasamos por los parámetros y se empaqueta
        3) Se crea la entrada para el dato y se empaqueta
        
        Se devuelve la entrada 
        '''
        frame = tk.Frame(ventana_CrearFactura)
        frame.pack(pady = 5)
        label = tk.Label(frame, text = texto)
        label.pack(side = tk.LEFT)
        entrada = tk.Entry(frame, width = 50)
        entrada.pack(side = tk.LEFT)
        return entrada

    def anadir_elemento(self):
        ''' Método para hacer la entrada de elementos:
        1) Se usa el frame de los elementos (heredado) y se empaqueta
        2) A cada parte del elemento (Unidades/concepto/PrecioU) se le genera su etiqueta (y se empaqueta), y su entrada (y se la empaqueta)
        3) Luego cogemos por herencia la lista declarada en add_factura y le hacemos un append de cada parte del elemento de la factura
        Hay control de entrada donde los valores de unidad y precio se les autoasigna un 0 si no se les ha puesto valor alguno
        '''        
    
        frame = tk.Frame(self.ventana_CrearFactura)
        frame.pack(pady=5)

        self.etiquetaUnidades = tk.Label(frame, text="Unidades:")
        self.etiquetaUnidades.pack(side=tk.LEFT)
        self.entradaUnidades = tk.Entry(frame, width=5)
        self.entradaUnidades.pack(side=tk.LEFT)
        
        self.etiquetaElemento = tk.Label(frame, text="Elemento:")
        self.etiquetaElemento.pack(side=tk.LEFT)
        self.entradaElemento = tk.Entry(frame, width=20)
        self.entradaElemento.pack(side=tk.LEFT)

        self.etiquetaPrecio = tk.Label(frame, text="Precio U.:")
        self.etiquetaPrecio.pack(side=tk.LEFT)
        self.entradaPrecio = tk.Entry(frame, width=10)
        self.entradaPrecio.pack(side=tk.LEFT)

        self.listaElementos.append((self.entradaUnidades, self.entradaElemento, self.entradaPrecio))

        # Controles de entrada, de partida le pone un 0 a unidades y precio
        if self.entradaUnidades.get().isdigit() and self.entradaUnidades.get() == '' :
            pass
        else:
            self.entradaUnidades.delete(0, tk.END)
            self.entradaUnidades.insert(0, '0')
        
        if self.entradaPrecio.get().isdigit() and self.entradaUnidades.get() == '' :
            pass
        else:
            self.entradaPrecio.delete(0, tk.END)
            self.entradaPrecio.insert(0, '0')
    
    def guardar_factura(self):
        ''' Método que sirve para guardar los datos de la factura:
        1) Se genera diccionario (datos_factura) con cada dato introducido (incluido elementos de la factura)
            - Keys: numeroFactura, fecha, cliente, dni (para DNI/CIF), listaElementos
            - Control de entrada: del número de la factura -> Si hay una factura con el mismo nombre generará otra con el mismo nombre  + -copia
        2) El diccionario datos_factura se añade mediante el método append a la listaFacturas (archivo Json, ahora lista rescatado y cargado en memoria)
        3) La lista de diccionarios se transforma a un archivo json con json.dumps
        4) Se sobreescribe el archivo json con write_text
        5) Le decimos al usuario que se ha guardado la factura gracias al método de showinfo de la clase messagebox (librería tkinter)
        6) Destruimos la ventana de crear facturas y accedemos al método de crear_pdf para que se vaya generando el archivo mientras hacemos otras cosas en el menú principal
        '''
        
        listaFinalElementos = []
        for unidad, elemento, precio in self.listaElementos:
            unidad = str(unidad.get().lower().strip())
            elemento= str(elemento.get().lower().strip())
            precio= str(precio.get().lower().strip())
            listaFinalElementos.append([unidad, elemento, precio])

        self.datos_factura = {
            'numeroFactura': str(self.numeroFactura.get().lower().strip()),
            'fecha': self.fecha,
            'cliente': str(self.cliente.get().lower().strip()),
            'dni': str(self.dni.get().lower().strip()),
            'listaElementos': listaFinalElementos 
        }
        
        #Se le asigna el nombre de sn si no hay campo en número de factura y si existe un número de factura con el mismo nombre le va añadiendo copia -
        if self.datos_factura['numeroFactura'] == '':
            self.datos_factura['numeroFactura'] = 'sn'

        for factura in self.listaFacturas:
            if factura['numeroFactura'] == self.datos_factura['numeroFactura']:
                self.datos_factura['numeroFactura'] = f"copia - {self.datos_factura['numeroFactura']}" #{random.randint(0, 1000)}
        
        # Herramienta para ver si no hay datos en algún campo de unidad y precio para que se sustituya por un '0'
        for elemento1 in self.datos_factura['listaElementos']:
            try:
                float(elemento1[0])
            except ValueError:
                elemento1[0] = '0' 
      
        for elemento2 in self.datos_factura['listaElementos']:
            try:
                float(elemento2[2])
            except ValueError:
                elemento2[2] = '0'
                
        self.listaFacturas.append(self.datos_factura)
        contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
        self.path.write_text(contenido)
        messagebox.showinfo("Éxito", "Factura guardada")
        self.ventana_CrearFactura.destroy()
        CPDF(self.datos_factura)