"""20 · Dedos arrugados — PREVISUALIZACIÓN del MANUAL v2.0 (gancho + 4 escenas, formato «TE HAN MENTIDO»).
Datos: las arrugas de los dedos en el agua las provoca el sistema nervioso (vasoconstricción bajo la piel), no la
absorción de agua: con el nervio del dedo cortado no aparecen (Lewis y Pickering, Clin Sci, años 30; se usa aún como
prueba clínica de nervio). Hipótesis del agarre en mojado: Changizi 2011, Kareklas 2013 (a favor), Haseleu 2014 (no lo replica).
Novedades v2: escenas a pantalla completa con fondo ilustrado (tipo Titanic pro), subtítulos en sitios distintos
con caja, emojis que saltan HACIA EL CENTRO con la palabra clave."""
import math
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED, txt
from PIL import Image, ImageDraw, ImageFilter
import os
import pro
from pro import solid, glow, ojo, hook_text, lt, WHITE

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "20_Dedos_prev"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c20_dedos_prev")
VOICE = _VZ + ".mp3"
LINES = [
    "Tus dedos no se arrugan por culpa del agua. ¡Es tu *cerebro* el que lo hace a propósito!",
    "Pasas diez minutos en la *bañera* y tus dedos acaban como *pasas*.",
    "Siempre nos han dicho que la piel se *empapa* como una *esponja*.",
    "Pero hace casi *cien años* unos médicos descubrieron algo rarísimo.",
    "A las personas con un *nervio cortado* en el dedo *no se les arrugaba*. Ni un poco.",
]
OUTRO_LINE = "Entonces, ¿quién arruga tus dedos? Lo que viene ahora te va a sorprender."
NAMES = ["q", "banera", "esponja", "medicos", "nervio"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("esponja", 0.6)
HEAD = {i: ("", "") for i in range(len(NAMES))}
NARRATOR = {}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {}
FL.use("minimal", HEAD)

FRAME = vid2.frame
FPS = 60
BG = (40, 46, 80)
TRANS_POOL = ["suave"]
TRANS_PLAN = ["suave", "deriva_r", "suave_out", "deriva"]
TRANS_SEED = 20
TD = 0.9
CAM_PUSH = 0.06
SHAKE = 0
CUT_SFX = False
FL.TH["narr"] = True
OJO_TRAJE = "c_biologo"
OJO_POSES = {}
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"

SKIN = (246, 204, 172)
WRK = (196, 120, 100)
WATER = (90, 170, 220)
GOLD = (236, 190, 60)
GREEN = (60, 170, 100)
NERVE = (255, 214, 60)
SEPIA = (120, 90, 60)
MARK = (240, 70, 40)

# ------------------------------------------------------------------ fondos ilustrados (pre-renderizados, con parallax)
BW, BH = int(W * 1.12), int(H * 1.12)
_BG = {}


def _vign(img, k=170):
    v = Image.new("L", img.size, 0)
    dv = ImageDraw.Draw(v)
    w, h = img.size
    for i in range(36):
        dv.rounded_rectangle([i * 7, i * 11, w - i * 7, h - i * 11], radius=90, outline=int(k * (1 - i / 36) ** 2), width=8)
    return Image.composite(Image.new("RGB", img.size, (18, 20, 30)), img, v.filter(ImageFilter.GaussianBlur(40)))


def bano():
    if "bano" in _BG:
        return _BG["bano"]
    img = Image.new("RGB", (BW, BH))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(BH):                                     # pared con luz cálida arriba
        u = y / BH
        d.line([(0, y), (BW, y)], fill=(int(lerp(214, 150, u)), int(lerp(232, 186, u)), int(lerp(236, 198, u))))
    for r, y in enumerate(range(-20, 1500, 92)):            # azulejos con brillo
        for x in range(-40, BW, 92):
            d.rounded_rectangle([x + 4, y + 4, x + 88, y + 88], radius=10, fill=(255, 255, 255, 34), outline=(120, 160, 170, 90), width=3)
            d.line([(x + 14, y + 18), (x + 40, y + 12)], fill=(255, 255, 255, 90), width=4)
    d.rounded_rectangle([760, 180, 1120, 640], radius=24, fill=(250, 246, 220), outline=(150, 130, 110), width=14)
    d.line([(940, 180), (940, 640)], fill=(150, 130, 110), width=10)
    d.line([(760, 410), (1120, 410)], fill=(150, 130, 110), width=10)
    for i in range(5):                                      # vaho en la ventana
        d.ellipse([780 + i * 60, 450 + (i % 2) * 60, 900 + i * 60, 600 + (i % 2) * 40], fill=(255, 255, 255, 70))
    d.rectangle([60, 560, 300, 580], fill=(170, 140, 110))   # toallero con toalla
    d.rounded_rectangle([90, 570, 270, 900], radius=18, fill=(236, 120, 110), outline=(150, 70, 60), width=6)
    for y in (800, 830):
        d.line([(90, y), (270, y)], fill=(255, 220, 210), width=8)
    d.rounded_rectangle([420, 260, 640, 520], radius=110, fill=(220, 236, 240), outline=(150, 170, 176), width=10)  # espejo
    d.rectangle([0, 1500, BW, BH], fill=(176, 150, 128))     # suelo de madera
    for x in range(0, BW, 160):
        d.line([(x, 1500), (x - 60, BH)], fill=(150, 124, 104), width=5)
    img = _vign(img.filter(ImageFilter.GaussianBlur(5)), 150)
    _BG["bano"] = img
    return img


def hospital():
    if "hosp" in _BG:
        return _BG["hosp"]
    img = Image.new("RGB", (BW, BH))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(BH):
        u = y / BH
        d.line([(0, y), (BW, y)], fill=(int(lerp(226, 150, u)), int(lerp(206, 124, u)), int(lerp(170, 92, u))))
    d.rectangle([0, 1120, BW, 1170], fill=(130, 96, 66))     # zócalo
    for x in range(0, BW, 70):
        d.line([(x, 1170), (x, 1500)], fill=(150, 112, 78, 120), width=4)
    d.rectangle([0, 1500, BW, BH], fill=(110, 80, 56))
    d.rounded_rectangle([80, 300, 420, 1120], radius=10, fill=(150, 112, 76), outline=(90, 64, 44), width=10)  # vitrina
    for y in (500, 700, 900):
        d.line([(90, y), (410, y)], fill=(90, 64, 44), width=8)
        for j in range(4):
            d.rounded_rectangle([110 + j * 75, y - 90, 160 + j * 75, y - 4], radius=10, fill=(210, 230, 220, 160), outline=(90, 70, 50), width=3)
    d.line([(800, 0), (800, 240)], fill=(70, 50, 36), width=6)  # lámpara antigua
    d.chord([680, 200, 920, 380], 180, 360, fill=(70, 90, 70), outline=(40, 40, 30), width=6)
    d.rounded_rectangle([640, 820, 1120, 1120], radius=6, fill=(140, 100, 66), outline=(90, 64, 44), width=8)  # mesa
    img = _vign(img.filter(ImageFilter.GaussianBlur(5)), 190)
    _BG["hosp"] = img
    return img


SCENE_BG = {"q": bano, "banera": bano, "esponja": bano, "medicos": hospital, "nervio": hospital}


def _bg(img, name, T):
    b = SCENE_BG[name]()
    ox = (BW - W) / 2 + 46 * math.sin(T * 0.21)
    oy = (BH - H) / 2 + 30 * math.sin(T * 0.16 + 1.0)
    img.paste(b.crop((int(ox), int(oy), int(ox) + W, int(oy) + H)), (0, 0))


def _air(img, name, T):
    """Algo siempre en movimiento: vapor y burbujas en el baño; polvo dorado en el hospital."""
    if SCENE_BG[name] is bano:
        for i in range(9):
            sp = 26 + (i * 19) % 30
            x = (i * 137 + 60 + 50 * math.sin(T * 0.5 + i)) % W
            y = 1700 - ((T * sp + i * 211) % 1500)
            glow(img, x, y, 90 + (i % 3) * 30, 70, (255, 255, 255), 0.18)
        d = K.D(img)
        for i in range(8):
            x = (i * 151 + 40 + 20 * math.sin(T * 1.7 + i)) % W
            y = 1800 - ((T * (60 + i * 9) + i * 173) % 1400)
            r = 8 + (i % 4) * 5
            d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, 150), width=3)
            d.ellipse([x - r * 0.4, y - r * 0.6, x, y - r * 0.2], fill=(255, 255, 255, 170))
    else:
        d = K.D(img)
        for i in range(22):
            x = (i * 97 + 30 * math.sin(T * 0.6 + i)) % W
            y = (i * 181 + T * (14 + i % 5 * 4)) % H
            a = int(110 + 80 * math.sin(T * 2 + i))
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 236, 190, max(0, a)))


