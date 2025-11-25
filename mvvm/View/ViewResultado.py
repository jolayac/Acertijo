import tkinter as tk


class ViewResultado(tk.Frame):
    def __init__(self, master, mensaje, on_reintentar, on_cerrar):
        super().__init__(master)
        self.label = tk.Label(self, text=mensaje, font=("Arial", 18))
        self.label.pack(pady=30)
        self.btn_reintentar = tk.Button(
            self, text="Intentar de nuevo (R)", font=("Arial", 14), command=on_reintentar)
        self.btn_reintentar.pack(side=tk.LEFT, padx=30, pady=20)
        self.btn_salir = tk.Button(
            self, text="Cerrar (Esc)", font=("Arial", 14), command=on_cerrar)
        self.btn_salir.pack(side=tk.RIGHT, padx=30, pady=20)
        master.bind("<Escape>", lambda e: on_cerrar())
        master.bind("<r>", lambda e: on_reintentar())
        master.bind("<R>", lambda e: on_reintentar())
