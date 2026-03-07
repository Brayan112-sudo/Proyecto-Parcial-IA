import pygame;
from behavior_tree import Selector, Secuencia, Accion
from astar import Astar


class enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones, puntos_patru, mapa):
        super().__init__()
        self.mapa = mapa

        self.nombre = "Greñas"
        self.animaciones = animaciones
        self.puntos_patru = puntos_patru
        self.mapa = mapa
        self.jugador = None
        self.indice_patru = 0
        self.frame_index = 0
        self.image = self.animaciones[self.frame_index]
        self.update_time = pygame.time.get_ticks()

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 2
        self.flip = False

        # Árbol de comportamiento
        self.arbol = Selector([
            Secuencia([
                Accion(self.ver_jugador),
                Accion(self.perseguir_jugador)
            ]),
            Accion(self.patrullar)
        ])

        # Patrulla
        self.puntos_patru = puntos_patru
        self.indice_patru = 0
        self.camino_patru = []

        # Caminos
        self.camino = []

        # Jugador (se asigna después)
        self.jugador = None

    # --- Funciones del árbol ---
    def ver_jugador(self):
        if self.jugador is None:
            return False
        distancia = ((self.rect.centerx - self.jugador.rect.centerx)**2 +
                    (self.rect.centery - self.jugador.rect.centery)**2)**0.5
        return distancia > 200  # detecta jugador a 200 px

    def perseguir_jugador(self):
        if self.jugador is None:
           return False

        if not self.camino:
           self.camino = Astar(self.rect.topleft, self.jugador.rect.topleft).buscar()

        # Guardar posición anterior por si hay colisión
        paso_anterior = self.rect.topleft

        # Movimiento paso a paso
        if self.camino:
            siguiente = self.camino.pop(0)
            self.rect.topleft = siguiente
            if not self.mapa.puede_moverse(self.rect):
                self.rect.topleft = paso_anterior  # vuelve si choca

        return True

    def patrullar(self):
        mapa = self.mapa
        # Generar camino hacia el siguiente punto si no existe
        if not self.camino_patru:
           destino = self.puntos_patru[self.indice_patru]
           self.camino_patru = Astar(self.rect.topleft, destino).buscar()

        paso_anterior = self.rect.topleft

        if self.camino_patru:
            siguiente = self.camino_patru.pop(0)
            self.rect.topleft = siguiente
            if not mapa.puede_moverse(self.rect):
                self.rect.topleft = paso_anterior
        else:
            # Cambiar al siguiente punto de patrulla
            self.indice_patru = (self.indice_patru + 1) % len(self.puntos_patru)

        return True

    # --- Animación ---
    def update_animacion(self):
        cooldown_animacion = 120
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.image = self.animaciones[self.frame_index]
            self.update_time = pygame.time.get_ticks()

    # --- Dibujar ---
    def dibujar(self, ventana):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_flip, self.rect)