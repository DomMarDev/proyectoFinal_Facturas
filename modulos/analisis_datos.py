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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Prueba
from modulos. creacionPDF import crear_pdf as CPDF


class AnalizarFactura():

    def __init__(self, root):
        ''' Método para crear la ventana de Analisis de datos:
        Se le asigna un título, unas dimensiones base, se centra en el centro de la pantalla'''
        self.root = root
        self.root.title("Analitica de Facturas") # Título
        w, h = 500, 100  # Tamaño de la ventana
        centrar(self.root, w, h) # Centrado
        # Configuración del menú superior y botón Crear
        self.barraMenu = tk.Menu(self.root) 
        self.root.config(menu=self.barraMenu)
        self.root.resizable(False,False)

        # Botón de Analizar todas las facturas
        botonCrear= tk.Button(self.root,
                                text = 'Analizar',
                                font = ('Times', 15),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command =  self.abrir_json)
        botonCrear.pack(fill = tk.X, padx = 20, pady = 30)

        
        self.menuFactura = tk.Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Facturas", menu=self.menuFactura)
        self.menuFactura.add_command(label="Analizar Facturas", command=self.abrir_json)# Si se quiere abrir Json, cambiar abrir_json por add_factura
        self.menuFactura.add_separator()
        self.menuFactura.add_command(label="Salir", command=self.root.destroy)
        
    def abrir_json(self):
        ''' Método para abrir el archivo json automáticamente:
        1) Asignamos la ruta
        2) Si existe el archivo se invoca a la clase para introducir los datos de la factura
        '''
        self.root.destroy()
        ruta_Json = 'archivoJson/facturas.json'
        if ruta_Json:
            self.ventana_anadir_factura = Datos_Facturas(ruta_Json)
            self.ventana_anadir_factura.mostrar_analisis()


class Datos_Facturas:
                
    def __init__(self, ruta):
        ''' Se rescata la ruta del archivo json "facturas.json" y se carga para editarlo.'''
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas)

    def mostrar_analisis(self):

        # El array será una lista con los valores del total de la factura sumados / dia 
        iva = 1.21
        listaTotalesFacturas = []
        listaFechasFacturas = []
        for factura in self.listaFacturas:
            if factura:
                fechaFactura = f"{factura['fecha']}.{factura['numeroFactura']}"
                listaTotal = []
               
                for datos in factura['listaElementos']:
                    unidades = datos[0]
                    precio = datos[2]
                    total = (float(unidades) * float(precio))*iva
                    listaTotal.append(total)

            listaTotalesFacturas.append(sum(listaTotal))
            listaFechasFacturas.append(fechaFactura)

        if self.listaFacturas:

            # Generación del Gráfico
            plt.figure('Facturación', figsize = (10, 5))        

            plt.style.use('ggplot')
            
            for i in range(len(listaTotalesFacturas)):
                plt.bar(listaFechasFacturas, listaTotalesFacturas, color="blue", label="Python")
            
            plt.title("Beneficios/factura", fontsize= 24)
            plt.xlabel("Factura", fontsize= 14)
            plt.ylabel("Beneficios (€)", fontsize= 14)
            plt.show()
        else:
            messagebox.showinfo('Error', 'No hay facturas en la base de datos.')