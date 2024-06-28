import tkinter as tk
from tkinter.font import Font
from pathlib import Path

import sys

sys.path.append('.') # para añadir el directorio principal de donde estás ejecutando el programa (la raiz)


from utilidades_ventana.generic import leer_imagen as leer , centrar_ventanas as centrar
# import utilidades_ventana.generic as utl
from modulos.colores import *

from modulos.opciones import VentanaCrear as VC

class MenuPrincipal(tk.Tk):

    def ir_crear(self):
        '''Método que permite ir a crear una factura'''
        self.MP.destroy() # Eliminamos la ventana
        VC() # Muestra el menú principal

    def __init__(self):
        super().__init__()

        # Importamos el logo de la carpeta imagenes, le asignamos un tamaño y la ponemos dentro de una etiquta (toda la pantalla)
        ruta_logo = Path('imagenes/cuadrado.png')
        self.logo = leer(ruta_logo, (560, 136))
        self.perfil= leer(ruta_logo, (100, 100))
        self.configuracion_ventana()
        self.paneles()
        self.controles_barra_superior()
        self.controles_barra_lateral()

        label = tk.Label(self.ventana, image = self.logo, bg = '#fcfcfc')
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configuracion_ventana(self): # Configuración de la ventana del menú principal
        self.title('Menú Principal') # Se coloca el título de la ventana
        ruta_icono_menu = 'imagenes/lego.png'
        self.iconbitmap(ruta_icono_menu)

        w, h = 1024, 600 # Tamaño de la ventana
        self.geometry("%dx%d+0+0" % (w,h)) # Formateo de tuplas donde se indica el ancho y lo alto
        centrar(self, w, h)
    
    def paneles(self): # Creación de los paneles: Barra menú superior, menú lateral y cuerpo principal con instrucciones
            #Menú superior
        self.barra_superior = tk.Frame(
            self,
            bg= color_menu_superior,
            height= 50
            )
        self.barra_superior.pack(side= tk.TOP, fill= 'both')
            
            # Menú lateral
        self.menu_lateral = tk.Frame(
            self,
            bg= color_menu_lateral,
            width= 150
            )
        self.menu_lateral.pack(side= tk.LEFT, fill= 'both', expand= False)

            # Cuerpo central
        self.cuerpo = tk.Frame(
            self,
            bg= color_cuerpo
            )
        self.cuerpo.pack(side= tk.RIGHT, fill= 'both', expand= True)

    def controles_barra_superior(self):

        # Etiqueta del título
        self.labelTitulo = tk.Label(self.barra_superior, text= 'Empresa X')
        self.labelTitulo.config(fg= '#fff', font=('Roboto', 15), bg= color_menu_superior, pady= 10, width= 16)
        self.labelTitulo.pack(side= tk.LEFT)

        #Botón del menú lateral
        self.botonMenuLateral= tk.Button(self.barra_superior, text= 'Menu', font= ('Roboto', 12), 
                                           command=self.toggle_panel,
                                           bd= 0, bg= color_menu_superior, fg= 'white')
        self.botonMenuLateral.pack(side= tk.LEFT)

        # Etiqueta web de la empresa
        self.labelTitulo2= tk.Label(self.barra_superior, text= 'www.webempresa.com')
        self.labelTitulo2.config(fg= '#fff', font= ('Roboto', 10), bg=color_menu_superior, padx= 10, width= 20)
        self.labelTitulo2.pack(side= tk.RIGHT)
    
    def controles_barra_lateral(self):
        # Configuración menú lateral
        ancho = 20
        alto = 2

        # Etiqueta Perfil: foto de la empresa
        self.labelPerfil= tk.Label(self.menu_lateral, image= self.perfil, bg= color_menu_lateral)
        self.labelPerfil.pack(side= tk.TOP, pady= 10)

        # Botones sección del menú lateral
        self.botonCrear= tk.Button(self.menu_lateral)
        self.botonEliminar= tk.Button(self.menu_lateral)             
        self.botonBuscar= tk.Button(self.menu_lateral)        
        self.botonMostrar= tk.Button(self.menu_lateral)
        self.botonSalir= tk.Button(self.menu_lateral)
        self.botonDatos= tk.Button(self.menu_lateral)

        botones_info= [
            ('Crear Factura', '1)', self.botonCrear), # Texto, icono y objeto a insertar
            ('Eliminar Factura', '2)', self.botonEliminar),
            ('Buscar Factura', '3)', self.botonBuscar),
            ('Mostrar Factura', '4)', self.botonMostrar),
            ('Salir', '5)', self.botonSalir),
            ('Analítica datos', '6)', self.botonDatos)            
            ]
        for texto, icono, boton in botones_info:
            self.configurar_boton_menu(boton, texto, icono, ancho, alto)
    
    def configurar_boton_menu(self, boton, texto, icono, ancho, alto):
        boton.config(text= f" {icono}  {texto}", anchor= "w", bd= 0, bg= color_menu_lateral, fg= 'white', width= ancho, height= alto)
        boton.pack(side= tk.TOP)
        self.bind_hover_events(boton)
        # self.botonCrear.bind('<Return>', (lambda event: self.crear_factura()))
        

    def bind_hover_events(self, boton): # para que cuando pases se cambie el color
        #Asociar eventos Enter y Leave con la función dinámica
        boton.bind("<Enter>", lambda event: self.on_enter(event, boton))
        boton.bind("<Leave>", lambda event: self.on_leave(event, boton))
    
    def on_enter(self, event, boton):
        # Cambio el estilo al pasar con el ratón por encima
        boton.config(bg= color_menu_cursor_encima, fg= 'white')

    def on_leave(self, event, boton):
        # Si no está el ratón encima vuelve al color original
        boton.config(bg= color_menu_lateral, fg= 'white')

    def toggle_panel(self): # ALtera la visibilidad dentro de tkinter, en el menu lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side= tk.LEFT, fill= 'y')
            

