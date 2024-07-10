# Importaciones de librerías
import os                                               # Obtener rutas del sistema operativo
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

class ModificarFactura():

    def __init__(self, root):
        ''' Método para crear la ventana de Modificar Factura
        Se le asigna un título, unas dimensiones base, se centra en el centro de la pantalla'''        
        self.ventana_buscar_por_datos = root
        self.ventana_buscar_por_datos.title("Modificar Factura") # Título
        w, h = 500, 100  # Tamaño de la ventana
        centrar(self.ventana_buscar_por_datos, w, h) # Centrado
        # Configuración del menú superior y botón Buscar y Modificar
        self.barraMenu = tk.Menu(self.ventana_buscar_por_datos) # Creo una barra de menú
        self.ventana_buscar_por_datos.config(menu=self.barraMenu) 
        self.ventana_buscar_por_datos.resizable(False,False) # No quiero que se rescale
        
        # Configuración de la barra de menú
        self.menuArchivo = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Archivo", menu=self.menuArchivo)
        self.menuArchivo.add_command(label="Abrir PDF de Facturas", command=self.abrir_PDF)
        self.menuArchivo.add_separator()
        self.menuArchivo.add_command(label="Salir", command=self.ventana_buscar_por_datos.destroy)

        # Creo un botón que ejecutará la accion de ir a modificar la factura seleccionada una vez se abra el directorio con los PDF
        botonBuscarModificar= tk.Button(self.ventana_buscar_por_datos,
                                text = 'Buscar y Modificar',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.abrir_PDF)
        botonBuscarModificar.pack(fill = tk.X, padx = 20, pady = 30)

    def abrir_PDF(self):
        ''' Método para abrir el archivo PDF manualmente:
        1) Asignamos la ruta del json (necesaria)
        2) Obtenemos la ruta absoluta del archivo PDF seleccionado
        3) Se obtiene el nombre del archivo PDF
        4) Si existe el archivo se invoca a la clase para buscar la factura, pero la versión 2 donde no introducimos datos para buscar la factura
        '''
        self.ventana_buscar_por_datos.destroy()
        ruta_Json = ruta() # 'archivoJson/facturas.json' 
        ruta_PDF   = FD.askopenfilename(title="Selecciona la factura a modificar", filetypes=[("Archivo PDF", "*.pdf"),], initialdir= 'PDF')
        nombre_PDF = Path(ruta_PDF).stem
        if ruta_Json:
            self.ventana_modificar_factura = Modificar(ruta_Json)
            self.ventana_modificar_factura.buscar_factura(nombre_PDF)
    

