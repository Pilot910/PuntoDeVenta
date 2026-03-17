import tkinter as tk
from tabs.stock_tab import StockTab
from tabs.add_comic_tab import AddComicTab
from tabs.edit_comic_tab import EditComicTab
from tabs.actual_sale_tab import ActualSaleTab
# from tabs.backup_tab import BackupTab


class Dashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Comics México - Dashboard")
        self.master.geometry("1000x600")

        # 🧱 Contenedor principal
        self.main_frame = tk.Frame(master, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both")

        # 🎛️ Menú lateral
        self.menu_frame = tk.Frame(self.main_frame, bg="#333333", width=200)
        self.menu_frame.pack(side="left", fill="y")

        # 📦 Contenedor de pestañas (zona principal)
        self.content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.content_frame.pack(side="right", expand=True, fill="both")

        # 📘 Diccionario de pestañas
        self.tabs = {}

        # 🧩 Crear instancias de pestañas EN EL ORDEN CORRECTO
        self.tabs["actual_sale"] = ActualSaleTab(self.content_frame)  # Primero la venta actual
        self.tabs["stock"] = StockTab(self.content_frame, actual_sale_tab=self.tabs["actual_sale"])  # Pasamos la referencia
        self.tabs["add_comic"] = AddComicTab(self.content_frame)
        self.tabs["edit_comic"] = EditComicTab(self.content_frame)
        # self.tabs["backup"] = BackupTab(self.content_frame)

        # 📁 Crear botones del menú
        self.add_menu_button("📚 Stock", lambda: self.show_tab("stock"))
        self.add_menu_button("➕ Agregar Cómic", lambda: self.show_tab("add_comic"))
        self.add_menu_button("✏️ Editar Cómic", lambda: self.show_tab("edit_comic"))
        self.add_menu_button("💰 Venta Actual", lambda: self.show_tab("actual_sale"))
        self.add_menu_button("💾 Respaldo", lambda: self.show_tab("backup"))

        # Ocultar todas las pestañas antes de mostrar la predeterminada
        for tab in self.tabs.values():
            tab.frame.pack_forget()

        # Mostrar pestaña por defecto
        self.show_tab("stock")

    def add_menu_button(self, text, command):
        """Crea un botón estilizado en el menú lateral"""
        btn = tk.Button(
            self.menu_frame,
            text=text,
            fg="white",
            bg="#333333",
            activebackground="#555555",
            activeforeground="white",
            bd=0,
            padx=10,
            pady=15,
            anchor="w",
            font=("Segoe UI", 10),
            command=command
        )
        btn.pack(fill="x")

        # Separador visual
        separator = tk.Frame(self.menu_frame, height=1, bg="#444444")
        separator.pack(fill="x")

    def show_tab(self, tab_name):
        """Muestra una pestaña y oculta las demás"""
        for tab in self.tabs.values():
            tab.frame.pack_forget()

        # Mostrar la pestaña seleccionada
        current_tab = self.tabs.get(tab_name)
        if current_tab:
            current_tab.frame.pack(expand=True, fill="both")

            # Si la pestaña tiene un método on_show(), lo ejecutamos
            if hasattr(current_tab, "on_show"):
                current_tab.on_show()