# ------------------------------------------------------------------ piezas
def capsule(d, p0, p1, r, fill, outline=INK, w=6):
    ux, uy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(ux, uy) or 1
    ux, uy = ux / ln, uy / ln
    nx, ny = -uy, ux
    pts = []
    a0 = math.atan2(ny, nx)
    for j in range(13):                                     # punta
        a = a0 - math.pi * j / 12
        pts.append((p1[0] + r * math.cos(a), p1[1] + r * math.sin(a)))
    for j in range(13):                                     # base
        a = a0 + math.pi - math.pi * j / 12
        pts.append((p0[0] + r * math.cos(a), p0[1] + r * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline, width=w)


def _fingers(cx, cy, s):
    out = []
    for bx, ln, ang in ((-105, 232, -0.13), (-35, 272, -0.04), (35, 258, 0.04), (105, 204, 0.13)):
        p0 = (cx + bx * s, cy)
        p1 = (p0[0] + math.sin(ang) * ln * s, p0[1] - math.cos(ang) * ln * s)
        out.append((p0, p1))
    tb = (cx - 118 * s, cy + 160 * s)
    out.append((tb, (tb[0] - 118 * s, tb[1] - 160 * s)))
    return out


def hand(Lr, cx, cy, s=1.0, wr=0.0, t=0.0, nerve=None):
    """Mano abierta, dedos hacia arriba. wr 0..1 = arrugas en las yemas. nerve = (k_dibujo, cortado 0..1)."""
    d = K.D(Lr)
    w = max(3, int(6 * s))
    tip = tuple(int(lerp(a, b, wr * 0.5)) for a, b in zip(SKIN, (236, 176, 160)))
    d.rounded_rectangle([cx - 110 * s, cy + 200 * s, cx + 110 * s, cy + 560 * s], radius=int(40 * s), fill=SKIN, outline=INK, width=w)
    fs = _fingers(cx, cy, s)
    for p0, p1 in fs:
        capsule(d, p0, p1, 36 * s, SKIN, INK, w)
    d.rounded_rectangle([cx - 145 * s, cy - 40 * s, cx + 145 * s, cy + 270 * s], radius=int(95 * s), fill=SKIN, outline=INK, width=w)
    d.rectangle([cx - 136 * s, cy - 34 * s, cx + 136 * s, cy + 6 * s], fill=SKIN)
    for p0, p1 in fs:
        ux, uy = p1[0] - p0[0], p1[1] - p0[1]
        nx, ny = -uy, ux
        ln = math.hypot(nx, ny) or 1
        nx, ny = nx / ln, ny / ln
        tx, ty = p0[0] + ux * 0.86, p0[1] + uy * 0.86          # yema más rosada
        d.ellipse([tx - 30 * s, ty - 34 * s, tx + 30 * s, ty + 34 * s], fill=tip)
        for f in (0.45,):                                       # pliegue de nudillo
            mx, my = p0[0] + ux * f, p0[1] + uy * f
            d.line([(mx - nx * 18 * s, my - ny * 18 * s), (mx + nx * 18 * s, my + ny * 18 * s)], fill=(200, 150, 120), width=max(2, int(4 * s)))
        nxp, nyp = p0[0] + ux * 0.97, p0[1] + uy * 0.97         # uña
        d.ellipse([nxp - 18 * s, nyp - 10 * s, nxp + 18 * s, nyp + 18 * s], fill=(252, 228, 218), outline=(200, 150, 130), width=max(2, int(3 * s)))
        if wr > 0.02:                                          # arrugas: ondas que crecen
            for j in range(5):
                f = 0.64 + j * 0.065
                mx, my = p0[0] + ux * f, p0[1] + uy * f
                pts = []
                for q in range(9):
                    v = (q / 8 - 0.5) * 2
                    amp = 7 * s * wr * math.sin(q * 1.7 + j)
                    pts.append((mx + nx * v * 27 * s + ux / (ln or 1) * amp, my + ny * v * 27 * s + uy / (ln or 1) * amp))
                d.line(pts, fill=WRK + (int(230 * clamp(wr * 1.4)),), width=max(2, int(4 * s)))
    d.arc([cx - 90 * s, cy + 60 * s, cx + 60 * s, cy + 200 * s], 200, 330, fill=(200, 150, 120), width=max(2, int(4 * s)))
    if nerve:
        kd, cut = nerve
        p0, p1 = fs[1]
        path = [(cx + 10 * s, cy + 540 * s), (cx, cy + 260 * s), (cx - 20 * s, cy + 80 * s), p0, (p0[0] + (p1[0] - p0[0]) * 0.8, p0[1] + (p1[1] - p0[1]) * 0.8)]
        e = _poly_k(d, path, kd, NERVE + (240,), max(4, int(10 * s)))
        if cut > 0:
            x, y = cx - 5 * s, cy + 300 * s
            r = 46 * s * pop(cut)
            d.line([(x - r, y - r), (x + r, y + r)], fill=RED, width=max(5, int(14 * s)))
            d.line([(x + r, y - r), (x - r, y + r)], fill=RED, width=max(5, int(14 * s)))


def _poly_k(d, pts, k, col, w):
    segs = list(zip(pts, pts[1:]))
    tot = sum(math.dist(a, b) for a, b in segs)
    s = tot * clamp(k)
    e = pts[0]
    for a, b in segs:
        ln = math.dist(a, b)
        if s <= 0:
            break
        u = min(1.0, s / ln)
        e = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
        d.line([a, e], fill=col, width=w)
        s -= ln
    return e


def water(img, y0, t, x0=0, x1=W, a=150):
    d = K.D(img)
    top = [(x, y0 + 12 * math.sin(x / 70 + t * 2.2) + 6 * math.sin(x / 31 - t * 3)) for x in range(int(x0), int(x1) + 20, 20)]
    d.polygon(top + [(x1, H), (x0, H)], fill=WATER + (a,))
    d.line(top, fill=(255, 255, 255, 200), width=6)
    for i in range(5):
        x = x0 + (i * 211 + t * 40) % max(1, (x1 - x0))
        d.line([(x, y0 + 40 + i * 30), (x + 70, y0 + 40 + i * 30)], fill=(255, 255, 255, 90), width=4)


def drops(img, pts, t, period=1.1):
    d = K.D(img)
    for j, (x, y) in enumerate(pts):
        u = ((t + j * 0.37) % period) / period
        yy = y + 420 * u * u
        a = int(230 * (1 - u))
        d.polygon([(x, yy - 22), (x + 12, yy), (x, yy + 12), (x - 12, yy)], fill=(140, 200, 240, a), outline=(40, 90, 140, a))


def brain(Lr, cx, cy, s=1.0, pulse=0.0):
    d = K.D(Lr)
    col = (246, 160, 180)
    d.ellipse([cx - 150 * s, cy - 100 * s, cx + 150 * s, cy + 100 * s], fill=col, outline=INK, width=max(3, int(7 * s)))
    d.line([(cx, cy - 96 * s), (cx, cy + 90 * s)], fill=(200, 100, 130), width=max(2, int(5 * s)))
    for j in range(6):
        x = cx + (-120 + j * 48) * s
        d.arc([x - 34 * s, cy - 70 * s, x + 34 * s, cy - 10 * s], 180, 360, fill=(200, 100, 130), width=max(2, int(5 * s)))
        d.arc([x - 30 * s, cy + 0 * s, x + 30 * s, cy + 60 * s], 0, 180, fill=(200, 100, 130), width=max(2, int(5 * s)))
    d.rounded_rectangle([cx - 20 * s, cy + 80 * s, cx + 20 * s, cy + 150 * s], radius=int(14 * s), fill=col, outline=INK, width=max(3, int(6 * s)))


def signal(img, a, b, t, n=5, col=NERVE):
    """Impulsos eléctricos que viajan del cerebro a la mano por una curva."""
    mx, my = (a[0] + b[0]) / 2 + 160, (a[1] + b[1]) / 2
    d = K.D(img)
    pts = []
    for j in range(31):
        u = j / 30
        pts.append(((1 - u) ** 2 * a[0] + 2 * (1 - u) * u * mx + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * my + u * u * b[1]))
    for j in range(0, 30, 2):
        d.line([pts[j], pts[j + 1]], fill=col + (140,), width=6)
    for k in range(n):
        u = ((t * 0.9 + k / n) % 1.0)
        i = int(u * 29)
        x, y = pts[i]
        glow(img, x, y, 34, 34, col, 0.9)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 255, 255))


