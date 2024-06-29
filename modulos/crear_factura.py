import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog as FD
import sys
from fpdf import FPDF
from datetime import date


sys.path.append('.')

from modulos.generic import leer_imagen as leer , centrar_ventanas as centrar
from modulos.leer_archivo import Lectura_archivo

from ruta import ruta

class Datos_Factura:

    def __init__(self, ruta):
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)

    def add_factura(self):
        self.ventana_facturas = tk.Toplevel()
        self.ventana_facturas.title("Añadir Factura")
        w, h = 500, 500  # Tamaño de la ventana
        centrar(self.ventana_facturas, w, h)

        fecha = date.today()

        self.numeroFactura = self.entradaDatos(self.ventana_facturas, "Introduce el Nº de la factura: ")
        self.fecha = fecha.strftime("%d/%m/%Y")
        self.cliente = self.entradaDatos(self.ventana_facturas, "Introduce el cliente: ")
        self.dni = self.entradaDatos(self.ventana_facturas, "Introduce el DNI del cliente: ")

        self.listaElementos = []
        self.elementos_frame = tk.Frame(self.ventana_facturas)
        self.elementos_frame.pack(pady=10)
        self.botonElemento = tk.Button(self.ventana_facturas, text="Añadir Elemento", command=self.anadir_elemento)
        self.botonElemento.pack(pady=5)

        self.botonGuardar = tk.Button(self.ventana_facturas, text="Guardar Factura", command=self.guardar_factura)
        self.botonGuardar.pack(pady=10)

    def entradaDatos(self, ventana_facturas, texto):
        frame = tk.Frame(ventana_facturas)
        frame.pack(pady=5)
        label = tk.Label(frame, text=texto)
        label.pack(side=tk.LEFT)
        entrada = tk.Entry(frame, width=50)
        entrada.pack(side=tk.LEFT)
        return entrada

    def anadir_elemento(self):
        frame = tk.Frame(self.elementos_frame)
        frame.pack(pady=5)

        etiquetaUnidades = tk.Label(frame, text="Unidades:")
        etiquetaUnidades.pack(side=tk.LEFT)
        entradaUnidades = tk.Entry(frame, width=5)
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

    def guardar_factura(self):# Esto lo he tenido que pedir a una IA, no me salía
        self.datos_factura = {
            'numeroFactura': self.numeroFactura.get().lower().strip(),
            'fecha': self.fecha,
            'cliente': self.cliente.get().lower().strip(),
            'dni': self.dni.get().lower().strip(),
            'listaElementos': [[unidades.get().lower().strip(), elemento.get().lower().strip(), precio.get().lower().strip()] for unidades, elemento, precio in self.listaElementos] 
        }

        self.listaFacturas.append(self.datos_factura)
        contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
        self.path.write_text(contenido)
        messagebox.showinfo("Éxito", "Factura guardada")
        self.ventana_facturas.destroy()
        self.crear_pdf()
    
    def crear_pdf(self):
        # doc = input('Dime el nombre del documento')

        # ruta_pdf = f'factura_DM\PDF/{doc}.pfd' 


        # Ruta para guardar el PDF

        hoy= date.today()
        dia= hoy.strftime("%d")
        mes= hoy.strftime("%m")
        anyo= hoy.strftime("%Y")
        fecha= f'{dia}_{mes}_{anyo}'

        ruta_pdf = f"PDF/{fecha}_{self.datos_factura['numeroFactura']}.pdf"

        # Creamos el PDF:
        pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')

        pdf.add_page()

        pdf.set_font('Times', '', 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)

        # Elementos del PDF

        ruta_logo = 'imagenes\lego.png'

        pdf.image(ruta_logo, x = 10, y = 10, w = 30, h= 30) # Logo


        # pdf.text(x= 60, y = 50, txt = 'FACTURA' ) # Título 'Factura'

        pdf.set_font('Times', '', 50) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 0, h = 15, txt = 'Factura', border = 0, ln = 1, align = 'C', fill= 0) # Título Factura

        pdf.set_font('Times', '', 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)

        # Datos de mi empresa
        info_empresa = f'DOMINGO MARCHAN DEL PINO\nC/ CIFO la Violeta\nBarcelona\nCP Barcelona\nTlf.: +34 XXXXXXXXX\nC.I.F./N.I.F.: DNI\nDomingo-Marchan@hotmail.com' 
        pdf.multi_cell(w = 0, h = 5, txt = info_empresa, border = 0, align = 'R', fill= 0) # Info Empresa

        # Tabla datos factura:

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

        # encabezados datos cliente
        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 30, h = 10, txt = 'Nº factura', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Fecha', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Cliente', border = 1, align = 'C', fill= 0) 
        pdf.multi_cell(w = 30, h = 10, txt = 'DNI/NIF', border = 1, align = 'C', fill= 0)

        # Valores datos cliente
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 30, h = 10, txt = lista_datos['numeroFactura'], border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = lista_datos['fecha'], border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = lista_datos['cliente'], border = 1, align = 'C', fill= 0) 
        pdf.multi_cell(w = 30, h = 10, txt = lista_datos['DNI/NIF'], border = 1, align = 'C', fill= 0)

        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía

        # Encabezados datos a facturar

        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía
        pdf.set_font('Times', "B", 13) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)

        pdf.cell(w = 30, h = 10, txt = 'Unidades', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 100, h = 10, txt = 'Concepto', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Precio U.', border = 1, align = 'C', fill= 0) 
        pdf.multi_cell(w = 30, h = 10, txt = 'Total', border = 1, align = 'C', fill= 0)

        # Valores factura
        #lista_factura = ((unidades, 'Concepto', Precio U., Total))
        
        
        pdf.set_font('Times', "", 12,  ) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        lista2 = self.datos_factura['listaElementos']

        for elemento in lista2:
            elemento[0] = float(elemento[0])
            elemento[2] = float(elemento[2])
            pdf.cell(w = 30, h = 10, txt = f'{elemento[0]}', border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 100, h = 10, txt = elemento[1], border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 30, h = 10, txt = f'{elemento[2]}' + chr(128), border = 1, align = 'C', fill= 0) 
            pdf.multi_cell(w = 30, h = 10, txt = f'{elemento[0]*elemento[2]} {chr(128)}', border = 1, align = 'C', fill= 0)


        # Resumen precio factura

        # Encabezados Resumen factura

        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía
        pdf.set_font('Times', "B", 13) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)

        pdf.cell(w = 40, h = 10, txt = 'Importe Bruto', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 20, h = 10, txt = 'IVA % *', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 40, h = 10, txt = 'Base Imponible', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 40, h = 10, txt = 'IVA *', border = 1, align = 'C', fill= 0)
        pdf.multi_cell(w = 50, h = 10, txt = 'Total Factura', border = 1, align = 'C', fill= 0) 


        # Valores factura
        #lista_factura = ((unidades, 'Concepto', Precio U., Total))
        suma1 = 0
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        for lista in self.datos_factura['listaElementos']:
            lista[0] = float(lista[0])
            lista[2] = float(lista[2])
            suma1 = lista[0]*lista[2] + suma1


        pdf.cell(w = 40, h = 10, txt = f'{str(suma1)} {chr(128)}', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 20, h = 10, txt ='21 %', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 40, h = 10, txt = f'{str(suma1)} {chr(128)}', border = 1, align = 'C', fill= 0)
        pdf.cell(w = 40, h = 10, txt = f'{str(suma1 * 0.21)} ' + chr(128), border = 1, align = 'C', fill= 0)  
        pdf.multi_cell(w = 50, h = 10, txt = f'{str(suma1 * 1.21)} {chr(128)}', border = 1, align = 'C', fill= 0)

        hoy= date.today()
        mes= int(hoy.strftime("%m"))
        anyo= hoy.strftime("%Y")
        mesFin= str(mes+1)
        if len(mesFin) == 1:
            mesFin = f'0{mesFin}'
        fechafin= f'01/{mesFin}/{anyo}'
        

        # Como pagar la factura:
        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Vencimiento', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = fechafin , border = 1, align = 'C', fill= 0) 

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Forma de Pago', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = 'Contado' , border = 1, align = 'C', fill= 0) 

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Banco', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = 'La Caixa' , border = 1, align = 'C', fill= 0)

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'IBAN', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = 'ES ................' , border = 1, align = 'C', fill= 0) 


        pdf.output(ruta_pdf)    

    

class CrearFactura():

    def __init__(self, root):
        
        self.root = root
        self.root.title("Crear Factura")
        w, h = 500, 100  # Tamaño de la ventana
        centrar(self.root, w, h)
        
        self.barraMenu = tk.Menu(self.root)
        self.root.config(menu=self.barraMenu)
        self.root.resizable(False,False)
    

        botonCrear= tk.Button(self.root,
                                text = 'Crear',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.abrir_json)
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


    #Por si queremos que el usuario escoja el json
    # def abrir_json(self):
    #     ruta_Json = FD.askopenfilename(title="Selecciona el archivo de facturas", filetypes=[("Archivo JSON", "*.json"),], initialdir= 'archivoJson')
    #     if ruta_Json:
    #         self.ventana_anadir_factura = Datos_Factura(ruta_Json)
    #         self.ventana_anadir_factura.add_factura()
    
    def abrir_json(self):
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
    