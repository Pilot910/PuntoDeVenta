import tkinter as tk
from tkinter import messagebox
from dashboard import Dashboard

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("350x260")
        self.master.configure(bg="#F5F5F5")  # Fondo gris claro
        self.master.resizable(False, False)

        # Frame central
        self.frame = tk.Frame(master, bg="#FFFFFF", bd=1, relief="solid")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=230)

        # Título
        tk.Label(self.frame, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        # Usuario
        tk.Label(self.frame, text="Usuario", font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=20)
        self.username = tk.Entry(self.frame, font=("Arial", 12), bg="#EFEFEF", bd=1, relief="solid")
        self.username.pack(pady=5, ipady=4, fill="x", padx=20)

        # Contraseña
        tk.Label(self.frame, text="Contraseña", font=("Arial", 12), bg="#FFFFFF").pack(anchor="w", padx=20)
        self.password = tk.Entry(self.frame, show="*", font=("Arial", 12), bg="#EFEFEF", bd=1, relief="solid")
        self.password.pack(pady=5, ipady=4, fill="x", padx=20)

        # Botón Login / Ingresar (más alto)
        self.login_btn = tk.Button(
            self.frame,
            text="Ingresar",
            font=("Arial", 12, "bold"),
            bg="#2D89EF",
            fg="white",
            bd=0,
            command=self.login
        )
        self.login_btn.pack(pady=15, ipadx=10, ipady=8)  # ipady aumentado de 4 → 8

        # Vincular Enter al login
        self.master.bind('<Return>', self.login_event)

    def login_event(self, event):
        self.login()

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user == "admin" and pwd == "admin":
            self.frame.destroy()
            Dashboard(self.master)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
