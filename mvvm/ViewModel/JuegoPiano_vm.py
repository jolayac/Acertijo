import threading
import time
from mvvm.Model.juegoPiano import JuegoPianoModel
from mvvm.ViewModel.ReproductorSonidos_vm import ReproductorSonidos


class JuegoPianoVM:
    '''Controlador que enlaza Modelo y Vistas, maneja temporizador y reproducción.'''
    def __init__(self, teclas, notas, ruta_notas, vista_juego, vista_resultado_callback, cantidad_notas_melodia=6):
        '''Inicializa modelo, reproductor y arranca temporizador.'''
        self.modelo = JuegoPianoModel(teclas, notas, cantidad_notas_melodia)
        self.reproductor = ReproductorSonidos(ruta_notas, notas)
        self.vista_juego = vista_juego
        self.vista_resultado_callback = vista_resultado_callback
        self.timer_thread = None
        self.iniciar_temporizador()

    def procesar_tecla(self, tecla):
        '''Procesa una tecla pulsada, sombrear, reproducir sonido y verificar acierto.'''
        if not self.modelo.en_ejecucion or tecla not in self.modelo.teclas:
            return
        # Sombrear la tecla sin usar hilos
        self.vista_juego.sombrear_tecla(tecla)
        
        nota = self.modelo.tecla_a_nota[tecla]
        self.reproductor.reproducir(nota)
        self.modelo.agregar_nota_usuario(nota)
        if self.modelo.usuario_acerto():
            self.modelo.en_ejecucion = False
            self.vista_resultado_callback(
                "¡Felicitaciones, acertaste la melodía!")

    def reproducir_melodia(self):
        '''Lanza un hilo para reproducir la melodía nota por nota.'''
        if self.modelo.en_ejecucion:
            threading.Thread(target=self._hilo_melodia, daemon=True).start()

    def _hilo_melodia(self):
        for nota in self.modelo.melodia:
            if hasattr(self.vista_juego, "_cerrar") and self.vista_juego._cerrar:
                break
            self.reproductor.reproducir(nota)
            time.sleep(0.5)

    def iniciar_temporizador(self):
        self.timer_thread = threading.Thread(target=self._hilo_temporizador)
        self.timer_thread.start()

    def _hilo_temporizador(self):
        while self.modelo.tiempo_restante > 0 and self.modelo.en_ejecucion:
            if hasattr(self.vista_juego, "_cerrar") and self.vista_juego._cerrar:
                return
            self.modelo.tiempo_restante -= 1
            try:
                self.vista_juego.after(
                    0, lambda: self.vista_juego.actualizar_tiempo(self.modelo.tiempo_restante))
            except RuntimeError:
                # La ventana principal ya está cerrada
                return
            time.sleep(1)
        if self.modelo.tiempo_restante == 0 and self.modelo.en_ejecucion:
            if hasattr(self.vista_juego, "_cerrar") and self.vista_juego._cerrar:
                return
            self.modelo.en_ejecucion = False
            try:
                self.vista_juego.after(
                    0, lambda: self.vista_resultado_callback("Se acabó el tiempo"))
            except RuntimeError:
                return

    def reiniciar(self, cantidad_notas_melodia=None):
        self.modelo.reiniciar(cantidad_notas_melodia)
        try:
            self.vista_juego.actualizar_tiempo(self.modelo.tiempo_restante)
        except Exception:
            pass
        self.iniciar_temporizador()
