import pygame
from astar import Astar, Estado

TAMANO_CELDA    = 47
RANGO_DETECTAR  = 200
RANGO_PERDER    = 350   # distancia a la que pierde al jugador
TIEMPO_ESPERA   = 2000  # ms quieto antes de reanudar patrulla

class Nodo:
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)


class Selector(Nodo):
    def __init__(self, hijos=None):
        super().__init__()
        if hijos is None:
            hijos = []
        self.hijos = hijos

    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False


class Secuencia(Nodo):
    def __init__(self, hijos=None):
        super().__init__()
        if hijos is None:
            hijos = []
        self.hijos = hijos

    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True


class Accion(Nodo):
    def __init__(self, funcion):
        super().__init__()
        self.accion = funcion

    def ejecutar(self):
        return self.accion()


class Invertir(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        return not self.hijos[0].ejecutar()


class Timer(Nodo):
    def __init__(self, tiempo):
        super().__init__()
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

    def ejecutar(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return False
        else:
            self.tiempo_restante = self.tiempo
            if self.hijos:
                self.hijos[0].ejecutar()
            return True


class Guardia:
    def __init__(self, enemigo, mapa, puntos_patru, rango_deteccion=RANGO_DETECTAR):
        self.enemigo         = enemigo
        self.mapa            = mapa
        self.jugador         = None
        self.alertado        = False
        self.puntos_patru    = puntos_patru
        self.patru_index     = 0
        self.ruta_actual     = []
        self.ruta_patru      = []
        self.tiempo_ruta     = 0
        self.rango_deteccion = rango_deteccion

        # ── Estados del ciclo patrulla/persecución ──
        # "patrullando" | "persiguiendo" | "esperando"
        self.estado          = "patrullando"
        self.timer_espera    = 0   # marca de tiempo cuando entró en "esperando"

        self.comportamiento  = Selector()
        self.secuenciaAtaque = Secuencia()
        self.secuenciaPatru  = Secuencia()
        # ── Secuencia de espera (perdió al jugador) ──
        self.secuenciaEspera = Secuencia()

        # Orden del Selector: espera → ataque → patrulla
        self.comportamiento.agregar_hijo(self.secuenciaEspera)
        self.comportamiento.agregar_hijo(self.secuenciaAtaque)
        self.comportamiento.agregar_hijo(self.secuenciaPatru)

        # Espera: solo se activa si está en estado "esperando"
        self.secuenciaEspera.agregar_hijo(Accion(self.esta_esperando))
        self.secuenciaEspera.agregar_hijo(Accion(self.esperar))

        # Ataque: detecta → persigue
        self.secuenciaAtaque.agregar_hijo(Accion(self.detectar_jugador))
        self.secuenciaAtaque.agregar_hijo(Accion(self.atacar))

        # Patrulla: movimiento entre puntos
        self.secuenciaPatru.agregar_hijo(Accion(self.Patrullar))

        self.arbol = self.comportamiento

    def Agregar_objetivo(self, jugador):
        self.jugador = jugador
        self.enemigo.jugador = jugador

    def _distancia_jugador(self):
        if self.jugador is None:
            return float("inf")
        dx = self.jugador.rect.centerx - self.enemigo.rect.centerx
        dy = self.jugador.rect.centery - self.enemigo.rect.centery
        return (dx**2 + dy**2) ** 0.5

    # ── Nuevo: condición para la secuencia de espera ──
    def esta_esperando(self):
        return self.estado == "esperando"

    # ── Nuevo: lógica de espera antes de retomar patrulla ──
    def esperar(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.timer_espera >= TIEMPO_ESPERA:
            # Terminó la espera → reanudar patrulla
            self.estado    = "patrullando"
            self.alertado  = False
            self.ruta_patru = []   # recalcular ruta al próximo punto
        return True   # mientras espera, bloquea ataque y patrulla

    def detectar_jugador(self):
        if self.jugador is None:
            return False

        distancia = self._distancia_jugador()

        # Detecta al jugador → persiguiendo
        if distancia <= self.rango_deteccion:
            self.alertado = True
            self.estado   = "persiguiendo"

        # ── Nuevo: pierde al jugador → esperando ──
        if self.alertado and distancia > RANGO_PERDER:
            self.alertado     = False
            self.estado       = "esperando"
            self.timer_espera = pygame.time.get_ticks()
            self.ruta_actual  = []
            return False   # corta la secuencia de ataque

        return self.alertado

    def atacar(self):
        if self.jugador is None:
            return False

        ahora          = pygame.time.get_ticks()
        ruta_vacia     = len(self.ruta_actual) == 0
        tiempo_vencido = (ahora - self.tiempo_ruta) > 400

        if ruta_vacia or tiempo_vencido:
            inicio = Estado(
                self.enemigo.rect.centerx // TAMANO_CELDA,
                self.enemigo.rect.centery // TAMANO_CELDA
            )
            final = Estado(
                self.jugador.rect.centerx // TAMANO_CELDA,
                self.jugador.rect.centery // TAMANO_CELDA
            )
            nueva = Astar(inicio, final, mapa=self.mapa, tam_celda=TAMANO_CELDA).buscar()
            if nueva:
                self.ruta_actual = nueva
                self.tiempo_ruta = ahora
                if self.ruta_actual:
                    self.ruta_actual.pop(0)

        if self.ruta_actual:
            destino_px, destino_py = self.ruta_actual[0]
            dx = destino_px - self.enemigo.rect.centerx
            dy = destino_py - self.enemigo.rect.centery
            distancia = max(1, (dx**2 + dy**2) ** 0.5)

            if distancia < self.enemigo.velocidad + 1:
                self.ruta_actual.pop(0)
            else:
                paso_anterior = self.enemigo.rect.topleft
                self.enemigo.rect.x += int(self.enemigo.velocidad * dx / distancia)
                self.enemigo.rect.y += int(self.enemigo.velocidad * dy / distancia)
                if not self.mapa.puede_moverse(self.enemigo.rect):
                    self.enemigo.rect.topleft = paso_anterior
                    self.ruta_actual = []
                self.enemigo.flip = dx < 0

        return True

    def Patrullar(self):
        if not self.puntos_patru:
            return False

        destino = self.puntos_patru[self.patru_index]

        if not self.ruta_patru:
            inicio = Estado(
                self.enemigo.rect.centerx // TAMANO_CELDA,
                self.enemigo.rect.centery // TAMANO_CELDA
            )
            final = Estado(
                destino[0] // TAMANO_CELDA,
                destino[1] // TAMANO_CELDA
            )
            self.ruta_patru = Astar(inicio, final, mapa=self.mapa, tam_celda=TAMANO_CELDA).buscar()
            if self.ruta_patru:
                self.ruta_patru.pop(0)

        if self.ruta_patru:
            dest_px, dest_py = self.ruta_patru[0]
            dx = dest_px - self.enemigo.rect.centerx
            dy = dest_py - self.enemigo.rect.centery
            distancia = max(1, (dx**2 + dy**2) ** 0.5)

            if distancia < self.enemigo.velocidad + 1:
                self.ruta_patru.pop(0)
            else:
                paso_anterior = self.enemigo.rect.topleft
                self.enemigo.rect.x += int(self.enemigo.velocidad * dx / distancia)
                self.enemigo.rect.y += int(self.enemigo.velocidad * dy / distancia)
                if not self.mapa.puede_moverse(self.enemigo.rect):
                    self.enemigo.rect.topleft = paso_anterior
                    self.ruta_patru = []
                self.enemigo.flip = dx < 0
        else:
            # Llegó al punto, avanzar al siguiente
            self.patru_index = (self.patru_index + 1) % len(self.puntos_patru)
            self.ruta_patru  = []

        return True

    def Actualizar(self):
        self.comportamiento.ejecutar()