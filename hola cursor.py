import unicodedata
import sys
import tkinter as tk
from tkinter import ttk, messagebox

def quitar_acentos(cadena):
    return ''.join(
        c for c in unicodedata.normalize('NFD', cadena)
        if unicodedata.category(c) != 'Mn'
    )

# Mapeo de colores a códigos HEX para Tkinter
COLOR_HEX = {
    'Rojo': '#FF4444',
    'Azul': '#3380CC',
    'Verde': '#33B233',
    'Amarillo': '#FFD700',
    'Naranja': '#FFA500',
    'Morado': '#7D3C98',
    'Negro': '#222222',
    'Blanco': '#EEEEEE',
}

def validar_no_vacio(valor):
    return valor.strip() != ""

class AppRegistro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro - IA con Python (Cursor)")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        self.tratamientos = ['Sr', 'Srita', 'Dr', 'Ing', 'Lic', 'Prof', 'Mtro', 'Otro']
        self.estados_mexico = [
            "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas",
            "Chihuahua", "Ciudad de México", "Coahuila", "Colima", "Durango", "Estado de México",
            "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit",
            "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí",
            "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
        ]
        self.sexos = ['Masculino', 'Femenino', 'Otro']
        self.estados_civiles = ['Soltero/a', 'Casado/a', 'Divorciado/a', 'Viudo/a', 'Unión libre', 'Otro']
        self.colores = ['Rojo', 'Azul', 'Verde', 'Amarillo', 'Naranja', 'Morado', 'Negro', 'Blanco']

        self.crear_widgets()

    def crear_widgets(self):
        row = 0
        ttk.Label(self, text="Opciones de tratamiento: Sr, Srita, Dr, Ing, Lic, Prof, Mtro, etc.").grid(row=row, column=0, columnspan=2, pady=2)
        row += 1
        ttk.Label(self, text="Tratamiento:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.tratamiento_var = tk.StringVar(value=self.tratamientos[0])
        ttk.Combobox(self, textvariable=self.tratamiento_var, values=self.tratamientos, state="readonly").grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Label(self, text="Nombre:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.nombre_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.nombre_var).grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Label(self, text="Estado de origen:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.estado_var = tk.StringVar(value=self.estados_mexico[0])
        ttk.Combobox(self, textvariable=self.estado_var, values=self.estados_mexico, state="readonly").grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Label(self, text="Teléfono:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.telefono_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.telefono_var).grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Label(self, text="Dirección:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.direccion_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.direccion_var).grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Label(self, text="Sexo:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.sexo_var = tk.StringVar(value=self.sexos[0])
        ttk.Combobox(self, textvariable=self.sexo_var, values=self.sexos, state="readonly").grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Label(self, text="Estado civil:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.estado_civil_var = tk.StringVar(value=self.estados_civiles[0])
        ttk.Combobox(self, textvariable=self.estado_civil_var, values=self.estados_civiles, state="readonly").grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        ttk.Label(self, text="Color preferido:").grid(row=row, column=0, sticky="e", padx=3, pady=2)
        self.color_var = tk.StringVar(value=self.colores[0])
        ttk.Combobox(self, textvariable=self.color_var, values=self.colores, state="readonly").grid(row=row, column=1, sticky="w", pady=2)
        row += 1

        self.boton_registrar = ttk.Button(self, text="Registrar", command=self.registrar)
        self.boton_registrar.grid(row=row, column=0, columnspan=2, pady=10)

        self.texto_resultado = tk.Text(self, width=50, height=10, state='disabled', wrap="word", borderwidth=2, relief="sunken")
        self.texto_resultado.grid(row=row+1, column=0, columnspan=2, pady=(6,0))

    def registrar(self):
        nombre = self.nombre_var.get()
        tratamiento = self.tratamiento_var.get()
        estado = self.estado_var.get()
        telefono = self.telefono_var.get()
        direccion = self.direccion_var.get()
        sexo = self.sexo_var.get()
        estado_civil = self.estado_civil_var.get()
        color = self.color_var.get()

        if not all([
            validar_no_vacio(nombre),
            validar_no_vacio(tratamiento),
            validar_no_vacio(telefono),
            validar_no_vacio(direccion)
        ]):
            messagebox.showerror("Error", "Por favor completa todos los campos requeridos.")
            return

        info = (
            "¡Registro completo!\n"
            f"Hola {tratamiento} {nombre}, bienvenido al curso de inteligencia artificial con Python usando Cursor.\n"
            f"Estado: {estado}\n"
            f"Teléfono: {telefono}\n"
            f"Dirección: {direccion}\n"
            f"Sexo: {sexo}\n"
            f"Estado Civil: {estado_civil}\n"
            f"Color preferido para tu información: {color}\n"
        )

        self.texto_resultado.configure(state='normal')
        self.texto_resultado.delete('1.0', tk.END)
        self.texto_resultado.insert(tk.END, info)
        # Cambia el fondo al color preferido (en un tono suave)
        color_hex = COLOR_HEX.get(color, '#EEEEEE')
        self.texto_resultado.configure(bg=color_hex)
        self.texto_resultado.configure(state='disabled')

if __name__ == "__main__":
    try:
        app = AppRegistro()
        app.mainloop()
    except Exception as e:
        print("Error al iniciar la interfaz:", e)