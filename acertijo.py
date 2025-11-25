import tkinter as tk
import sys
import os
from mvvm.View.ViewJuego import ViewJuego
from mvvm.View.ViewResultado import ViewResultado

from mvvm.ViewModel.JuegoPiano_vm import JuegoPianoVM

if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Juego de Piano")
        self.geometry("1800x400")
        self.teclas = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K']
        self.notas = ['G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4']
        self.ruta_notas = r"C:\Users\LENOVO\3D Objects\Acertijo\notas"
        self.frame_actual = None
        self.mostrar_juego()

    def mostrar_juego(self):
        self.geometry("1800x400")
        if self.frame_actual:
            # Señal para terminar hilos activos del frame anterior
            if hasattr(self.frame_actual, "_cerrar"):
                self.frame_actual._cerrar = True
            self.frame_actual.destroy()
        self.vista_juego = ViewJuego(
            self, self.teclas, self.notas, self.on_tecla, self.on_reproducir_melodia)
        self.vista_juego._cerrar = False  # Bandera para hilos
        self.frame_actual = self.vista_juego
        self.frame_actual.pack(fill=tk.BOTH, expand=True)
        self.vm = JuegoPianoVM(
            self.teclas, self.notas, self.ruta_notas, self.vista_juego, self.mostrar_resultado)
        self.bind("<KeyPress>", self.on_keypress)

    def mostrar_resultado(self, mensaje):
        self.geometry("900x400")
        if self.frame_actual:
            # Señal para terminar hilos activos del frame anterior
            if hasattr(self.frame_actual, "_cerrar"):
                self.frame_actual._cerrar = True
            self.frame_actual.destroy()
        self.frame_actual = ViewResultado(
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
