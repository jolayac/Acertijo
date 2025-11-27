import pygame
import os


class ReproductorSonidos:
    '''Encapsula la carga y reproducción de archivos de audio usando pygame.'''
    def __init__(self, ruta_notas, lista_notas):
        '''Inicializa el mezclador y carga los archivos .MP3 desde la ruta dada.'''
        pygame.mixer.init()
        self.sonidos = {}
        for nota in lista_notas:
            archivo = f"{nota}.MP3"
            path = os.path.join(ruta_notas, archivo)
            if not os.path.exists(path):
                raise FileNotFoundError(f"No se encontró {path}")
            self.sonidos[nota] = pygame.mixer.Sound(path)

    def reproducir(self, nota):
        '''Reproduce la nota solicitada si existe en el diccionario de sonidos.'''
        if nota in self.sonidos:
            self.sonidos[nota].play()