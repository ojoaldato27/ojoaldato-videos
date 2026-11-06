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
TITLE = "22_Supermercado_PREVIA"
VOICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c22_super_prev.mp3")
LINES = [
    "El súper está diseñado para que compres cosas que no necesitas. ¡Y empieza en la puerta!",
    "Nada más entrar te encuentras la *fruta*. Colores vivos y olor a fresco. Y es a propósito.",
    "La idea es que entres de *buen humor* y con ganas de llenar el carro.",
    "Ahora fíjate en la *leche* y el *pan*. Casi siempre están al *fondo*.",
    "Para llegar hasta ellos tienes que cruzar la *tienda entera*. Pasillo a pasillo.",
]
OUTRO_LINE = "Y lo de los carros es todavía más descarado."
NAMES = ["q", "fruta", "humor", "fondo", "recorrido"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS, HYPE, FOLLOW, NARRATOR, PUSH = {}, None, None, {}, {}
NOTIF = ("humor", 0.4)
HEAD = {i: ("", "") for i in range(len(NAMES))}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
FL.use("minimal", HEAD)
FRAME = vid2.frame
FPS = 60
BG = (40, 46, 80)
TRANS_POOL = ["suave"]
TRANS_PLAN = ["suave", "deriva_r", "suave_out", "deriva"]
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


# ------------------------------------------------------------------ subtítulos, emojis y montaje (de c20_dedos)
D.CAP_POS.update({"q": 1760, "fruta": 330, "humor": 330, "fondo": 1620, "recorrido": 1620})
D.EMOJI.update({"q": ["🛒"], "fruta": ["🍎", "🍊"], "humor": ["😄"], "fondo": ["🥛", "🍞"], "recorrido": ["🚶", "😩"]})
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


OUTRO_MIN = 4.0
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
AUDIO = {"music": [("q", "lofi_hh")], "gains": {}, "amb": {},
         "sfx": [(0.05, "pop", 0.05), ("fruta+0.3", "pop", 0.04), ("humor+0.4", "ding", 0.04), ("fondo+0.3", "pop", 0.05),
                 ("recorrido+0.2", "tick", 0.04)], "bpm": 96}
