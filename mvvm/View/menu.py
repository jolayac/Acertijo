import tkinter as tk


class Menu(tk.Frame):
    def __init__(self, master, on_dificultad_seleccionada):
        super().__init__(master)
        self.on_dificultad_seleccionada = on_dificultad_seleccionada
        self.botones_dificultad = {}
        
        # Label título centrado
        self.label_titulo = tk.Label(
            self, text="ACIERTA LA MELODÍA", font=("Arial", 32, "bold"))
        self.label_titulo.pack(pady=40)
        
        # Frame para los botones
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(pady=20)
        
        # Botones de dificultad
        dificultades = ["Fácil", "Medio", "Difícil"]
        for dificultad in dificultades:
            btn = tk.Button(
                self.frame_botones,
                text=dificultad,
                font=("Arial", 24, "bold"),
                width=10,
                height=5,
                bg="white",
                relief="raised",
                command=lambda d=dificultad: self._on_dificultad_click(d)
            )
            btn.pack(side=tk.LEFT, padx=15)
            self.botones_dificultad[dificultad] = btn
    
    def _on_dificultad_click(self, dificultad):
        '''sombrear el botón brevemente y llamar al callback con la dificultad.'''
        btn = self.botones_dificultad[dificultad]
        btn.config(relief="sunken", bg="gray")
        self.after(200, lambda: btn.config(relief="raised", bg="white"))
        self.on_dificultad_seleccionada(dificultad)
