import random


class JuegoPianoModel:
    def __init__(self, teclas, notas, cantidad_notas_melodia=6):
        self.teclas = teclas
        self.notas = notas
        self.cantidad_notas_melodia = cantidad_notas_melodia
        self.tecla_a_nota = dict(zip(teclas, notas))
        self.melodia = random.choices(self.notas, k=cantidad_notas_melodia)
        self.secuencia_usuario = []
        self.tiempo_restante = 60
        self.en_ejecucion = True

    def reiniciar(self, cantidad_notas_melodia=None):
        if cantidad_notas_melodia:
            self.cantidad_notas_melodia = cantidad_notas_melodia
        self.melodia = random.choices(self.notas, k=self.cantidad_notas_melodia)
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
