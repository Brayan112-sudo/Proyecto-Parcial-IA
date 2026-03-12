import pygame
from collections import deque

# Brayan Obed Solano Febles
# Matrícula= 23-SISN-2-005


TAMANO_CELDA = 47


class enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones, mapa):
        super().__init__()
        self.mapa = mapa
        self.nombre = "Grenas"
        self.animaciones = animaciones
        self.jugador = None

        self.frame_index = 0
        self.image = self.animaciones[self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocidad = 5
        self.flip = False

    def update_animacion(self):
        cooldown = 120
        if pygame.time.get_ticks() - self.update_time >= cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.image = self.animaciones[self.frame_index]
            self.update_time = pygame.time.get_ticks()

    def dibujar(self, ventana):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_flip, self.rect)