import tkinter as tk
import threading
import time
import random
import pygame
import os


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


class JuegoPiano:
    def __init__(self, teclas, notas):
        self.teclas = teclas
        self.notas = notas
        self.tecla_a_nota = dict(zip(teclas, notas))
        self.melodia = random.choices(self.notas, k=6)
        self.secuencia_usuario = []
        self.tiempo_restante = 60
        self.en_ejecucion = True
        print("Melodía :", " → ".join(self.melodia))

    def reiniciar(self):
        self.melodia = random.choices(self.notas, k=6)
        self.secuencia_usuario = []
        self.tiempo_restante = 60
        self.en_ejecucion = True

    def agregar_nota_usuario(self, nota):
        self.secuencia_usuario.append(nota)
        if len(self.secuencia_usuario) > len(self.melodia):
            self.secuencia_usuario = self.secuencia_usuario[-len(
                self.melodia):]

    def usuario_acerto(self):
        return self.secuencia_usuario == self.melodia


class FrameResultado(tk.Frame):
    def __init__(self, master, mensaje, callback_reintentar, callback_salir):
        super().__init__(master)
        self.label = tk.Label(self, text=mensaje, font=("Arial", 18))
        self.label.pack(pady=30)
        self.btn_reintentar = tk.Button(self, text="Intentar de nuevo (R)", font=(
            "Arial", 14), command=callback_reintentar)
        self.btn_reintentar.pack(side=tk.LEFT, padx=30, pady=20)
        self.btn_salir = tk.Button(self, text="Cerrar (Esc)", font=(
            "Arial", 14), command=callback_salir)
        self.btn_salir.pack(side=tk.RIGHT, padx=30, pady=20)
        master.bind("<Escape>", lambda e: callback_salir())
        master.bind("<r>", lambda e: callback_reintentar())
        master.bind("<R>", lambda e: callback_reintentar())


class FrameJuego(tk.Frame):
    def __init__(self, master, juego, reproductor, mostrar_resultado_callback):
        super().__init__(master)
        self.juego = juego
        self.reproductor = reproductor
        self.mostrar_resultado_callback = mostrar_resultado_callback
        self.sombra_lock = threading.Lock()
        self.sombra_timers = {}
        self.timer_thread = None
        self.crear_interfaz()
        self.iniciar_temporizador()
        master.bind("<KeyPress>", self.manejar_tecla)

    def crear_interfaz(self):
        self.timer_label = tk.Label(
            self, text=f"Tiempo: {self.juego.tiempo_restante}", font=("Arial", 20))
        self.timer_label.pack(pady=10)
        self.frame_teclas = tk.Frame(self)
        self.frame_teclas.pack()
        self.botones_teclas = {}
        for tecla in self.juego.teclas:
            nota = self.juego.tecla_a_nota[tecla]
            btn = tk.Button(self.frame_teclas, text=f"{tecla}\n{nota}", font=("Arial", 24, "bold"), width=10, height=5, bg="white", relief="raised",
                            command=lambda t=tecla: self.manejar_boton_tecla(t))
            btn.pack(side=tk.LEFT, padx=5)
            self.botones_teclas[tecla] = btn
        self.btn_melodia = tk.Button(self, text="Reproducir Melodía", font=(
            "Arial", 16), command=self.reproducir_melodia)
        self.btn_melodia.pack(pady=20)

    def manejar_boton_tecla(self, tecla):
        self.procesar_entrada(tecla)

    def manejar_tecla(self, event):
        tecla = event.keysym.upper()
        if tecla == "SPACE":
            self.reproducir_melodia()
            return
        if tecla == "R":
            self.mostrar_resultado_callback("Reiniciar")
            return
        if tecla == "ESCAPE":
            self.mostrar_resultado_callback("Cerrar")
            return
        self.procesar_entrada(tecla)

    def procesar_entrada(self, tecla):
        if not self.juego.en_ejecucion or tecla not in self.juego.teclas:
            return
        threading.Thread(target=self.sombrear_tecla,
                         args=(tecla,), daemon=True).start()
        nota = self.juego.tecla_a_nota[tecla]
        self.reproductor.reproducir(nota)
        self.juego.agregar_nota_usuario(nota)
        if self.juego.usuario_acerto():
            self.juego.en_ejecucion = False
            self.mostrar_resultado_callback(
                "¡Felicitaciones, acertaste la melodía!")

    def sombrear_tecla(self, tecla, duracion_ms=200):
        with self.sombra_lock:
            if tecla in self.sombra_timers:
                try:
                    self.after_cancel(self.sombra_timers[tecla])
                except:
                    pass
            btn = self.botones_teclas[tecla]
            btn.config(relief="sunken", bg="gray")
            timer_id = self.after(duracion_ms, lambda: btn.config(
                relief="raised", bg="white"))
            self.sombra_timers[tecla] = timer_id

    def reproducir_melodia(self):
        if self.juego.en_ejecucion:
            threading.Thread(target=self._hilo_melodia).start()

    def _hilo_melodia(self):
        for nota in self.juego.melodia:
            self.reproductor.reproducir(nota)
            time.sleep(0.5)

    def iniciar_temporizador(self):
        self.timer_thread = threading.Thread(target=self._hilo_temporizador)
        self.timer_thread.start()

    def _hilo_temporizador(self):
        while self.juego.tiempo_restante > 0 and self.juego.en_ejecucion:
            self.juego.tiempo_restante -= 1
            self.after(0, self.actualizar_label_tiempo)
            time.sleep(1)
        if self.juego.tiempo_restante == 0 and self.juego.en_ejecucion:
            self.juego.en_ejecucion = False
            self.after(0, lambda: self.mostrar_resultado_callback(
                "Se acabó el tiempo"))

    def actualizar_label_tiempo(self):
        self.timer_label.config(text=f"Tiempo: {self.juego.tiempo_restante}")

    def reiniciar(self):
        self.juego.reiniciar()
        self.timer_label.config(text=f"Tiempo: {self.juego.tiempo_restante}")
        for tecla, btn in self.botones_teclas.items():
            btn.config(relief="raised", bg="white")
        self.timer_thread = threading.Thread(target=self._hilo_temporizador)
        self.timer_thread.start()


class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Juego de Piano")
        self.geometry("1800x400")
        # Listas configurables
        self.teclas = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K']
        self.notas = ['C4', 'D4', 'E4', 'F4', 'G4', 'A#4', 'B4', 'C5']
        self.ruta_notas = r"C:\Users\LENOVO\3D Objects\Acertijo\notas mp3"
        self.juego = JuegoPiano(self.teclas, self.notas)
        self.reproductor = ReproductorSonidos(self.ruta_notas, self.notas)
        self.frame_actual = None
        self.mostrar_juego()

    def mostrar_juego(self):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.juego.reiniciar()
        self.frame_actual = FrameJuego(
            self, self.juego, self.reproductor, self.mostrar_resultado)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)

    def mostrar_resultado(self, mensaje):
        if self.frame_actual:
            self.frame_actual.destroy()
        if mensaje == "Reiniciar":
            self.mostrar_juego()
            return
        if mensaje == "Cerrar":
            self.destroy()
            return
        self.frame_actual = FrameResultado(
            self, mensaje, self.mostrar_juego, self.destroy)
        self.frame_actual.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()
