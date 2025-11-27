import tkinter as tk


class ViewResultado(tk.Frame):

    def __init__(self, master, mensaje, on_reintentar, on_cerrar, on_mostrar_menu):
        super().__init__(master)
        self.label = tk.Label(self, text=mensaje, font=("Arial", 18))
        self.label.pack(pady=30)
        
        # Frame con botones
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(pady=20)
        
        self.btn_reintentar = tk.Button(
            self.frame_botones, text="Intentar de nuevo (R)", font=("Arial", 14), command=on_reintentar)
        self.btn_reintentar.pack(side=tk.LEFT, padx=15)
        
        self.btn_menu = tk.Button(
            self.frame_botones, text="Menú (M)", font=("Arial", 14), command=on_mostrar_menu)
        self.btn_menu.pack(side=tk.LEFT, padx=15)
        
        self.btn_salir = tk.Button(
            self.frame_botones, text="Cerrar (Esc)", font=("Arial", 14), command=on_cerrar)
        self.btn_salir.pack(side=tk.LEFT, padx=15)
        
        master.bind("<Escape>", lambda e: on_cerrar())
        master.bind("<r>", lambda e: on_reintentar())
        master.bind("<R>", lambda e: on_reintentar())
