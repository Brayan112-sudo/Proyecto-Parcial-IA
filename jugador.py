import pygame


# Brayan Obed Solano Febles
# Matrícula= 23-SISN-2-005

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


        # Sistema de vida

        self.vida_maxima = 100
        self.vida = 100
        self.invulnerable = False
        self.tiempo_invulnerable = 0
        self.duracion_invulnerable = 1000


        # Sonidos del jugador

        self.sonido_daño   = pygame.mixer.Sound("assets/sounds/sonido_daño_jugador.wav")
        self.sonido_muerte = pygame.mixer.Sound("assets/sounds/muerte_jugador.wav")
        self.sonido_pasos  = pygame.mixer.Sound("assets/sounds/pasos_jugador.wav")

        self.sonido_daño.set_volume(0.8)
        self.sonido_muerte.set_volume(1.0)
        self.sonido_pasos.set_volume(0.4)


        # Control de pasos

        self.tiempo_ultimo_paso = 0
        self.intervalo_pasos    = 350


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


        # Limitar los bordes de la ventana
        self.rect.x = max(0, min(self.rect.x, ancho - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, alto  - self.rect.height))


        # Pasos solo si se está moviendo
        caminando = (delta_x != 0 or delta_y != 0)
        ahora = pygame.time.get_ticks()
        if caminando and ahora - self.tiempo_ultimo_paso >= self.intervalo_pasos:
            self.sonido_pasos.play()
            self.tiempo_ultimo_paso = ahora

    def recibir_daño(self, cantidad=10):

        if self.invulnerable:
            return

        self.vida -= cantidad
        self.invulnerable = True
        self.tiempo_invulnerable = pygame.time.get_ticks()

        self.sonido_daño.play()

        if self.vida <= 0:
            self.vida = 0
            self.morir()

    def update(self):
        # Actualizar invulnerabilidad
        if self.invulnerable:
            if pygame.time.get_ticks() - self.tiempo_invulnerable >= self.duracion_invulnerable:
                self.invulnerable = False

        # Animación
        cooldown_animacion = 100
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.update_time = pygame.time.get_ticks()
            self.image = self.animaciones[self.frame_index]


    def dibujar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.rect)


    def dibujar_barra_vida(self, interfaz):

        margen_x    = 20
        margen_y    = 20
        barra_ancho = 200
        barra_alto  = 20
        radio       = 6

        font = pygame.font.SysFont("consolas", 14, bold=True)


        # Etiqueta HP

        label = font.render("HP", True, (220, 220, 220))
        interfaz.blit(label, (margen_x, margen_y - 1))
        offset_x = margen_x + label.get_width() + 8


        # Fondo de la barra gris oscuro 

        fondo_rect = pygame.Rect(offset_x, margen_y, barra_ancho, barra_alto)
        pygame.draw.rect(interfaz, (50, 50, 50), fondo_rect, border_radius=radio)


        # Relleno de vida

        porcentaje = self.vida / self.vida_maxima
        fill_ancho = int(barra_ancho * porcentaje)

        if porcentaje > 0.5:
            color_vida = (50, 200, 80)
        elif porcentaje > 0.25:
            color_vida = (230, 180, 0)
        else:
            color_vida = (200, 40, 40)

        if fill_ancho > 0:
            fill_rect = pygame.Rect(offset_x, margen_y, fill_ancho, barra_alto)
            pygame.draw.rect(interfaz, color_vida, fill_rect, border_radius=radio)


        # Borde blanco

        pygame.draw.rect(interfaz, (200, 200, 200), fondo_rect, 2, border_radius=radio)


        # Texto numérico centrado en la barra

        texto_vida = font.render(f"{self.vida} / {self.vida_maxima}", True, (255, 255, 255))
        interfaz.blit(texto_vida, (
            offset_x + barra_ancho // 2 - texto_vida.get_width()  // 2,
            margen_y  + barra_alto  // 2 - texto_vida.get_height() // 2
        ))

    def morir(self):
        self.sonido_muerte.play()
        print("El jugador ha muerto")