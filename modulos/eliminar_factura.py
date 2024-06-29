import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog as FD
import sys
from fpdf import FPDF
from datetime import date

sys.path.append('.')

from modulos.leer_archivo import Lectura_archivo
from modulos.generic import leer_imagen as leer , centrar_ventanas as centrar

class Eliminar:

    def __init__(self, ruta):
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)

    def eliminar_factura(self):
            self.ventana_eliminar = tk.Toplevel()
            self.ventana_eliminar.title("Eliminar Factura")
            w, h = 500, 100  # Tamaño de la ventana
            centrar(self.ventana_eliminar, w, h)

            self.numeroFacturaEliminar = self.entradaDatos(self.ventana_eliminar, "Introduce el Nº de la factura a eliminar: ")
            self.fechaEliminar = self.entradaDatos(self.ventana_eliminar, "Introduce la fecha de la factura (dd/mm/yyyy): ")

            self.botonEliminar = tk.Button(self.ventana_eliminar, text="Eliminar Factura", command=self.borrado_factura)
            self.botonEliminar.pack(pady=10)
    
    def entradaDatos(self, ventana_facturas, texto):
        frame = tk.Frame(ventana_facturas)
        frame.pack(pady=5)
        label = tk.Label(frame, text=texto)
        label.pack(side=tk.LEFT)
        entrada = tk.Entry(frame, width=50)
        entrada.pack(side=tk.LEFT)
        return entrada

    def borrado_factura(self):
            numeroFactura = self.numeroFacturaEliminar.get().lower().strip()
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
                self.ventana_eliminar.destroy()
            else:
                messagebox.showerror("Error", "Factura no encontrada")
    ###################################################
    def borrado_factura2(self, nombrePDF):
        
        self.nombrePDF = str(nombrePDF)

        numFactura0= self.nombrePDF[11:]
        fecha1= self.nombrePDF[0:10]
        fecha0 = fecha1.replace('_', '/')
        numeroFactura = numFactura0
        fecha = fecha0

        factura_encontrada = False

        for factura in self.listaFacturas:
            if factura['numeroFactura'] == numeroFactura and factura['fecha'] == fecha:
                self.listaFacturas.remove(factura)
                factura_encontrada = True
                break

        if factura_encontrada:
            contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
            self.path.write_text(contenido)

            fechaCorregida = fecha.replace('/', '_')

            ruta_pdf = f"PDF/{fechaCorregida}_{numeroFactura}.pdf"

            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)

            messagebox.showinfo("Éxito", "Factura eliminada correctamente")
            self.ventana_eliminar.destroy()
        else:
            messagebox.showerror("Error", "Factura no encontrada")
    ###############################################

class EliminarFactura():

    def __init__(self, root):
        self.root = root
        self.root.title("Eliminar Factura")
        w, h = 500, 200  # Tamaño de la ventana
        centrar(self.root, w, h)
        self.barraMenu = tk.Menu(self.root)
        self.root.config(menu=self.barraMenu)
        self.root.resizable(False, False)

        botonCrear= tk.Button(self.root,
                                text = 'Eliminar',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.abrir_json)
        botonCrear.pack(fill = tk.X, padx = 20, pady = 30)

        botonBuscarEliminar= tk.Button(self.root,
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

    # Por si queremos que el usuario escoja el PDF
        self.menuArchivo = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Archivo", menu=self.menuArchivo)
        self.menuArchivo.add_command(label="Abrir PDF de Facturas", command=self.abrir_PDF)
        self.menuArchivo.add_separator()
        self.menuArchivo.add_command(label="Salir", command=self.root.quit)


        self.menuFactura = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Facturas", menu=self.menuFactura)
        self.menuFactura.add_command(label="Eliminar Factura", command=self.abrir_json) # Si se quiere abrir Json, cambiar abrir_json por eliminar_factura
    
    #Por si queremos que el usuario escoja el json
    # def abrir_json(self):
    #     ruta_Json = FD.askopenfilename(title="Selecciona el archivo de facturas", filetypes=[("Archivo JSON", "*.json"),], initialdir= 'archivoJson')
    #     if ruta_Json:
    #         self.ventana_anadir_factura = Eliminar(ruta_Json)
    #         self.ventana_anadir_factura.eliminar_factura()
    
    def abrir_PDF(self):
        ruta_PDF   = FD.askopenfilename(title="Selecciona la factura a modificar", filetypes=[("Archivo PDF", "*.pdf"),], initialdir= 'PDF')
        nombre_PDF = Path(ruta_PDF).stem

        ruta_Json  = 'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_modificar_factura = Eliminar(ruta_Json)
            self.ventana_modificar_factura.borrado_factura2(nombre_PDF)
    
    def abrir_json(self):
        ruta_Json = 'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_anadir_factura = Eliminar(ruta_Json)
            self.ventana_anadir_factura.eliminar_factura()
    
    #Por si queremos que el usuario escoja el json
    # def eliminar_factura(self):
    #     if hasattr(self, 'Ventana de Añadir Factura'):
    #         self.ventana_anadir_factura.eliminar_factura()
    #     else:
    #         messagebox.showwarning("Archivo no seleccionado", "Primero seleccione un archivo JSON de facturas desde el menú Archivo -> Abrir JSON de Facturas.")