def raisin(Lr, cx, cy, s=1.0):
    d = K.D(Lr)
    d.ellipse([cx - 90 * s, cy - 70 * s, cx + 90 * s, cy + 70 * s], fill=(110, 60, 70), outline=INK, width=max(3, int(6 * s)))
    for j in range(5):
        x = cx + (-60 + j * 30) * s
        d.arc([x - 30 * s, cy - 50 * s, x + 30 * s, cy + 50 * s], 250, 330 + j * 4, fill=(70, 30, 40), width=max(2, int(5 * s)))
    d.ellipse([cx - 50 * s, cy - 50 * s, cx - 10 * s, cy - 30 * s], fill=(170, 110, 120))


def tub_front(img, y, t):
    d = K.D(img)
    d.rounded_rectangle([-40, y, W + 40, H + 60], radius=120, fill=(250, 250, 252), outline=INK, width=8)
    for j in range(12):                                     # volumen: sombra que baja
        d.rectangle([0, y + 60 + j * 40, W, y + 100 + j * 40], fill=(120, 150, 180, 6 + j * 5))
    d.line([(60, y + 40), (W - 60, y + 40)], fill=(220, 226, 232), width=10)
    d.rounded_rectangle([80, y + 90, 240, y + 300], radius=40, fill=(255, 255, 255, 120))
    for i in range(6):                                      # burbujas que suben por delante
        bx = (i * 191 + 80 + 30 * math.sin(t + i)) % W
        by = H - ((t * (70 + i * 12) + i * 97) % (H - y))
        r = 14 + (i % 3) * 8
        d.ellipse([bx - r, by - r, bx + r, by + r], outline=(150, 190, 220, 200), width=4)
    for i in range(14):                                     # espuma en el borde
        x = i * 84 + 20 * math.sin(t * 1.5 + i)
        r = 40 + 14 * math.sin(i * 2.1 + t)
        d.ellipse([x - r, y - r * 0.9, x + r, y + r * 0.5], fill=(255, 255, 255, 240), outline=(200, 214, 226), width=3)


