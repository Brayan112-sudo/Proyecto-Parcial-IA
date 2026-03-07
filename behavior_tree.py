

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
    def __init__(self, enemigo, mapa, puntos_patru, tiempoAtacando=120, rango_deteccion=200):
        self.enemigo = enemigo
        self.mapa = mapa
        self.objetivo = None
        self.puntos_patru = puntos_patru
        self.patru_index = 0
        self.ruta_actual = []
        self.tiempoAtacando = tiempoAtacando
        self.rango_deteccion = rango_deteccion

        # Árbol de comportamiento
        self.comportamiento = Selector()

        # Secuencias
        self.secuenciaReposo = Secuencia()
        self.secuenciaAtaque = Secuencia()
        self.secuenciaPatrulla = Secuencia()

        # Agregar secuencias al selector
        self.comportamiento.agregar_hijo(self.secuenciaReposo)
        self.comportamiento.agregar_hijo(self.secuenciaAtaque)
        self.comportamiento.agregar_hijo(self.secuenciaPatrulla)

        # --- Reposo: cuando no hay objetivo ---
        hay_objetivo = Accion(lambda: self.objetivo is not None)
        self.secuenciaReposo.agregar_hijo(Invertir(hay_objetivo))
        self.secuenciaReposo.agregar_hijo(Accion(self.Reposo))

        # --- Ataque: si hay objetivo y está cerca ---
        self.secuenciaAtaque.agregar_hijo(Accion(self.objetivo_cerca))
        self.secuenciaAtaque.agregar_hijo(Accion(self.atacar))
        timer_ataque = Timer(tiempoAtacando)
        timer_ataque.agregar_hijo(Accion(self.Desactivar_objetivo))
        self.secuenciaAtaque.agregar_hijo(timer_ataque)

        # --- Patrulla ---
        self.secuenciaPatrulla.agregar_hijo(Accion(self.Patrullar))

    # ------------------ MÉTODOS ------------------

    def Agregar_objetivo(self, objetivo):
        self.objetivo = objetivo

    def Desactivar_objetivo(self):
        self.objetivo = None
        return True

    def objetivo_cerca(self):
        if self.objetivo:
            dx = self.objetivo.rect.centerx - self.enemigo.rect.centerx
            dy = self.objetivo.rect.centery - self.enemigo.rect.centery
            distancia = (dx**2 + dy**2)**0.5
            return distancia <= self.rango_deteccion
        return False

    def atacar(self):
        if self.objetivo:
            # Aquí puedes poner animación o lógica real de ataque
            print(f"{self.enemigo.nombre} atacando al jugador!")
        return True

    def Reposo(self):
        # Animación o lógica de espera
        # Ejemplo: enemigo se queda quieto
        return True

    def Patrullar(self):
        if not self.ruta_actual or self.enemigo.rect.topleft == self.ruta_actual[-1]:
            siguiente_punto = self.puntos_patru[self.patru_index]
            self.ruta_actual = (self.mapa, self.enemigo.rect.topleft, siguiente_punto)
            self.patru_index = (self.patru_index + 1) % len(self.puntos_patru)

        if self.ruta_actual:
            paso = self.ruta_actual[0]
            dx = paso[0] - self.enemigo.rect.x
            dy = paso[1] - self.enemigo.rect.y
            distancia = max(1, (dx**2 + dy**2)**0.5)
            self.enemigo.rect.x += int(self.enemigo.velocidad * dx / distancia)
            self.enemigo.rect.y += int(self.enemigo.velocidad * dy / distancia)

            if abs(dx) + abs(dy) < 1:
                self.ruta_actual.pop(0)
        return True

    def Actualizar(self):
        self.comportamiento.ejecutar()