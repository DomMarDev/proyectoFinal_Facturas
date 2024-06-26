# Librerías importadas
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
from pathlib import Path

import utilidades_ventana.generic as utl

from modulos.menu_principal import MenuPrincipal

class Login:

    def verificacion(self):
        '''Método que permite verificar el usuario y contraseña'''
        user = self.usuario.get()
        password = self.contrasena.get()

        if (user == 'user' and password == '1234'):
            self.ventana.destroy() # Eliminamos la ventana
            MenuPrincipal() # Muestra el menú principal
        else:
            messagebox.showerror(message = "Las credenciales no son correctas", title = "Error")



    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de Sesión') # Se coloca el título de la ventana
        
        # Se busca el ancho y lo alto de la ventana, para que se maximice
        w, h = self.ventana.winfo_screenmmwidth(), self.ventana.winfo_screenmmheight()
        
        # Formateo de tuplas donde se indica el ancho y lo alto
        self.ventana.geometry("%dx%d+0+0" % (w,h))
        
        # Configuramos el fondo de la ventana -> blanco (#fcfcfc). Y que no redimensione la ventana.
        self.ventana.config(bg = '#fcfcfc')
        self.ventana.resizable(width = 0, height = 0 )

        # Centramos la ventana
        utl.centrar_ventanas(self.ventana, 800, 500)

        # # Importamos el logo de la carpeta imagenes, le asignamos un tamaño y la ponemos dentro de una etiquta (toda la pantalla)
        ruta_logo = Path('factura_DM\imagenes\cuadrado.png')
        logo = utl.leer_imagen(ruta_logo, (200, 200))

        # Configuramos el frame o Panel:

        frame_logo = tk.Frame(self.ventana, 
                              bd = 0, 
                              width = 300, 
                              relief = tk.SOLID, 
                              padx = 10, 
                              pady = 10, 
                              bg = '#2BE7E7'
                              )
        frame_logo.pack(side = 'left',
                        expand = tk.NO,
                        fill= tk.BOTH
                        )
        # Generamos etiqueta de logo
        label = tk.Label(frame_logo, image = logo, bg = '#2BE7E7')
        label.place(x = 0,
                    y= 0,
                    relwidth = 1,
                    relheight = 1
                    )

        # Panel de datos Login
        frame_Login = tk.Frame(self.ventana, 
                              bd = 0, 
                              relief = tk.SOLID, 
                              bg = '#fcfcfc'
                              )
        frame_Login.pack(side = 'right',
                        expand = tk.YES,
                        fill= tk.BOTH
                        )
        
        # Título de Login "Inicio de sesion"
        frame_LoginTitulo = tk.Frame(frame_Login, 
                              bd = 0,
                              height = 50, 
                              relief = tk.SOLID, 
                              bg = 'black'
                              )
        frame_LoginTitulo.pack(side = 'top', fill = tk.X)

        titulo = tk.Label(frame_LoginTitulo,
                          text = "Inicio de sesión",
                          font = ('Times', 30),
                          fg = "#666a88",
                          bg = '#fcfcfc',
                          pady = 50 )
        titulo.pack(expand = tk.YES, fill = tk.BOTH)

        # Panel de inicio sesión de relleno de credenciales debajo del frame_LoginTitulo
        frame_LoginCredenciales = tk.Frame(frame_Login, 
                              bd = 0,
                              height = 50, 
                              relief = tk.SOLID, 
                              bg = '#fcfcfc'
                              )
        frame_LoginCredenciales.pack(side = 'bottom', expand= tk.YES, fill = tk.BOTH)


        # Etiquetas de nombre usuario y contraseña
        etiquetaUsuario = tk.Label(frame_LoginCredenciales,
                                   text = 'Usuario:',
                                   font = ('Times', 14),
                                   fg = '#666a88',
                                   bg = '#fcfcfc',
                                   anchor = 'w')
        etiquetaUsuario.pack(fill = tk.X, padx = 20, pady = 5)
        self.usuario = ttk.Entry(frame_LoginCredenciales, font = ('Times', 14))
        self.usuario.pack(fill = tk.X, padx = 20, pady = 10)

        etiquetaContrasena = tk.Label(frame_LoginCredenciales,
                                   text = 'Contraseña:',
                                   font = ('Times', 14),
                                   fg = '#666a88',
                                   bg = '#fcfcfc',
                                   anchor = 'w')
        etiquetaContrasena.pack(fill = tk.X, padx = 20, pady = 5)
        self.contrasena = ttk.Entry(frame_LoginCredenciales, font = ('Times', 14))
        self.contrasena.pack(fill = tk.X, padx = 20, pady = 10)
        self.contrasena.config(show = '*') # Lo que te muestra son *

        # Creando el botón de inicio de sesión
        inicioSesion= tk.Button(frame_LoginCredenciales,
                                text = 'Iniciar sesion',
                                font = ('Times', 15, BOLD),
                                bg = '#3a7ff6',
                                bd = 0,
                                fg = '#fff',
                                command = self.verificacion)
        inicioSesion.pack(fill = tk.X, padx = 20, pady = 20)

        # Asignación de user y pass
        
        inicioSesion.bind('<Return>', (lambda event: self.verificacion())) # Si damos click con un enter lanzamos el método de verificación.


        self.ventana.mainloop()