def duck(Lr, cx, cy, s=1.0):
    d = K.D(Lr)
    d.ellipse([cx - 80 * s, cy - 30 * s, cx + 80 * s, cy + 60 * s], fill=(255, 210, 50), outline=INK, width=6)
    d.ellipse([cx + 10 * s, cy - 100 * s, cx + 90 * s, cy - 20 * s], fill=(255, 210, 50), outline=INK, width=6)
    d.polygon([(cx + 86 * s, cy - 66 * s), (cx + 130 * s, cy - 56 * s), (cx + 86 * s, cy - 44 * s)], fill=(250, 130, 40), outline=INK)
    d.ellipse([cx + 48 * s, cy - 76 * s, cx + 62 * s, cy - 62 * s], fill=INK)


def clock(img, cx, cy, mins, k=1.0):
    d = K.D(img)
    r = 110 * pop(k)
    if r < 20:
        return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 240), outline=INK, width=8)
    a = -math.pi / 2 + mins / 10 * 2 * math.pi
    d.pieslice([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], -90, -90 + mins * 36, fill=(90, 170, 220, 120))
    d.line([(cx, cy), (cx + 0.78 * r * math.cos(a), cy + 0.78 * r * math.sin(a))], fill=INK, width=8)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    FL.big(img, cx, cy + r + 50, f"{int(mins)} MIN", 56, WHITE, k)


