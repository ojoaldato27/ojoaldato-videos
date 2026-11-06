"""22 · Lo que nadie te cuenta del supermercado — formato «LO QUE NADIE TE CUENTA DE… #1» (manual v2). PREVIA (gancho + 4 escenas).
Base de piezas: c20_dedos.py (import D). Datos (técnicas de diseño de tiendas muy documentadas en marketing/retail): fruta y verdura
a la entrada (frescura y color, ánimo de compra), productos básicos (leche, pan, huevos) al fondo para recorrer la tienda,
productos más caros a la altura de los ojos, golosinas en caja, carros grandes. Decirlo como «técnicas habituales», sin cifras inventadas.
GUION COMPLETO (para el vídeo entero, tras el sí de Iker):
  Gancho · fruta en la entrada · buen humor · leche y pan al fondo · recorrido entero · [re-gancho] los carros son enormes:
  un carro medio vacío parece que «falta algo» · los caros a la altura de tus ojos; los baratos, abajo · [giro] la música
  lenta te hace andar más despacio · los chicles y chocolatinas en la caja, cuando ya estás cansado · respuesta: el súper
  es un recorrido diseñado; truco: ir con lista · reflexión + despedida.
"""
import math
import os
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED
from PIL import Image, ImageDraw, ImageFilter
import pro
from pro import solid, glow, ojo, hook_text, lt, WHITE
import c20_dedos as D

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "22_Supermercado"
VOICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c22_super.mp3")
LINES = [
    "El súper está diseñado para que compres cosas que no necesitas. ¡Y empieza en la puerta!",
    "Nada más entrar te encuentras la *fruta*. Colores vivos y olor a fresco. Y es a propósito.",
    "La idea es que entres de *buen humor* y con ganas de llenar el carro.",
    "Ahora fíjate en la *leche* y el *pan*. Casi siempre están al *fondo*.",
    "Para llegar hasta ellos tienes que cruzar la *tienda entera*. Pasillo a pasillo.",
    "Y mira el *carro*. Cada vez son más *grandes*.",
    "Con un carro enorme y medio vacío parece que te *falta algo*. Así que sigues metiendo cosas.",
    "Los productos más *caros* suelen estar a la altura de tus *ojos*.",
    "Las marcas *baratas* están más *abajo*. Tienes que agacharte para verlas.",
    "Pero aquí viene lo más curioso. La *música*.",
    "Una música lenta hace que camines *más despacio*. Y cuanto más rato estás, más compras.",
    "Y al final, en la *caja*, te esperan chicles y *chocolatinas*.",
    "Llegas cansado y esperando en la cola. Es el momento perfecto para un *capricho*.",
    "Así que el súper no está ordenado al azar. Es un *recorrido* pensado para que gastes más.",
    "El truco para ganarles es fácil. Ve con una *lista* y no te salgas de ella.",
]
OUTRO_LINE = "Ahora ya conoces su juego. Sígueme para más trucos como este. ¡Ojo al dato!"
NAMES = ["q", "fruta", "humor", "fondo", "recorrido", "carros", "vacio", "ojos", "abajo", "musica", "lenta", "caja", "cansado",
         "answer", "truco"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS, HYPE, FOLLOW, NARRATOR, PUSH = {}, None, None, {}, {}
NOTIF = ("ojos", 0.3)
HEAD = {i: ("", "") for i in range(len(NAMES))}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
FL.use("minimal", HEAD)
FRAME = vid2.frame
FPS = 60
BG = (40, 46, 80)
TRANS_POOL = ["suave"]
TRANS_PLAN = ["suave", "deriva_r", "suave_out", "deriva"] * 4
TRANS_SEED = 22
TD = 0.9
CAM_PUSH = 0.06
SHAKE = 0
CUT_SFX = False
FL.TH["narr"] = True
OJO_TRAJE = "c_clasico"
OJO_POSES = {}
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
GREEN = D.GREEN
PROD = [(230, 70, 60), (60, 130, 220), (250, 200, 60), (90, 180, 110), (240, 140, 60), (170, 90, 200), (250, 250, 250)]


# ------------------------------------------------------------------ fondo: pasillo del súper en perspectiva
def super_bg():
    if "super" in D._BG:
        return D._BG["super"]
    img = Image.new("RGB", (D.BW, D.BH))
    d = ImageDraw.Draw(img, "RGBA")
    cx, hy = D.BW / 2, 760
    for y in range(D.BH):
        u = y / D.BH
        d.line([(0, y), (D.BW, y)], fill=(int(lerp(236, 200, u)), int(lerp(240, 206, u)), int(lerp(244, 214, u))))
    d.polygon([(0, D.BH), (D.BW, D.BH), (cx + 120, hy + 120), (cx - 120, hy + 120)], fill=(214, 210, 200))
    for side in (-1, 1):                                    # estanterías en perspectiva
        for r in range(6):
            y0 = 260 + r * 230
            pts_out = (cx + side * D.BW / 2, y0)
            for j in range(10):
                u0, u1 = j / 10, (j + 1) / 10
                xa = lerp(cx + side * 620, cx + side * 140, u0)
                xb = lerp(cx + side * 620, cx + side * 140, u1)
                ya = lerp(y0, hy - 200 + r * 64, u0)
                yb = lerp(y0, hy - 200 + r * 64, u1)
                ha = lerp(150, 44, u0)
                hb = lerp(150, 44, u1)
                d.polygon([(xa, ya), (xb, yb), (xb, yb + hb), (xa, ya + ha)], fill=PROD[(j + r * 3 + (side > 0) * 2) % 7] + (220,))
            d.polygon([(cx + side * 640, y0 + 150), (cx + side * 140, hy - 200 + r * 64 + 44), (cx + side * 140, hy - 190 + r * 64 + 44), (cx + side * 640, y0 + 175)], fill=(150, 150, 160))
    for j in range(5):                                       # luces del techo
        y = 60 + j * 46
        w = lerp(380, 60, j / 5)
        d.rounded_rectangle([cx - w, y, cx + w, y + 18], radius=8, fill=(255, 255, 240))
    img = D._vign(img.filter(ImageFilter.GaussianBlur(6)), 150)
    D._BG["super"] = img
    return img


# ------------------------------------------------------------------ piezas
def cart(Lr, cx, cy, s=1.0, n=0, t=0.0):
    d = K.D(Lr)
    w = max(3, int(7 * s))
    for j in range(n):                                       # productos dentro (asoman por arriba)
        x = cx - 200 * s + (j * 71 % 380) * s
        h = (60 + (j * 37) % 90) * s
        y = cy - 150 * s - (j // 6) * 40 * s
        d.rounded_rectangle([x, y - h, x + 64 * s, y + 20 * s], radius=int(8 * s), fill=PROD[j % 7], outline=INK, width=3)
    d.polygon([(cx - 260 * s, cy - 160 * s), (cx + 240 * s, cy - 160 * s), (cx + 200 * s, cy + 60 * s), (cx - 210 * s, cy + 60 * s)], fill=(200, 210, 220, 150), outline=INK)
    for q in range(1, 7):
        x = lerp(cx - 260 * s, cx + 240 * s, q / 7)
        d.line([(x, cy - 160 * s), (x - 6 * s, cy + 60 * s)], fill=(120, 130, 140), width=w - 2)
    d.line([(cx - 260 * s, cy - 160 * s), (cx - 330 * s, cy - 230 * s)], fill=INK, width=w)
    d.line([(cx - 330 * s, cy - 230 * s), (cx - 380 * s, cy - 230 * s)], fill=RED, width=w + 6)
    d.line([(cx - 210 * s, cy + 60 * s), (cx - 200 * s, cy + 130 * s), (cx + 190 * s, cy + 130 * s), (cx + 200 * s, cy + 60 * s)], fill=INK, width=w)
    for x in (cx - 170 * s, cx + 160 * s):
        a = t * 6
        d.ellipse([x - 30 * s, cy + 130 * s, x + 30 * s, cy + 190 * s], fill=(50, 50, 60), outline=INK, width=4)
        d.line([(x, cy + 160 * s), (x + 22 * s * math.cos(a), cy + 160 * s + 22 * s * math.sin(a))], fill=(200, 200, 210), width=4)


def fruit_stand(Lr, cx, cy, s=1.0, t=0.0):
    d = K.D(Lr)
    cols = [(230, 50, 50), (250, 150, 40), (250, 210, 60), (110, 190, 70), (150, 60, 140)]
    for c in range(3):
        x0 = cx - 390 * s + c * 270 * s
        d.polygon([(x0, cy), (x0 + 250 * s, cy), (x0 + 230 * s, cy + 200 * s), (x0 + 20 * s, cy + 200 * s)], fill=(190, 140, 90), outline=INK, width=5)
        for j in range(3):
            d.line([(x0 + 10 * s, cy + (50 + j * 50) * s), (x0 + 240 * s, cy + (50 + j * 50) * s)], fill=(150, 100, 60), width=4)
        for q in range(9):
            fx = x0 + (40 + (q % 4) * 55) * s
            fy = cy - (20 + (q // 4) * 46) * s + 4 * math.sin(t * 3 + q)
            r = 30 * s
            col = cols[(c * 2 + q % 2) % 5]
            d.ellipse([fx - r, fy - r, fx + r, fy + r], fill=col, outline=INK, width=3)
            d.ellipse([fx - r * 0.5, fy - r * 0.6, fx - r * 0.1, fy - r * 0.25], fill=(255, 255, 255, 160))
        d.rounded_rectangle([x0 + 70 * s, cy + 210 * s, x0 + 180 * s, cy + 270 * s], radius=10, fill=WHITE, outline=INK, width=3)


def milk(Lr, x, y, s=1.0):
    d = K.D(Lr)
    d.rectangle([x - 50 * s, y - 70 * s, x + 50 * s, y + 90 * s], fill=WHITE, outline=INK, width=5)
    d.polygon([(x - 50 * s, y - 70 * s), (x, y - 120 * s), (x + 50 * s, y - 70 * s)], fill=(60, 130, 220), outline=INK)
    d.rectangle([x - 50 * s, y, x + 50 * s, y + 40 * s], fill=(60, 130, 220))


def bread(Lr, x, y, s=1.0):
    d = K.D(Lr)
    d.rounded_rectangle([x - 110 * s, y - 40 * s, x + 110 * s, y + 40 * s], radius=int(40 * s), fill=(220, 160, 80), outline=INK, width=5)
    for j in range(4):
        xx = x - 70 * s + j * 46 * s
        d.line([(xx, y - 30 * s), (xx + 24 * s, y + 10 * s)], fill=(170, 110, 50), width=5)


def store_map(img, t, kpath):
    """Plano del súper visto desde arriba: entrada abajo, leche y pan al fondo; la ruta se dibuja sola."""
    d = K.D(img)
    x0, y0, x1, y1 = 120, 470, 960, 1420
    d.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=(250, 248, 240, 240), outline=INK, width=8)
    for j in range(4):                                      # pasillos
        x = 230 + j * 180
        d.rounded_rectangle([x, 640, x + 90, 1240], radius=10, fill=PROD[j] + (200,), outline=INK, width=3)
    d.rectangle([460, 1400, 620, 1440], fill=(90, 200, 120))
    FL.big(img, 540, 1470, "ENTRADA", 40, INK, 1.0)
    path = [(540, 1390), (540, 1290), (180, 1290), (180, 560), (900, 560), (900, 1290), (600, 1290), (600, 1390)]
    seg = list(zip(path, path[1:]))
    tot = sum(math.dist(a, b) for a, b in seg)
    s_ = tot * clamp(kpath)
    for i, (a, b) in enumerate(seg):
        ln = math.dist(a, b)
        n = int(ln / 34)
        for q in range(n):
            if s_ - q * 34 <= 0:
                break
            u = q / n
            x, y = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
            d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=RED)
        s_ -= ln
        if s_ <= 0:
            break


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    """GANCHO: un carro desbordado que rueda solo hacia la cámara, con tickets volando; Ojo flipando."""
    k = ease(clamp(t / 0.8))
    solid(img, lambda Lr: cart(Lr, 520, 1180, 1.25 + 0.1 * k, 18, t))
    d = K.D(img)
    for j in range(6):                                       # tickets que vuelan
        u = (t * 0.6 + j / 6) % 1
        x = 200 + j * 140 + 40 * math.sin(t * 2 + j)
        y = 1000 - 500 * u
        d.rectangle([x - 26, y - 40, x + 26, y + 40], fill=(255, 255, 255, int(230 * (1 - u))), outline=INK + (int(200 * (1 - u)),))
    FL.big(img, 820, 760, "149,90 €", 70, RED, clamp((t - 0.4) / 0.3))
    ojo(img, 900, 1720, 0.6, "surprise", t=t)
    hook_text(img, [("EL SÚPER ESTÁ HECHO", False), ("PARA QUE GASTES", True)], 1.0 if t < T - 0.6 else clamp((T - t) / 0.6), y=330, size=80)


def sh_fruta(img, t, T, L):
    """Entrada: el puesto de fruta brilla, con olor (ondas) y destellos de color."""
    solid(img, lambda Lr: fruit_stand(Lr, 540, 980, 1.05, t))
    d = K.D(img)
    for j in range(4):                                       # «olor a fresco»
        x = 260 + j * 190
        pts = [(x + 18 * math.sin(t * 3 + q * 0.8 + j), 860 - q * 30) for q in range(8)]
        d.line(pts, fill=(120, 200, 120, 160), width=6)
    k = clamp((t - lt(L, 0, 0.6)) / 0.3)
    if k > 0:
        FL.stamp(img, 540, 520, "A PROPÓSITO", k, col=RED)
    ojo(img, 160, 1720, 0.6, "point", t=t)


def sh_humor(img, t, T, L):
    """Ojo contento con corazones; el carro se va llenando solo, producto a producto."""
    n = int(16 * ease(clamp((t - 0.3) / max(1.0, T - 0.8))))
    solid(img, lambda Lr: cart(Lr, 600, 1150, 1.0, n, t))
    d = K.D(img)
    for j in range(5):
        u = (t * 0.7 + j / 5) % 1
        x = 220 + 30 * math.sin(t * 2 + j * 2)
        y = 1300 - 600 * u
        r = 26
        a = int(230 * (1 - u))
        d.ellipse([x - r, y - r, x, y], fill=(240, 80, 110, a))
        d.ellipse([x, y - r, x + r, y], fill=(240, 80, 110, a))
        d.polygon([(x - r, y - r / 2), (x + r, y - r / 2), (x, y + r * 0.8)], fill=(240, 80, 110, a))
    FL.pill(img, 600, 560, "BUEN HUMOR = MÁS COMPRAS", clamp((t - lt(L, 0, 0.3)) / 0.3), col=(240, 80, 110))
    ojo(img, 220, 1720, 0.75, "smirk", t=t)


def sh_fondo(img, t, T, L):
    """Plano desde arriba: leche y pan aparecen al FONDO del súper, lejísimos de la entrada."""
    store_map(img, t, 0.0)
    km = clamp((t - lt(L, 0, 0.3)) / 0.3)
    kb = clamp((t - lt(L, 0, 0.45)) / 0.3)
    if km > 0:
        solid(img, lambda Lr: milk(Lr, 400, 560, 0.8 * pop(km)), sh=0.25)
    if kb > 0:
        solid(img, lambda Lr: bread(Lr, 700, 560, 0.8 * pop(kb)), sh=0.25)
    kf = clamp((t - lt(L, 0, 0.75)) / 0.3)
    if kf > 0:
        d = K.D(img)
        y = 700 + 30 * math.sin(t * 5)
        d.line([(540, 1350), (540, y)], fill=RED + (200,), width=12)
        d.polygon([(510, y), (570, y), (540, y - 50)], fill=RED)
        FL.pill(img, 540, 400, "AL FONDO DEL TODO", kf, col=RED)
    ojo(img, 950, 1760, 0.5, "think", t=t)


def sh_recorrido(img, t, T, L):
    """La ruta se dibuja sola por todos los pasillos; contador de pasos que sube."""
    kp = ease(clamp((t - 0.2) / max(1.0, T - 0.6)))
    store_map(img, t, kp)
    solid(img, lambda Lr: milk(Lr, 400, 560, 0.8), sh=0.2)
    solid(img, lambda Lr: bread(Lr, 700, 560, 0.8), sh=0.2)
    FL.big(img, 540, 400, f"{int(380 * kp)} PASOS", 84, RED, clamp(t / 0.3))
    ojo(img, 950, 1760, 0.5, "surprise" if kp > 0.8 else "point", t=t)


# ------------------------------------------------------------------ planos del vídeo entero
def sh_carros(img, t, T, L):
    """Tres carros de más pequeño a más grande, apareciendo uno tras otro."""
    for i, (x, s) in enumerate(((220, 0.45), (500, 0.7), (820, 1.0))):
        k = clamp((t - 0.2 - i * 0.45) / 0.3)
        if k > 0:
            solid(img, lambda Lr, x=x, s=s, k=k: cart(Lr, x, 1250 - 40 * s, s * pop(k), 0, t), sh=0.25)
    k = clamp((t - lt(L, 0, 0.6)) / 0.3)
    if k > 0:
        d = K.D(img)
        d.line([(160, 820), (900, 620)], fill=RED + (230,), width=14)
        d.polygon([(900, 590), (950, 610), (905, 650)], fill=RED)
        FL.pill(img, 540, 560, "CADA VEZ MÁS GRANDES", k, col=RED)
    ojo(img, 160, 1760, 0.5, "surprise" if k > 0 else "point", t=t)


def sh_vacio(img, t, T, L):
    """Carro enorme con pocas cosas: bocadillo de «¿falta algo?» y se van añadiendo productos."""
    n = 3 + int(9 * ease(clamp((t - lt(L, 0, 0.55)) / max(0.8, T * 0.4))))
    solid(img, lambda Lr: cart(Lr, 600, 1150, 1.3, n, t))
    d = K.D(img)
    k = clamp((t - lt(L, 0, 0.2)) / 0.3)
    if k > 0:
        d.rounded_rectangle([140, 520, 600, 720], radius=60, fill=(255, 255, 255, 240), outline=INK, width=6)
        d.polygon([(260, 715), (320, 715), (240, 800)], fill=WHITE, outline=INK)
        FL.big(img, 370, 620, "¿FALTA ALGO?", 58, INK, k)
    ojo(img, 200, 1760, 0.6, "think", t=t)


def shelf(img, y0, rows=4):
    d = K.D(img)
    d.rectangle([60, y0, 1020, y0 + rows * 230], fill=(236, 232, 224, 235), outline=INK, width=6)
    for r in range(rows):
        y = y0 + (r + 1) * 230
        d.rectangle([60, y - 16, 1020, y], fill=(150, 150, 160), outline=INK, width=3)
    return [y0 + (r + 1) * 230 - 16 for r in range(rows)]


def box(Lr, x, yb, w, h, col, gold=False):
    d = K.D(Lr)
    d.rounded_rectangle([x - w / 2, yb - h, x + w / 2, yb], radius=10, fill=col, outline=INK, width=4)
    d.rectangle([x - w / 2 + 10, yb - h * 0.6, x + w / 2 - 10, yb - h * 0.35], fill=(255, 255, 255, 200))
    if gold:
        d.rectangle([x - w / 2, yb - h, x + w / 2, yb - h + 16], fill=(236, 190, 60))


def sh_ojos(img, t, T, L):
    """Estantería: la balda de la altura de los ojos se ilumina con productos caros (etiqueta €€€)."""
    ys = shelf(img, 500)
    for r, y in enumerate(ys):
        for j in range(6):
            x = 150 + j * 155
            gold = r == 1
            solid(img, lambda Lr, x=x, y=y, j=j, gold=gold, r=r: box(Lr, x, y, 110, 150 + (j % 2) * 30, PROD[(j + r * 2) % 7], gold), sh=0.12)
    k = clamp((t - lt(L, 0, 0.4)) / 0.3)
    if k > 0:
        glow(img, 540, ys[1] - 90, 520, 110, (255, 220, 120), 0.5 * k)
        d = K.D(img)
        d.line([(40, ys[1] - 90), (1040, ys[1] - 90)], fill=RED + (int(220 * k),), width=6)
        FL.pill(img, 540, ys[1] - 250, "ALTURA DE TUS OJOS = €€€", k, col=RED)
    ojo(img, 540, 1760, 0.6, "surprise" if k > 0 else "point", t=t)


def sh_abajo(img, t, T, L):
    """Las marcas baratas, abajo del todo: flecha hacia abajo y Ojo agachándose."""
    ys = shelf(img, 500)
    for r, y in enumerate(ys):
        for j in range(6):
            x = 150 + j * 155
            solid(img, lambda Lr, x=x, y=y, j=j, r=r: box(Lr, x, y, 110, 150, PROD[(j + r * 2) % 7], r == 1), sh=0.12)
    k = clamp((t - lt(L, 0, 0.3)) / 0.3)
    if k > 0:
        glow(img, 540, ys[3] - 80, 520, 110, (120, 240, 140), 0.5 * k)
        d = K.D(img)
        y = ys[3] - 330 + 20 * math.sin(t * 5)
        d.line([(900, y - 160), (900, y)], fill=GREEN, width=16)
        d.polygon([(870, y), (930, y), (900, y + 50)], fill=GREEN)
        FL.pill(img, 540, ys[3] + 70, "LO BARATO, ABAJO", k, col=GREEN)
    ojo(img, 200, 1760 + 30 * clamp((t - 0.6) / 0.4), 0.55, "think", t=t)


def speaker(Lr, cx, cy, s, t):
    d = K.D(Lr)
    d.rounded_rectangle([cx - 120 * s, cy - 180 * s, cx + 120 * s, cy + 180 * s], radius=int(24 * s), fill=(50, 54, 66), outline=INK, width=6)
    for y, r in ((-80, 60), (70, 90)):
        rr = r * s * (1 + 0.05 * math.sin(t * 6))
        d.ellipse([cx - rr, cy + y * s - rr, cx + rr, cy + y * s + rr], fill=(90, 94, 110), outline=INK, width=5)
        d.ellipse([cx - rr * 0.35, cy + y * s - rr * 0.35, cx + rr * 0.35, cy + y * s + rr * 0.35], fill=(30, 30, 36))


def notes(img, cx, cy, t, n=5, spd=0.4):
    for j in range(n):
        u = (t * spd + j / n) % 1
        x = cx + 260 * u + 40 * math.sin(t * 2 + j)
        y = cy - 360 * u
        a = int(240 * (1 - u))
        d = K.D(img)
        d.ellipse([x - 26, y - 18, x + 18, y + 18], fill=(250, 200, 60, a), outline=INK + (a,), width=3)
        d.line([(x + 16, y), (x + 16, y - 90)], fill=INK + (a,), width=6)
        d.line([(x + 16, y - 90), (x + 50, y - 64)], fill=INK + (a,), width=6)


def sh_musica(img, t, T, L):
    """PERO AQUÍ VIENE LO MÁS CURIOSO: altavoz del techo con notas."""
    if t < 1.2:
        FL.stamp(img, 540, 480, "LO MÁS CURIOSO", clamp(t / 0.3) * clamp((1.2 - t) / 0.25), col=RED)
    solid(img, lambda Lr: speaker(Lr, 400, 1000, 1.1, t))
    notes(img, 520, 1000, t)
    ojo(img, 860, 1760, 0.6, "surprise", t=t)


def sh_lenta(img, t, T, L):
    """Música lenta: Ojo camina despacio con el carro; un metrónomo lento y un reloj que avanza."""
    x = 200 + 120 * t
    solid(img, lambda Lr: cart(Lr, x + 220, 1250, 0.6, int(min(14, t * 3)), t), sh=0.2)
    ojo(img, x, 1700, 0.6, "smirk", t=t)
    notes(img, 600, 700, t, 4, 0.25)
    d = K.D(img)
    a = 0.5 * math.sin(t * 1.6)
    d.polygon([(760, 900), (980, 900), (900, 560), (840, 560)], fill=(180, 130, 80), outline=INK)
    d.line([(870, 880), (870 + 300 * math.sin(a), 880 - 300 * math.cos(a))], fill=INK, width=8)
    FL.pill(img, 540, 480, "MÁS DESPACIO = MÁS COMPRAS", clamp((t - lt(L, 0, 0.5)) / 0.3), col=(150, 90, 200))


def checkout(Lr, cx, cy, s):
    d = K.D(Lr)
    d.rectangle([cx - 400 * s, cy, cx + 300 * s, cy + 220 * s], fill=(90, 100, 120), outline=INK, width=6)
    d.rectangle([cx - 400 * s, cy - 20 * s, cx + 300 * s, cy + 10 * s], fill=(40, 40, 50))
    d.rounded_rectangle([cx + 120 * s, cy - 180 * s, cx + 280 * s, cy - 30 * s], radius=10, fill=(30, 34, 44), outline=INK, width=5)
    d.rectangle([cx + 140 * s, cy - 160 * s, cx + 260 * s, cy - 100 * s], fill=(120, 230, 140))


def candy_rack(Lr, cx, cy, s, t):
    d = K.D(Lr)
    d.rectangle([cx - 140 * s, cy - 420 * s, cx + 140 * s, cy], fill=(200, 60, 60), outline=INK, width=6)
    for r in range(4):
        for j in range(4):
            x = cx - 105 * s + j * 70 * s
            y = cy - 380 * s + r * 95 * s
            col = PROD[(r + j) % 7]
            d.rounded_rectangle([x - 28 * s, y, x + 28 * s, y + 70 * s], radius=8, fill=col, outline=INK, width=3)


def sh_caja(img, t, T, L):
    """La caja con el expositor de chicles y chocolatinas brillando."""
    solid(img, lambda Lr: checkout(Lr, 520, 1120, 1.0))
    solid(img, lambda Lr: candy_rack(Lr, 880, 1130, 1.0, t))
    k = clamp((t - lt(L, 0, 0.5)) / 0.3)
    if k > 0:
        glow(img, 880, 920, 220, 260, (255, 220, 120), 0.45 * k * (0.7 + 0.3 * math.sin(t * 6)))
        FL.pill(img, 760, 560, "CHUCHES EN LA CAJA", k, col=RED)
    ojo(img, 200, 1760, 0.55, "point", t=t)


def sh_cansado(img, t, T, L):
    """Cola de gente; Ojo cansado esperando; el chocolate «llama» con destellos."""
    d = K.D(img)
    for j in range(4):                                      # cola de siluetas
        x = 180 + j * 170
        d.ellipse([x - 50, 880, x + 50, 980], fill=(110, 120, 150))
        d.rounded_rectangle([x - 70, 980, x + 70, 1300], radius=40, fill=(110, 120, 150))
    solid(img, lambda Lr: candy_rack(Lr, 900, 1250, 0.9, t))
    k = clamp((t - lt(L, 0, 0.6)) / 0.3)
    if k > 0:
        FL.big(img, 740, 760, "¡CÓMPRAME!", int(64 * pop(k)) + 1, RED, k)
    FL.pill(img, 420, 720, "CANSADO + ESPERANDO", clamp((t - 0.3) / 0.3), col=(120, 120, 130))
    ojo(img, 760, 1780, 0.6, "think", t=t)


def listpaper(Lr, cx, cy, s, ticks):
    d = K.D(Lr)
    d.rectangle([cx - 200 * s, cy - 300 * s, cx + 200 * s, cy + 300 * s], fill=(255, 252, 236), outline=INK, width=6)
    for j in range(5):
        y = cy - 220 * s + j * 100 * s
        d.rectangle([cx - 160 * s, y - 22 * s, cx - 116 * s, y + 22 * s], outline=INK, width=4)
        d.line([(cx - 90 * s, y), (cx + 150 * s, y)], fill=(120, 120, 140), width=6)
        if j < ticks:
            d.line([(cx - 156 * s, y), (cx - 140 * s, y + 18 * s), (cx - 108 * s, y - 26 * s)], fill=GREEN, width=8)


def sh_truco(img, t, T, L):
    """El truco: una lista que se va tachando sola; Ojo guiña el ojo."""
    n = int(5 * ease(clamp((t - 0.3) / max(1.0, T - 0.6))))
    solid(img, lambda Lr: listpaper(Lr, 540, 960, 1.1, n))
    FL.stamp(img, 540, 480, "EL TRUCO", clamp(t / 0.3), col=GREEN)
    ojo(img, 880, 1760, 0.6, "smirk", t=t)


def _r_fruta(Lr, x, y, s):
    d = K.D(Lr)
    for j, col in enumerate(((230, 50, 50), (250, 150, 40), (110, 190, 70))):
        xx = x - 60 * s + j * 60 * s
        d.ellipse([xx - 34 * s, y - 34 * s, xx + 34 * s, y + 34 * s], fill=col, outline=INK, width=3)


def _r_pasillo(Lr, x, y, s):
    milk(Lr, x - 50 * s, y + 20 * s, 0.55 * s + 0.01)
    bread(Lr, x + 40 * s, y + 70 * s, 0.4 * s + 0.01)


def _r_caja(Lr, x, y, s):
    candy_rack(Lr, x, y + 100 * s, 0.4 * s + 0.01, 0)


def sh_answer(img, t, T, L):
    ks = [clamp((t - lt(L, 0, 0.15)) / 0.35), clamp((t - lt(L, 0, 0.45)) / 0.35), clamp((t - lt(L, 0, 0.7)) / 0.35)]
    pro.chain(img, t, [("FRUTA", GREEN), ("FONDO", (60, 130, 220)), ("CAJA", RED)], ks, y=1000, drawers=[_r_fruta, _r_pasillo, _r_caja])
    hook_text(img, [("¿POR QUÉ GASTAS MÁS?", False), ("ES UN RECORRIDO", True)], clamp((t - 0.1) / 0.4), y=480, size=76)
    ojo(img, 540, 1760, 0.6, "smirk", t=t)


# ------------------------------------------------------------------ subtítulos, emojis y montaje (de c20_dedos)
D.CAP_POS.update({"q": 1760, "fruta": 330, "humor": 330, "fondo": 1620, "recorrido": 1620, "carros": 330, "vacio": 1620,
                  "ojos": 330, "abajo": 330, "musica": 1600, "lenta": 330, "caja": 330, "cansado": 330, "answer": 1390, "truco": 1560})
D.EMOJI.update({"q": ["🛒"], "fruta": ["🍎", "🍊"], "humor": ["😄"], "fondo": ["🥛", "🍞"], "recorrido": ["🚶", "😩"],
                "carros": ["🛒", "📈"], "vacio": ["🤔"], "ojos": ["💸", "👀"], "abajo": ["⬇️", "💰"], "musica": ["🎵"],
                "lenta": ["🐢"], "caja": ["🧾", "🍫"], "cansado": ["🍬"], "answer": ["🧠"], "truco": ["📝"]})
CAPTION = D.CAPTION
NO_EMOJI = set(NAMES)
NARR = None
D.SCENE_BG.clear()
D.SCENE_BG.update({n: super_bg for n in NAMES})
pro.setup(globals(), OJO_TRAJE, super_bg().resize((W, H)), NAMES)


def _wrap(fn, name):
    def run(img, t, T, L):
        T_ = pro.NOW[0]
        D._bg(img, name, T_)
        dd = K.D(img)
        for i in range(10):                                  # destellos de las luces del techo (siempre algo moviéndose)
            x = (i * 131 + 40 * math.sin(T_ * 0.5 + i)) % W
            y = (i * 211 + T_ * 20) % 1500
            a = max(0.0, math.sin(T_ * 2 + i * 1.7))
            if a > 0.4:
                r = 10 * a
                dd.line([(x - r, y), (x + r, y)], fill=(255, 255, 255, int(200 * a)), width=3)
                dd.line([(x, y - r), (x, y + r)], fill=(255, 255, 255, int(200 * a)), width=3)
        fn(img, t, T, L)
        pro._stimuli(img, name, globals())
    return run


FNS = {n: _wrap(globals()["sh_" + n], n) for n in NAMES}
_base = FRAME


def FRAME(V, shots, chunks, total, i):
    if not D._SHOT_AT:
        for s in shots:
            D._SHOT_AT[s["name"]] = (s["start"], s["end"])
    return _base(V, shots, chunks, total, i)


OUTRO_MIN = 5.0
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
AUDIO = {"music": [("q", "lofi_hh")], "gains": {}, "amb": {},
         "sfx": [(0.05, "pop", 0.05), ("fruta+0.3", "pop", 0.04), ("humor+0.4", "ding", 0.04), ("fondo+0.3", "pop", 0.05),
                 ("recorrido+0.2", "tick", 0.04), ("carros+0.2", "pop", 0.05),
                 ("ojos+0.4", "ding", 0.04), ("musica+0.05", "pop", 0.07), ("caja+0.5", "ding", 0.04), ("answer+0.5", "ding", 0.06),
                 ("truco+0.1", "pop", 0.06)], "bpm": 96}
