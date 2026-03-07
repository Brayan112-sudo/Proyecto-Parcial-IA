import pygame;
import random;


# Clase mapa
class mapa:
    def __init__(self,configuracion,cordenadas):
        self.configuracion = configuracion
        self.cordenadas = cordenadas
        self.tamano = len(configuracion)

        self.tamano_celda = 90

        # 0 = suelo
        # 1 = edificio destruido
        # 2 = árbol seco
        # 3 = calle
        # 4 = ruinas

        self.mapa = [
        [0,0,3,3,3,0,3,3,3,0],
        [1,1,3,3,3,1,1,3,3,1],
        [1,4,3,0,0,3,4,3,0,1],
        [3,3,3,0,2,0,3,3,3,3],
        [3,0,0,0,0,0,0,0,0,3],
        [1,3,0,2,0,2,0,3,1,3],
        [1,3,0,0,4,0,0,3,1,3],
        [3,3,3,0,0,0,3,3,3,3],
        [1,4,3,0,2,0,3,4,0,1]
        ]

        self.ancho_mundo = len(self.mapa[0]) * self.tamano_celda
        self.alto_mundo = len(self.mapa) * self.tamano_celda

    def dibujar(self, ventana):
        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):

                x = columna * self.tamano_celda
                y = fila * self.tamano_celda

                tipo = self.mapa[fila][columna]

                # Suelo marrón sucio
                if tipo == 0:
                    color = (101, 67, 33)

                # Edificio destruido
                elif tipo == 1:
                    color = (60, 60, 60)

                # Inicio
                elif tipo == "S":
                    color = (0, 200, 0)

                # Destino
                elif tipo == "E":
                    color = (200, 0, 0)

                # Árbol seco
                elif tipo == 2:
                    color = (120, 100, 60)

                # Calle
                elif tipo == 3:
                    color = (40, 40, 40)

                # Ruinas
                elif tipo == 4:
                    color = (90, 80, 70)

                pygame.draw.rect(ventana, color, (x, y, self.tamano_celda, self.tamano_celda))


                # Detalles visuales
        if tipo == 1:
            pygame.draw.rect(ventana, (30,30,30), (x+10,y+10,20,20))
            pygame.draw.rect(ventana, (20,20,20), (x+40,y+40,20,20))

        if tipo == 2:
            pygame.draw.line(ventana,(80,60,40),(x+40,y+20),(x+40,y+60),4)
            pygame.draw.line(ventana,(80,60,40),(x+40,y+30),(x+25,y+45),3)
            pygame.draw.line(ventana,(80,60,40),(x+40,y+30),(x+55,y+45),3)

        if tipo == 4:
            pygame.draw.circle(ventana,(70,70,70),(x+20,y+40),10)
            pygame.draw.circle(ventana,(70,70,70),(x+50,y+30),8)


    def puede_moverse(self, rect):

        columna = rect.centerx // self.tamano_celda
        fila = rect.centery // self.tamano_celda

        if fila < 0 or fila >= len(self.mapa):
            return False
        if columna < 0 or columna >= len(self.mapa[0]):
            return False

        tipo = self.mapa[fila][columna]

        # Bloques que NO se pueden atravesar
        if tipo == 1 or tipo == 2 or tipo == 4:
            return False

        return True


    def GenerarSucesores(self):
            sucesores = []
            movimientos_validos = [[0,1],[1,0],[0,-1],[-1,0]]

            for movimiento in movimientos_validos:
                x = self.cordenadas [0] + movimiento [0]
                y = self.cordenadas [1] + movimiento [1]

                if x>=0 and x<self.tamano and y>=0 and y<self.tamano:
                    if self.configuracion[x][y]!=1:
                        nueva_configuracion=self.configuracion.copy()
                        sucesores.append(mapa(nueva_configuracion,[x,y]))
                    
            return sucesores
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, mapa):
            return self.cordenadas==__o.cordenadas
        return self.cordenadas==__o

    def __hash__(self) -> int:
        return hash(str(self.configuracion))

    def __str__(self):
        mapa_string = ""

        for i, fila in enumerate(self.configuracion):
            for j, elemento in enumerate(fila):
                if i == self.cordenadas[0] and j == self.cordenadas[1] and elemento != "E" and elemento != "S":

                    mapa_string += "* "
                else:
                    mapa_string += str(elemento) + " "
            mapa_string += "\n"
        return mapa_string

    def Costo(self,estado_final):
        return abs(self.cordenadas[0]-estado_final.cordenadas[0]) + \
               abs(self.cordenadas[1]-estado_final.cordenadas[1])


# =========================
# GENERAR MUNDO
# =========================

def generar_mundo(n):
    mapa = [[0 for _ in range(n)] for _ in range(n)]
    mapa[0][0] = "S"

    destino = [random.randint(1, n-1), random.randint(1, n-1)]
    mapa[destino[0]][destino[1]] = "E"

    for i in range(n):
        for j in range(n):
            if mapa[i][j] in ["S", "E"]:
                continue
            if i ==destino[0] and j == destino[1]:
                continue
            if random.random() < 0.1:
                mapa[i][j] = 1

    return mapa, destino