def sponge(Lr, cx, cy, s=1.0, wet=0.0):
    d = K.D(Lr)
    col = tuple(int(lerp(a, b, wet)) for a, b in zip((255, 220, 90), (230, 186, 60)))
    w, h = 260 * s * (1 + 0.06 * wet), 160 * s * (1 + 0.1 * wet)
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=int(46 * s), fill=col, outline=INK, width=7)
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy - h + 60 * s], radius=int(30 * s), fill=(80, 170, 90), outline=INK, width=7)
    for j in range(16):
        x = cx + ((j * 97) % int(2 * w - 60) - w + 30)
        y = cy + ((j * 53) % int(2 * h - 120) - h + 90)
        r = (10 + (j % 3) * 7) * s
        d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 160, 40))


def doctor(Lr, cx, cy, s=1.0, t=0.0):
    """Médico antiguo en sepia: bata, gafas redondas, bigote y libreta."""
    d = K.D(Lr)
    d.rounded_rectangle([cx - 150 * s, cy, cx + 150 * s, cy + 420 * s], radius=int(60 * s), fill=(246, 236, 214), outline=INK, width=7)
    d.polygon([(cx - 40 * s, cy), (cx, cy + 90 * s), (cx + 40 * s, cy)], fill=(90, 70, 50))
    d.ellipse([cx - 100 * s, cy - 210 * s, cx + 100 * s, cy + 10 * s], fill=(236, 200, 160), outline=INK, width=7)
    d.chord([cx - 104 * s, cy - 220 * s, cx + 104 * s, cy - 80 * s], 180, 360, fill=(110, 90, 70))
    for sx in (-1, 1):
        ex = cx + sx * 42 * s
        d.ellipse([ex - 30 * s, cy - 130 * s, ex + 30 * s, cy - 70 * s], outline=INK, width=6)
        blink = 1 if (t % 3.1) < 0.12 else 0
        if not blink:
            d.ellipse([ex - 7 * s, cy - 107 * s, ex + 7 * s, cy - 93 * s], fill=INK)
    d.line([(cx - 12 * s, cy - 100 * s), (cx + 12 * s, cy - 100 * s)], fill=INK, width=5)
    d.chord([cx - 60 * s, cy - 60 * s, cx + 60 * s, cy - 10 * s], 180, 360, fill=(90, 70, 50))
    wr = 6 * math.sin(t * 5)
    d.rounded_rectangle([cx + 40 * s, cy + 140 * s, cx + 190 * s, cy + 330 * s], radius=10, fill=(250, 244, 226), outline=INK, width=6)
    for j in range(5):
        d.line([(cx + 60 * s, cy + (170 + j * 30) * s), (cx + (160 + wr * (j == 4)) * s, cy + (170 + j * 30) * s)], fill=(140, 120, 100), width=4)
    d.arc([cx - 80 * s, cy + 20 * s, cx + 20 * s, cy + 200 * s], 90, 270, fill=(60, 60, 70), width=7)   # fonendo


