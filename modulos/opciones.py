import tkinter as tk
from tkinter.font import Font

from modulos.generic import leer_imagen as leer , centrar_ventanas as centrar

from modulos.colores import *

from modulos.crear_PDF import crear_pdf as CPDF


class VentanaCrear(tk.Toplevel): # Hereda de tk.Toplevel para que cuando se muera la ventana principal se muera tambien esta.
    
    def __init__(self):
        super().__init__()
    
    def configuracion_ventana(self): # Configuración de la ventana del menú principal
        self.title('Opciones') # Se coloca el título de la ventana
        ruta_icono_menu = 'imagenes\lego.png'
        self.iconbitmap(ruta_icono_menu)

        w, h = 400, 100 # Tamaño de la ventana
        self.geometry("%dx%d+0+0" % (w,h)) # Formateo de tuplas donde se indica el ancho y lo alto
        centrar(self, w, h)
    
    def construirWidget(self):
        self.labelVersion= tk.Label( self, text= 'Version 1') # Para poner una label
        self.labelVersion.config(fg='#000000')
        

