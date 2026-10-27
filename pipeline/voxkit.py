"""Piezas para los vídeos «pixel 3D» (21/10): suelos, rampa, coches de fondo, cohete, F1 de 1978 con ventilador,
ventilador, depósito, cápsula espacial, monedas, asientos, texto 3D de cubitos, partículas y rótulos de videojuego."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
import vox as V
from vox import Model, box, mat, LW, LH

M_ = {}
SAND = mat("sand", (206, 150, 92))
SAND2 = mat("sand2", (190, 134, 80))
ASPH = mat("asph", (58, 60, 70))
ASPH2 = mat("asph2", (66, 68, 78))
LINEW = mat("linew", (236, 236, 228))
CONC = mat("conc", (150, 150, 158))
CONC2 = mat("conc2", (132, 132, 142))
YEL = mat("yel", (255, 204, 48))
YEL_E = mat("yel_e", (255, 214, 70), True)
RED = mat("red", (222, 40, 46))
RED_E = mat("red_e", (255, 60, 60), True)
GRN_E = mat("grn_e", (60, 240, 110), True)
OFF = mat("off", (40, 40, 48))
WHITE = mat("white", (236, 238, 242))
BLUE = mat("blue", (56, 112, 220))
GREEN = mat("green", (70, 170, 90))
ORANGE = mat("orange", (238, 126, 40))
BLACK = mat("black", (26, 26, 32))
DGRAY = mat("dgray", (70, 72, 82))
GOLD = mat("gold", (250, 196, 46))
GOLD2 = mat("gold2", (204, 146, 30))
CYAN_E = mat("cyan_e", (90, 220, 255), True)
GRASS = mat("grass", (88, 176, 76))
GRASS2 = mat("grass2", (76, 160, 66))
DIRT = mat("dirt", (140, 96, 60))
WOOD = mat("wood", (120, 78, 46))
LEAF = mat("leaf", (52, 140, 64))
SKIN = mat("skin", (240, 196, 150))
PURP = mat("purp", (150, 90, 220))
PANEL = mat("panel", (40, 70, 150))
TILEB = mat("tileb", (32, 32, 38))


def once(fn):
    def w(*a):
        k = (fn.__name__,) + a
        if k not in M_:
            M_[k] = fn(*a)
        return M_[k]
    return w


def grid(X, Y, Z):
    return np.zeros((X, Y, Z), np.uint8)


def ijk(G):
    return np.meshgrid(np.arange(G.shape[0]), np.arange(G.shape[1]), np.arange(G.shape[2]), indexing="ij")


# ------------------------------------------------------------------ suelos
@once
def floor(X, Z, a=SAND, b=SAND2, seed=1, p=0.22):
    rng = np.random.default_rng(seed)
    G = np.where(rng.random((X, 1, Z)) < p, b, a).astype(np.uint8)
    return Model(G, seed=seed)


@once
def road(X, Z, dash=8, kerb=False):
    """Carretera a lo largo de x con línea discontinua en el centro (y bordillos rojos y blancos si kerb)."""
    rng = np.random.default_rng(2)
    G = np.where(rng.random((X, 1, Z)) < 0.25, ASPH2, ASPH).astype(np.uint8)
    zc = Z // 2
    for x in range(X):
        if (x // dash) % 2 == 0:
            G[x, 0, zc - 1:zc + 1] = LINEW
        if kerb:
            c = RED if (x // 4) % 2 == 0 else WHITE
            G[x, 0, :2] = c
            G[x, 0, -2:] = c
        else:
            G[x, 0, 1] = LINEW
            G[x, 0, -2] = LINEW
    return Model(G, seed=2)


# ------------------------------------------------------------------ rampa de media tubería con techo
@once
def halfpipe(R=20, th=2, Zw=18, ceil=46):
    X, Y = ceil + R + th + 1, 2 * R + th + 1
    G = grid(X, Y, Zw)
    i, j, k = ijk(G)
    xc, yc = ceil, R - 0.5
    d = np.hypot(i - xc, j - yc)
    ring = (d >= R) & (d <= R + th) & (i >= xc)
    G[ring] = CONC
    G[(i <= xc) & (j >= 2 * R - 0.5) & (j <= 2 * R + th - 0.5)] = CONC
    G[(i <= 2) & (j < 2 * R) & ((k <= 1) | (k >= Zw - 2))] = CONC2        # pilares del techo
    G[ring & ((k == 0) | (k == Zw - 1)) & (((i + j) // 3) % 2 == 0)] = YEL  # franjas amarillas en el borde
    m = Model(G, seed=5, pivot=(xc, -0.5, (Zw - 1) / 2))
    return m


@once
def parked(col):
    """Coche normal de fondo (compacto), 26 × 10 × 12 vóxeles."""
    G = grid(26, 10, 12)
    box(G, 0, 26, 2, 6, 0, 12, col)
    box(G, 6, 19, 6, 10, 1, 11, col)
    box(G, 7, 18, 6, 9, 1, 11, V.GLASS)
    box(G, 8, 17, 6, 9, 2, 10, col)
    box(G, 6, 19, 9, 10, 1, 11, col)
    for wx in (5, 20):
        box(G, wx - 3, wx + 3, 0, 4, 0, 2, V.TIRE)
        box(G, wx - 3, wx + 3, 0, 4, 10, 12, V.TIRE)
    box(G, 25, 26, 4, 5, 1, 4, V.LAMP)
    box(G, 25, 26, 4, 5, 8, 11, V.LAMP)
    box(G, 0, 1, 4, 5, 1, 3, V.TAIL)
    box(G, 0, 1, 4, 5, 9, 11, V.TAIL)
    return Model(G, seed=hash(col) % 99)


# ------------------------------------------------------------------ cohete y torre (base de lanzamiento genérica)
@once
def rocket(r=6, h=70):
    X = Z = 2 * r + 9
    G = grid(X, h + 14, Z)
    i, j, k = ijk(G)
    c = (X - 1) / 2
    d = np.hypot(i - c, k - c)
    rr = np.where(j < h, r, r * np.clip(1 - (j - h) / 13.0, 0, 1) ** 0.7)
    body = d <= rr + 0.3
    G[body] = V.STEEL
    G[body & (i < c - r * 0.25) & (j > 8)] = TILEB                   # escudo térmico negro en un lado
    for y0 in (h - 10, 6):                                           # aletas
        G[(np.abs(k - c) < 1) & (np.abs(i - c) < r + 4) & (np.abs(i - c) > r - 1) & (j >= y0) & (j < y0 + 8)] = DGRAY
    return Model(G, seed=9)


@once
def tower(h=80):
    G = grid(8, h, 8)
    i, j, k = ijk(G)
    edge = ((i <= 1) | (i >= 6)) & ((k <= 1) | (k >= 6))
    brace = ((j % 8) < 1) & ((i <= 1) | (i >= 6) | (k <= 1) | (k >= 6))
    G[edge | brace] = DGRAY
    G[(j >= h - 12) & (j < h - 10) & (i >= 6)] = DGRAY
    return Model(G, seed=3)


@once
def stage(X=56, Z=30):
    G = grid(X, 2, Z)
    G[:] = CONC
    G[:, 1, :] = DGRAY
    G[0, 1, :] = YEL_E
    G[-1, 1, :] = YEL_E
    G[:, 1, 0] = YEL_E
    G[:, 1, -1] = YEL_E
    return Model(G, seed=4)


@once
def mesa(X=26, H=14, Z=18, seed=1):
    rng = np.random.default_rng(seed)
    G = grid(X, H, Z)
    i, j, k = ijk(G)
    taper = (np.abs(i - X / 2) < X / 2 - j * 0.45) & (np.abs(k - Z / 2) < Z / 2 - j * 0.3)
    G[taper] = np.where(rng.random(G.shape) < 0.3, DIRT, ORANGE)[taper]
    return Model(G, seed=seed)


# ------------------------------------------------------------------ F1 de 1978 con ventilador (Brabham BT46B, rojo y blanco)
@once
def f1():
    G = grid(32, 9, 15)
    box(G, 4, 28, 1, 4, 5, 10, RED)        # monocasco
    box(G, 6, 22, 1, 3, 3, 12, RED)        # pontones
    box(G, 6, 22, 3, 4, 3, 12, WHITE)
    box(G, 26, 32, 0, 1, 1, 14, RED)       # alerón delantero
    box(G, 28, 32, 1, 2, 1, 3, WHITE)
    box(G, 28, 32, 1, 2, 12, 14, WHITE)
    box(G, 14, 18, 4, 6, 6, 9, BLACK)      # cabina
    box(G, 15, 17, 5, 7, 6, 9, YEL)        # casco
    box(G, 8, 14, 4, 6, 5, 10, RED)        # tapa motor
    box(G, 0, 3, 1, 8, 3, 12, DGRAY)       # ventilador trasero (disco)
    box(G, 0, 1, 2, 7, 4, 11, BLACK)
    for wx, ww in ((24, 3), (6, 4)):
        box(G, wx - ww, wx + ww, 0, 5, 0, 3, V.TIRE)
        box(G, wx - ww, wx + ww, 0, 5, 12, 15, V.TIRE)
    return Model(G, seed=6)


# ------------------------------------------------------------------ ventilador de succión (gira con yaw)
@once
def fan(r=7):
    D = 2 * r + 1
    G = grid(D, 2, D)
    i, j, k = ijk(G)
    d = np.hypot(i - r, k - r)
    G[(d <= r + 0.4) & (d >= r - 1) & (j == 0)] = DGRAY
    G[(d <= r + 0.4) & (d >= r - 1) & (j == 1)] = DGRAY
    ang = np.arctan2(k - r, i - r)
    blade = (d < r - 1) & (np.cos(4 * ang + d * 0.35) > 0.55) & (j == 1)
    G[blade] = WHITE
    G[(d <= 1.6) & (j <= 1)] = YEL
    return Model(G, seed=7, pivot=(r, 0.5, r))


@once
def tank(level):
    r, h = 6, 28
    D = 2 * r + 1
    G = grid(D, h + 2, D)
    i, j, k = ijk(G)
    d = np.hypot(i - r, k - r)
    G[(d <= r + 0.3) & (j < h)] = V.STEEL
    cap = (np.hypot(i - r, k - r) <= r * np.sqrt(np.clip(1 - ((j - h + 0.5) / 2.2) ** 2, 0, 1)) + 0.3) & (j >= h)
    G[cap] = V.STEEL
    win = (d > r - 1.2) & (np.abs(i - r) < 2.2) & (k > r) & (j > 2) & (j < h - 2)
    G[win] = V.GLASS
    G[win & (j < 2 + (h - 4) * level)] = CYAN_E
    G[(d <= r + 0.3) & ((j == 3) | (j == h - 3))] = DGRAY
    return Model(G, seed=8)


@once
def capsule():
    G = grid(17, 16, 17)
    i, j, k = ijk(G)
    d = np.hypot(i - 8, k - 8)
    rr = 8 - j * 0.32
    G[(d <= rr) & (j >= 2) & (j < 13)] = WHITE
    G[(d <= 8.2) & (j < 2)] = BLACK
    G[(d <= rr) & (d > rr - 1.2) & (j > 6) & (j < 9) & (((np.arctan2(k - 8, i - 8) * 4 / math.pi) % 2) < 0.6)] = V.GLASS
    G[(d <= 2.2) & (j >= 13) & (j < 15)] = DGRAY
    return Model(G, seed=10, pivot=(8, 7.5, 8))


@once
def satellite():
    G = grid(44, 9, 9)
    box(G, 16, 28, 0, 9, 0, 9, GOLD)
    box(G, 17, 27, 1, 8, 9 - 1, 9, GOLD2)
    for x0 in (0, 30):
        box(G, x0, x0 + 14, 3, 6, 2, 7, PANEL)
        for xx in range(x0 + 2, x0 + 14, 3):
            box(G, xx, xx + 1, 3, 6, 2, 7, BLUE)
    box(G, 14, 16, 4, 5, 4, 5, DGRAY)
    box(G, 28, 30, 4, 5, 4, 5, DGRAY)
    return Model(G, seed=11, pivot=(21.5, 4, 4))


@once
def coin():
    G = grid(11, 11, 2)
    i, j, k = ijk(G)
    d = np.hypot(i - 5, j - 5)
    G[d <= 5.3] = GOLD
    G[(d <= 5.3) & (d > 4.2)] = GOLD2
    G[(np.abs(i - 5) < 0.6) & (np.abs(j - 5) < 3.5)] = GOLD2       # «$» sencillo: barra vertical
    G[(np.abs(j - 5) < 0.6) & (np.abs(i - 5) < 2.5)] = GOLD2
    return Model(G, seed=12, pivot=(5, 5, 0.5))


@once
def seat(col=BLACK):
    G = grid(8, 12, 8)
    box(G, 0, 8, 0, 4, 0, 8, col)
    box(G, 0, 3, 4, 12, 0, 8, col)
    box(G, 1, 2, 5, 11, 2, 6, RED)
    box(G, 0, 3, 10, 12, 2, 6, DGRAY)
    return Model(G, seed=13)


@once
def flag(col, h=18):
    G = grid(9, h, 1)
    box(G, 0, 1, 0, h, 0, 1, WOOD)
    box(G, 1, 9, h - 6, h, 0, 1, col)
    return Model(G, seed=14, pivot=(0, -0.5, 0))


@once
def tree(h=8, seed=1):
    G = grid(7, h + 6, 7)
    box(G, 3, 4, 0, h, 3, 4, WOOD)
    i, j, k = ijk(G)
    G[(np.hypot(i - 3, k - 3) + np.abs(j - h - 1) * 0.9 <= 3.4) & (j >= h - 2)] = LEAF
    return Model(G, seed=seed)


@once
def island(X=88, Z=88, seed=3):
    """Isla del «mapa del mundo» (como un videojuego): césped, borde de tierra de 3 de alto."""
    rng = np.random.default_rng(seed)
    G = grid(X, 4, Z)
    i, j, k = ijk(G)
    G[j < 3] = DIRT
    G[j == 3] = GRASS
    top = G[:, 3, :]
    top[rng.random((X, Z)) < 0.25] = GRASS2
    return Model(G, seed=seed)


@once
def lamp_tree():
    """Semáforo de salida de las carreras de aceleración (poste con 3 luces)."""
    G = grid(3, 30, 3)
    box(G, 1, 2, 0, 30, 1, 2, DGRAY)
    return Model(G, seed=15, pivot=(1, -0.5, 1))


@once
def light(m):
    G = grid(3, 3, 3)
    G[:] = m
    return Model(G, seed=16, pivot=(1, 1, 1))


@once
def cube(m, n=2):
    G = grid(n, n, n)
    G[:] = m
    return Model(G, seed=17, pivot=((n - 1) / 2, (n - 1) / 2, (n - 1) / 2))


# ------------------------------------------------------------------ texto 3D de cubitos (fuente pixel de 8 × 8)
@once
def text3d(txt, m=YEL, depth=3, edge=None):
    fo = V.font(8)
    w = int(fo.getlength(txt)) + 2
    im = Image.new("L", (w, 10), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    d.text((1, 1), txt, font=fo, fill=255)
    a = np.asarray(im)[::-1].T > 0                    # (x, y) con y hacia arriba
    G = np.zeros((a.shape[0], a.shape[1], depth), np.uint8)
    G[a] = m
    if edge:
        G[a, :] = m
        G[:, :, 0][a] = edge
    xs = np.nonzero(a.any(1))[0]
    return Model(G, seed=18, pivot=((xs.min() + xs.max()) / 2 if len(xs) else 0, 4.5, (depth - 1) / 2))


# ------------------------------------------------------------------ partículas (deterministas en función de t)
def puffs(cv, org, dirv, t, t0=0.0, t1=99.0, rate=26, life=0.7, speed=16, spread=0.35, size=(2, 5), col=(236, 242, 255), seed=1):
    """Chorro de gas frío: cubitos blancos que salen, crecen y se apagan."""
    if t < t0:
        return
    rng = random.Random(seed)
    n0 = int(max(0, (t - life - t0)) * rate)
    n1 = int((min(t, t1) - t0) * rate) + 1
    dx, dy, dz = dirv
    for n in range(n0, n1):
        tb = t0 + n / rate
        age = t - tb
        if age < 0 or age > life or tb > t1:
            continue
        r2 = random.Random(seed * 7919 + n)
        u = age / life
        jx, jy, jz = (r2.uniform(-spread, spread) for _ in range(3))
        dist = speed * age * (1 - 0.4 * u)
        x = org[0] + (dx + jx) * dist
        y = org[1] + (dy + jy) * dist
        z = org[2] + (dz + jz) * dist
        sz = int(round(size[0] + (size[1] - size[0]) * u))
        cv.dot(x, y, z, col, sz, alpha=max(0.0, 1 - u) * 0.9)


def flow(cv, pts, t, n=24, speed=0.7, col=(110, 230, 255), size=2, seed=2):
    """Partículas que recorren una polilínea del mundo (aire que entra por debajo del coche)."""
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.dist(a, b))
    tot = L[-1]
    for i in range(n):
        u = (t * speed + i / n) % 1.0
        dd = u * tot
        s = next(k for k in range(1, len(L)) if L[k] >= dd)
        f = (dd - L[s - 1]) / max(1e-6, L[s] - L[s - 1])
        a, b = pts[s - 1], pts[s]
        r = random.Random(seed * 31 + i)
        p = [a[q] + (b[q] - a[q]) * f + r.uniform(-1.2, 1.2) for q in range(3)]
        cv.dot(*p, col, size, alpha=0.95)


# ------------------------------------------------------------------ rótulos de videojuego (en baja resolución)
INK = (16, 14, 26)
CREAM = (255, 244, 214)
GOLDC = (255, 206, 60)
REDC = (255, 74, 74)
CYANC = (100, 224, 255)


def label(cv, x, y, txt, k=1.0, fg=CREAM, bd=GOLDC, bg=INK, size=8, anchor="c"):
    """Cartel con borde doble como los menús de las consolas. Aparece con un pequeño salto."""
    if k <= 0:
        return
    fo = V.font(size)
    w = int(fo.getlength(txt)) + 12
    h = size + 10
    yy = int(y + (1 - k) * 8)
    x0 = int(x - w / 2) if anchor == "c" else int(x)
    im = Image.fromarray(np.clip(cv.c, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    d.rectangle([x0 + 2, yy + 2, x0 + w + 2, yy + h + 2], fill=(0, 0, 0))
    d.rectangle([x0, yy, x0 + w, yy + h], fill=bg, outline=bd)
    d.rectangle([x0 + 2, yy + 2, x0 + w - 2, yy + h - 2], outline=tuple(int(c * 0.55) for c in bd))
    d.text((x0 + 6, yy + 5), txt, font=fo, fill=fg)
    cv.c = np.asarray(im).astype(np.float32)


def text(cv, x, y, txt, col=CREAM, size=8, anchor="mm", outline=True):
    im = Image.fromarray(np.clip(cv.c, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    fo = V.font(size)
    if outline:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1)):
            d.text((x + dx, y + dy), txt, font=fo, fill=INK, anchor=anchor)
    d.text((x, y), txt, font=fo, fill=col, anchor=anchor)
    cv.c = np.asarray(im).astype(np.float32)


def draw(cv):
    """Devuelve (imagen PIL de baja resolución, función para volcarla de nuevo en el lienzo)."""
    im = Image.fromarray(np.clip(cv.c, 0, 255).astype(np.uint8))
    return im, ImageDraw.Draw(im)


def commit(cv, im):
    cv.c = np.asarray(im).astype(np.float32)


def arrow_up(d, x, y, h, col=GOLDC):
    d.rectangle([x - 2, y - h + 6, x + 2, y], fill=col, outline=INK)
    d.polygon([(x - 7, y - h + 7), (x + 7, y - h + 7), (x, y - h)], fill=col, outline=INK)


def stamp(cv, x, y, txt, k, col=REDC, size=16, ang=-10):
    """Sello tipo «PROHIBIDO» que cae desde grande con giro."""
    if k <= 0:
        return
    fo = V.font(size)
    w = int(fo.getlength(txt)) + 20
    h = size + 18
    st = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(st)
    d.fontmode = "1"
    d.rectangle([4, 4, w + 3, h + 3], outline=col + (255,), width=3)
    d.text((w / 2 + 4, h / 2 + 4), txt, font=fo, fill=col + (255,), anchor="mm")
    sc = 1 + 1.4 * (1 - k)
    st = st.resize((int(st.width * sc), int(st.height * sc)), Image.NEAREST).rotate(ang, expand=True, resample=Image.NEAREST)
    im = Image.fromarray(np.clip(cv.c, 0, 255).astype(np.uint8))
    im.paste(st, (int(x - st.width / 2), int(y - st.height / 2)), st)
    cv.c = np.asarray(im).astype(np.float32)
