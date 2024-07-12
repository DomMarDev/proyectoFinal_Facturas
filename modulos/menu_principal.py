# Importaciones de librerias
import os                                                                       # Obtener rutas del sistema operativo y abrir documentos
from pathlib import Path                                                        # Trabajar con las rutas
import webbrowser                                                               # Incorporar la función de ir a la web de la empresa
import tkinter as tk                                                            # Interfaz gráfica
from tkinter import messagebox
from tkinter import font                                                        # Asignar un tipo de fuente de texto
from tkinter.font import Font                                                   # Asignar un tipo de fuente de texto
from tkinter import filedialog as FD                                            # Por si queremos agregar la función de escoger el archivo json
import sys                                                                      # Necesario para que no haya errores a la hora de importar módulos  
                                                                                    # para añadir el directorio principal de donde estás ejecutando el programa (la raiz)
sys.path.append('.')

from modulos.generic import leer_imagen as leer , centrar_ventanas as centrar   # Necesario para importar la función de centrar y leer
from modulos.colores_y_rutas import *                                           # Necesario para autoasignar ciertos campos de colores e imagenes
                                          
# Importacion de modulos que dan funcionalidad al programa
from modulos.crear_factura import CrearFactura as CF
from modulos.eliminar_factura import EliminarFactura as EF
from modulos.modificar_factura import ModificarFactura as MF
from modulos.borrar_json import EliminarJson_PDF as EJ
from modulos.analisis_datos import AnalizarFactura as AF

# web unicode: https://www.rapidtables.com/code/text/unicode-characters.html

