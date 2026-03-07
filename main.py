import pygame;
import random;
from jugador import jugador;
from mapa import mapa, generar_mundo
from enemigos import enemigo;

pygame.init()

# Función para escalar la imagen del enemigo
def escalar_img(image, width, height):
    return pygame.transform.scale(image, (width, height))

# Configuración
ancho = 800
alto = 700
fps = 60


# Crear la ventana del juego
ventana = pygame.display.set_mode((ancho, alto))


# GENERAR MAPA

mapa_datos, destino = generar_mundo(10)
mapa = mapa(mapa_datos, [0,0])

pygame.display.set_caption("Sobrevive a los enemigos")


# --- AQUÍ VA EL BLOQUE DE PRUEBA DE GREÑAS ---
from behavior_tree import Guardia  # asegúrate de importar la clase

# Crear dos Greñas
Grena1 = Guardia("Greñas 1", 3)
Grena2 = Guardia("Greñas 2", 3)

print("Sin objetivo")
Grena1.Actualizar()
Grena2.Actualizar()

print("Agregar objetivo")
Grena1.Agregar_objetivo("Jugador")  # o tu objeto jugador real
Grena2.Agregar_objetivo("Jugador")

print("Actualizando")
for i in range(8):
    print("Ciclo:", i+1)
    Grena1.Actualizar()
    Grena2.Actualizar()

# Animaciones del enemigo
animaciones_grenas = []
for i in range(4):
    img = pygame.image.load(f"assets//images//characters//enemies//greñas//Greñas_{i}.png").convert_alpha()
    img = escalar_img(img, 35, 45)
    animaciones_grenas.append(img)

# Crear enemigos
enemigo1 = enemigo(500, 300, animaciones_grenas)
enemigo2 = enemigo(200, 150, animaciones_grenas)

enemigo1.jugador= jugador
enemigo2.jugador= jugador

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

       # Dibujar
       mapa.dibujar(ventana)

       # Dibujar enemigos
       enemigo1.dibujar(ventana)
       enemigo2.dibujar(ventana)

       # Dibujar jugador
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

       
       # Actualizar
       jugador.update()

       enemigo1.perseguir(jugador, mapa)
       enemigo2.perseguir(jugador, mapa)

       enemigo1.update()
       enemigo2.update()


       
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