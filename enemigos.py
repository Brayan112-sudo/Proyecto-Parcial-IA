import pygame;
from behavior_tree import Selector, Secuencia, Accion
from astar import Astar


class enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, animaciones):
        super().__init__()

        self.nombre = "Greñas"

        self.animaciones = animaciones
        self.frame_index = 0
        self.image = self.animaciones[self.frame_index]
        self.update_time = pygame.time.get_ticks()

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 2
        self.flip = False

    # --- Inteligencia artificial ---
        self.arbol = Selector([
            Secuencia([
                Accion(self.ver_jugador),
                Accion(self.perseguir_jugador)
            ]),
            Accion(self.patrullar)
        ])

    # --- Funciones del árbol ---
    def ver_jugador(self):
        # Devuelve True si el jugador está cerca
        distancia = abs(self.rect.x - self.jugador.rect.x)
        return distancia < 200

    def perseguir_jugador(self):
        # Crear A* cada vez que se quiere perseguir
        astar = Astar(self.rect.topleft, self.jugador.rect.topleft)
        camino = astar.buscar() # Buscar ruta hacia el jugador

        if camino:
            siguiente = camino[0]
            self.rect.x = siguiente[0]
            self.rect.y = siguiente[1]
        return True

    def patrullar(self):
        # Movimiento simple de patrullaje
        self.rect.x += self.velocidad
        return True



    def perseguir(self, jugador, mapa):

        dx = 0
        dy = 0

        # Comparar posiciones
        if jugador.rect.x > self.rect.x:
            dx = self.velocidad
            self.flip = False
        if jugador.rect.x < self.rect.x:
            dx = -self.velocidad
            self.flip = True

        if jugador.rect.y > self.rect.y:
            dy = self.velocidad
        if jugador.rect.y < self.rect.y:
            dy = -self.velocidad

        # Movimiento X
        self.rect.x += dx
        if not mapa.puede_moverse(self.rect):
            self.rect.x -= dx

        # Movimiento Y
        self.rect.y += dy
        if not mapa.puede_moverse(self.rect):
            self.rect.y -= dy

        # Evita que salga del mapa
        self.rect.x = max(0, min(self.rect.x, mapa.ancho_mundo - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, mapa.alto_mundo - self.rect.height))

    def atacar(self, jugador):
        if self.rect.colliderect(jugador.rect):
            jugador.morir()


    def update(self):
        # Ejecuta árbol de comportamiento
        self.arbol.ejecutar()


        cooldown_animacion = 120
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            # Avanzar al siguiente frame de la animación
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)
            self.image = self.animaciones[self.frame_index]
            self.update_time = pygame.time.get_ticks()


    def dibujar(self, ventana):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_flip, self.rect)
        #pygame.draw.rect(interfaz, (255, 255, 0), self.rect, 1) # debug