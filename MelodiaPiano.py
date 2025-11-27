import tkinter as tk
import sys
import os
from mvvm.View.ViewJuego import ViewJuego
from mvvm.View.ViewResultado import ViewResultado
from mvvm.View.menu import Menu

from mvvm.ViewModel.JuegoPiano_vm import JuegoPianoVM

if __package__ in (None, ""):
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class Interfaz(tk.Tk):
    '''Ventana principal que gestiona frames del menú, juego y resultado.'''
    def __init__(self):
        '''Inicializa configuración básica, rutas y muestra el menú inicial.'''
        super().__init__()
        self.title("Juego de Piano")
        self.teclas = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K']
        self.notas = ['G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4']
        self.ruta_notas = os.path.join(os.path.dirname(__file__), "notas")
        self.frame_actual = None
        self.dificultad_actual = None
        self.vm = None
        self.mostrar_menu()

    def mostrar_menu(self):
        self.geometry("800x400")
        if self.frame_actual:
            # Señal para terminar hilos activos del frame anterior
            if hasattr(self.frame_actual, "_cerrar"):
                self.frame_actual._cerrar = True
            self.frame_actual.destroy()
        
        self.frame_actual = Menu(self, self._on_dificultad_seleccionada)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)

    def _on_dificultad_seleccionada(self, dificultad):
        self.dificultad_actual = dificultad
        self.mostrar_juego()

    def mostrar_juego(self):
        self.geometry("1000x500")
        if self.frame_actual:
            # Señal para terminar hilos activos del frame anterior
            if hasattr(self.frame_actual, "_cerrar"):
                self.frame_actual._cerrar = True
            self.frame_actual.destroy()
        
        # Obtener cantidad de notas según dificultad
        cantidad_notas = {
            "Fácil": 3,
            "Medio": 5,
            "Difícil": 7
        }.get(self.dificultad_actual, 6)
        
        self.vista_juego = ViewJuego(
            self, self.teclas, self.notas, self.on_tecla, self.on_reproducir_melodia, self.mostrar_menu, self.mostrar_juego)
        self.vista_juego._cerrar = False  # Bandera para hilos
        self.frame_actual = self.vista_juego
        self.frame_actual.pack(fill=tk.BOTH, expand=True)
        self.vm = JuegoPianoVM(
            self.teclas, self.notas, self.ruta_notas, self.vista_juego, self.mostrar_resultado, cantidad_notas)
        self.bind("<KeyPress>", self.on_keypress)
        # Reproducir la melodía automáticamente al iniciar el juego
        self.vista_juego.after(100, self.on_reproducir_melodia)

    def mostrar_resultado(self, mensaje):
        self.geometry("800x300")
        if self.frame_actual:
            # Señal para terminar hilos activos del frame anterior
            if hasattr(self.frame_actual, "_cerrar"):
                self.frame_actual._cerrar = True
            self.frame_actual.destroy()
        self.frame_actual = ViewResultado(
            self, mensaje, self.mostrar_juego, self.destroy, self.mostrar_menu)
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
            # Solo reiniciar si estamos en el juego
            if isinstance(self.frame_actual, ViewJuego):
                self.mostrar_juego()
            return
        if tecla == "M":
            self.mostrar_menu()
            return
        if tecla == "ESCAPE":
            self.destroy()
            return
        self.on_tecla(tecla)


if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()
