import pygame;

class jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, image, animaciones):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0)) # verde
        self.animaciones = image
        self.flip = False
        self.animaciones = animaciones

        # Imagen de la animación que se muestra actual
        self.frame_index = 0

        # Aquí se almacena la hora actual (en milisegundo desde que se inició pygame)
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Escalar la imagen al tamaño indicado
        self.rect = self.image.get_rect()


        # Velocidad de movimiento
        self.velocidad = 3

    def movimiento(self, delta_x, delta_y, ancho, alto, mapa):
        self.rect.x += delta_x
        self.rect.y += delta_y


        # Limitar horizontal
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ancho:
            self.rect.right = ancho

        # Limitar vertical
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > alto:
            self.rect.bottom = alto

        # Voltear sprite
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


        # Limitar ventana
        self.rect.x = max(0, min(self.rect.x, ancho - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, alto - self.rect.height))


    def update(self):
        cooldown_animacion = 100
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()
            self.image = self.animaciones[self.frame_index]
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, flip_y=False)
        interfaz.blit(imagen_flip, self.rect)
        #pygame.draw.rect(interfaz, (255, 255, 0), self.rect, 1) # debug

    def morir(self):
      print("El jugador ha muerto")