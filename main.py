import pygame;
import random;
from jugador import jugador;
from mapa import mapa, generar_mundo
from enemigos import enemigo;
from behavior_tree import Guardia;

pygame.init()

def escalar_img(image, width, height):
    return pygame.transform.scale(image, (width, height))

fps = 60

ventana = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
ancho = ventana.get_width()
alto  = ventana.get_height()

pygame.display.set_caption("Sobrevive a los enemigos")

from behavior_tree import Guardia

reloj = pygame.time.Clock()

# ── Cargar animaciones (una sola vez) ────────────────────────────────────────
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

pantalla_completa = True


# ── Estados del juego ────────────────────────────────────────────────────────
ESTADO_MENU    = "menu"
ESTADO_JUGANDO = "jugando"
ESTADO_GANASTE = "ganaste"
ESTADO_PERDISTE = "perdiste"


# ── Función para crear una partida nueva ─────────────────────────────────────
def nueva_partida():
    mapa_datos, destino = generar_mundo(10)
    mapa_obj = mapa(mapa_datos, [0, 0])

    jugador_obj = jugador(x=23, y=23, image=animaciones_jugador[0], animaciones=animaciones_jugador)

    en1 = enemigo(446, 305, animaciones_grenas, mapa_obj)
    en2 = enemigo(540, 164, animaciones_grenas, mapa_obj)
    en3 = enemigo(164, 352, animaciones_grenas, mapa_obj)

    puntos_patru = [(70, 164), (305, 164), (305, 352), (70, 352)]
    g1 = Guardia(en1, mapa_obj, puntos_patru)
    g2 = Guardia(en2, mapa_obj, puntos_patru)
    g3 = Guardia(en3, mapa_obj, puntos_patru)

    en1.jugador = jugador_obj
    en2.jugador = jugador_obj
    en3.jugador = jugador_obj
    g1.Agregar_objetivo(jugador_obj)
    g2.Agregar_objetivo(jugador_obj)
    g3.Agregar_objetivo(jugador_obj)

    return mapa_obj, jugador_obj, [g1, g2, g3]


# ── Botón reutilizable ────────────────────────────────────────────────────────
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

        # Sombra
        sombra = self.rect.move(4, 4)
        pygame.draw.rect(ventana, (10, 10, 10), sombra, border_radius=8)
        # Botón
        pygame.draw.rect(ventana, color_actual, self.rect, border_radius=8)
        # Borde
        pygame.draw.rect(ventana, (255, 255, 255, 80), self.rect, 2, border_radius=8)
        # Texto
        texto_surf = self.font.render(self.texto, True, self.color_texto)
        ventana.blit(texto_surf, (
            self.rect.centerx - texto_surf.get_width()  // 2,
            self.rect.centery - texto_surf.get_height() // 2
        ))

    def fue_clickeado(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


# ── Dibujar fondo de menú ─────────────────────────────────────────────────────
def dibujar_fondo_menu(ventana, ancho, alto, titulo, subtitulo="", color_titulo=(220,50,50)):
    # Fondo oscuro con gradiente simulado
    ventana.fill((15, 15, 20))
    for i in range(0, alto, 4):
        alpha = int(30 * (1 - i / alto))
        pygame.draw.rect(ventana, (30, 25, 20), (0, i, ancho, 2))

    # Líneas decorativas
    for x in range(0, ancho, 60):
        pygame.draw.line(ventana, (30, 30, 35), (x, 0), (x, alto), 1)
    for y in range(0, alto, 60):
        pygame.draw.line(ventana, (30, 30, 35), (0, y), (ancho, y), 1)

    # Título
    font_titulo = pygame.font.SysFont("consolas", 72, bold=True)
    font_sub    = pygame.font.SysFont("consolas", 28)

    titulo_surf = font_titulo.render(titulo, True, color_titulo)
    # Sombra del título
    sombra_surf = font_titulo.render(titulo, True, (80, 10, 10))
    ventana.blit(sombra_surf, (ancho // 2 - titulo_surf.get_width() // 2 + 4, alto // 4 + 4))
    ventana.blit(titulo_surf, (ancho // 2 - titulo_surf.get_width() // 2,     alto // 4))

    if subtitulo:
        sub_surf = font_sub.render(subtitulo, True, (180, 180, 180))
        ventana.blit(sub_surf, (ancho // 2 - sub_surf.get_width() // 2, alto // 4 + 85))


# ── Crear botones ─────────────────────────────────────────────────────────────
def crear_botones_menu(ancho, alto):
    bw, bh = 280, 55
    cx = ancho // 2 - bw // 2
    btn_iniciar   = Boton(" INICIAR",   cx, alto // 2,       bw, bh, (180,30,30), (220,60,60))
    btn_salir     = Boton(" SALIR",     cx, alto // 2 + 75,  bw, bh, (50,50,60),  (80,80,95))
    return btn_iniciar, btn_salir

def crear_botones_fin(ancho, alto):
    bw, bh = 280, 55
    cx = ancho // 2 - bw // 2
    btn_reiniciar = Boton(" REINICIAR", cx, alto // 2 + 20,  bw, bh, (180,30,30), (220,60,60))
    btn_menu      = Boton(" MENÚ",      cx, alto // 2 + 95,  bw, bh, (50,50,60),  (80,80,95))
    return btn_reiniciar, btn_menu


# ── Estado inicial ────────────────────────────────────────────────────────────
estado = ESTADO_MENU
mapa_obj, jugador_obj, guardias = None, None, []

btn_iniciar, btn_salir         = crear_botones_menu(ancho, alto)
btn_reiniciar, btn_menu_fin    = crear_botones_fin(ancho, alto)

run = True
while run:

    reloj.tick(fps)

    # ── MENÚ PRINCIPAL ────────────────────────────────────────────────────────
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

    # ── JUGANDO ───────────────────────────────────────────────────────────────
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

        if mapa_obj.jugador_llego_a_meta(jugador_obj.rect):
            estado = ESTADO_GANASTE

        for guardia in guardias:
            guardia.arbol.ejecutar()
            guardia.enemigo.update_animacion()
            guardia.enemigo.dibujar(ventana)

            if guardia.enemigo.rect.colliderect(jugador_obj.rect):
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
                    btn_iniciar,  btn_salir    = crear_botones_menu(ancho, alto)
                    btn_reiniciar, btn_menu_fin = crear_botones_fin(ancho, alto)

    # ── GANASTE ───────────────────────────────────────────────────────────────
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

    # ── PERDISTE ──────────────────────────────────────────────────────────────
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