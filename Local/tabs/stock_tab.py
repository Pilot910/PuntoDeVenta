import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils.api import get_comics, get_covers
import os
import platform

class StockTab:
    def __init__(self, master, actual_sale_tab=None):
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, fill="both")
        self.current_view = "comics"
        self.venta_actual = []  # Carrito temporal local
        self.cover_images = []  # Mantener referencias de imágenes
        self.actual_sale_tab = actual_sale_tab  # Referencia a la pestaña ActualSaleTab
        self.current_comic_title = None  # Título del cómic actual (para encabezado)

        # ===============================
        # HEADER (Título, búsqueda, actualizar)
        # ===============================
        header = tk.Frame(self.frame)
        header.pack(fill="x", pady=10, padx=10)

        tk.Label(header, text="Stock de cómics", font=("Arial", 18, "bold")).pack(side="left")

        # Barra de búsqueda
        search_frame = tk.Frame(header)
        search_frame.pack(side="left", expand=True, fill="x", padx=20)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=(0,5))
        tk.Button(search_frame, text="Buscar", command=self.search_comics).pack(side="left")

        # Botón actualizar
        self.btn_refresh = tk.Button(header, text="Actualizar", command=self.load_comics)
        self.btn_refresh.pack(side="right")

        # ===============================
        # TREEVIEW (Lista de cómics)
        # ===============================
        self.tree_frame = tk.Frame(self.frame)
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=(0,10))

        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Double-1>", self.on_double_click)

        columns = ("ID", "Título", "Número", "Stock")
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center", stretch=True)

        # Botón volver (para vista de portadas)
        self.btn_back = tk.Button(self.frame, text="← Volver", command=self.show_comics)

        # ===============================
        # CANVAS scrollable (vista de portadas)
        # ===============================
        self.canvas_frame = tk.Frame(self.frame)
        self.canvas = tk.Canvas(self.canvas_frame)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

        self.canvas.pack(side="left", expand=True, fill="both")
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_frame.pack_forget()  # Oculto hasta mostrar portadas

        # Encabezado dinámico del cómic seleccionado
        self.comic_header_label = tk.Label(self.frame, text="", font=("Arial", 16, "bold"))
        self.comic_header_label.pack_forget()

        # ===============================
        # Habilitar scroll con la rueda del mouse
        # ===============================
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _on_mousewheel_mac(event):
            self.canvas.yview_scroll(int(-1*event.delta), "units")

        if platform.system() == "Darwin":
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel_mac)
        else:
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ===============================
        # Cargar datos iniciales
        # ===============================
        self.load_comics()

    # ===============================
    # Cargar/Actualizar lista de cómics
    # ===============================
    def load_comics(self):
        self.current_view = "comics"

        self.canvas_frame.pack_forget()
        self.comic_header_label.pack_forget()
        self.btn_back.pack_forget()
        self.tree_frame.pack(expand=True, fill="both", padx=10, pady=(0,10))
        self.btn_refresh.pack(side="right", padx=10, pady=5)

        for item in self.tree.get_children():
            self.tree.delete(item)

        comics = get_comics()
        for comic in comics:
            self.tree.insert("", "end", values=(comic["id"], comic["titulo"], comic["numero"], comic["stock_total"]))

    # ===============================
    # Búsqueda de cómics por título
    # ===============================
    def search_comics(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self.load_comics()
            return

        comics = get_comics()
        filtered = [c for c in comics if query in c["titulo"].lower()]

        for item in self.tree.get_children():
            self.tree.delete(item)
        for comic in filtered:
            self.tree.insert("", "end", values=(comic["id"], comic["titulo"], comic["numero"], comic["stock_total"]))

    # ===============================
    # Mostrar portadas del cómic seleccionado
    # ===============================
    def mostrar_detalles(self, comic_id=None, comic_title=None):
        self.current_view = "covers"
        self.tree_frame.pack_forget()
        self.canvas_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.btn_back.pack(pady=(0,10))
        self.btn_refresh.pack_forget()

        # Mostrar encabezado con el título del cómic
        if comic_title:
            self.current_comic_title = comic_title
            self.comic_header_label.config(text=f"Portadas de: {comic_title}")
            self.comic_header_label.pack(pady=(0,10))
        else:
            self.comic_header_label.pack_forget()

        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.cover_images.clear()

        # Obtener portadas del cómic seleccionado
        covers_to_show = []
        if comic_id:
            try:
                covers_to_show = get_covers(comic_id)
            except Exception as e:
                print(f"Error cargando portadas del comic {comic_id}: {e}")
        else:
            # Comportamiento anterior (mostrar todas)
            all_comics = get_comics()
            for comic in all_comics:
                try:
                    covers = get_covers(comic["id"])
                    covers_to_show.extend(covers)
                except Exception as e:
                    print(f"Error cargando portadas del comic {comic['id']}: {e}")

        columns = 4
        for idx, cover in enumerate(covers_to_show):
            row = idx // columns
            col = idx % columns

            frame = tk.Frame(self.inner_frame, bd=1, relief="solid", padx=5, pady=5)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            ruta_imagen = cover.get("ruta_imagen", "")
            photo = None
            if ruta_imagen and os.path.exists(ruta_imagen):
                try:
                    img = Image.open(ruta_imagen)
                    img = img.resize((100,150))
                    photo = ImageTk.PhotoImage(img)
                    self.cover_images.append(photo)
                except Exception as e:
                    print(f"Error al cargar imagen {ruta_imagen}: {e}")

            lbl_img = tk.Label(frame, image=photo)
            lbl_img.image = photo
            lbl_img.pack()

            precio = 0.0
            try:
                precio = float(cover.get("precio", 0))
            except ValueError:
                precio = 0.0

            tk.Label(frame, text=f"{cover['ilustracion']}", font=("Arial", 10)).pack()
            tk.Label(frame, text=f"Stock: {cover['stock']}", font=("Arial", 10)).pack()
            tk.Label(frame, text=f"Precio: ${precio:.2f}", font=("Arial", 10)).pack()

            tk.Button(frame, text="Agregar al carrito",
                      command=lambda c=cover: self.add_to_actual_sale(c)).pack(pady=5)

    # ===============================
    # Agregar portada al carrito (ActualSaleTab)
    # ===============================
    def add_to_actual_sale(self, cover):
        if self.actual_sale_tab:
            precio = 0.0
            try:
                precio = float(cover.get("precio", 0))
            except ValueError:
                precio = 0.0

            self.actual_sale_tab.agregar_al_carrito({
                "id": cover["id"],
                "ilustracion": cover["ilustracion"],
                "ruta_imagen": cover.get("ruta_imagen", ""),
                "stock": cover.get("stock", 0),
                "precio": precio
            })
            messagebox.showinfo("Carrito", f"{cover['ilustracion']} agregado al carrito.")
        else:
            messagebox.showwarning("Aviso", "No se encontró la pestaña de Venta Actual.")

    # ===============================
    # Volver a lista principal
    # ===============================
    def show_comics(self):
        self.load_comics()

    # ===============================
    # Doble clic en tabla abre portadas del cómic
    # ===============================
    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        comic_id = item["values"][0]
        comic_title = item["values"][1]
        if self.current_view == "comics":
            self.mostrar_detalles(comic_id, comic_title)
