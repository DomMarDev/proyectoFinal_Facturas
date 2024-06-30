# Importaciones de librerías
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
import random
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
        self.listaElementos = []
                # /// Se hace un frame para los elementos y se empaqueta luego
        self.frameElementos = tk.Frame(self.ventana_CrearFactura) 
        self.frameElementos.pack(pady = 10)
                # /// Se hace un botón para los elementos, se le asigna el comando anadir_elemento y se empaqueta luego        
        self.botonElemento = tk.Button(self.ventana_CrearFactura, text="Añadir Elemento", command=self.anadir_elemento) 
        self.botonElemento.pack(pady = 5)
                # /// Se hace un botón para los Guardar la factura, se le asigna el comando guardar_factura y se empaqueta luego    
        self.botonGuardar = tk.Button(self.ventana_CrearFactura, text="Guardar Factura", command=self.guardar_factura)
        self.botonGuardar.pack(pady = 10)

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
        '''        
        frame = tk.Frame(self.frameElementos)
        frame.pack(pady=5)

        etiquetaUnidades = tk.Label(frame, text="Unidades:")
        etiquetaUnidades.pack(side=tk.LEFT)
        entradaUnidades = tk.Entry(frame, width=5)
        entradaUnidades.pack(side=tk.LEFT)
        entradaUnidades.pack(side=tk.LEFT)
        
                

        etiquetaElemento = tk.Label(frame, text="Elemento:")
        etiquetaElemento.pack(side=tk.LEFT)
        entradaElemento = tk.Entry(frame, width=20)
        entradaElemento.pack(side=tk.LEFT)

        etiquetaPrecio = tk.Label(frame, text="Precio:")
        etiquetaPrecio.pack(side=tk.LEFT)
        entradaPrecio = tk.Entry(frame, width=10)
        entradaPrecio.pack(side=tk.LEFT)       
       

        self.listaElementos.append((entradaUnidades, entradaElemento, entradaPrecio))

    def guardar_factura(self):# Esto lo he tenido que pedir a una IA, no me salía, sobretodo para añadir los elementos con el bucle for
        ''' Método que sirve para guardar los datos de la factura:
        1) Se genera diccionario (datos_factura) con cada dato introducido (incluido elementos de la factura)
            - Keys: numeroFactura, fecha, cliente, dni (para DNI/CIF), listaElementos
        2) El diccionario datos_factura se añade mediante el método append a la listaFacturas (archivo Json, ahora lista rescatado y cargado en memoria)
        3) La lista de diccionarios se transforma a un archivo json con json.dumps
        4) Se sobreescribe el archivo json con write_text
        5) Le decimos al usuario que se ha guardado la factura gracias al método de showinfo de la clase messagebox (librería tkinter)
        6) Destruimos la ventana de crear facturas y accedemos al método de crear_pdf para que se vaya generando el archivo mientras hacemos otras cosas en el menú principal
        '''
        self.datos_factura = {
            'numeroFactura': str(self.numeroFactura.get().lower().strip()),
            'fecha': self.fecha,
            'cliente': str(self.cliente.get().lower().strip()),
            'dni': str(self.dni.get().lower().strip()),
            'listaElementos': [[str(unidades.get().lower().strip()), str(elemento.get().lower().strip()), str(precio.get().lower().strip())] for unidades, elemento, precio in self.listaElementos] 
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
        self.ventana_CrearFactura.destroy()
        self.crear_pdf()
    
    def crear_pdf(self):
        ''' Método para crear el archivo PDF usando los datos introducidos por el usuario (datos + elementos factura):
        1) Se le asigna una ruta de guardado al archivo PDF de forma automática. Para ello se usa:
            - PDF/{fecha}_{self.datos_factura['numeroFactura']}.pdf
                -  PDF es la carpeta de PDF donde se guardarán una vez generados
                -  fecha es la fecha del día en que se crea el archivo PDF
                -  self.datos_factura['numeroFactura'] es el elemento de la key numeroFactura dentro del diccionario datos_factura creado en guardar_factura
        2) Se crea ercivo PDF con: 
            - pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4'), aquí queremos que sea vertical en su orientación y sea en dinA4
            - pdf.add_page(), es para agregar una página (si quiseramos generar otra página con otra información se podría hacer, pero requiere de otro pdf.add_page())
            - Elementos del PDF:
                a) Logo empresa
                b) Título Factura
                c) Datos de nuestra empresa
                d) Tabla datos de la factura
                e) Tabla elementos de la factura
                f) Tabla económica
                g) Tabla pago
            - Se genera el PDF dada la ruta que generamos en 1
            
        '''
        '''
        Formato del PFD (P de Portrait):
        Vertical: 297 mm
        Horizontal: 210 mm

        A4 = 210 x 297 mm
        '''

        ''' 
        Distribución de textos y grids:

        Bordes (Border):

        0 = no | 1 = Si | T = arriba | B = abajo | L = izq | R = der

        Align:

        C = centro | L = izq | R = der

        '''

        # / Ruta para guardar el PDF
        hoy= date.today()
        dia= hoy.strftime("%d")
        mes= hoy.strftime("%m")
        anyo= hoy.strftime("%Y")
        fecha= f'{dia}_{mes}_{anyo}'

        ruta_pdf = f"PDF/{fecha}_{self.datos_factura['numeroFactura']}.pdf"

        # / Creamos el PDF:
        pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')

        pdf.add_page()

        # / Elementos del PDF
            # // a) Logo empresa
        ruta_logo = ruta_logo_empresa
        pdf.image(ruta_logo, x = 10, y = 10, w = 30, h= 30)

            # // b) Título Factura                 
        pdf.set_font('Times', '', 50) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 0, h = 15, txt = 'Factura', border = 0, ln = 1, align = 'C', fill= 0) # pdf.text(x= 60, y = 50, txt = 'FACTURA' ) si se quiere colocar en algun lado

        pdf.set_font('Times', '', 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)

            # // c) Datos de nuestra empresa
        info_empresa = f'{nombreCompleto}\n{calleEmpresa}\n{poblacionEmpresa}\n{cpProvinciaEmpresa}\n{telEmpresa}\n{dniCifEmpresa}\n{correoEmpresa}' 
        pdf.multi_cell(w = 0, h = 5, txt = info_empresa, border = 0, align = 'R', fill= 0)

            # // d) Tabla datos de la factura:
        nf = self.datos_factura['numeroFactura']
        f  = self.datos_factura['fecha']
        c  = self.datos_factura['cliente']
        d  = self.datos_factura['dni']

        lista_datos ={
        'numeroFactura': nf,
        'fecha': f,
        'cliente': c,
        'DNI/NIF': d
        } 
                # /// Encabezados datos cliente
        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 30, h = 10, txt = 'Nº factura', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Fecha', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Cliente', border = 1, align = 'C', fill= 0) 
        pdf.multi_cell(w = 30, h = 10, txt = 'DNI/NIF', border = 1, align = 'C', fill= 0)
                # /// Valores datos cliente
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 30, h = 10, txt = lista_datos['numeroFactura'], border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = lista_datos['fecha'], border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = lista_datos['cliente'], border = 1, align = 'C', fill= 0) 
        pdf.multi_cell(w = 30, h = 10, txt = lista_datos['DNI/NIF'], border = 1, align = 'C', fill= 0)

        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía
        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía

            # // e) Tabla elementos de la factura
                # /// Encabezados datos a facturar (Unidades/ Concepto / Precio U. / Total)
        pdf.set_font('Times', "B", 13) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 30, h = 10, txt = 'Unidades', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 100, h = 10, txt = 'Concepto', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Precio U.', border = 1, align = 'C', fill= 0) 
        pdf.multi_cell(w = 30, h = 10, txt = 'Total', border = 1, align = 'C', fill= 0)
                # /// Valores elementos factura
        pdf.set_font('Times', "", 12,  ) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        tabla2 = self.datos_factura['listaElementos'] # tabla2 = [unidades, concepto , precio U., total]
        for elemento in tabla2:
            # Se convierten los elementos de unidades y total a float
            if elemento[0]:
                elemento[0] = float(elemento[0])
            else:
                elemento[0] = 0
            if elemento[2]:
                elemento[2] = float(elemento[2])
            else:
                elemento[2] = 0
            pdf.cell(w = 30, h = 10, txt = f'{elemento[0]}', border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 100, h = 10, txt = elemento[1], border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 30, h = 10, txt = f'{elemento[2]}' + chr(128), border = 1, align = 'C', fill= 0) 
            pdf.multi_cell(w = 30, h = 10, txt = f'{elemento[0]*elemento[2]} {chr(128)}', border = 1, align = 'C', fill= 0)
        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía

            # // f) Tabla económica
                # /// Encabezados tabla económica
        pdf.set_font('Times', "B", 13) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Importe Bruto', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 20, h = 10, txt = 'IVA % *', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 40, h = 10, txt = 'Base Imponible', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 40, h = 10, txt = 'IVA *', border = 1, align = 'C', fill= 0)
        pdf.multi_cell(w = 50, h = 10, txt = 'Total Factura', border = 1, align = 'C', fill= 0) 
                # /// Valores tabla económica
        suma1 = 0
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        # Se hace una suma de las unidades * precio U. para calcular el total
        for lista in self.datos_factura['listaElementos']:
            lista[0] = float(lista[0])
            lista[2] = float(lista[2])
            suma1 = lista[0]*lista[2] + suma1
        pdf.cell(w = 40, h = 10, txt = f'{str(suma1)} {chr(128)}', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 20, h = 10, txt ='21 %', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 40, h = 10, txt = f'{str(suma1)} {chr(128)}', border = 1, align = 'C', fill= 0)
        pdf.cell(w = 40, h = 10, txt = f'{str(suma1 * 0.21)} ' + chr(128), border = 1, align = 'C', fill= 0)  
        pdf.multi_cell(w = 50, h = 10, txt = f'{str(suma1 * 1.21)} {chr(128)}', border = 1, align = 'C', fill= 0)

        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía

            # // g) Tabla pago
        # Se recupera la fecha de hoy y se hace una nueva para que se deba de pagar el 1 del més siguiente.
        hoy= date.today()
        mes= int(hoy.strftime("%m"))
        anyo= hoy.strftime("%Y")
        mesFin= str(mes+1)
        if len(mesFin) == 1:
            mesFin = f'0{mesFin}'
        fechafin= f'01/{mesFin}/{anyo}'
                # /// Encabezados y valores tabla pago
        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Vencimiento', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = fechafin , border = 1, align = 'C', fill= 0) 

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Forma de Pago', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = formaPago , border = 1, align = 'C', fill= 0) 

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Banco', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = bancoPagar , border = 1, align = 'C', fill= 0)

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'IBAN', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = iban , border = 1, align = 'C', fill= 0) 

        # / Generación del PDF
        pdf.output(ruta_pdf)

        messagebox.showinfo("PDF Generado", f"El PDF se ha generado correctamente.")    

    

class CrearFactura():

    def __init__(self, root):
        ''' Método para crear la ventana de Crear Factura
        Se le asigna un título, unas dimensiones base, se centra en el centro de la pantalla'''
        self.root = root
        self.root.title("Crear Factura") # Título
        w, h = 500, 100  # Tamaño de la ventana
        centrar(self.root, w, h) # Centrado
        # Configuración del menú superior y botón Crear
        self.barraMenu = tk.Menu(self.root) 
        self.root.config(menu=self.barraMenu)
        self.root.resizable(False,False)
    
        botonCrear= tk.Button(self.root,
                                text = 'Crear',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command =  self.abrir_json)
        botonCrear.pack(fill = tk.X, padx = 20, pady = 30)
        

        #Por si queremos que el usuario escoja el json
        # self.menuArchivo = tk.Menu(self.barraMenu, tearoff=0)
        # self.barraMenu.add_cascade(label="Archivo", menu=self.menuArchivo)
        # self.menuArchivo.add_command(label="Abrir JSON de Facturas", command=self.abrir_json)
        # self.menuArchivo.add_separator()
        # self.menuArchivo.add_command(label="Salir", command=self.root.quit)
        
        self.menuFactura = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Facturas", menu=self.menuFactura)
        self.menuFactura.add_command(label="Añadir Factura", command=self.abrir_json)# Si se quiere abrir Json, cambiar abrir_json por add_factura
        self.menuFactura.add_separator()
        self.menuFactura.add_command(label="Salir", command=self.root.destroy)
        
        #Por si queremos que el usuario escoja el json
        # def abrir_json(self):
        #     ruta_Json = FD.askopenfilename(title="Selecciona el archivo de facturas", filetypes=[("Archivo JSON", "*.json"),], initialdir= 'archivoJson')
        #     if ruta_Json:
        #         self.ventana_anadir_factura = Datos_Factura(ruta_Json)
        #         self.ventana_anadir_factura.add_factura()
        
    def abrir_json(self):
        ''' Método para abrir el archivo json automáticamente:
        1) Asignamos la ruta
        2) Si existe el archivo se invoca a la clase para introducir los datos de la factura
        '''
        self.root.destroy()
        ruta_Json = 'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_anadir_factura = Datos_Factura(ruta_Json)
            self.ventana_anadir_factura.add_factura()
    
    #Por si queremos que el usuario escoja el json
    # def add_factura(self):
    #     if hasattr(self, 'Ventana de Añadir Factura'):
    #         self.ventana_anadir_factura.add_factura()
    #     else:
    #         messagebox.showwarning("Archivo no seleccionado", "Primero seleccione un archivo JSON de facturas desde el menú Archivo -> Abrir JSON de Facturas.")