import tkinter as tk
from tkinter import simpledialog, messagebox, Menu
import json
from pathlib import Path
from fpdf import FPDF  # Instala fpdf usando: pip install fpdf

class ContactDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Nombre:").grid(row=0, column=0, sticky="e")
        tk.Label(master, text="Correo Electrónico:").grid(row=1, column=0, sticky="e")
        tk.Label(master, text="Número de Teléfono:").grid(row=2, column=0, sticky="e")

        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)

        self.email_entry = tk.Entry(master)
        self.email_entry.grid(row=1, column=1)

        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=2, column=1)

        return self.name_entry

    def apply(self):
        self.result = {
            "name": self.name_entry.get(),
            "email": self.email_entry.get(),
            "phone": self.phone_entry.get()
        }

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")

        self.contacts = []

        # Frame lateral izquierdo para botones de opción
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.add_button = tk.Button(left_frame, text="Añadir Contacto", command=self.add_contact)
        self.add_button.pack(pady=5)

        self.edit_button = tk.Button(left_frame, text="Editar Contacto", command=self.edit_contact)
        self.edit_button.pack(pady=5)

        self.delete_button = tk.Button(left_frame, text="Borrar Contacto", command=self.delete_contact)
        self.delete_button.pack(pady=5)

        # Frame lateral derecho para el Listbox
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(right_frame, width=50, height=20)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Menú de la aplicación
        self.menu_bar = Menu(root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exportar a PDF", command=self.export_to_pdf)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.on_closing)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        root.config(menu=self.menu_bar)

        self.load_contacts()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_contacts(self):
        contacts_file = Path("contacts.json")
        if contacts_file.exists():
            with open(contacts_file, 'r') as file:
                self.contacts = json.load(file)
            self.update_listbox()

    def save_contacts(self):
        contacts_file = Path("contacts.json")
        with open(contacts_file, 'w') as file:
            json.dump(self.contacts, file)

    def on_closing(self):
        self.save_contacts()
        self.root.destroy()

    def add_contact(self):
        dialog = ContactDialog(self.root)
        if dialog.result:
            self.contacts.append(dialog.result)
            self.update_listbox()

    def edit_contact(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un contacto para editar.")
            return

        index = selected_index[0]
        # selected_contact = self.contacts[index]

        dialog = ContactDialog(self.root)
        if dialog.result:
            self.contacts[index] = dialog.result
            self.update_listbox()

    def delete_contact(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un contacto para borrar.")
            return

        index = selected_index[0]
        del self.contacts[index]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            contact_info = f"Nombre: {contact['name']} | Email: {contact['email']} | Teléfono: {contact['phone']}"
            self.listbox.insert(tk.END, contact_info)

    def export_to_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for contact in self.contacts:
            contact_info = f"Nombre: {contact['name']} | Email: {contact['email']} | Teléfono: {contact['phone']}"
            pdf.cell(200, 10, txt=contact_info, ln=True)

        pdf_file = "contacts.pdf"
        pdf.output(pdf_file)
        messagebox.showinfo("Exportar a PDF", f"Los contactos se han exportado a {pdf_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
