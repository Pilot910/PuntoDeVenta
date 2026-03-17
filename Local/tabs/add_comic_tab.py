import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import requests

class AddComicTab:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.portadas = []  # Lista de portadas

        # ==========================
        # Campos del comic
        # ==========================
        form_frame = tk.Frame(self.frame)
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky="e")
        tk.Label(form_frame, text="Número:").grid(row=1, column=0, sticky="e")
        tk.Label(form_frame, text="Editorial:").grid(row=2, column=0, sticky="e")
        tk.Label(form_frame, text="Descripción:").grid(row=3, column=0, sticky="ne")

        self.title_var = tk.StringVar()
        self.number_var = tk.StringVar()
        self.editorial_var = tk.StringVar()
        self.desc_var = tk.StringVar()

        tk.Entry(form_frame, textvariable=self.title_var, width=40).grid(row=0, column=1, padx=5, pady=2)
        tk.Entry(form_frame, textvariable=self.number_var, width=40).grid(row=1, column=1, padx=5, pady=2)
        tk.Entry(form_frame, textvariable=self.editorial_var, width=40).grid(row=2, column=1, padx=5, pady=2)
        self.desc_entry = tk.Text(form_frame, width=50, height=4)
        self.desc_entry.grid(row=3, column=1, padx=5, pady=2)

        # ==========================
        # Botón seleccionar imágenes
        # ==========================
        tk.Button(form_frame, text="Seleccionar portadas", command=self.select_images).grid(row=4, column=0, columnspan=2, pady=10)

        # ==========================
        # Encabezados de portadas
        # ==========================
        headers_frame = tk.Frame(self.frame)
        headers_frame.pack(fill="x", padx=15)
        tk.Label(headers_frame, text="Archivo", width=30, anchor="w").pack(side="left", padx=2)
        tk.Label(headers_frame, text="Ilustración", width=15).pack(side="left", padx=2)
        tk.Label(headers_frame, text="Stock", width=10).pack(side="left", padx=2)
        tk.Label(headers_frame, text="Precio", width=10).pack(side="left", padx=2)
        tk.Label(headers_frame, text="Acción", width=12).pack(side="left", padx=2)

        # ==========================
        # Scrollable frame para portadas
        # ==========================
        self.canvas_frame = tk.Frame(self.frame)
        self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=5)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.inner_frame = tk.Frame(self.canvas)

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

        self.canvas.pack(side="left", expand=True, fill="both")
        self.scrollbar.pack(side="right", fill="y")

        # ==========================
        # Botón final agregar comic
        # ==========================
        tk.Button(self.frame, text="Agregar cómic", command=self.add_comic_to_api, bg="#28a745", fg="white").pack(pady=10)

    # ==========================
    # Selección de imágenes
    # ==========================
    def select_images(self):
        files = filedialog.askopenfilenames(filetypes=[("Imágenes JPG", "*.jpg"), ("Todos los archivos", "*.*")])
        for file in files:
            self.add_portada_row(file)

    # ==========================
    # Crear fila de portada
    # ==========================
    def add_portada_row(self, filepath):
        row_frame = tk.Frame(self.inner_frame, bd=1, relief="solid", padx=5, pady=5)
        row_frame.pack(fill="x", pady=2)

        # Thumbnail
        try:
            img = Image.open(filepath)
            img.thumbnail((50, 75))
            photo = ImageTk.PhotoImage(img)
        except:
            photo = None

        tk.Label(row_frame, image=photo).pack(side="left", padx=5)
        if photo: row_frame.image = photo  # mantener referencia

        # Entries: Ilustración, Stock, Precio
        ilustracion_var = tk.StringVar()
        stock_var = tk.StringVar()
        price_var = tk.StringVar()

        tk.Label(row_frame, text=os.path.basename(filepath), width=30, anchor="w").pack(side="left", padx=2)
        tk.Entry(row_frame, textvariable=ilustracion_var, width=15).pack(side="left", padx=2)
        tk.Entry(row_frame, textvariable=stock_var, width=10).pack(side="left", padx=2)
        tk.Entry(row_frame, textvariable=price_var, width=10).pack(side="left", padx=2)

        # Botón eliminar
        btn_del = tk.Button(row_frame, text="Eliminar", bg="#dc3545", fg="white",
                            command=lambda rf=row_frame, fp=filepath: self.remove_portada(rf, fp))
        btn_del.pack(side="left", padx=5)

        # Guardamos la info en lista
        portada_dict = {
            "filepath": filepath,
            "ilustracion_var": ilustracion_var,
            "stock_var": stock_var,
            "price_var": price_var,
            "frame": row_frame
        }
        self.portadas.append(portada_dict)

    # ==========================
    # Eliminar portada
    # ==========================
    def remove_portada(self, frame, filepath):
        frame.destroy()
        self.portadas = [p for p in self.portadas if p["filepath"] != filepath]

    # ==========================
    # Agregar cómic a la API
    # ==========================
    def add_comic_to_api(self):
        title = self.title_var.get().strip()
        number = self.number_var.get().strip()
        editorial = self.editorial_var.get().strip()
        description = self.desc_entry.get("1.0", "end").strip()

        if not title or not number:
            messagebox.showerror("Error", "Título y número son obligatorios")
            return
        if len(self.portadas) == 0:
            messagebox.showerror("Error", "Debes seleccionar al menos una portada")
            return

        comic_data = {
            "titulo": title,
            "numero": number,
            "editorial": editorial,
            "descripcion": description
        }

        try:
            # 1️⃣ Crear comic
            resp = requests.post("http://localhost/comicsmexico/backend/add_comic.php", json=comic_data)
            resp.raise_for_status()
            comic_id = resp.json().get("id")

            # 2️⃣ Subir portadas
            for portada in self.portadas:
                filepath = portada["filepath"]
                files = {"file": open(filepath, "rb")}
                data = {
                    "comic_id": comic_id,
                    "ilustracion": portada["ilustracion_var"].get(),
                    "stock": portada["stock_var"].get(),
                    "precio": portada["price_var"].get()
                }
                r = requests.post("http://localhost/comicsmexico/backend/add_cover.php", files=files, data=data)
                r.raise_for_status()

            messagebox.showinfo("Éxito", "Cómic agregado correctamente")
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el cómic: {e}")

    # ==========================
    # Limpiar formulario
    # ==========================
    def clear_form(self):
        self.title_var.set("")
        self.number_var.set("")
        self.editorial_var.set("")
        self.desc_entry.delete("1.0", "end")
        for portada in self.portadas:
            portada["frame"].destroy()
        self.portadas.clear()
