import pygame
import random
from jugador import jugador
from mapa import mapa, generar_mundo
from enemigos import enemigo
from behavior_tree import Guardia

pygame.init()
pygame.mixer.init()

def escalar_img(image, width, height):
    return pygame.transform.scale(image, (width, height))

fps = 60

ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ancho = ventana.get_width()
alto  = ventana.get_height()


pygame.display.set_caption("Sobrevive a los enemigos")

reloj = pygame.time.Clock()


# Cargar animaciones

animaciones_grenas = []
for i in range(4):
    img = pygame.image.load(f"assets//images//characters//enemies//grenas//Grenas_{i}.png").convert_alpha()
    img = escalar_img(img, 35, 45)
    animaciones_grenas.append(img)


animaciones_jugador = []
for i in range(8):
    img = pygame.image.load(f"assets//images//characters//player//Personaje_{i}.png").convert_alpha()
    img = escalar_img(img, 35, 45)
    animaciones_jugador.append(img)


# Cargar sonidos globales

musica_fondo     = "assets/sounds/musica_motivacion_game.wav"
sonido_meta      = pygame.mixer.Sound("assets/sounds/meta.wav")
sonido_pasos_z   = pygame.mixer.Sound("assets/sounds/pasos_zombie.wav")
sonido_gruñido_z = pygame.mixer.Sound("assets/sounds/gruñido_zombie1.wav")
sonido_ataque_z  = pygame.mixer.Sound("assets/sounds/ataque_zombie.wav")

sonido_meta.set_volume(1.0)
sonido_pasos_z.set_volume(0.4)
sonido_gruñido_z.set_volume(0.6)
sonido_ataque_z.set_volume(0.8)


# Temporizadores de sonido para enemigos compartidos

tiempo_ultimo_paso_z   = 0
tiempo_ultimo_gruñido  = 0
intervalo_pasos_z      = 400   # ms
intervalo_gruñido      = 3000  # ms


pantalla_completa = True
meta_sonada       = False   # El sonido de meta suena una vez


# Estados del juego

ESTADO_MENU     = "menu"
ESTADO_JUGANDO  = "jugando"
ESTADO_GANASTE  = "ganaste"
ESTADO_PERDISTE = "perdiste"


# Función para iniciar música de fondo

def iniciar_musica():
    pygame.mixer.music.load(musica_fondo)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # -1 = loop infinito


def detener_musica():
    pygame.mixer.music.stop()


# Función nueva
def spawn_enemigos(posiciones, animaciones, mapa_obj, jugador_obj, puntos_patru):

    guardias = []
    for (x, y) in posiciones:
        en = enemigo(x, y, animaciones, mapa_obj)
        en.jugador = jugador_obj
        g = Guardia(en, mapa_obj, puntos_patru)
        g.Agregar_objetivo(jugador_obj)
        guardias.append(g)
    return guardias


# Función para crear una partida nueva

def nueva_partida():
    global meta_sonada, tiempo_ultimo_paso_z, tiempo_ultimo_gruñido
    meta_sonada             = False
    tiempo_ultimo_paso_z    = 0
    tiempo_ultimo_gruñido   = 0

    mapa_datos, destino = generar_mundo(10)
    mapa_obj = mapa(mapa_datos, [0, 0])

    jugador_obj = jugador(x=23, y=23, image=animaciones_jugador[0], animaciones=animaciones_jugador)

    puntos_patru = [(70, 164), (305, 164), (305, 352), (70, 352)]

    # Agrega o quita posiciones aquí para tener más o menos enemigos ──
    posiciones_enemigos = [
        (446, 305),
        (540, 164),
        (164, 352),
        (150, 250),
        (300, 450),
        (550, 425),
        (370, 600),
        (260, 650),
    ]

    guardias = spawn_enemigos(posiciones_enemigos, animaciones_grenas, mapa_obj, jugador_obj, puntos_patru)

    # Cambia este número para ajustar la velocidad de todos los enemigos ──
    for g in guardias:
        g.enemigo.velocidad = 4

    return mapa_obj, jugador_obj, guardias