def basin(img, cx, y, w=420):
    d = K.D(img)
    d.chord([cx - w / 2, y - 120, cx + w / 2, y + 200], 0, 180, fill=(236, 240, 244), outline=INK, width=8)
    d.ellipse([cx - w / 2, y - 40, cx + w / 2, y + 40], fill=(110, 170, 210, 200), outline=INK, width=8)


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    """GANCHO: mano gigante sale del agua y las yemas se arrugan EN DIRECTO; un cerebro manda impulsos a la mano."""
    wr = 0.2 + 0.8 * ease(clamp(t / 2.2))
    rise = 60 * (1 - ease(clamp(t / 0.8)))
    solid(img, lambda Lr: hand(Lr, 470, 980 + rise, 1.25, wr, t))
    fs = _fingers(470, 980 + rise, 1.25)
    drops(img, [p1 for _, p1 in fs[:4]], t)
    water(img, 1360, t)
    bk = pop(clamp((t - lt(L, 0, 0.6)) / 0.35))
    if bk > 0:
        solid(img, lambda Lr: brain(Lr, 860, 700, 0.75 * bk), sh=0.25)
        glow(img, 860, 700, 170, 130, (255, 150, 190), 0.35 + 0.2 * math.sin(t * 8))
        signal(img, (800, 790), fs[1][1], t)
    ojo(img, 880, 1520, 0.65, "surprise", t=t)
    hook_text(img, [("NO ES EL AGUA", False), ("ES TU CEREBRO", True)], 1.0 if t < T - 0.6 else clamp((T - t) / 0.6), y=330, size=100)


def sh_banera(img, t, T, L):
    """Ojo en la bañera con el patito; reloj 0→10 min; lupa a la yema que se convierte en pasa."""
    ojo(img, 300, 1700 + 10 * math.sin(t * 2), 0.95, "smirk", t=t)
    tub_front(img, 1460, t)
    solid(img, lambda Lr: duck(Lr, 760 + 30 * math.sin(t * 1.2), 1390 + 12 * math.sin(t * 2.4), 1.0), sh=0.2)
    m = 10 * ease(clamp(t / max(1.0, lt(L, 0, 0.55))))
    clock(img, 850, 560, m, clamp(t / 0.3))
    wr = clamp(m / 10)
    cx, cy, r = 300, 720, 190
    lens = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = K.D(lens)
    ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))
    capsule(ld, (cx, cy + 260), (cx, cy - 90), 125, tuple(int(lerp(a, b, wr * 0.5)) for a, b in zip(SKIN, (236, 176, 160))), INK, 7)
    for j in range(7):
        y = cy - 120 + j * 34
        ld.line([(cx - 110 + q * 27.5, y + 13 * wr * math.sin(q * 1.6 + j)) for q in range(9)], fill=WRK + (int(250 * wr),), width=7)
    m_ = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m_).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    lens.putalpha(Image.composite(lens.getchannel("A"), m_, m_))
    d = K.D(img)
    d.line([(cx + 140, cy + 140), (cx + 250, cy + 250)], fill=INK, width=26)
    img.paste(lens, (0, 0), lens)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=10)
    k = clamp((t - lt(L, 0, 0.6)) / 0.4)
    if k > 0:
        FL.big(img, 590, 860, "=", 120, WHITE, k)
        solid(img, lambda Lr: raisin(Lr, 820, 900, 1.3 * pop(k)), sh=0.3)
        FL.pill(img, 820, 1060, "PASA", k, col=(110, 60, 70))


