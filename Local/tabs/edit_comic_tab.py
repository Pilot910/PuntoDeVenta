import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_KEY = "123456"

class EditComicTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.api_url = "http://localhost/comicsmexico/backend/get_comics.php"
        self.covers_url = "http://localhost/comicsmexico/backend/get_covers.php"
        self.update_comic_url = "http://localhost/comicsmexico/backend/update_comic.php"
        self.update_cover_url = "http://localhost/comicsmexico/backend/update_cover.php"
        self.delete_cover_url = "http://localhost/comicsmexico/backend/delete_cover.php"
        self.delete_comic_url = "http://localhost/comicsmexico/backend/delete_comic.php"

        # Tabla de cómics
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Título", "Número", "Editorial"), show="headings")
        for col in ("ID", "Título", "Número", "Editorial"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Actualizar tabla", command=self.load_comics).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Editar seleccionado", command=self.open_covers_window).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar cómic seleccionado", command=self.delete_selected_comic).pack(side="left", padx=5)

        self.selected_comic_id = None
        self.load_comics()

    # ===============================
    # Cargar todos los cómics
    # ===============================
    def load_comics(self):
        try:
            print("\n [DEBUG] Solicitando lista de cómics...")
            response = requests.get(self.api_url, params={"api_key": API_KEY})
            print("[DEBUG] Código de estado:", response.status_code)
            print("[DEBUG] Respuesta del servidor:", response.text[:200])  # muestra primeros 200 caracteres

            response.raise_for_status()
            comics = response.json()

            for row in self.tree.get_children():
                self.tree.delete(row)
            for comic in comics:
                self.tree.insert("", "end", values=(comic.get("id"), comic.get("titulo"), comic.get("numero"), comic.get("editorial")))

            print("[DEBUG] Se cargaron", len(comics), "cómics correctamente.\n")

        except Exception as e:
            print(" [ERROR load_comics]", e)
            messagebox.showerror("Error", f"No se pudieron cargar los cómics:\n{e}")

    # ===============================
    # Eliminar cómic completo (y sus portadas)
    # ===============================
    def delete_selected_comic(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un cómic para eliminar.")
            return

        values = self.tree.item(selected[0], "values")
        comic_id = values[0]
        comic_title = values[1]

        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que deseas eliminar el cómic '{comic_title}' y todas sus portadas?"
        )

        if not confirm:
            return

        try:
            print("\n [DEBUG] Intentando eliminar cómic:")
            print("   → ID:", comic_id)
            print("   → Título:", comic_title)

            response = requests.post(
                self.delete_comic_url,
                json={"comic_id": comic_id},
                headers={"Api-Key": API_KEY}
            )

            print("[DEBUG] Código de estado:", response.status_code)
            print("[DEBUG] Respuesta del servidor:", response.text[:300])

            response.raise_for_status()
            result = response.json()

            print("[DEBUG] JSON parseado:", result)

            if "success" in result and result["success"]:
                messagebox.showinfo("Éxito", f"El cómic '{comic_title}' y todas sus portadas fueron eliminados correctamente.")
                self.tree.delete(selected[0])
                print(" [DEBUG] Cómic eliminado correctamente.\n")
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el cómic:\n{result.get('error', 'Error desconocido')}")
                print(" [DEBUG] Error al eliminar el cómic:", result.get('error', 'Error desconocido'))

        except Exception as e:
            print(" [ERROR delete_selected_comic]", e)
            messagebox.showerror("Error", f"Error al intentar eliminar el cómic:\n{e}")

    # ===============================
    # Abrir ventana de portadas
    # ===============================
    def open_covers_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un cómic para editar.")
            return

        values = self.tree.item(selected[0], "values")
        self.selected_comic_id = values[0]

        covers_window = tk.Toplevel(self.frame)
        covers_window.title(f"Portadas de {values[1]}")

        tree_covers = ttk.Treeview(covers_window, columns=("ID", "Nombre", "Ruta", "Stock", "Precio"), show="headings")
        for col in ("ID", "Nombre", "Ruta", "Stock", "Precio"):
            tree_covers.heading(col, text=col)
        tree_covers.pack(fill="both", expand=True, padx=10, pady=10)

        # Cargar portadas
        try:
            print("\n [DEBUG] Solicitando portadas del cómic ID:", self.selected_comic_id)
            response = requests.get(self.covers_url, params={"api_key": API_KEY, "comic_id": self.selected_comic_id})
            print("[DEBUG] Código de estado:", response.status_code)
            print("[DEBUG] Respuesta del servidor:", response.text[:200])

            response.raise_for_status()
            covers = response.json()

            for cover in covers:
                tree_covers.insert("", "end", values=(
                    cover.get("id"),
                    cover.get("ilustracion"),
                    cover.get("ruta_imagen"),
                    cover.get("stock"),
                    cover.get("precio")
                ))

            print("[DEBUG] Se cargaron", len(covers), "portadas correctamente.\n")

        except Exception as e:
            print(" [ERROR open_covers_window]", e)
            messagebox.showerror("Error", f"No se pudieron cargar las portadas:\n{e}")
            covers_window.destroy()
            return

        # Botones de edición / eliminación de portada
        def edit_cover():
            sel = tree_covers.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecciona una portada para editar.")
                return
            cover_values = tree_covers.item(sel[0], "values")
            self.edit_cover_window(cover_values, tree_covers)

        def delete_cover():
            sel = tree_covers.selection()
            if not sel:
                messagebox.showwarning("Aviso", "Selecciona una portada para eliminar.")
                return
            cover_values = tree_covers.item(sel[0], "values")
            cover_id = cover_values[0]
            if messagebox.askyesno("Confirmar", "¿Eliminar esta portada?"):
                try:
                    print("\n [DEBUG] Eliminando portada con ID:", cover_id)
                    response = requests.post(self.delete_cover_url, json={"cover_id": cover_id}, headers={"Api-Key": API_KEY})
                    print("[DEBUG] Código de estado:", response.status_code)
                    print("[DEBUG] Respuesta del servidor:", response.text[:200])
                    response.raise_for_status()
                    tree_covers.delete(sel[0])
                    print(" [DEBUG] Portada eliminada correctamente.\n")
                except Exception as e:
                    print(" [ERROR delete_cover]", e)
                    messagebox.showerror("Error", f"No se pudo eliminar la portada:\n{e}")

        btn_frame = ttk.Frame(covers_window)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Editar", command=edit_cover).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar portada", command=delete_cover).pack(side="left", padx=5)

    # ===============================
    # Ventana de edición de portada
    # ===============================
    def edit_cover_window(self, cover_values, tree_covers):
        cover_id, nombre, ruta, stock, precio = cover_values

        win = tk.Toplevel(self.frame)
        win.title(f"Editar Portada {nombre}")

        ttk.Label(win, text="Nombre de variante:").grid(row=0, column=0, sticky="e")
        name_entry = ttk.Entry(win, width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=2)
        name_entry.insert(0, nombre)

        ttk.Label(win, text="Ruta Imagen:").grid(row=1, column=0, sticky="e")
        ruta_entry = ttk.Entry(win, width=40)
        ruta_entry.grid(row=1, column=1, padx=5, pady=2)
        ruta_entry.insert(0, ruta)

        ttk.Label(win, text="Stock:").grid(row=2, column=0, sticky="e")
        stock_entry = ttk.Entry(win, width=40)
        stock_entry.grid(row=2, column=1, padx=5, pady=2)
        stock_entry.insert(0, stock)

        ttk.Label(win, text="Precio:").grid(row=3, column=0, sticky="e")
        precio_entry = ttk.Entry(win, width=40)
        precio_entry.grid(row=3, column=1, padx=5, pady=2)
        precio_entry.insert(0, precio)

        def save_changes():
            data = {
                "cover_id": cover_id,
                "ilustracion": name_entry.get(),
                "ruta_imagen": ruta_entry.get(),
                "stock": stock_entry.get(),
                "precio": precio_entry.get()
            }

            try:
                print("\n [DEBUG] Enviando actualización de portada:", data)
                response = requests.post(self.update_cover_url, json=data, headers={"Api-Key": API_KEY})
                print("[DEBUG] Código de estado:", response.status_code)
                print("[DEBUG] Respuesta del servidor:", response.text[:200])
                response.raise_for_status()
                result = response.json()
                print("[DEBUG] JSON parseado:", result)

                if "success" in result:
                    messagebox.showinfo("Éxito", "Portada actualizada correctamente.")
                    tree_covers.item(tree_covers.selection()[0], values=(
                        cover_id,
                        name_entry.get(),
                        ruta_entry.get(),
                        stock_entry.get(),
                        precio_entry.get()
                    ))
                    win.destroy()
                    print(" [DEBUG] Portada actualizada correctamente.\n")
                else:
                    messagebox.showerror("Error", f"No se pudo actualizar la portada:\n{result.get('error', 'Error desconocido')}")
                    print(" [DEBUG] Error al actualizar portada:", result.get('error', 'Error desconocido'))

            except Exception as e:
                print(" [ERROR save_changes]", e)
                messagebox.showerror("Error", f"No se pudo actualizar la portada:\n{e}")

        ttk.Button(win, text="Guardar cambios", command=save_changes).grid(row=4, column=0, columnspan=2, pady=10)
