import tkinter as tk
from login_window import LoginWindow

def main():
    root = tk.Tk()
    root.title("Comics México")
    root.geometry("1200x700")
    root.resizable(False, False)

    LoginWindow(root)

    root.mainloop()

if __name__ == "__main__":
    main()