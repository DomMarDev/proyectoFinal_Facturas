# Importamos las librerías de Tkinter y la de utilidades de ventana para centrarla y leerla.
# Fuente: https://www.youtube.com/watch?v=fDyO2vKrSfw&t=6s&ab_channel=Autodidacta
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
from pathlib import Path

import utilidades_ventana.generic as utl

from modulos.crear_PDF import CrearPDF


class MenuPrincipal:
    # Ir a Crear
    def ir_crear(self):
        '''Método que permite ir a crear una factura'''
        self.ventana.destroy() # Eliminamos la ventana
        CrearPDF() # Muestra el menú principal

    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Menú Principal') # Se coloca el título de la ventana
        
        # Se busca el ancho y lo alto de la ventana, para que se maximice
        w, h = self.ventana.winfo_screenmmwidth(), self.ventana.winfo_screenmmheight()
        
        # Formateo de tuplas donde se indica el ancho y lo alto
        self.ventana.geometry("%dx%d+0+0" % (w,h))
        
        # Configuramos el fondo de la ventana -> blanco (#fcfcfc). Y que no redimensione la ventana.
        self.ventana.config(bg = '#fcfcfc')
        self.ventana.resizable(width = 0, height = 0 )

        # Centramos la ventana
        utl.centrar_ventanas(self.ventana, 800, 500)

        # Importamos el logo de la carpeta imagenes, le asignamos un tamaño y la ponemos dentro de una etiquta (toda la pantalla)
        ruta_logo = Path('factura_DM\imagenes\cuadrado.png')
        logo = utl.leer_imagen(ruta_logo, (200, 200))

        label = tk.Label(self.ventana, image = logo, bg = '#fcfcfc')
        label.place(x=0, y=0, relwidth=1, relheight=1)


     
        # Menú Opciones crear, modificar, eliminar, mostrar o buscar.

        # Configuramos el Panel de Crear:
        ancho = 300
        frame_Crear = tk.Frame(self.ventana, 
                              bd = 0, 
                              width = ancho, 
                              relief = tk.SOLID, 
                              padx = 0, 
                              pady = 20, 
                              bg = ''
                              )
        frame_Crear.pack(side = 'left',
                        expand = tk.NO,
                        fill= tk.BOTH
                        )
        
        # Generamos etiqueta de Crear
        ruta_logo_crear = Path('factura_DM\imagenes\crear.png')
        crear_logo = utl.leer_imagen(ruta_logo_crear, (200, 200))
        # Creamos el título de Crear Factura
        label = tk.Label(frame_Crear, image = crear_logo, bg = '#fcfcfc')
        label.place(x = 0,
                    y= 70,
                    relwidth = 1,
                    relheight = 1
                    )
        
        frame_Crear_titulo = tk.Frame(
            frame_Crear, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_Crear_titulo.pack(side="top", fill=tk.X)
        title = tk.Label(frame_Crear_titulo, text=f"Crear\nFactura", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # Creando el botón de inicio de sesión
        botonCrear= tk.Button(frame_Crear,
                                text = 'Crear',
                                font = ('Times', 15, BOLD),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.ir_crear)
        botonCrear.pack(fill = tk.X, padx = 20, pady = 20)

        # Asignación de user y pass
        
        botonCrear.bind('<Return>', (lambda event: self.ir_crear())) # Si damos click con un enter lanzamos el método de verificación.





        # Configuramos el Panel de Eliminar:
        ancho = 200
        frame_Eliminar = tk.Frame(self.ventana, 
                              bd = 0, 
                              width = ancho, 
                              relief = tk.SOLID, 
                              padx = 0, 
                              pady = 20, 
                              bg = ''
                              )
        frame_Eliminar.pack(side = 'left',
                        expand = tk.NO,
                        fill= tk.BOTH
                        )
        
        # Generamos etiqueta de Eliminar
        ruta_logo_Eliminar = Path('factura_DM\imagenes\eliminar.png')
        Eliminar_logo = utl.leer_imagen(ruta_logo_Eliminar, (200, 200))
        # Creamos el título de Eliminar Factura
        label = tk.Label(frame_Eliminar, image = Eliminar_logo, bg = '#fcfcfc')
        label.place(x = 0,
                    y= 70,
                    relwidth = 1,
                    relheight = 1
                    )
        
        frame_Eliminar_titulo = tk.Frame(
            frame_Eliminar, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_Eliminar_titulo.pack(side="top", fill=tk.X)
        title = tk.Label(frame_Eliminar_titulo, text="Eliminar\nFactura", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)


        # Configuramos el Panel de Mostrar:
        ancho = 170
        frame_Mostrar = tk.Frame(self.ventana, 
                              bd = 0, 
                              width = ancho, 
                              relief = tk.SOLID, 
                              padx = 0, 
                              pady = 20, 
                              bg = ''
                              )
        frame_Mostrar.pack(side = 'left',
                        expand = tk.NO,
                        fill= tk.BOTH
                        )
        
        # Generamos etiqueta de Mostrar
        ruta_logo_Mostrar = Path('factura_DM\imagenes\mostrar.png')
        Mostrar_logo = utl.leer_imagen(ruta_logo_Mostrar, (200, 200))
        # Creamos el título de Mostrar Factura
        label = tk.Label(frame_Mostrar, image = Mostrar_logo, bg = '#fcfcfc')
        label.place(x = 0,
                    y= 70,
                    relwidth = 1,
                    relheight = 1
                    )
        
        frame_Mostrar_titulo = tk.Frame(
            frame_Mostrar, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_Mostrar_titulo.pack(side="top", fill=tk.X)
        title = tk.Label(frame_Mostrar_titulo, text="Mostrar\nFactura", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        
        
        # Configuramos el Panel de Buscar:
        ancho = 170
        frame_Buscar = tk.Frame(self.ventana, 
                              bd = 0, 
                              width = ancho, 
                              relief = tk.SOLID, 
                              padx = 0, 
                              pady = 20, 
                              bg = ''
                              )
        frame_Buscar.pack(side = 'left',
                        expand = tk.NO,
                        fill= tk.BOTH
                        )
        
        # Generamos etiqueta de Buscar
        ruta_logo_Buscar = Path('factura_DM\imagenes\iuscar.png')
        Buscar_logo = utl.leer_imagen(ruta_logo_Buscar, (200, 200))
        # Creamos el título de Buscar Factura
        label = tk.Label(frame_Buscar, image = Buscar_logo, bg = '#fcfcfc')
        label.place(x = 0,
                    y= 70,
                    relwidth = 1,
                    relheight = 1
                    )
        
        frame_Buscar_titulo = tk.Frame(
            frame_Buscar, height=30, bd=0, relief=tk.SOLID, bg='black')
        frame_Buscar_titulo.pack(side="top", fill=tk.X)
        title = tk.Label(frame_Buscar_titulo, text="Buscar\nFactura", font=(
            'Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)



        self.ventana.mainloop()



# Funciones del menú:

# class Factura:

#     def crear_factura(self):
#         '''Método que permite crear factura'''
#         user = self.usuario.get()
#         password = self.contrasena.get()

#         if (user == 'user' and password == '1234'):
#             self.ventana.destroy() # Eliminamos la ventana
#             MenuPrincipal() # Muestra el menú principal
#         else:
#             messagebox.showerror(message = "Las credenciales no son correctas", title = "Error")



# # Botones

#         # Creando el botón crear factura
#         crear= tk.Button(frame_MenuCrear,
#                                 text = 'Crear Factura',
#                                 font = ('Times', 15, BOLD),
#                                 bg = '#3a7ff6',
#                                 bd = 0,
#                                 fg = '#fff',
#                                 command = self.crear_factura)
#         crear.pack(fill = tk.X, padx = 20, pady = 20)

#         # Asignación de user y pass
        
#         crear.bind('<Return>', (lambda event: self.crear_factura())) # Si damos click con un enter lanzamos el método crear factura






