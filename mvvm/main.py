import tkinter as tk
from vista import VistaJuego, VistaResultado
from vm import JuegoPianoVM


class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Juego de Piano")
        self.geometry("1800x400")
        self.teclas = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K']
        self.notas = ['C4', 'D4', 'E4', 'F4', 'G4', 'A#4', 'B4', 'C5']
        self.ruta_notas = r"C:\Users\LENOVO\3D Objects\Acertijo\notas"
        self.frame_actual = None
        self.mostrar_juego()

    def mostrar_juego(self):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.vista_juego = VistaJuego(
            self, self.teclas, self.notas, self.on_tecla, self.on_reproducir_melodia)
        self.frame_actual = self.vista_juego
        self.frame_actual.pack(fill=tk.BOTH, expand=True)
        self.vm = JuegoPianoVM(
            self.teclas, self.notas, self.ruta_notas, self.vista_juego, self.mostrar_resultado)
        self.bind("<KeyPress>", self.on_keypress)

    def mostrar_resultado(self, mensaje):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = VistaResultado(
            self, mensaje, self.mostrar_juego, self.destroy)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)

    def on_tecla(self, tecla):
        self.vm.procesar_tecla(tecla)

    def on_reproducir_melodia(self):
        self.vm.reproducir_melodia()

    def on_keypress(self, event):
        tecla = event.keysym.upper()
        if tecla == "SPACE":
            self.on_reproducir_melodia()
            return
        if tecla == "R":
            self.mostrar_juego()
            return
        if tecla == "ESCAPE":
            self.destroy()
            return
        self.on_tecla(tecla)


if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()