class MenuPrincipalFinal(tk.Tk):

    def crear_facturas(self):
        '''Método que permite ir a crear una factura'''
        self.new_window = tk.Toplevel(self) # Genero una ventana por encima del menú principal y se la paso a CF
        CF(self.new_window)
        # app.wm_state('iconic') # Minimizar ventana para trabajar mejor, segunda opción -> app.iconify()
        # messagebox.showinfo('Minimizado', 'El menú principal se ha minimizado')

    def eliminar_facturas(self):
        '''Método que permite ir a eliminar una factura'''
        self.new_window = tk.Toplevel(self) # Genero una ventana por encima del menú principal y se la paso a EF
        EF(self.new_window)
        
    def mostrar_facturas(self):
        '''Método para mostrar las facturas'''
        archivo = FD.askopenfile(title='Dale a Abrir con...', initialdir='PDF',
                                 filetypes=(('Archivo PDF', '*.pdf'),))  # título ventana, directorio inicial donde buscar y tipo archivos

        if archivo is not None:  # Si hay algo en el archivo va a abrirlo usando su ruta
            ruta_pdf = Path(archivo.name)  # Se obtiene la ruta del archivo
            os.startfile(ruta_pdf)  # Se abre el archivo
    
    def modificar(self):
        '''Método que permite ir a modificar una factura'''
        self.new_window = tk.Toplevel(self) # Genero una ventana por encima del menú principal y se la paso a MF
        MF(self.new_window)        
        # app.wm_state('iconic')
        # messagebox.showinfo('Minimizado', 'El menú principal se ha minimizado')

    def salir_programa(self):
        '''Método para salir del programa'''
        exit()

    def borrar_json_pdf(self):
        '''Método que permite borrar todo registro de las facturas en el archivo json y de los PDF'''
        self.new_window = tk.Toplevel(self)# Genero una ventana por encima del menú principal y se la paso a EJ
        EJ(self.new_window)
    
    def analisis_datos(self):
        '''Método que permite visualizar las ganancias/factura'''
        self.new_window = tk.Toplevel(self)# Genero una ventana por encima del menú principal y se la paso a AF
        AF(self.new_window)


    def __init__(self):
        super().__init__()

        # Importamos el logo de la carpeta imágenes, le asignamos un tamaño y la ponemos dentro de una etiqueta
        alto = 550
        ancho = 600
        self.logo = leer(ruta_logo_programa, (ancho, alto))
        self.perfil = leer(ruta_logo_empresa, (100, 100))
        self.configuracion_ventana()
        self.paneles()
        self.controles_barra_superior()
        self.controles_barra_lateral()
        self.controles_cuerpo()
        self.resizable(False, False) # No quiero que se pueda reescalar 

    def configuracion_ventana(self):  # Configuración de la ventana del menú principal
        ''' Método para realizar la configuración de la ventana del menú principal'''
        self.title('Menú Principal')  # Se coloca el título de la ventana
        ruta_icono_menu = 'imagenes/lego.png' 
        self.iconbitmap(ruta_icono_menu) # Se coloca el logo/icono deseado en el frame del centro del menú principal
        w, h = 1024, 600  # Tamaño de la ventana
        centrar(self, w, h) # Se centra la ventana

    def paneles(self):  # Creación de los paneles: Barra menú superior, menú lateral y cuerpo principal con instrucciones
        ''' Método para crear los 3 paneles del menú principal:
        1) Barra/Menú superior
        2) Barra/Menú lateral
        3) Cuerpo o centro del menú principal'''
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
        ''' Método para configurar el 1) Barra/Menú superior
        Botones:
            a) Menú/ Instrucciones -> Permite visualizar el menú lateral o las instrucciones del programa
            b) Link o web empresa  -> Permite acceder a la Web de la empresa
            c) Correo              -> Permite abrir nuestro correo electrónico
        '''
        # Configuración de la barra superior

        # Etiqueta del título
        self.labelTitulo = tk.Label(self.barra_superior, text= empresa)
        self.labelTitulo.config(fg='#fff', font=('Roboto', 15), bg=color_menu_superior, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.botonMenuLateral = tk.Button(self.barra_superior, text="Menú/Instrucciones", font= ('Roboto', 13),
                                          command=self.toggle_panel,
                                          bd=0, bg=color_menu_superior, fg='white')
        self.botonMenuLateral.pack(side=tk.LEFT)

        # Botón Url de la Empresa
        self.botonLinkEmpresa = tk.Button(self.barra_superior, text="Web Empresa", font= ('Roboto', 13),
                                          command= self.urlEmpresa,
                                          bd=0, bg=color_menu_superior, fg='white')
        self.botonLinkEmpresa.pack(side=tk.RIGHT, padx= 10)

        # Botón Url de la Hotmail
        self.botonLinkHotmail = tk.Button(self.barra_superior, text="Correo", font= ('Roboto', 13),
                                          command= self.urlCorreo,
                                          bd=0, bg=color_menu_superior, fg='white')
        self.botonLinkHotmail.pack(side=tk.RIGHT, padx= 10)          
        
    def urlEmpresa(self):
        # Se usa webbrowser para abrir un url hacia la web de la empresa
        webbrowser.open(urlEmpresa)
    
    def urlCorreo(self):
        # Se usa webbrowser para abrir un url hacia el correo de la empresa
        webbrowser.open(urlCorreo)

    def controles_barra_lateral(self):
        ''' Método para configurar el 2) Barra/Menú lateral
        Botones del menú lateral que llevan a ejecutar las diferentes funciones del programa:
            Crear Factura
            Eliminar Factura
            Buscar Factura
            Modificar Factura
            Salir
            Borrar json y PDF
            Analisis datos
        '''
        # Configuración menú lateral
        ancho = 20
        alto = 2
        font_awesome = font.Font(family='Roboto', size=15)
        
        # Etiqueta Perfil: foto de la empresa
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=color_menu_lateral)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones sección del menú lateral
        self.botonCrear = tk.Button(self.menu_lateral)
        self.botonEliminar = tk.Button(self.menu_lateral)
        self.botonBuscar = tk.Button(self.menu_lateral)
        self.botonMostrar = tk.Button(self.menu_lateral)
        self.botonSalir = tk.Button(self.menu_lateral)
        self.botonBorrarJsonPDF = tk.Button(self.menu_lateral)
        self.botonAnalisis = tk.Button(self.menu_lateral)

        botones_info = [
            ('Crear Factura', '\u26CF' , self.botonCrear, self.crear_facturas),  # Texto, icono, objeto a insertar y comando
            ('Eliminar Factura', '\u26D4', self.botonEliminar, self.eliminar_facturas),
            ('Buscar Factura', '\u2328', self.botonBuscar, self.mostrar_facturas),
            ('Modificar Factura', '\u2692', self.botonMostrar, self.modificar), # self.mostrar_facturas
            ('Salir', '\u267F', self.botonSalir, self.salir_programa), #'\uf013'
            ('Borrar json y PDF', '\u26F6', self.botonBorrarJsonPDF, self.borrar_json_pdf),
            ('Analisis datos', '\u26F6', self.botonAnalisis, self.analisis_datos)
        ]
        for texto, icono, boton, comando in botones_info:
            self.configurar_boton_menu(boton, texto, icono, font_awesome, ancho, alto, comando)
    
    def configurar_boton_menu(self, boton, texto, icono, font_awesome, ancho, alto, comando):
        '''Método para configurar los botones del menú lateral'''
        # Configuración de botones menu lateral
        boton.config(text=f" {icono}  {texto}", anchor="w", font=font_awesome, bd=0, bg=color_menu_lateral, fg='white', width=ancho, height=alto, command= comando)
        boton.pack(side=tk.TOP)
        self.bind_hover_events(boton)

    def bind_hover_events(self, boton):  # Para que cuando pases se cambie el color
        '''Método para poder ilumniar o no los botones del menú lateral'''
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
        '''Método para poder replegar o no el menú lateral y así también mostrar las instrucciones o no'''
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
            self.controles_cuerpo2()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')
            self.controles_cuerpo()
    
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo, image=self.logo,
                         bg=color_cuerpo)
        label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def controles_cuerpo2(self):
        # Imagen en el cuerpo principal
        alto = 550
        ancho = 450
        self.instrucciones = leer(ruta_imagen_instrucciones, (ancho, alto))
        label = tk.Label(self.cuerpo, image=self.instrucciones,
                         bg=color_cuerpo)
        label.place(x=0, y=0, relwidth=1, relheight=1)

if __name__ == "__main__":
    app= MenuPrincipalFinal()
    app.mainloop()