import random


class JuegoPianoModelo:
    def __init__(self, teclas, notas):
        self.teclas = teclas
        self.notas = notas
        self.tecla_a_nota = dict(zip(teclas, notas))
        self.melodia = random.choices(self.notas, k=6)
        self.secuencia_usuario = []
        self.tiempo_restante = 60
        self.en_ejecucion = True

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
