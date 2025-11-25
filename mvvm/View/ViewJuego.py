import tkinter as tk


class ViewJuego(tk.Frame):
    def __init__(self, master, teclas, notas, on_tecla, on_reproducir_melodia):
        super().__init__(master)
        self.teclas = teclas
        self.notas = notas
        self.on_tecla = on_tecla
        self.on_reproducir_melodia = on_reproducir_melodia
        self.botones_teclas = {}
        self.timer_label = tk.Label(
            self, text="Tiempo: 60", font=("Arial", 20))
        self.timer_label.pack(pady=10)
        self.frame_teclas = tk.Frame(self)
        self.frame_teclas.pack()
        for tecla, nota in zip(teclas, notas):
            btn = tk.Button(self.frame_teclas, text=f"{tecla}\n{nota}", font=("Arial", 24, "bold"), width=10, height=5, bg="white", relief="raised",
                            command=lambda t=tecla: self.on_tecla(t))
            btn.pack(side=tk.LEFT, padx=5)
            self.botones_teclas[tecla] = btn
        self.btn_melodia = tk.Button(self, text="Reproducir Melodía", font=(
            "Arial", 16), command=self.on_reproducir_melodia)
        self.btn_melodia.pack(pady=20)

    def actualizar_tiempo(self, tiempo):
        self.timer_label.config(text=f"Tiempo: {tiempo}")

    def sombrear_tecla(self, tecla, duracion_ms=200):
        btn = self.botones_teclas[tecla]
        btn.config(relief="sunken", bg="gray")
        self.after(duracion_ms, lambda: btn.config(
            relief="raised", bg="white"))