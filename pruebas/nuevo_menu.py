import tkinter as tk
from tkinter import font
import sys

sys.path.append('.') # para añadir el directorio principal de donde estás ejecutando el programa (la raiz)


from modulos.generic import leer_imagen as leer , centrar_ventanas as centrar
# import utilidades_ventana.generic as utl
from modulos.colores_y_rutas import *

class FormularioMaestroDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        self.logo = leer("imagenes\lego.png", (560, 136))
        self.perfil = leer("imagenes\cuadrado.png", (100, 100))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo()
    
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Python GUI')
        self.iconbitmap("imagenes\lego.png")
        w, h = 1024, 600        
        centrar(self, w, h)        

    def paneles(self):        
         # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(
            self, bg= color_menu_superior, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=color_menu_lateral, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(
            self, bg=color_cuerpo)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Autodidacta")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=color_menu_superior, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=color_menu_superior, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de informacion
        self.labelTitulo = tk.Label(
            self.barra_superior, text="servicio@autodidacta.mx")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 10), bg=color_menu_superior, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)
    
    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)
         
         # Etiqueta de perfil
        self.labelPerfil = tk.Label(
            self.menu_lateral, image=self.perfil, bg=color_menu_lateral)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        
        self.buttonDashBoard = tk.Button(self.menu_lateral)        
        self.buttonProfile = tk.Button(self.menu_lateral)        
        self.buttonPicture = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)        
        self.buttonSettings = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Dashboard", "\uf109", self.buttonDashBoard),
            ("Profile", "\uf007", self.buttonProfile),
            ("Picture", "\uf03e", self.buttonPicture),
            ("Info", "\uf129", self.buttonInfo),
            ("Settings", "\uf013", self.buttonSettings)
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)                    
    
    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                         bg=color_cuerpo)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=color_menu_lateral, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=color_menu_cursor_encima, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=color_menu_lateral, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

app = FormularioMaestroDesign()
app.mainloop()