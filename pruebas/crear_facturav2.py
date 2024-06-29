import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog as FD
import sys

sys.path.append('.')

from modulos.leer_archivo import Lectura_archivo

class Add_factura:

    def __init__(self, ruta):
        self.path = Path(ruta)
        self.facturas = Lectura_archivo.lee_archivo(ruta)
        self.listaFacturas = json.loads(self.facturas) if self.facturas else []

    def add_factura(self):
        self.factura_window = tk.Toplevel()
        self.factura_window.title("Añadir Factura")

        self.nombreEmpresa = self.create_entry(self.factura_window, "Introduce el nombre de la empresa: ")
        self.fecha = self.create_entry(self.factura_window, "Introduce fecha de hoy: ")
        self.cliente = self.create_entry(self.factura_window, "Introduce el cliente: ")
        self.dni = self.create_entry(self.factura_window, "Introduce el DNI del cliente: ")
        self.localizacion = self.create_entry(self.factura_window, "Introduce la localización de la empresa: ")

        self.listaElementos = []
        self.elementos_frame = tk.Frame(self.factura_window)
        self.elementos_frame.pack(pady=10)
        self.add_element_button = tk.Button(self.factura_window, text="Añadir Elemento", command=self.add_element)
        self.add_element_button.pack(pady=5)

        self.save_button = tk.Button(self.factura_window, text="Guardar Factura", command=self.save_factura)
        self.save_button.pack(pady=10)

    def create_entry(self, parent, label_text):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=50)
        entry.pack(side=tk.LEFT)
        return entry

    def add_element(self):
        frame = tk.Frame(self.elementos_frame)
        frame.pack(pady=5)

        unidades_label = tk.Label(frame, text="Unidades:")
        unidades_label.pack(side=tk.LEFT)
        unidades_entry = tk.Entry(frame, width=5)
        unidades_entry.pack(side=tk.LEFT)

        elementos_label = tk.Label(frame, text="Elemento:")
        elementos_label.pack(side=tk.LEFT)
        elementos_entry = tk.Entry(frame, width=20)
        elementos_entry.pack(side=tk.LEFT)

        precio_label = tk.Label(frame, text="Precio:")
        precio_label.pack(side=tk.LEFT)
        precio_entry = tk.Entry(frame, width=10)
        precio_entry.pack(side=tk.LEFT)

        self.listaElementos.append((unidades_entry, elementos_entry, precio_entry))

    def save_factura(self):
        datos_factura = {
            'nombreEmpresa': self.nombreEmpresa.get().lower().strip(),
            'fecha': self.fecha.get().lower().strip(),
            'cliente': self.cliente.get().lower().strip(),
            'dni': self.dni.get().lower().strip(),
            'localizacion': self.localizacion.get().lower().strip(),
            'listaElementos': [(unidades.get().lower().strip(), elemento.get().lower().strip(), precio.get().lower().strip()) for unidades, elemento, precio in self.listaElementos]
        }

        self.listaFacturas.append(datos_factura)
        contenido = json.dumps(self.listaFacturas, indent=4, sort_keys=False)
        self.path.write_text(contenido)
        messagebox.showinfo("Éxito", "Factura guardada exitosamente")
        self.factura_window.destroy()

class CrearFactura:

    def __init__(self, root):
        self.root = root
        self.root.title("Crear Factura")
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Abrir JSON de Facturas", command=self.open_json_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit)

        self.factura_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Facturas", menu=self.factura_menu)
        self.factura_menu.add_command(label="Añadir Factura", command=self.add_factura)

    def open_json_file(self):
        ruta = FD.askopenfilename(title="Selecciona el archivo de facturas", filetypes=[("JSON files", "*.json")])
        if ruta:
            self.add_factura_window = Add_factura(ruta)
            self.add_factura_window.add_factura()

    def add_factura(self):
        if hasattr(self, 'add_factura_window'):
            self.add_factura_window.add_factura()
        else:
            messagebox.showwarning("Archivo no seleccionado", "Primero seleccione un archivo JSON de facturas desde el menú Archivo -> Abrir JSON de Facturas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CrearFactura(root)
    root.mainloop()
