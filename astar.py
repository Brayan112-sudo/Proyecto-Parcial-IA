import heapq;
import time;

class NodoA:
    def __init__(self, estado, padre = None):
        self.estado = estado
        self.padre = padre

def Astar(estado_inicial, estado_final):

    abiertos = []
    visitados = set()

    nodo_actual = NodoA (estado_inicial, None, estado_inicial.Costo(estado_final))

    heapq.heappush (abiertos, nodo_actual)

    total = 1
    inicio = time.perf_counter()

    while abiertos:

        nodo_actual = heapq.heappop (abiertos)

        if nodo_actual.estado == estado_final:
            break

        visitados.add (nodo_actual.estado)

        sucesores = nodo_actual.estado.GenerarSucesores()

        total += len (sucesores)

        for sucesor in sucesores:

            if sucesor in visitados:
                continue

            nuevo = NodoA (sucesor, nodo_actual, sucesor.Costo(estado_final))

            heapq.heappush (abiertos, nuevo)

    # Reconstruir camino
    camino = []

    while nodo_actual:
        camino.append(nodo_actual.estado)
        nodo_actual = nodo_actual.padre

    camino.reverse()

    fin = time.perf_counter()

    return camino, total, fin - inicio