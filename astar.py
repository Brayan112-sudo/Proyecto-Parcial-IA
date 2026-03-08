import heapq


TAMANO_CELDA = 47


class Estado:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def heuristica(self, otro):
        return abs(self.x - otro.x) + abs(self.y - otro.y)

    def GenerarSucesores(self):
        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return [Estado(self.x + dx, self.y + dy) for dx, dy in movimientos]

    def __eq__(self, otro):
        return self.x == otro.x and self.y == otro.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, otro):
        return False


class NodoA:
    def __init__(self, estado, padre=None, g=0, h=0):
        self.estado = estado
        self.padre = padre
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, otro):
        return self.f < otro.f


class Astar:
    def __init__(self, inicio, final, mapa=None, tam_celda=TAMANO_CELDA):
        self.inicio = inicio
        self.final = final
        self.mapa = mapa
        self.tam_celda = tam_celda

    def _es_valido(self, estado):
        if self.mapa is None:
            return True
        import pygame
        rect_prueba = pygame.Rect(
            estado.x * self.tam_celda + 2,
            estado.y * self.tam_celda + 2,
            self.tam_celda - 4,
            self.tam_celda - 4
        )
        return self.mapa.puede_moverse(rect_prueba)

    def buscar(self, limite_nodos=800):
        abiertos = []
        visitados = set()

        nodo_inicial = NodoA(self.inicio, None, g=0, h=self.inicio.heuristica(self.final))
        heapq.heappush(abiertos, nodo_inicial)
        visitados.add(self.inicio)

        nodo_final = None
        nodos_explorados = 0

        while abiertos:
            nodo_actual = heapq.heappop(abiertos)
            nodos_explorados += 1

            if nodos_explorados > limite_nodos:
                nodo_final = nodo_actual
                break

            if nodo_actual.estado == self.final:
                nodo_final = nodo_actual
                break

            for sucesor in nodo_actual.estado.GenerarSucesores():
                if sucesor in visitados:
                    continue
                if not self._es_valido(sucesor):
                    visitados.add(sucesor)
                    continue
                visitados.add(sucesor)
                g = nodo_actual.g + 1
                h = sucesor.heuristica(self.final)
                heapq.heappush(abiertos, NodoA(sucesor, nodo_actual, g, h))

        if nodo_final is None:
            return []

        camino = []
        nodo = nodo_final
        while nodo:
            px = nodo.estado.x * self.tam_celda + self.tam_celda // 2
            py = nodo.estado.y * self.tam_celda + self.tam_celda // 2
            camino.append((px, py))
            nodo = nodo.padre

        camino.reverse()
        return camino