def sh_esponja(img, t, T, L):
    """La explicación de toda la vida: la piel como esponja que chupa agua (con interrogante creciendo)."""
    wet = ease(clamp(t / 2.0))
    solid(img, lambda Lr: sponge(Lr, 540, 900, 1.15, wet))
    drops(img, [(380, 520), (540, 480), (700, 520), (460, 440), (620, 450)], t, 0.9)
    d = K.D(img)
    for j in range(3):                                       # flechas de «agua entra»
        y = 620 + j * 20
        x = 300 + j * 240
        u = (t * 1.4 + j * 0.3) % 1.0
        d.line([(x, y - 80 + 80 * u), (x, y + 40 * u)], fill=(60, 140, 210, 220), width=10)
        d.polygon([(x - 22, y + 40 * u), (x + 22, y + 40 * u), (x, y + 30 + 40 * u)], fill=(60, 140, 210, 220))
    FL.pill(img, 540, 1160, "LA PIEL «CHUPA» AGUA", clamp((t - lt(L, 0, 0.5)) / 0.3), col=(60, 140, 210))
    q = clamp((t - lt(L, 0, 0.92)) / 0.3)
    if q > 0:
        FL.big(img, 900, 560 + 10 * math.sin(t * 4), "?", int(220 * pop(q)) + 1, RED, q)
    ojo(img, 200, 1560, 0.6, "think", t=t)


def sh_medicos(img, t, T, L):
    """«PERO OJO»: viaje al pasado — contador de años que baja y un médico antiguo tomando notas."""
    if t < 1.3:
        FL.stamp(img, 540, 400, "PERO OJO", clamp(t / 0.3) * clamp((1.3 - t) / 0.25), col=RED)
    k = clamp((t - 1.3) / 1.0)
    yr = int(lerp(2026, 1930, ease(k)))
    if k > 0:
        FL.big(img, 540, 400, str(yr) if k < 1 else "AÑOS 30", 130, GOLD, clamp(k * 3))
    d = K.D(img)
    fx, fy = 540, 1000
    d.rounded_rectangle([fx - 280, fy - 360, fx + 280, fy + 330], radius=12, fill=(232, 214, 180), outline=(90, 64, 44), width=16)
    solid(img, lambda Lr: doctor(Lr, fx - 30, fy - 120, 0.95, t), sh=0.2)
    for i in range(10):                                    # grano de película antigua
        x = (i * 113 + int(t * 600) * 7) % 560 + fx - 280
        y = (i * 197 + int(t * 600) * 13) % 690 + fy - 360
        d.line([(x, y), (x + 2, y + 18)], fill=(80, 60, 40, 90), width=2)
    ojo(img, 900, 1600, 0.6, "think", t=t)


def sh_nervio(img, t, T, L):
    """Dos manos en dos palanganas: la del nervio sano se arruga; la del nervio cortado se queda LISA."""
    wr = ease(clamp((t - 0.6) / 1.6))
    cut = clamp((t - lt(L, 0, 0.3)) / 0.3)
    solid(img, lambda Lr: hand(Lr, 290, 800, 0.8, wr, t, nerve=(clamp(t / 0.6), 0.0)))
    solid(img, lambda Lr: hand(Lr, 790, 800, 0.8, 0.0, t, nerve=(clamp(t / 0.6), cut)))
    basin(img, 290, 1240)
    basin(img, 790, 1240)
    FL.pill(img, 290, 600, "NERVIO SANO", clamp((t - 0.2) / 0.3), col=GREEN)
    FL.pill(img, 790, 600, "NERVIO CORTADO", cut, col=RED)
    k = clamp((t - lt(L, 0, 0.75)) / 0.3)
    if k > 0:
        FL.big(img, 790, 1440, "¡LISO!", int(110 * pop(k)) + 1, WHITE, k)
        glow(img, 790, 700, 160, 200, (255, 255, 255), 0.3 * k)
    ojo(img, 540, 1720, 0.6, "surprise" if k > 0 else "point", t=t)


# ------------------------------------------------------------------ subtítulos v2: caja, sitio distinto por escena y emoji hacia el centro
CAP_POS = {"q": 1760, "banera": 300, "esponja": 1330, "medicos": 1760, "nervio": 300}
EMOJI = {"q": ["🧠"], "banera": ["🛁", "🍇"], "esponja": ["💧", "🧽"], "medicos": ["⏳"], "nervio": ["✂️", "😱"]}
NO_EMOJI = set(NAMES)                     # los emojis los saca el subtítulo, no pro._stimuli
_SHOT_AT = {}


