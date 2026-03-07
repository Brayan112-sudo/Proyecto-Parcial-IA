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

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        # Devuelve True si algún hijo devuelve True
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False


class Secuencia(Nodo):
    def __init__(self, hijos):
        super().__init__()
        self.hijos = hijos

    def ejecutar(self):
        # Devuelve False si algún hijo devuelve False
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True


class Accion(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

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
            self.hijos[0].ejecutar()
            return True


class Guardia:

    def __init__(self, nombre, tiempoAtacando):

        self.nombre = nombre
        self.objetivo = None

        self.comportamiento = Selector([])       # Selector vacío
        secuenciaAtaque = Secuencia([])          # Secuencia de ataque vacía
        secuenciaPatrulla = Secuencia([])        # Secuencia de patrulla vacía

        self.comportamiento.agregar_hijo(secuenciaAtaque)
        self.comportamiento.agregar_hijo(secuenciaPatrulla)

        hay_objetivo = Accion(lambda: self.objetivo is not None)

        # ATAQUE
        secuenciaAtaque.agregar_hijo(hay_objetivo)
        secuenciaAtaque.agregar_hijo(Accion(self.objetivo_cerca))
        secuenciaAtaque.agregar_hijo(Accion(self.atacar))

        temporizador = Timer(tiempoAtacando)
        temporizador.agregar_hijo(Accion(self.Desactivar_objetivo))

        secuenciaAtaque.agregar_hijo(temporizador)

        # PATRULLA
        secuenciaPatrulla.agregar_hijo(Invertir(hay_objetivo))
        secuenciaPatrulla.agregar_hijo(Accion(self.Patrullar))

    # =====================
    # ACCIONES
    # =====================

    def Agregar_objetivo(self, objetivo):
        self.objetivo = objetivo
        print(self.nombre + ": Objetivo agregado " + objetivo)

    def Desactivar_objetivo(self):
        print(self.nombre + ": Objetivo desactivado")
        self.objetivo = None
        return True

    def objetivo_cerca(self):
        if self.objetivo is not None:
            print(self.nombre + ": Objetivo cerca")
            return True
        return False

    def atacar(self):
        if self.objetivo is not None:
            print(self.nombre + ": Atacando a " + self.objetivo)
            return True
        return False

    def Patrullar(self):
        print(self.nombre + ": Patrullando")
        return True

    def Actualizar(self):
        self.comportamiento.ejecutar()


# Crear dos Greñas

Grena1 = Guardia("Greñas 1", 3)
Grena2 = Guardia("Greñas 2", 3)


print("Sin objetivo")

Grena1.Actualizar()
Grena2.Actualizar()


print("Agregar objetivo")

Grena1.Agregar_objetivo("Jugador")
Grena2.Agregar_objetivo("Jugador")


print("Actualizando")

for i in range(8):

    print("Ciclo:", i+1)

    Grena1.Actualizar()
    Grena2.Actualizar()