import threading
import time
import pygame
import os
from modelo import JuegoPianoModelo


class ReproductorSonidos:
    def __init__(self, ruta_notas, lista_notas):
        pygame.mixer.init()
        self.sonidos = {}
        for nota in lista_notas:
            archivo = f"{nota}.mp3"
            path = os.path.join(ruta_notas, archivo)
            if not os.path.exists(path):
                raise FileNotFoundError(f"No se encontró {path}")
            self.sonidos[nota] = pygame.mixer.Sound(path)

    def reproducir(self, nota):
        self.sonidos[nota].play()


class JuegoPianoVM:
    def __init__(self, teclas, notas, ruta_notas, vista_juego, vista_resultado_callback):
        self.modelo = JuegoPianoModelo(teclas, notas)
        self.reproductor = ReproductorSonidos(ruta_notas, notas)
        self.vista_juego = vista_juego
        self.vista_resultado_callback = vista_resultado_callback
        self.timer_thread = None
        self.iniciar_temporizador()

    def procesar_tecla(self, tecla):
        if not self.modelo.en_ejecucion or tecla not in self.modelo.teclas:
            return
        threading.Thread(target=self.vista_juego.sombrear_tecla,
                         args=(tecla,), daemon=True).start()
        nota = self.modelo.tecla_a_nota[tecla]
        self.reproductor.reproducir(nota)
        self.modelo.agregar_nota_usuario(nota)
        if self.modelo.usuario_acerto():
            self.modelo.en_ejecucion = False
            self.vista_resultado_callback(
                "¡Felicitaciones, acertaste la melodía!")

    def reproducir_melodia(self):
        if self.modelo.en_ejecucion:
            threading.Thread(target=self._hilo_melodia).start()

    def _hilo_melodia(self):
        for nota in self.modelo.melodia:
            self.reproductor.reproducir(nota)
            time.sleep(0.5)

    def iniciar_temporizador(self):
        self.timer_thread = threading.Thread(target=self._hilo_temporizador)
        self.timer_thread.start()

    def _hilo_temporizador(self):
        while self.modelo.tiempo_restante > 0 and self.modelo.en_ejecucion:
            self.modelo.tiempo_restante -= 1
            self.vista_juego.after(
                0, lambda: self.vista_juego.actualizar_tiempo(self.modelo.tiempo_restante))
            time.sleep(1)
        if self.modelo.tiempo_restante == 0 and self.modelo.en_ejecucion:
            self.modelo.en_ejecucion = False
            self.vista_juego.after(
                0, lambda: self.vista_resultado_callback("Se acabó el tiempo"))

    def reiniciar(self):
        self.modelo.reiniciar()
        self.vista_juego.actualizar_tiempo(self.modelo.tiempo_restante)
        self.iniciar_temporizador()
