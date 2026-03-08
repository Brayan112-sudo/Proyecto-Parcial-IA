import pygame
import random
import os


class mapa:
    def __init__(self, configuracion, cordenadas):
        self.configuracion = configuracion
        self.cordenadas = cordenadas
        self.tamano = len(configuracion)
        self.tamano_celda = 47

        # 0 = suelo       (transitable)
        # 1 = edificio    (Colisión)
        # 2 = árbol seco  (Colisión)
        # 3 = calle       (transitable)
        # 4 = ruinas      (Colisión)
        # "E" = meta      (transitable, roja)


        self.mapa = [
            [0, 0, 3, 3, 3, 0, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 0, 3, 3, 0, 0, 3, 3, 3, 0, 0, 3, 0],
            [0, 3, 3, 0, 0, 2, 3, 0, 3, 0, 1, 3, 0, 4, 3, 2, 0, 1, 3, 0, 2, 3, 1, 0, 3, 1, 0, 2, 0],
            [0, 0, 3, 4, 0, 1, 4, 3, 0, 3, 4, 0, 3, 0, 3, 0, 0, 4, 0, 3, 0, 1, 0, 3, 4, 0, 1, 0, 3],
            [3, 3, 3, 0, 2, 0, 3, 3, 2, 3, 0, 0, 3, 3, 2, 3, 0, 3, 2, 0, 3, 3, 2, 3, 3, 0, 3, 3, 0],
            [3, 0, 2, 0, 1, 0, 4, 0, 2, 3, 3, 0, 0, 0, 2, 3, 3, 0, 1, 0, 2, 0, 1, 3, 0, 0, 2, 0, 3],
            [0, 3, 0, 2, 0, 2, 0, 1, 3, 0, 4, 0, 3, 3, 4, 0, 3, 2, 0, 3, 0, 2, 0, 0, 3, 3, 0, 2, 0],
            [3, 3, 0, 0, 4, 0, 0, 3, 0, 0, 3, 3, 0, 0, 4, 3, 0, 0, 3, 0, 4, 3, 1, 0, 4, 0, 3, 1, 0],
            [0, 3, 4, 0, 0, 1, 3, 4, 3, 3, 0, 4, 3, 0, 1, 3, 0, 3, 0, 4, 0, 1, 3, 4, 3, 0, 0, 4, 0],
            [0, 0, 3, 0, 0, 0, 3, 3, 0, 3, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 3, 3, 0, 3, 0, 3, 0, 0, 3],
            [3, 0, 1, 2, 0, 3, 1, 0, 3, 0, 1, 0, 4, 0, 3, 1, 0, 3, 1, 0, 0, 3, 1, 0, 3, 0, 4, 3, 0],
            [0, 3, 3, 0, 1, 0, 3, 3, 1, 3, 3, 3, 0, 1, 0, 3, 3, 0, 3, 3, 1, 0, 3, 3, 0, 1, 0, 3, 3],
            [3, 1, 0, 3, 0, 2, 0, 1, 0, 3, 0, 0, 3, 0, 3, 0, 1, 2, 0, 1, 0, 3, 0, 1, 3, 0, 3, 0, 1],
            [0, 3, 3, 1, 0, 0, 3, 3, 4, 0, 3, 0, 0, 3, 1, 3, 0, 0, 3, 3, 4, 0, 3, 0, 0, 3, 1, 3, 0],
            [3, 0, 1, 0, 3, 3, 1, 0, 3, 3, 0, 3, 1, 0, 3, 0, 3, 3, 0, 1, 0, 3, 3, 1, 0, 3, 0, 0, 3],
            [0, 3, 0, 3, 0, 0, 3, 3, 0, 1, 3, 0, 3, 3, 0, 3, 1, 0, 3, 0, 3, 1, 0, 3, 3, 0, 3, 1, 0],
            [3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 0, 3, 0, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 0, "E"],
        ]

        self.ancho_mundo = len(self.mapa[0]) * self.tamano_celda
        self.alto_mundo  = len(self.mapa)    * self.tamano_celda

        self.BLOQUEANTES = {1, 2, 4}

        self._tiles = self._cargar_tiles()

    def _cargar_tiles(self):
        ruta = os.path.join("assets", "images", "tiles")
        nombres = {
            0: "suelo",
            1: "edificio",
            2: "arbol",
            3: "calle",
            4: "ruinas",
        }
        tiles = {}
        for tipo, nombre in nombres.items():
            path = os.path.join(ruta, f"{nombre}.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                tiles[tipo] = pygame.transform.scale(img, (self.tamano_celda, self.tamano_celda))
            else:
                fallback = pygame.Surface((self.tamano_celda, self.tamano_celda))
                colores_fallback = {
                    0: (101, 67, 33),
                    1: (60, 60, 60),
                    2: (120, 100, 60),
                    3: (40, 40, 40),
                    4: (90, 80, 70),
                }
                fallback.fill(colores_fallback.get(tipo, (100, 100, 100)))
                tiles[tipo] = fallback


        # Tile de meta

        meta = pygame.Surface((self.tamano_celda, self.tamano_celda))
        meta.fill((180, 20, 20))
        pygame.draw.rect(meta, (220, 40, 40), (4, 4, self.tamano_celda - 8, self.tamano_celda - 8))
        font = pygame.font.SysFont(None, 24)
        texto = font.render("META", True, (255, 255, 255))
        meta.blit(texto, (self.tamano_celda // 2 - texto.get_width() // 2,
                          self.tamano_celda // 2 - texto.get_height() // 2))
        pygame.draw.rect(meta, (255, 80, 80), (0, 0, self.tamano_celda, self.tamano_celda), 3)
        tiles["E"] = meta

        return tiles

    def dibujar(self, ventana):
        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):
                x = columna * self.tamano_celda
                y = fila    * self.tamano_celda
                tipo = self.mapa[fila][columna]

                tile = self._tiles.get(tipo)
                if tile:
                    ventana.blit(tile, (x, y))

                if tipo == "E":
                    pulso = abs((pygame.time.get_ticks() % 1000) - 500) / 500
                    alpha = int(60 + pulso * 120)
                    brillo = pygame.Surface((self.tamano_celda, self.tamano_celda), pygame.SRCALPHA)
                    brillo.fill((255, 100, 100, alpha))
                    ventana.blit(brillo, (x, y))

    def puede_moverse(self, rect):
        puntos = [
            (rect.left  + 2, rect.top    + 2),
            (rect.right - 2, rect.top    + 2),
            (rect.left  + 2, rect.bottom - 2),
            (rect.right - 2, rect.bottom - 2),
        ]
        for px, py in puntos:
            columna = px // self.tamano_celda
            fila    = py // self.tamano_celda
            if fila < 0 or fila >= len(self.mapa):
                return False
            if columna < 0 or columna >= len(self.mapa[0]):
                return False
            if self.mapa[fila][columna] in self.BLOQUEANTES:
                return False
        return True

    def jugador_llego_a_meta(self, rect):
        columna = rect.centerx // self.tamano_celda
        fila    = rect.centery // self.tamano_celda
        if 0 <= fila < len(self.mapa) and 0 <= columna < len(self.mapa[0]):
            return self.mapa[fila][columna] == "E"
        return False

    def GenerarSucesores(self):
        sucesores = []
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x = self.cordenadas[0] + dx
            y = self.cordenadas[1] + dy
            if 0 <= x < self.tamano and 0 <= y < self.tamano:
                if self.configuracion[x][y] not in (1, 2, 4):
                    nueva = self.configuracion.copy()
                    sucesores.append(mapa(nueva, [x, y]))
        return sucesores

    def __eq__(self, otro):
        if isinstance(otro, mapa):
            return self.cordenadas == otro.cordenadas
        return self.cordenadas == otro

    def __hash__(self):
        return hash(str(self.cordenadas))

    def __str__(self):
        resultado = ""
        for i, fila in enumerate(self.configuracion):
            for j, elem in enumerate(fila):
                if i == self.cordenadas[0] and j == self.cordenadas[1] and elem not in ("E","S"):
                    resultado += "* "
                else:
                    resultado += str(elem) + " "
            resultado += "\n"
        return resultado

    def Costo(self, estado_final):
        return (abs(self.cordenadas[0] - estado_final.cordenadas[0]) +
                abs(self.cordenadas[1] - estado_final.cordenadas[1]))


# Generar mundo

def generar_mundo(n):
    mapa_datos = [[0 for _ in range(n)] for _ in range(n)]
    mapa_datos[0][0] = "S"

    destino = [random.randint(1, n-1), random.randint(1, n-1)]
    mapa_datos[destino[0]][destino[1]] = "E"

    for i in range(n):
        for j in range(n):
            if mapa_datos[i][j] in ("S", "E"):
                continue
            if random.random() < 0.1:
                mapa_datos[i][j] = 1

    return mapa_datos, destino