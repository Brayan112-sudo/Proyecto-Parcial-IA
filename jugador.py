import pygame

class jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, image, animaciones):
        super().__init__()
        self.animaciones = animaciones
        self.flip = False

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocidad = 3

    def movimiento(self, delta_x, delta_y, ancho, alto, mapa):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        # Movimiento en X
        self.rect.x += delta_x
        if not mapa.puede_moverse(self.rect):
            self.rect.x -= delta_x

        # Movimiento en Y
        self.rect.y += delta_y
        if not mapa.puede_moverse(self.rect):
            self.rect.y -= delta_y

        # Limitar a los bordes de la ventana
        self.rect.x = max(0, min(self.rect.x, ancho - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, alto  - self.rect.height))

    def update(self):
        cooldown_animacion = 100
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()
            self.image = self.animaciones[self.frame_index]

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.rect)

    def morir(self):
        print("El jugador ha muerto")