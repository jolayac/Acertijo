import tkinter as tk


class ViewJuego(tk.Frame):
    def __init__(self, master, teclas, notas, on_tecla, on_reproducir_melodia, on_mostrar_menu, on_reiniciar):
        super().__init__(master)
        self.teclas = teclas
        self.notas = notas
        self.on_tecla = on_tecla
        self.on_reproducir_melodia = on_reproducir_melodia
        self.on_mostrar_menu = on_mostrar_menu
        self.on_reiniciar = on_reiniciar
        self.botones_teclas = {}
        
        # Frame superior con timer y botón menú
        self.frame_superior = tk.Frame(self)
        self.frame_superior.pack(pady=10)
        
        self.timer_label = tk.Label(
            self.frame_superior, text="Tiempo: 60", font=("Arial", 16))
        self.timer_label.pack(side=tk.LEFT, padx=20)
        
        
        # Frame central con botones de notas
        self.frame_central = tk.Frame(self)
        self.frame_central.pack(pady=10)
        
        self.frame_teclas = tk.Frame(self.frame_central)
        self.frame_teclas.pack()
        for tecla, nota in zip(teclas, notas):
            btn = tk.Button(self.frame_teclas, text=f"{tecla}", font=("Arial", 14, "bold"), width=6, height=3, bg="white", relief="raised",
                            command=lambda t=tecla: self.on_tecla(t))
            btn.pack(side=tk.LEFT, padx=2)
            self.botones_teclas[tecla] = btn
        
        # Frame inferior con botones de control
        self.frame_inferior = tk.Frame(self)
        self.frame_inferior.pack(pady=10)
        
        self.btn_menu = tk.Button(
            self.frame_inferior, text="Menú (M)", font=("Arial", 12), command=on_mostrar_menu)
        self.btn_menu.pack(side=tk.LEFT, padx=15)
        
        self.btn_melodia = tk.Button(self.frame_inferior, text="Reproducir Melodía (Space)", font=(
            "Arial", 12), command=self.on_reproducir_melodia)
        self.btn_melodia.pack(side=tk.LEFT, padx=15)
        
        self.btn_reiniciar = tk.Button(self.frame_inferior, text="Reiniciar (R)", font=(
            "Arial", 12), command=on_reiniciar)
        self.btn_reiniciar.pack(side=tk.RIGHT, padx=15)

    def actualizar_tiempo(self, tiempo):
        self.timer_label.config(text=f"Tiempo: {tiempo}")

    def sombrear_tecla(self, tecla, duracion_ms=200):
        if tecla not in self.botones_teclas:
            return
        btn = self.botones_teclas[tecla]
        try:
            btn.config(relief="sunken", bg="gray")
            self.after(duracion_ms, lambda: self._restaurar_boton(btn))
        except tk.TclError:
            # El botón ya fue destruido
            pass

    def _restaurar_boton(self, btn):
        try:
            btn.config(relief="raised", bg="white")
        except tk.TclError:
            # El botón ya fue destruido
            pass