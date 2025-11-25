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