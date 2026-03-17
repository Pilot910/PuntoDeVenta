import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_KEY = "123456"
SELL_COVERS_URL = "http://localhost/comicsmexico/backend/sell_comics.php"

class ActualSaleTab:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True, fill="both")
        self.venta_actual = []

        # -------------------------
        # Treeview de ventas
        # -------------------------
        columns = ("ID", "titulo", "Stock", "Precio")
        self.tree_venta = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree_venta.heading(col, text=col)
            self.tree_venta.column(col, width=100, anchor="center")
        self.tree_venta.pack(expand=True, fill="both", padx=10, pady=10)

        # -------------------------
        # Botones de control
        # -------------------------
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Eliminar seleccionado", command=self.eliminar_item).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Limpiar venta", command=self.limpiar_venta).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Vender", command=self.vender_items).pack(side="left", padx=5)

        # -------------------------
        # Label de total
        # -------------------------
        self.total_label = tk.Label(self.frame, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=5)

    # -------------------------
    # Agregar cover al carrito
    # -------------------------
    def agregar_al_carrito(self, cover):
        self.venta_actual.append(cover)
        self.tree_venta.insert("", "end", values=(
            cover["id"],
            cover["ilustracion"],
            cover.get("stock", 0),
            f"${cover.get('precio', 0.0):.2f}"
        ))
        self.actualizar_total()

    # -------------------------
    # Eliminar item seleccionado
    # -------------------------
    def eliminar_item(self):
        selected = self.tree_venta.selection()
        if not selected:
            return
        for item in selected:
            values = self.tree_venta.item(item, "values")
            cover_id = int(values[0])
            self.venta_actual = [c for c in self.venta_actual if c["id"] != cover_id]
            self.tree_venta.delete(item)
        self.actualizar_total()

    # -------------------------
    # Limpiar toda la venta
    # -------------------------
    def limpiar_venta(self):
        for item in self.tree_venta.get_children():
            self.tree_venta.delete(item)
        self.venta_actual.clear()
        self.actualizar_total()

    # -------------------------
    # Calcular total
    # -------------------------
    def actualizar_total(self):
        total = sum([c.get("precio", 0.0) for c in self.venta_actual])
        self.total_label.config(text=f"Total: ${total:.2f}")

    # -------------------------
    # Vender items
    # -------------------------
    def vender_items(self):
        if not self.venta_actual:
            messagebox.showwarning("Aviso", "No hay items en la venta.")
            return

        # Construir payload para el backend
        payload = {
            "metodo_pago": "efectivo",  # puedes cambiar dinámicamente
            "items": [{"cover_id": c["id"], "cantidad": 1} for c in self.venta_actual]
        }

        try:
            response = requests.post(
                SELL_COVERS_URL,
                json=payload,
                headers={"Api-Key": API_KEY}
            )
            response.raise_for_status()
            result = response.json()

            if result.get("success"):
                messagebox.showinfo("Éxito", f"Venta realizada correctamente. ID: {result.get('venta_id')}")
                # Limpiar carrito y Treeview
                self.limpiar_venta()
            else:
                errores = result.get("errores", ["Error desconocido"])
                messagebox.showerror("Error en la venta", "\n".join(errores))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo completar la venta:\n{e}")
