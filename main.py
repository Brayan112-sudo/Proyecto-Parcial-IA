import pygame;
import random;
from jugador import jugador
from mapa import Mapa, generar_mundo

pygame.init()

# Configuración
ancho = 800
alto = 700
fps = 60


# Crear la ventana del juego
ventana = pygame.display.set_mode((ancho, alto))


# GENERAR MAPA

mapa_datos, destino = generar_mundo(10)
mapa = Mapa(mapa_datos, [0,0])

pygame.display.set_caption("Sobrevive a los enemigos")


# Controlar el frame rate
reloj = pygame.time.Clock()
    

    # Busqueda de ruta en el mapa

    # Generar mapa
def generar_mundo(n):
    mapa = [[0 for _ in range(n)] for _ in range(n)]
    mapa[0][0] = "S"

    destino=[ random.randint(1,n-1), random.randint(1,n-1)]
    mapa[destino[0]][destino[1]] = "E"

    for i in range(n):
        for j in range(n):
            if mapa[i][j] in ["S", "E"]:
                continue
            if i ==destino[0] and j == destino[1]:
                continue
            if random.random() < 0.2:
                mapa[i][j] = 1

    return mapa, destino


# Clase jugador-----------

def escalar_img(image, width, height):
      return pygame.transform.scale(image, (width, height))

animaciones = []
for i in range(8):
       img = pygame.image.load(f"assets//images//characters//player//Personaje_{i}.png").convert_alpha()
       img = escalar_img(img, 35, 45)
       animaciones.append(img)


# Crear jugador
jugador = jugador(x=20, y=10, image= animaciones[0], animaciones=animaciones)

# Ancho jugador
with_jugador = 35
height_jugador = 45


# Definir las variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False


# Loop principal
correr = True
while correr:
       

       # Que valla a 60 FPS
       reloj.tick(60)

       # Dibujar ventana
       ventana.fill((30, 30, 30))

        # Dibujar mapa
       mapa.dibujar(ventana)

        # Dibujar
       jugador.dibujar(ventana)


       # Calcular el movimiento del jugador
       delta_x = 0
       delta_y = 0

       teclas = pygame.key.get_pressed()

       if mover_derecha == True:
              delta_x = velocidad = 3
       if mover_izquierda == True:
              delta_x = velocidad = -3
       if mover_arriba == True:
              delta_y = velocidad = -3
       if mover_abajo == True:
              delta_y = velocidad = 3

        # Guardar posición anterior
       posicion_anterior = jugador.rect.copy()


       # Mover al jugador
       jugador.rect.x += delta_x
       jugador.rect.y += delta_y

       if not mapa.puede_moverse(jugador.rect):
        jugador.rect = posicion_anterior


       jugador.update()

       
       # Eventos
       for event in pygame.event.get():


              # Para cerrar el juego
              if event.type == pygame.QUIT:
                     correr = False

              if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_a:
                            mover_izquierda = True
                     if event.key == pygame.K_d:
                            mover_derecha = True
                     if event.key == pygame.K_w:
                            mover_arriba = True
                     if event.key == pygame.K_s:
                            mover_abajo = True


              # Para cuando se suelta la tecla
              if event.type == pygame.KEYUP:
                     if event.key == pygame.K_a:
                            mover_izquierda = False
                     if event.key == pygame.K_d:
                            mover_derecha = False
                     if event.key == pygame.K_w:
                            mover_arriba = False
                     if event.key == pygame.K_s:
                            mover_abajo = False

       pygame.display.update()


pygame.quit()