class Modificar:

    def __init__(self, ruta):
        ''' Se rescata la ruta del archivo json "facturas.json" y se carga para editarlo.'''
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)

    def buscar_factura(self, nombrePDF):
        ''' Método para buscar una factura sin introducir los datos de búsqueda de la factura:
        1) Se importa el nombre del archivo PDF y se coge la fecha y el número de la factura mediante splicing (fecha_numeroFactura):
        2) Se convierte en string el nombre y se separan los elementos de fecha y numeroFactura
        3) Se adapta la fecha para que pueda buscarla en la lista de diccionarios de facturas

        Se recorre la lista de diccionarios de las facturas creadas y si coincide el número de la factura y la fecha:
            1) Se asigna a la variable facturaEncontrada el diccionario correspondiente ala factura
            2) Se invoca al método para modificar los datos y elementos de la factura (formulario_edicion)
        Si no coincide alguno de los datos va a decir que no se pudo encontrar la factura con los datos proporcionados
        '''

        self.nombrePDF = str(nombrePDF)
        numFactura0= self.nombrePDF[11:] # El resto será el número de factura
        fecha0 = self.nombrePDF[0:10].replace('_', '/') # La fecha siempre tiene esta medida
        self.numeroFacturaZ = numFactura0.lower().strip()
        self.fechaZ = fecha0.lower().strip()

        facturaEncontrada = None
        
        for factura in self.listaFacturas:
            if factura['numeroFactura'] == self.numeroFacturaZ and factura['fecha'] == self.fechaZ:
                facturaEncontrada = factura
                self.listaFacturas.remove(factura)
                break
            
        if facturaEncontrada:
            self.formulario_edicion(facturaEncontrada)
  
        else:
            messagebox.showerror("Error", "No se encontró una factura con los datos proporcionados")

    def formulario_edicion(self, factura):
        ''' Método para editar los campos de la factura seleccionada manualmente:
        Se van a mostrar todas los campos de la factura original y se podrán editar
        Cuando se acabe se pulsa el botón de editar factura y se invoca el método de guardar_cambios
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

        # Se recuperan los elementos de la lista de elementos de la factura y se pasan a anadir_elemento para que los muestre
        for elemento in factura['listaElementos']:
            self.anadir_elemento(elemento[0], elemento[1], elemento[2])
            
                    # /// Se hace un botón para los elementos, se le asigna el comando anadir_elemento y se empaqueta luego        
        self.botonElemento = tk.Button(self.ventana_EditarFactura, text="Añadir Elemento", command=self.anadir_elemento) 
        self.botonElemento.pack(pady = 5)  
                    # /// Se hace un botón para los guardar, se le asigna el comando guardar_cambios y se empaqueta luego  
        self.botonGuardar = tk.Button(self.ventana_EditarFactura, text="Guardar Cambios", command=lambda: self.guardar_cambios(factura))
        self.botonGuardar.pack(pady=10)

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
    
    def anadir_elemento(self, unidades="0", elemento="", precio="0"):
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

    def guardar_cambios(self, factura):
        ''' Método para guardar los cambios realizados en la factura:
        Se borra el PDF antiguo y el diccionario antiguo para volver a introducirlos posteriormente modificados
        Se asignan los valores introducios en el formulario de edición al diccionario de la factura seleccionada (datos_factura)
        Se realiza un append de este diccionario a la lista de diccionarios
        Se pasa a formato json y se sobreescribe al anterior
        Se muestra un mensaje conforme la factura ha sido guardada
        La diferencia aqui no se destruye la ventana de modificar factura porque nunca se generó (si no, peta)
        Se invoca al método de crear_pdf
        '''
        # Uso la terminación en Z para decir que es la final
        fechaCorregidaZ = self.fechaZ.replace('/', '_')

        ruta_pdf = f"PDF/{fechaCorregidaZ}_{self.numeroFacturaZ}.pdf"
        # Elimino el documento PDF
        if os.path.exists(ruta_pdf):
            os.remove(ruta_pdf)
        #Cargo la lista de elementos de la factura
        listaFinalElementos = []
        for unidad, elemento, precio in self.listaElementos:
            unidad = str(unidad.get().lower().strip())
            elemento= str(elemento.get().lower().strip())
            precio= str(precio.get().lower().strip())
            listaFinalElementos.append([unidad, elemento, precio])
        # Obtención de las variables que van a ir en los elementos del diccionario de la factura
        numFact = str(self.numeroFactura.get().lower().strip())
        date_fecha = self.fecha.get().lower().strip()
        client = str(self.cliente.get().lower().strip())
        dni = str(self.dni.get().lower().strip())
        
        # En el caso de que el usuario haya borrado la fecha o haya puesto una fecha no válida, va a poner la del día en que se está haciendo la factura, luego la puede modificar
        if date_fecha:
            if len(date_fecha) == 10:
                pass
            else:                
                hoy= date.today()
                dia= hoy.strftime("%d")
                mes= hoy.strftime("%m")
                anyo= hoy.strftime("%Y")
                fecha0= f'{dia}/{mes}/{anyo}'
                date_fecha = fecha0
                messagebox.showinfo('Error', f'La fecha introducida no era válida. Se ha asignado la siguiente {date_fecha}.') 
        else:
            hoy= date.today()
            dia= hoy.strftime("%d")
            mes= hoy.strftime("%m")
            anyo= hoy.strftime("%Y")
            fecha0= f'{dia}/{mes}/{anyo}'
            date_fecha = fecha0  
            messagebox.showinfo('Error', f'La fecha introducida no era válida. Se ha asignado la siguiente {date_fecha}.')

        self.datos_factura = {
            'numeroFactura': numFact,
            'fecha': date_fecha,
            'cliente': client,
            'dni': dni,
            'listaElementos': listaFinalElementos 
        }
        
        #Se le asigna el nombre de sn si no hay campo en número de factura y si existe un número de factura con el mismo nombre le va añadiendo copia -
        if self.datos_factura['numeroFactura'] == '':
            self.datos_factura['numeroFactura'] = 'sn'

        for factura in self.listaFacturas:
            if factura['numeroFactura'] == self.datos_factura['numeroFactura']:
                self.datos_factura['numeroFactura'] = f"copia - {self.datos_factura['numeroFactura']}" #{random.randint(0, 1000)}

        # Herramienta para ver si no hay datos en algún campo de unidad y precio para que se sustituya por un '0'       
        # for elemento1 in self.datos_factura['listaElementos']:
        #     if elemento1[0].isdigit():
        #         elemento1[0] = elemento1[0]
        #     else:
        #         elemento1[0] = '0'                
        
        # for elemento2 in self.datos_factura['listaElementos']:
        #     if elemento2[2].isdigit():
        #         elemento2[2] = elemento2[2]
        #     else:
        #         elemento2[2] = '0'   

        ################################
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
        ################################

        self.listaFacturas.append(self.datos_factura)
        contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
        self.path.write_text(contenido)
        messagebox.showinfo("Éxito", "Factura guardada")
        self.ventana_EditarFactura.destroy()
        CPDF(self.datos_factura)