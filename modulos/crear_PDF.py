from fpdf import FPDF
import datetime

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
from pathlib import Path

import utilidades_ventana.generic as utl


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
class CrearPDF:
    
    # Ventana para rellenar datos:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Crear Factura') # Se coloca el título de la ventana
        
        # Se busca el ancho y lo alto de la ventana, para que se maximice
        w, h = self.ventana.winfo_screenmmwidth(), self.ventana.winfo_screenmmheight()
        
        # Formateo de tuplas donde se indica el ancho y lo alto
        self.ventana.geometry("%dx%d+0+0" % (w,h))
        
        # Configuramos el fondo de la ventana -> blanco (#fcfcfc). Y que no redimensione la ventana.
        self.ventana.config(bg = '#fcfcfc')
        self.ventana.resizable(width = 0, height = 0 )

        # Centramos la ventana
        utl.centrar_ventanas(self.ventana, 800, 500)


        # Variables:
        self.numero_factura = '49-K' 
        day0 = datetime.date.today()
        self.fecha_Pagar = str(day0 + datetime.timedelta(days = 30)) # Se paga a 30 días de que se crea la factura
        self.cliente = input('')
        self.dni_nif = input('')
        
        #lista_factura = ((unidades, 'Concepto', Precio U., Total))

        tabla= ttk.Treeview(self.ventana, columns = 4)
        tabla.grid(row=4)

        lista_elementos = tk.Listbox(self.ventana)

        for indice, elemento in enumerate(lista_elementos):
            lista_elementos.insert(indice, ('unidades', 'Concepto', 'Precio U.', 'Total'))


        #factura = consulta(conexion)


        # Colocar datos de nuestra base de datos en una tabla https://www.youtube.com/watch?v=O-Q_Y1_wV-E&ab_channel=ProgramadorNovato


    
    def crear_pdf(self):
        # doc = input('Dime el nombre del documento')

        # ruta_pdf = f'factura_DM\PDF/{doc}.pfd' 

        ruta_pdf = 'factura_DM\PDF/hojaPrueba.pfd' 


        # Creamos el PDF:
        pdf = FPDF(orientation = 'P', unit = 'mm', format = 'A4')

        pdf.add_page()

        pdf.set_font('Times', '', 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)


        # Elementos del PDF

        ruta_logo = 'factura_DM\imagenes\lego.png'

        pdf.image(ruta_logo, x = 10, y = 10, w = 30, h= 30) # Logo



        # pdf.text(x= 60, y = 50, txt = 'FACTURA' ) # Título 'Factura'


        pdf.set_font('Times', '', 50) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 0, h = 15, txt = 'Factura', border = 0, ln = 1, align = 'C', fill= 0) # Título Factura

        pdf.set_font('Times', '', 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)


        # Datos de mi empresa
        info_empresa = f'DOMINGO MARCHAN DEL PINO\nC/ CIFO la Violeta\nBarcelona\nCP Barcelona\nTlf.: +34 XXXXXXXXX\nC.I.F./N.I.F.: DNI\nDomingo-Marchan@hotmail.com' 
        pdf.multi_cell(w = 0, h = 5, txt = info_empresa, border = 0, align = 'R', fill= 0) # Info Empresa

        # Tabla datos factura:
        numero_factura = '49-K' 
        day0 = datetime.date.today()
        fecha_Pagar = str(day0 + datetime.timedelta(days = 30)) # Se paga a 30 días de que se crea la factura
        cliente = 'K'
        dni_nif = 'sadjka8-K'



        lista_datos ={
            'numero factura': numero_factura,
            'fecha': fecha_Pagar,
            'cliente': cliente,
            'DNI/NIF': dni_nif
            } 
        # encabezados datos cliente
        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 30, h = 10, txt = 'Nº factura', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Fecha', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 30, h = 10, txt = 'Cliente', border = 1, align = 'C', fill= 0) 
        pdf.multi_cell(w = 30, h = 10, txt = 'DNI/NIF', border = 1, align = 'C', fill= 0)

        # Valores datos cliente
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 30, h = 10, txt = lista_datos['numero factura'], border = 1, align = 'C', fill= 0) 
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

        lista_factura = (
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 "),
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 "),
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 "),
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 "),
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 "),
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 "),
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 "),
            ("2", "Macarrones a la bolonyesa y mucha carne picada jaja", "20 ", "40 ")
            )

        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        for lista in lista_factura:
            pdf.cell(w = 30, h = 10, txt = lista[0], border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 100, h = 10, txt = lista[1], border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 30, h = 10, txt = lista[2] + ' euros', border = 1, align = 'C', fill= 0) 
            pdf.multi_cell(w = 30, h = 10, txt = lista[3] + ' euros', border = 1, align = 'C', fill= 0)


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
        for lista in lista_factura:
            suma1 = float(lista[3]) + suma1


        pdf.cell(w = 40, h = 10, txt = f'{str(suma1)} euros', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 20, h = 10, txt ='21 %', border = 1, align = 'C', fill= 0) 
        pdf.cell(w = 40, h = 10, txt = f'{str(suma1)} euros', border = 1, align = 'C', fill= 0)
        pdf.cell(w = 40, h = 10, txt = f'{str(suma1 * 0.21)} euros', border = 1, align = 'C', fill= 0)  
        pdf.multi_cell(w = 50, h = 10, txt = f'{str(suma1 * 1.21)} euros', border = 1, align = 'C', fill= 0)


        # Como pagar la factura:
        pdf.multi_cell(w = 0, h = 5, txt = '', border = 0, align = 'C', fill= 0) #Linea vacía

        pdf.set_font('Times', "B", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente)
        pdf.cell(w = 40, h = 10, txt = 'Vencimiento', border = 1, align = 'C', fill= 0)
        pdf.set_font('Times', "", 12) #pdf.set_font('Fuente', 'BOLD etc', Tamaño fuente) 
        pdf.multi_cell(w = 150, h = 10, txt = fecha_Pagar , border = 1, align = 'C', fill= 0) 

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