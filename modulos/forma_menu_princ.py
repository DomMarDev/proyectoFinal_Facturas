import sys

sys.path.append('.')

import os
import tkinter as tk
from tkinter import font
from tkinter.font import Font
from tkinter import ttk, messagebox
from pathlib import Path
from tkinter import filedialog as FD


 # para añadir el directorio principal de donde estás ejecutando el programa (la raiz)


from modulos.generic import leer_imagen as leer , centrar_ventanas as centrar
# import utilidades_ventana.generic as utl
from modulos.colores import *

from modulos.crear_factura import CrearFactura as CF
from modulos.eliminar_factura import EliminarFactura as EF





class MenuPrincipalFinal(tk.Tk):

    def crear_facturas(self):
        '''Método que permite ir a crear una factura'''
        self.new_window = tk.Toplevel(self)
        CF(self.new_window)


    def eliminar_facturas(self):
        '''Método que permite ir a crear una factura'''
        self.new_window = tk.Toplevel(self)
        EF(self.new_window)


    def mostrar_facturas(self):
        '''Método para mostrar las facturas'''
        archivo = FD.askopenfile(title='Dale a Abrir con...', initialdir='PDF',
                                 filetypes=(('Archivo PDF', '*.pdf'),))  # título ventana, directorio inicial donde buscar y tipo archivos

        if archivo is not None:  # Si hay algo en el archivo va a abrirlo usando su ruta
            ruta_pdf = Path(archivo.name)  # Se obtiene la ruta del archivo
            os.startfile(ruta_pdf)  # Se abre el archivo

    def __init__(self):
        super().__init__()

        # Importamos el logo de la carpeta imágenes, le asignamos un tamaño y la ponemos dentro de una etiqueta
        self.logo = leer("imagenes/lego.png", (560, 136))
        self.perfil = leer("imagenes/cuadrado.png", (100, 100))
        self.configuracion_ventana()
        self.paneles()
        self.controles_barra_superior()
        self.controles_barra_lateral()
        self.controles_cuerpo()

    def configuracion_ventana(self):  # Configuración de la ventana del menú principal
        self.title('Menú Principal')  # Se coloca el título de la ventana
        ruta_icono_menu = 'imagenes/lego.png'
        self.iconbitmap(ruta_icono_menu)
        w, h = 1024, 600  # Tamaño de la ventana
        centrar(self, w, h)

    def paneles(self):  # Creación de los paneles: Barra menú superior, menú lateral y cuerpo principal con instrucciones
        # Menú superior
        self.barra_superior = tk.Frame(
            self,
            bg=color_menu_superior,
            height=50
        )
        self.barra_superior.pack(side=tk.TOP, fill='both')

        # Menú lateral
        self.menu_lateral = tk.Frame(
            self,
            bg=color_menu_lateral,
            width=150
        )
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        # Cuerpo central
        self.cuerpo = tk.Frame(
            self,
            bg=color_cuerpo
        )
        self.cuerpo.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta del título
        self.labelTitulo = tk.Label(self.barra_superior, text= empresa)
        self.labelTitulo.config(fg='#fff', font=('Roboto', 15), bg=color_menu_superior, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.botonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                          command=self.toggle_panel,
                                          bd=0, bg=color_menu_superior, fg='white')
        self.botonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta web de la empresa
        self.labelTitulo2 = tk.Label(self.barra_superior, text= mail_empresa)
        self.labelTitulo2.config(fg='#fff', font=('Roboto', 10), bg=color_menu_superior, padx=10, width=20)
        self.labelTitulo2.pack(side=tk.RIGHT)

    def controles_barra_lateral(self):
        # Configuración menú lateral
        ancho = 20
        alto = 2
        font_awesome = font.Font(family='FontAwesome', size=15)
        

        # Etiqueta Perfil: foto de la empresa
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=color_menu_lateral)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones sección del menú lateral
        self.botonCrear = tk.Button(self.menu_lateral)
        self.botonEliminar = tk.Button(self.menu_lateral)
        self.botonBuscar = tk.Button(self.menu_lateral)
        self.botonMostrar = tk.Button(self.menu_lateral)
        self.botonSalir = tk.Button(self.menu_lateral)
        self.botonDatos = tk.Button(self.menu_lateral)

        botones_info = [
            ('Crear Factura', '\uf109', self.botonCrear, self.crear_facturas),  # Texto, icono, objeto a insertar y comando
            ('Eliminar Factura', '\uf007', self.botonEliminar, self.eliminar_facturas),
            ('Buscar Factura', '\uf03e', self.botonBuscar, self.mostrar_facturas),
            ('Mostrar Factura', '4)', self.botonMostrar, self.mostrar_facturas), # self.mostrar_facturas
            ('Salir', '\uf013', self.botonSalir, self.mostrar_facturas),
            ('Analítica datos', '\uf129', self.botonDatos, self.mostrar_facturas)
        ]
        for texto, icono, boton, comando in botones_info:
            self.configurar_boton_menu(boton, texto, icono, font_awesome, ancho, alto, comando)
    
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo, image=self.logo,
                         bg=color_cuerpo)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, boton, texto, icono, font_awesome, ancho, alto, comando):
        boton.config(text=f" {icono}  {texto}", anchor="w", font=font_awesome, bd=0, bg=color_menu_lateral, fg='white', width=ancho, height=alto, command= comando)
        boton.pack(side=tk.TOP)
        self.bind_hover_events(boton)

    def bind_hover_events(self, boton):  # Para que cuando pases se cambie el color
        # Asociar eventos Enter y Leave con la función dinámica
        boton.bind("<Enter>", lambda event: self.on_enter(event, boton))
        boton.bind("<Leave>", lambda event: self.on_leave(event, boton))

    def on_enter(self, event, boton):
        # Cambio el estilo al pasar con el ratón por encima
        boton.config(bg=color_menu_cursor_encima, fg='white')

    def on_leave(self, event, boton):
        # Si no está el ratón encima vuelve al color original
        boton.config(bg=color_menu_lateral, fg='white')

    def toggle_panel(self):  # Altera la visibilidad dentro de tkinter, en el menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

if __name__ == "__main__":
    app=MenuPrincipalFinal()
    app.mainloop()

        
# # Iniciar el bucle principal de la ventana
#     self.ventana.mainloop()
# if __name__ == "__main__":            
#     app = MenuPrincipalFinal()