# Botón reutilizable

class Boton:
    def __init__(self, texto, x, y, w, h, color, color_hover, color_texto=(255,255,255)):
        self.texto       = texto
        self.rect        = pygame.Rect(x, y, w, h)
        self.color       = color
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.font        = pygame.font.SysFont("consolas", 28, bold=True)

    def dibujar(self, ventana):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)
        color_actual = self.color_hover if hover else self.color

        sombra = self.rect.move(4, 4)
        pygame.draw.rect(ventana, (10, 10, 10), sombra, border_radius=8)
        pygame.draw.rect(ventana, color_actual, self.rect, border_radius=8)
        pygame.draw.rect(ventana, (255, 255, 255, 80), self.rect, 2, border_radius=8)
        texto_surf = self.font.render(self.texto, True, self.color_texto)
        ventana.blit(texto_surf, (
            self.rect.centerx - texto_surf.get_width()  // 2,
            self.rect.centery - texto_surf.get_height() // 2
        ))

    def fue_clickeado(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


# Dibujar fondo de menú

def dibujar_fondo_menu(ventana, ancho, alto, titulo, subtitulo="", color_titulo=(220,50,50)):
    ventana.fill((15, 15, 20))
    for i in range(0, alto, 4):
        pygame.draw.rect(ventana, (30, 25, 20), (0, i, ancho, 2))
    for x in range(0, ancho, 60):
        pygame.draw.line(ventana, (30, 30, 35), (x, 0), (x, alto), 1)
    for y in range(0, alto, 60):
        pygame.draw.line(ventana, (30, 30, 35), (0, y), (ancho, y), 1)

    font_titulo = pygame.font.SysFont("consolas", 72, bold=True)
    font_sub    = pygame.font.SysFont("consolas", 28)

    titulo_surf = font_titulo.render(titulo, True, color_titulo)
    sombra_surf = font_titulo.render(titulo, True, (80, 10, 10))
    ventana.blit(sombra_surf, (ancho // 2 - titulo_surf.get_width() // 2 + 4, alto // 4 + 4))
    ventana.blit(titulo_surf, (ancho // 2 - titulo_surf.get_width() // 2,     alto // 4))

    if subtitulo:
        sub_surf = font_sub.render(subtitulo, True, (180, 180, 180))
        ventana.blit(sub_surf, (ancho // 2 - sub_surf.get_width() // 2, alto // 4 + 85))


# Crear botones

def crear_botones_menu(ancho, alto):
    bw, bh = 280, 55
    cx = ancho // 2 - bw // 2
    btn_iniciar = Boton(" INICIAR", cx, alto // 2,      bw, bh, (180,30,30), (220,60,60))
    btn_salir   = Boton(" SALIR",   cx, alto // 2 + 75, bw, bh, (50,50,60),  (80,80,95))
    return btn_iniciar, btn_salir

def crear_botones_fin(ancho, alto):
    bw, bh = 280, 55
    cx = ancho // 2 - bw // 2
    btn_reiniciar = Boton(" REINICIAR", cx, alto // 2 + 20, bw, bh, (180,30,30), (220,60,60))
    btn_menu      = Boton(" MENÚ",      cx, alto // 2 + 95, bw, bh, (50,50,60),  (80,80,95))
    return btn_reiniciar, btn_menu


# Estado inicial

estado = ESTADO_MENU
mapa_obj, jugador_obj, guardias = None, None, []
meta_sonada = False
tiempo_ultimo_paso_z  = 0
tiempo_ultimo_gruñido = 0

btn_iniciar, btn_salir      = crear_botones_menu(ancho, alto)
btn_reiniciar, btn_menu_fin = crear_botones_fin(ancho, alto)

iniciar_musica()

run = True
while run:

    reloj.tick(fps)


    # Menú principal

    if estado == ESTADO_MENU:
        dibujar_fondo_menu(ventana, ancho, alto, "SOBREVIVE", "Llega a la META sin que te atrapen")
        btn_iniciar.dibujar(ventana)
        btn_salir.dibujar(ventana)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False
            if btn_iniciar.fue_clickeado(event):
                mapa_obj, jugador_obj, guardias = nueva_partida()
                estado = ESTADO_JUGANDO
            if btn_salir.fue_clickeado(event):
                run = False


    # Jugando

    elif estado == ESTADO_JUGANDO:
        ventana.fill((30, 30, 30))
        mapa_obj.dibujar(ventana)

        teclas = pygame.key.get_pressed()
        delta_x = 0
        delta_y = 0

        if teclas[pygame.K_w]: delta_y = -3
        if teclas[pygame.K_s]: delta_y =  3
        if teclas[pygame.K_a]: delta_x = -3
        if teclas[pygame.K_d]: delta_x =  3

        jugador_obj.movimiento(delta_x, delta_y, ancho, alto, mapa_obj)
        jugador_obj.update()
        jugador_obj.dibujar(ventana)
        jugador_obj.dibujar_barra_vida(ventana)  # Barra de vida


        # Meta

        if mapa_obj.jugador_llego_a_meta(jugador_obj.rect):
            if not meta_sonada:
                sonido_meta.play()
                meta_sonada = True
            estado = ESTADO_GANASTE


        # Sonidos de enemigos para todos

        ahora = pygame.time.get_ticks()

        enemigos_activos = [g.enemigo for g in guardias]
        hay_enemigo_cerca = any(
            abs(e.rect.x - jugador_obj.rect.x) < 200 and
            abs(e.rect.y - jugador_obj.rect.y) < 200
            for e in enemigos_activos
        )

        # Pasos zombie

        if ahora - tiempo_ultimo_paso_z >= intervalo_pasos_z:
            sonido_pasos_z.play()
            tiempo_ultimo_paso_z = ahora


        # Gruñido zombie

        if hay_enemigo_cerca and ahora - tiempo_ultimo_gruñido >= intervalo_gruñido:
            sonido_gruñido_z.play()
            tiempo_ultimo_gruñido = ahora


        # Guardias

        for guardia in guardias:
            guardia.arbol.ejecutar()
            guardia.enemigo.update_animacion()
            guardia.enemigo.dibujar(ventana)

            if guardia.enemigo.rect.colliderect(jugador_obj.rect):
                sonido_ataque_z.play()          # sonido de ataque al golpear
                jugador_obj.recibir_daño(10)
                if jugador_obj.vida <= 0:
                    estado = ESTADO_PERDISTE


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pantalla_completa = not pantalla_completa
                    if pantalla_completa:
                        ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        ventana = pygame.display.set_mode((800, 700))
                    ancho = ventana.get_width()
                    alto  = ventana.get_height()
                    btn_iniciar,   btn_salir    = crear_botones_menu(ancho, alto)
                    btn_reiniciar, btn_menu_fin = crear_botones_fin(ancho, alto)

    # Ganaste

    elif estado == ESTADO_GANASTE:
        dibujar_fondo_menu(ventana, ancho, alto, "¡GANASTE!", "Llegaste a la META", color_titulo=(50,200,80))
        btn_reiniciar.dibujar(ventana)
        btn_menu_fin.dibujar(ventana)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if btn_reiniciar.fue_clickeado(event):
                mapa_obj, jugador_obj, guardias = nueva_partida()
                estado = ESTADO_JUGANDO
            if btn_menu_fin.fue_clickeado(event):
                estado = ESTADO_MENU

    # Perdiste

    elif estado == ESTADO_PERDISTE:
        dibujar_fondo_menu(ventana, ancho, alto, "¡PERDISTE!", "Un enemigo te atrapó", color_titulo=(200,50,50))
        btn_reiniciar.dibujar(ventana)
        btn_menu_fin.dibujar(ventana)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if btn_reiniciar.fue_clickeado(event):
                mapa_obj, jugador_obj, guardias = nueva_partida()
                estado = ESTADO_JUGANDO
            if btn_menu_fin.fue_clickeado(event):
                estado = ESTADO_MENU

    pygame.display.update()


pygame.quit()