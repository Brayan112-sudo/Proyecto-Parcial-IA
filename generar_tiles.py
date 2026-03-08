import pygame
import os
import random

pygame.init()
TILE = 90
OUT = "assets/images/tiles"
os.makedirs(OUT, exist_ok=True)

def guardar(surface, nombre):
    pygame.image.save(surface, f"{OUT}/{nombre}.png")
    print(f"  Guardado: {nombre}.png")

def ruido_px(seed, i, j, escala=8):
    random.seed(seed + i * 73 + j * 37)
    return random.randint(-escala, escala)


# Suelo tipo 0

def tile_suelo():
    s = pygame.Surface((TILE, TILE))
    base = (52, 48, 42)
    s.fill(base)
    for i in range(TILE):
        for j in range(TILE):
            v = ruido_px(1, i // 4, j // 4, 10)
            c = tuple(max(0, min(255, base[k] + v)) for k in range(3))
            s.set_at((i, j), c)
    random.seed(42)
    for _ in range(4):
        x1 = random.randint(5, TILE-5)
        y1 = random.randint(5, TILE-5)
        x2 = x1 + random.randint(-20, 20)
        y2 = y1 + random.randint(10, 30)
        pygame.draw.line(s, (30, 28, 25), (x1, y1), (x2, y2), 1)
    return s


# Edificio destruido tipo 1 — colisión

def tile_edificio():
    s = pygame.Surface((TILE, TILE))
    s.fill((55, 52, 48))
    colores = [(72, 68, 62), (60, 57, 52), (80, 75, 68), (50, 48, 44)]
    random.seed(7)
    for row in range(3):
        for col in range(3):
            cx = col * 28 + 5
            cy = row * 25 + 5
            w  = random.randint(20, 26)
            h  = random.randint(18, 22)
            color = random.choice(colores)
            pygame.draw.rect(s, color, (cx, cy, w, h))
            pygame.draw.rect(s, (35, 33, 30), (cx, cy, w, h), 1)
    random.seed(13)
    for _ in range(3):
        wx = random.randint(8, TILE-20)
        wy = random.randint(8, TILE-20)
        pygame.draw.rect(s, (20, 25, 30), (wx, wy, 10, 8))
        pygame.draw.line(s, (80, 90, 100), (wx, wy), (wx+10, wy+8), 1)
        pygame.draw.line(s, (80, 90, 100), (wx+10, wy), (wx, wy+8), 1)
    for i in range(TILE):
        v = random.randint(0, 6)
        pygame.draw.rect(s, (90, 82, 70), (i, TILE-v-2, 1, v+2))
    pygame.draw.rect(s, (20, 18, 15), (0, 0, TILE, TILE), 2)
    return s


# Calle tipo 3

def tile_calle():
    s = pygame.Surface((TILE, TILE))
    base = (38, 36, 34)
    s.fill(base)
    for i in range(0, TILE, 3):
        for j in range(0, TILE, 3):
            v = ruido_px(3, i//3, j//3, 5)
            c = tuple(max(0, min(255, base[k] + v)) for k in range(3))
            pygame.draw.rect(s, c, (i, j, 3, 3))
    for y in range(0, TILE, 14):
        pygame.draw.rect(s, (200, 190, 60), (TILE//2 - 2, y, 4, 8))
    random.seed(99)
    for _ in range(2):
        ox = random.randint(10, TILE-20)
        oy = random.randint(10, TILE-20)
        pygame.draw.ellipse(s, (25, 22, 20), (ox, oy, 18, 10))
    return s


# Árbol seco tipo 2 — Colisión

def tile_arbol():
    s = pygame.Surface((TILE, TILE))
    base = (52, 48, 42)
    s.fill(base)
    for i in range(TILE):
        for j in range(TILE):
            v = ruido_px(2, i//4, j//4, 8)
            c = (max(0, min(255, 52+v)), max(0, min(255, 48+v)), max(0, min(255, 42+v)))
            s.set_at((i, j), c)
    cx = TILE // 2
    for seg in range(5):
        y_seg = TILE - 15 - seg * 9
        random.seed(seg * 10)
        offset = random.randint(-3, 3)
        pygame.draw.rect(s, (55, 38, 22), (cx-4+offset, y_seg, 8, 10))
        pygame.draw.rect(s, (40, 28, 15), (cx-4+offset, y_seg, 2, 10))
    ramas = [
        (cx, TILE-42, cx-22, TILE-58),
        (cx, TILE-42, cx+20, TILE-55),
        (cx, TILE-52, cx-15, TILE-68),
        (cx, TILE-52, cx+18, TILE-65),
        (cx, TILE-60, cx-8,  TILE-78),
        (cx, TILE-60, cx+10, TILE-75),
    ]
    for x1, y1, x2, y2 in ramas:
        pygame.draw.line(s, (50, 35, 20), (x1, y1), (x2, y2), 3)
        dx = x2 - x1; dy = y2 - y1
        pygame.draw.line(s, (45, 30, 18), (x2, y2), (x2+dx//3, y2-8), 1)
        pygame.draw.line(s, (45, 30, 18), (x2, y2), (x2-dx//3, y2-6), 1)
    return s


# Ruinas tipo 4 — Colisión

def tile_ruinas():
    s = pygame.Surface((TILE, TILE))
    s.fill((58, 50, 40))
    random.seed(55)
    for _ in range(12):
        rx = random.randint(4, TILE-15)
        ry = random.randint(4, TILE-15)
        rw = random.randint(8, 18)
        rh = random.randint(6, 14)
        color = random.choice([(85,78,68),(70,64,56),(95,87,76),(60,55,48)])
        pygame.draw.ellipse(s, color, (rx, ry, rw, rh))
        pygame.draw.ellipse(s, tuple(max(0,c-15) for c in color), (rx,ry,rw,rh), 1)
    pygame.draw.rect(s, (75,70,62), (10, 35, TILE-20, 12))
    pygame.draw.rect(s, (55,50,44), (10, 35, TILE-20, 12), 2)
    pygame.draw.line(s, (40,36,30), (30,35), (38,47), 2)
    pygame.draw.line(s, (40,36,30), (55,35), (50,47), 1)
    for _ in range(5):
        mx = random.randint(0, TILE-8)
        my = random.randint(0, TILE-8)
        pygame.draw.ellipse(s, (45,55,38), (mx, my, 7, 5))
    pygame.draw.rect(s, (30,27,23), (0, 0, TILE, TILE), 2)
    return s

print("Generando tiles de ciudad...")
guardar(tile_suelo(),    "suelo")
guardar(tile_edificio(), "edificio")
guardar(tile_calle(),    "calle")
guardar(tile_arbol(),    "arbol")
guardar(tile_ruinas(),   "ruinas")
print(f"Listo. Tiles guardados en '{OUT}/'")
pygame.quit()