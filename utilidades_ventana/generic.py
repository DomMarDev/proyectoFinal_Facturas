# Librería Pillow -> poder ajustar images
# Fuente: https://www.youtube.com/watch?v=fDyO2vKrSfw&t=6s&ab_channel=Autodidacta
from PIL import ImageTk, Image

def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))

def centrar_ventanas(ventana, aplicacion_ancho, aplicacion_largo):
    ''' Función que realiza un cálculo para ajustar el ancho y largo de la pantalla para centrar la ventana
    Operaciones:
        - Cálculo de X e Y (en píxels), cálculo de tamño de imagen para centrar'''
    anchoPantalla = ventana.winfo_screenwidth()
    largoPantalla = ventana.winfo_screenheight()

    x = int((anchoPantalla/2) - (aplicacion_ancho/2))
    y = int((largoPantalla/2) - (aplicacion_largo/2))

    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")
