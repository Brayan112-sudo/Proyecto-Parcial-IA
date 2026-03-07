import heapq;
import time;


class NodoA:
    def __init__(self, estado, padre=None, g=0, h=0):
        self.estado = estado
        self.padre = padre
        self.g = g  # costo desde inicio
        self.h = h  # heurística hasta objetivo
        self.f = g + h  # costo total estimado

    def __lt__(self, otro):
        return self.f < otro.f

def Astar(estado_inicial, estado_final):
    abiertos = []
    visitados = set()

    # Nodo inicial: g = 0, h = heurística hacia el objetivo
    nodo_inicial = NodoA(estado_inicial, None, g=0, h=estado_inicial.Costo(estado_final))
    heapq.heappush(abiertos, nodo_inicial)

    total_nodos = 1
    inicio = time.perf_counter()

    while abiertos:
        nodo_actual = heapq.heappop(abiertos)

        # Si llegamos al objetivo
        if nodo_actual.estado == estado_final:
            break

        visitados.add(nodo_actual.estado)

        # Generar sucesores
        sucesores = nodo_actual.estado.GenerarSucesores()
        total_nodos += len(sucesores)

        for sucesor in sucesores:
            if sucesor in visitados:
                continue

            g_sucesor = nodo_actual.g + 1  # o el costo de moverse a ese sucesor
            h_sucesor = sucesor.Costo(estado_final)
            nuevo_nodo = NodoA(sucesor, nodo_actual, g=g_sucesor, h=h_sucesor)
            heapq.heappush(abiertos, nuevo_nodo)

    # Reconstruir camino
    camino = []
    while nodo_actual:
        camino.append(nodo_actual.estado)
        nodo_actual = nodo_actual.padre

    camino.reverse()
    fin = time.perf_counter()

    return camino, total_nodos, fin - inicio