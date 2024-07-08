# Importaciones de librerías
from tkinter import messagebox                          # Mostrar mensaje de creación del PDF
import sys                                              # Necesario para que no haya errores a la hora de importar módulos
from fpdf import FPDF                                   # Necesario para crear el archivo PDF
from datetime import date                               # Necesario para manejar fechas

sys.path.append('.')

from modulos.colores_y_rutas import *                   # Necesario para autoasignar ciertos campos de la factura


def crear_pdf(datos_factura):

        datos_factura
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

        ruta_pdf = f"PDF/{fecha}_{datos_factura['numeroFactura']}.pdf"

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
        nf = datos_factura['numeroFactura']
        f  = datos_factura['fecha']
        c  = datos_factura['cliente']
        d  = datos_factura['dni']

        lista_datos ={
        'numeroFactura': nf.title(),
        'fecha': f,
        'cliente': c.title(),
        'DNI/NIF': d.title()
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
        
        tabla2 = datos_factura['listaElementos'] # tabla2 = [unidades, concepto , precio U., total]
        indice = len(tabla2)
        seguro = True
        contador = 0
        
        # Bucle while que va a ejecuarse tantas veces como elementos tenga una factura y se va a encargar de elminar los elementos que tengan un 0 en las unidades
        while seguro:
            if contador == indice:
                seguro = False 
            for elementoFactura in tabla2:
                #Prueba
                if elementoFactura[0] == '0':
                    messagebox.showinfo(f"¡Cuidado!", f"{elementoFactura[1]}\n No tiene unidades o estas son 0\n No constará en el PDF") # Avisa que hay elementos con 0 en sus unidades
                    tabla2.remove(elementoFactura)

                else:
                    pass
            contador+=1
        if not tabla2:
            messagebox.showinfo("Cuidado", "Has imprimido una factura sin elementos")

        for elemento in tabla2:
            # Se convierten los elementos de unidades y total a float
            if elemento[0]:
                elemento[0] = float(elemento[0])
            else:
                pass
            if elemento[2]:
                elemento[2] = float(elemento[2])
            else:
                pass

            pdf.cell(w = 30, h = 10, txt = f'{elemento[0]}', border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 100, h = 10, txt = elemento[1].capitalize(), border = 1, align = 'C', fill= 0) 
            pdf.cell(w = 30, h = 10, txt = f'{elemento[2]} {chr(128)}', border = 1, align = 'C', fill= 0) 
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
        for lista in datos_factura['listaElementos']:
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