def _shot_name(t):
    for n, (a, b) in _SHOT_AT.items():
        if a <= t < b:
            return n
    return "q"


def CAPTION(img, t, chunks, y=1580):
    cur = next((c for c in chunks if c[0] - 0.02 <= t < c[1]), None)
    if not cur:
        return
    t0, t1, words = cur
    name = _shot_name(t0 + 0.05)
    yy = CAP_POS.get(name, 1700)
    d = ImageDraw.Draw(img, "RGBA")
    size = 74
    while True:
        fo = F(FL.TH["cap"][0], size)
        sp = d.textlength(" ", font=fo)
        tw = sum(d.textlength(w, font=fo) + (32 if hl else 0) for w, hl, a, b in words) + sp * (len(words) - 1)
        if tw <= 940 or size <= 36:
            break
        size -= 6
    kin = ease(clamp((t - t0 + 0.04) / 0.18))
    bx0, bx1 = W / 2 - tw / 2 - 34, W / 2 + tw / 2 + 34
    by0, by1 = yy - size * 0.95 + (1 - kin) * 16, yy + size * 0.85 + (1 - kin) * 16
    d.rounded_rectangle([bx0 + 8, by0 + 12, bx1 + 8, by1 + 12], radius=36, fill=(10, 14, 30, int(70 * kin)))
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=36, fill=(255, 255, 255, int(238 * kin)))
    x = W / 2 - tw / 2
    hl_i = 0
    emo = EMOJI.get(name, ["👀"])
    for j, (w, hl, a, b) in enumerate(words):
        ww = d.textlength(w, font=fo)
        if t >= a - 0.04:
            k = ease(clamp((t - a + 0.04) / 0.12))
            if hl:
                x0, x1 = x, x + ww + 32
                y0, y1 = yy - size * 0.62, yy + size * 0.52
                xr = x0 + (x1 - x0) * clamp(k * 1.25)
                d.polygon([(x0 + 6, y0), (xr, y0 - 4), (xr - 6, y1), (x0, y1 + 4)], fill=MARK)
                d.text((x + 16, yy + (1 - k) * 10), w, font=fo, fill=(255, 255, 255), anchor="lm")
                u = (t - a) / 1.1                                   # emoji: salta desde el lado HACIA EL CENTRO
                if 0 <= u < 1:
                    side = -1 if hl_i % 2 == 0 else 1
                    sx, sy = 540 + side * 470, yy - 40
                    ex, ey = 540 + side * 150, yy - size - 120
                    e_ = ease(clamp(u / 0.45))
                    px, py = lerp(sx, ex, e_), lerp(sy, ey, e_) - 90 * math.sin(math.pi * clamp(u / 0.45))
                    im = pro._emoji(emo[hl_i % len(emo)], int(140 * pop(clamp(u * 3))) + 1)
                    al = 1 - clamp((u - 0.75) / 0.25)
                    if al < 1:
                        im.putalpha(im.getchannel("A").point(lambda v: int(v * al)))
                    img.paste(im, (int(px - im.width / 2), int(py - im.height / 2)), im)
            else:
                d.text((x, yy + (1 - k) * 14), w, font=fo, fill=(28, 28, 32), anchor="lm")
        if hl:
            hl_i += 1
        x += ww + (32 if hl else 0) + sp


# ------------------------------------------------------------------ montaje
NARR = None
pro.setup(globals(), OJO_TRAJE, bano().resize((W, H)), NAMES)


def _wrap(fn, name):
    def run(img, t, T, L):
        T_ = pro.NOW[0]
        _BG and None
        _bg(img, name, T_)
        _air(img, name, T_)
        fn(img, t, T, L)
        pro._stimuli(img, name, globals())
    return run


FNS = {n: _wrap(globals()["sh_" + n], n) for n in NAMES}
_base = FRAME


def FRAME(V, shots, chunks, total, i):
    if not _SHOT_AT:
        for s in shots:
            _SHOT_AT[s["name"]] = (s["start"], s["end"])
    return _base(V, shots, chunks, total, i)


OUTRO_MIN = 5.0
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
AUDIO = {
    "music": [("q", "playful")],
    "gains": {},
    "amb": {},
    "sfx": [(0.05, "pop", 0.05), ("q+1.6", "ding", 0.04), ("banera+0.3", "pop", 0.05), ("esponja+0.4", "pop", 0.04),
            ("medicos+0.05", "pop", 0.07), ("nervio+0.3", "click", 0.05)],
    "bpm": 104,
}
