"""21 · Un estornudo a cámara superlenta — formato «EN 1 SEGUNDO #1» (manual v2). PREVIA (gancho + 4 escenas).
Base de piezas: c20_dedos.py (import D). Datos: la velocidad de «160 km/h» es un mito muy repetido; medido con cámaras de alta
velocidad, el aire sale a unos 4–5 m/s (≈16 km/h, Tang et al., PLoS ONE 2013); la nube turbulenta lleva gotitas hasta 7–8 m
(Bourouiba, MIT, JAMA 2020). Estornudar con los ojos abiertos es muy difícil (reflejo), pero no imposible: decir «casi nadie».
GUION COMPLETO (para el vídeo entero, tras el sí de Iker):
  Gancho · superlenta · nariz detecta · coger aire · ojos se cierran · [re-gancho] el golpe: diafragma y pecho aprietan ·
  la lengua tapa la boca y todo sale por nariz y boca · ¿160 km/h? MITO: unos 16, como una bici · [giro] pero la nube viaja
  hasta 8 metros, como dos coches en fila · gotitas grandes caen en 1–2 m, las pequeñas flotan minutos · por eso el codo ·
  respuesta: no es rápido, es LEJOS · reflexión + despedida.
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
TITLE = "21_Estornudo"
VOICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c21_estornudo.mp3")
LINES = [
    "Un estornudo no sale a ciento sesenta kilómetros por hora. ¡Pero llega mucho más lejos de lo que crees!",
    "Vamos a verlo a *cámara superlenta*. Todo pasa en menos de *un segundo*.",
    "Primero tu *nariz* nota algo que no le gusta. *Polvo*, polen o un virus.",
    "Tu cerebro da la orden y *coges aire*. Mucho aire.",
    "Y los ojos se cierran solos. Casi nadie es capaz de estornudar con los *ojos abiertos*.",
    "Y ahora viene el golpe. El pecho y la barriga *aprietan* de golpe.",
    "El aire sale disparado por la *nariz* y por la *boca* a la vez.",
    "¿Y la famosa velocidad de ciento sesenta kilómetros por hora? Es un *mito*.",
    "Medido con cámaras superlentas sale a unos *dieciséis*. Más o menos como una *bici*.",
    "Pero aquí viene lo raro. Lo que sale no es solo un chorro. Es una *nube*.",
    "Esa nube puede llevar gotitas hasta *ocho metros*. Como dos coches en fila.",
    "Las gotas *grandes* caen al suelo en un par de metros.",
    "Pero las *pequeñas* se quedan flotando en el aire durante *minutos*.",
    "Por eso es mejor estornudar en el *codo*. Frena la nube antes de que despegue.",
    "Así que un estornudo no es tan rápido. Lo peligroso es *lo lejos* que llega.",
]
OUTRO_LINE = "La próxima vez que alguien estornude cerca, ya sabes lo que viaja hacia ti. Sígueme para más. ¡Ojo al dato!"
NAMES = ["q", "lenta", "nariz", "aire", "ojos", "golpe", "salida", "mito", "bici", "nube", "lejos", "grandes", "pequenas", "codo", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS, HYPE, FOLLOW, NARRATOR, PUSH = {}, None, None, {}, {}
NOTIF = ("bici", 0.3)
HEAD = {i: ("", "") for i in range(len(NAMES))}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
FL.use("minimal", HEAD)
FRAME = vid2.frame
FPS = 60
BG = (20, 24, 40)
TRANS_POOL = ["suave"]
TRANS_PLAN = ["suave", "deriva_r", "suave_out", "deriva"] * 4
TRANS_SEED = 21
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
SKIN = D.SKIN
DROP = (150, 210, 255)


# ------------------------------------------------------------------ fondo: estudio de cámara superlenta
def estudio():
    if "estudio" in D._BG:
        return D._BG["estudio"]
    img = Image.new("RGB", (D.BW, D.BH))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(D.BH):
        u = y / D.BH
        d.line([(0, y), (D.BW, y)], fill=(int(lerp(40, 14, u)), int(lerp(46, 18, u)), int(lerp(72, 34, u))))
    for x in range(0, D.BW, 90):
        d.line([(x, 0), (x, D.BH)], fill=(90, 110, 160, 50), width=2)
    for y in range(0, D.BH, 90):
        d.line([(0, y), (D.BW, y)], fill=(90, 110, 160, 50), width=2)
    for x in (140, 1050):                                   # focos de estudio
        d.polygon([(x - 50, 0), (x + 50, 0), (x + 260 * (1 if x < 600 else -1), 1500), (x - 160 * (1 if x < 600 else -1), 1500)], fill=(255, 250, 220, 22))
    img = D._vign(img.filter(ImageFilter.GaussianBlur(4)), 210)
    D._BG["estudio"] = img
    return img


# ------------------------------------------------------------------ piezas
def head_side(Lr, cx, cy, s=1.0, mouth=0.0, eyes=0.0, puff=0.0):
    """Cabeza de perfil mirando a la derecha. mouth 0..1 abre la boca, eyes 0..1 cierra los ojos, puff hincha el pecho."""
    d = K.D(Lr)
    w = max(3, int(7 * s))
    d.rounded_rectangle([cx - 150 * s, cy + 150 * s, cx + 120 * s, cy + 560 * s], radius=int(80 * s), fill=(90, 150, 220), outline=INK, width=w)
    d.ellipse([cx - 120 * s - 30 * s * puff, cy + 200 * s, cx + 90 * s + 30 * s * puff, cy + 420 * s], fill=(110, 170, 235))
    d.rectangle([cx - 50 * s, cy + 100 * s, cx + 40 * s, cy + 180 * s], fill=SKIN, outline=INK, width=w)
    d.ellipse([cx - 170 * s, cy - 200 * s, cx + 150 * s, cy + 150 * s], fill=SKIN, outline=INK, width=w)
    d.chord([cx - 180 * s, cy - 215 * s, cx + 150 * s, cy - 10 * s], 180, 330, fill=(80, 50, 40))
    d.polygon([(cx + 140 * s, cy - 40 * s), (cx + 215 * s, cy + 30 * s), (cx + 140 * s, cy + 46 * s)], fill=SKIN, outline=INK)
    ey = cy - 50 * s
    h = 20 * s * (1 - eyes)
    if h > 2:
        d.ellipse([cx + 60 * s, ey - h, cx + 100 * s, ey + h], fill=WHITE, outline=INK, width=4)
        d.ellipse([cx + 78 * s, ey - h * 0.6, cx + 96 * s, ey + h * 0.6], fill=INK)
    else:
        d.arc([cx + 58 * s, ey - 14 * s, cx + 102 * s, ey + 10 * s], 20, 160, fill=INK, width=6)
    mo = 50 * s * mouth
    d.ellipse([cx + 90 * s, cy + 70 * s - mo / 2, cx + 150 * s, cy + 86 * s + mo / 2], fill=(120, 40, 50), outline=INK, width=4)
    d.arc([cx - 90 * s, cy - 30 * s, cx - 50 * s, cy + 40 * s], 90, 270, fill=(200, 140, 120), width=max(3, int(8 * s)))


def spray(img, x, y, t, k, n=130, reach=720):
    d = K.D(img)
    for i in range(n):
        a = (i * 0.618) % 1 - 0.5
        sp = 0.35 + (i * 37 % 100) / 100
        u = clamp(k * (((t * 0.55 * sp + i * 0.137) % 1.0) * 0.85 + 0.03))
        px = x + reach * u * (0.8 + 0.2 * sp)
        py = y + a * 420 * u + 140 * u * u
        r = 6 + (i % 5) * 4
        d.ellipse([px - r, py - r, px + r, py + r], fill=DROP + (int(220 * (1 - 0.4 * u)),))
    if k > 0:
        glow(img, x + reach * 0.45 * k, y + 40 * k, 300 * k + 1, 180 * k + 1, (200, 230, 255), 0.35)


def speedo(img, cx, cy, val, k, maxv=200):
    if k <= 0:
        return
    s = pop(k)
    d = K.D(img)
    r = 170 * s
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(250, 250, 252, 240), outline=INK, width=8)
    for j in range(11):
        a = math.pi + j * math.pi / 10
        d.line([(cx + 0.82 * r * math.cos(a), cy + 0.82 * r * math.sin(a)), (cx + 0.95 * r * math.cos(a), cy + 0.95 * r * math.sin(a))], fill=INK, width=5)
    a = math.pi + math.pi * clamp(val / maxv)
    d.line([(cx, cy), (cx + 0.78 * r * math.cos(a), cy + 0.78 * r * math.sin(a))], fill=RED, width=10)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=INK)
    FL.big(img, cx, cy + 50 * s, f"{int(val)} KM/H", int(52 * s) + 1, WHITE, k)


def pollen(d, x, y, r, t):
    for j in range(10):
        a = j * math.pi / 5 + t
        d.line([(x, y), (x + r * 1.4 * math.cos(a), y + r * 1.4 * math.sin(a))], fill=(200, 150, 20), width=3)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 210, 60), outline=INK, width=3)


def virus(d, x, y, r, t):
    for j in range(8):
        a = j * math.pi / 4 + t * 0.7
        ex, ey = x + r * 1.5 * math.cos(a), y + r * 1.5 * math.sin(a)
        d.line([(x, y), (ex, ey)], fill=(60, 140, 80), width=4)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(240, 90, 90))
    d.ellipse([x - r, y - r, x + r, y + r], fill=(110, 200, 120), outline=INK, width=3)


def lungs(Lr, cx, cy, s, f):
    d = K.D(Lr)
    d.rectangle([cx - 14 * s, cy - 260 * s, cx + 14 * s, cy - 60 * s], fill=(230, 160, 170), outline=INK, width=4)
    for sx in (-1, 1):
        w = (130 + 40 * f) * s
        h = (230 + 60 * f) * s
        x0 = cx + sx * 30 * s
        box = [x0, cy - 110 * s, x0 + sx * w, cy - 110 * s + h] if sx > 0 else [x0 - w, cy - 110 * s, x0, cy - 110 * s + h]
        d.rounded_rectangle(box, radius=int(70 * s), fill=(244, 150, 170), outline=INK, width=6)
        for j in range(3):
            yy = cy + (j * 60) * s
            d.line([(x0, yy - 40 * s), (x0 + sx * w * 0.6, yy)], fill=(200, 100, 120), width=4)


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    """GANCHO: estornudo congelado en el aire (la imagen más fuerte va al principio) + velocímetro con 160 tachado."""
    k = ease(clamp(t / 0.9))
    solid(img, lambda Lr: head_side(Lr, 260, 1000, 1.0, 1.0, 1.0))
    spray(img, 400, 1075, t, 0.55 + 0.45 * k)
    v = 160 * ease(clamp(t / 0.8))
    speedo(img, 760, 760, v, clamp(t / 0.3))
    kx = clamp((t - lt(L, 0, 0.35)) / 0.3)
    if kx > 0:
        d = K.D(img)
        d.line([(600, 640), (920, 860)], fill=RED, width=18 if kx > 0.5 else 10)
    ojo(img, 880, 1700, 0.6, "surprise", t=t)
    hook_text(img, [("¿160 KM/H?", False), ("LLEGA MÁS LEJOS", True)], 1.0 if t < T - 0.6 else clamp((T - t) / 0.6), y=330, size=96)


def sh_lenta(img, t, T, L):
    """Cámara superlenta: cámara de cine, contador 0,000 s que avanza muy despacio y fotogramas que pasan."""
    d = K.D(img)
    for j in range(5):                                       # tira de película
        x = (j * 260 - t * 120) % 1300 - 160
        d.rounded_rectangle([x, 520, x + 230, 760], radius=10, fill=(30, 30, 40), outline=(200, 200, 210), width=4)
        for q in range(4):
            d.rectangle([x + 12 + q * 56, 530, x + 40 + q * 56, 546], fill=(200, 200, 210))
            d.rectangle([x + 12 + q * 56, 734, x + 40 + q * 56, 750], fill=(200, 200, 210))
        d.ellipse([x + 80, 590, x + 150, 690], fill=DROP + (200,))
    tt = clamp(t / max(1.0, T)) * 0.999
    FL.big(img, 540, 960, f"{tt:0.3f} s".replace(".", ","), 150, (255, 214, 60), clamp(t / 0.3))
    FL.pill(img, 540, 1110, "x1000 MÁS LENTO", clamp((t - lt(L, 0, 0.3)) / 0.3), col=RED)
    solid(img, lambda Lr: _camera(Lr, 260, 1360, t), sh=0.25)
    ojo(img, 820, 1720, 0.6, "point", t=t)


def _camera(Lr, x, y, t):
    d = K.D(Lr)
    d.rounded_rectangle([x - 150, y - 90, x + 110, y + 90], radius=20, fill=(60, 64, 80), outline=INK, width=6)
    d.rectangle([x + 110, y - 50, x + 200, y + 50], fill=(40, 44, 56), outline=INK, width=6)
    for j, cx in enumerate((x - 100, x + 20)):
        d.ellipse([cx - 60, y - 200, cx + 60, y - 80], fill=(80, 84, 100), outline=INK, width=6)
        a = t * 4 + j
        d.line([(cx, y - 140), (cx + 45 * math.cos(a), y - 140 + 45 * math.sin(a))], fill=(200, 200, 210), width=6)
    d.rectangle([x - 20, y + 90, x + 10, y + 260], fill=(50, 50, 60))


def sh_nariz(img, t, T, L):
    """Dentro de la nariz: entran polvo, polen y un virus; la nariz «se enfada» (alarma roja)."""
    d = K.D(img)
    d.ellipse([140, 560, 940, 1360], fill=(246, 190, 170), outline=INK, width=10)
    d.ellipse([300, 760, 780, 1240], fill=(200, 110, 110), outline=INK, width=8)
    for j in range(7):                                        # pelillos
        a = math.pi * 0.2 + j * 0.25
        d.line([(540 + 250 * math.cos(a), 1000 + 250 * math.sin(a)), (540 + 190 * math.cos(a + 0.2), 1000 + 190 * math.sin(a + 0.2))], fill=(90, 50, 50), width=6)
    k = [clamp((t - lt(L, 0, f)) / 0.4) for f in (0.35, 0.5, 0.65)]
    for i, kk in enumerate(k):
        if kk > 0:
            x = lerp(-60, 420 + i * 120, ease(kk))
            y = 900 + i * 110 + 20 * math.sin(t * 3 + i)
            if i == 0:
                for q in range(6):
                    d.ellipse([x + q * 30 - 14, y + (q % 2) * 26 - 14, x + q * 30 + 14, y + (q % 2) * 26 + 14], fill=(150, 150, 160), outline=INK)
            elif i == 1:
                pollen(d, x, y, 40, t)
            else:
                virus(d, x, y, 44, t)
    FL.pill(img, 540, 1420, "DENTRO DE TU NARIZ", clamp(t / 0.3), col=(200, 110, 110))
    a = clamp((t - lt(L, 0, 0.8)) / 0.3)
    if a > 0:
        glow(img, 540, 1000, 420, 420, (255, 60, 60), 0.35 * a * (0.6 + 0.4 * math.sin(t * 12)))
        FL.stamp(img, 540, 480, "¡ALARMA!", a, col=RED)
    ojo(img, 900, 1720, 0.55, "surprise" if a > 0 else "think", t=t)


def sh_aire(img, t, T, L):
    """El cerebro manda la orden y los pulmones se llenan muchísimo (flechas de aire entrando)."""
    f = ease(clamp((t - 0.4) / max(1.0, T - 0.8)))
    solid(img, lambda Lr: lungs(Lr, 540, 900, 1.2, f))
    solid(img, lambda Lr: D.brain(Lr, 540, 470, 0.5, 0), sh=0.2)
    D.signal(img, (540, 560), (540, 690), t, 3)
    d = K.D(img)
    for j in range(5):
        u = (t * 1.3 + j / 5) % 1
        y = 1500 - 500 * u
        x = 160 + j * 190
        d.line([(x, y), (x, y - 90)], fill=(220, 240, 255, int(220 * (1 - u))), width=12)
        d.polygon([(x - 20, y - 90), (x + 20, y - 90), (x, y - 120)], fill=(220, 240, 255, int(220 * (1 - u))))
    FL.pill(img, 540, 1330, "COGES AIRE", clamp((t - lt(L, 0, 0.3)) / 0.3), col=(60, 140, 210))
    ojo(img, 160, 1740, 0.55, "point", t=t)


def sh_ojos(img, t, T, L):
    """Primer plano: los ojos se cierran solos; Ojo intenta mantener el suyo abierto (y no puede)."""
    e = ease(clamp((t - lt(L, 0, 0.2)) / 0.4))
    solid(img, lambda Lr: head_side(Lr, 400, 900, 1.25, 0.4 * e, e, puff=1.0))
    FL.pill(img, 640, 560, "AUTOMÁTICO", clamp((t - lt(L, 0, 0.25)) / 0.3), col=(150, 90, 200))
    ojo(img, 860, 1720, 0.65, "surprise" if (t % 1.2) < 0.6 else "think", t=t)


# ------------------------------------------------------------------ planos del vídeo entero
def sh_golpe(img, t, T, L):
    """El golpe: pecho y barriga aprietan de golpe (pulmones que se chafan + flechas hacia dentro)."""
    sq = ease(clamp((t - 0.4) / 0.5))
    solid(img, lambda Lr: lungs(Lr, 540, 920, 1.2, 1.0 - 0.9 * sq))
    d = K.D(img)
    for sx in (-1, 1):
        for j in range(3):
            y = 850 + j * 130
            x = 540 + sx * (430 - 80 * sq)
            d.polygon([(x, y - 30), (x, y + 30), (x - sx * 60, y)], fill=RED + (230,))
    if sq > 0.3:
        FL.stamp(img, 540, 520, "¡APRIETA!", clamp((sq - 0.3) / 0.3), col=RED)
    ojo(img, 880, 1740, 0.55, "surprise" if sq > 0.5 else "point", t=t)


def sh_salida(img, t, T, L):
    """El aire sale disparado por nariz y boca a la vez."""
    k = ease(clamp((t - 0.3) / 0.8))
    solid(img, lambda Lr: head_side(Lr, 230, 950, 1.0, 1.0, 1.0))
    spray(img, 400, 1025, t, k, n=110, reach=640)
    spray(img, 450, 975, t * 1.1, k, n=50, reach=560)
    FL.pill(img, 760, 700, "NARIZ + BOCA", clamp((t - lt(L, 0, 0.5)) / 0.3), col=(60, 140, 210))
    ojo(img, 880, 1740, 0.55, "surprise", t=t)


def sh_mito(img, t, T, L):
    """¿160 km/h? MITO: velocímetro a tope y sello."""
    speedo(img, 540, 900, 160, clamp(t / 0.3))
    k = clamp((t - lt(L, 0, 0.75)) / 0.3)
    if k > 0:
        FL.stamp(img, 540, 1150, "MITO", k, col=RED)
    ojo(img, 200, 1740, 0.6, "think" if k <= 0 else "smirk", t=t)


def bike(Lr, cx, cy, s, t):
    d = K.D(Lr)
    for x in (cx - 160 * s, cx + 160 * s):
        d.ellipse([x - 110 * s, cy - 110 * s, x + 110 * s, cy + 110 * s], outline=INK, width=8)
        for j in range(6):
            a = t * 5 + j * math.pi / 3
            d.line([(x, cy), (x + 100 * s * math.cos(a), cy + 100 * s * math.sin(a))], fill=(150, 150, 160), width=3)
    pts = [(cx - 160 * s, cy), (cx - 20 * s, cy - 170 * s), (cx + 120 * s, cy - 170 * s), (cx + 160 * s, cy), (cx, cy), (cx - 20 * s, cy - 170 * s)]
    d.line(pts, fill=RED, width=10)
    d.line([(cx + 120 * s, cy - 170 * s), (cx + 110 * s, cy - 230 * s), (cx + 160 * s, cy - 240 * s)], fill=INK, width=8)
    d.rectangle([cx - 60 * s, cy - 200 * s, cx + 10 * s, cy - 180 * s], fill=INK)


def sh_bici(img, t, T, L):
    """La aguja baja de 160 a 16 y aparece una bici: va igual de rápido."""
    v = lerp(160, 16, ease(clamp((t - 0.2) / 1.0)))
    speedo(img, 540, 760, v, 1.0)
    k = clamp((t - lt(L, 0, 0.6)) / 0.3)
    if k > 0:
        solid(img, lambda Lr: bike(Lr, 540 + 30 * math.sin(t * 2), 1260, 0.9 * pop(k), t))
        FL.pill(img, 540, 1480, "COMO UNA BICI", k, col=GREEN)
    ojo(img, 900, 1760, 0.5, "smirk", t=t)


def sh_nube(img, t, T, L):
    """PERO AQUÍ VIENE LO RARO: no es un chorro, es una NUBE que crece y se arremolina."""
    if t < 1.1:
        FL.stamp(img, 540, 460, "LO RARO", clamp(t / 0.3) * clamp((1.1 - t) / 0.25), col=RED)
    k = ease(clamp((t - 0.5) / 1.5))
    solid(img, lambda Lr: head_side(Lr, 180, 1000, 0.8, 1.0, 1.0))
    for j in range(9):
        a = j * 0.7 + t * 0.8
        x = 420 + 380 * k + 120 * k * math.cos(a)
        y = 1060 + 90 * k * math.sin(a * 1.3)
        glow(img, x, y, 150 * k + 1, 110 * k + 1, (200, 225, 255), 0.35)
    spray(img, 330, 1060, t, 0.6 * k + 0.1, n=70, reach=650)
    FL.pill(img, 640, 700, "UNA NUBE", clamp((t - lt(L, 0, 0.7)) / 0.3), col=(60, 140, 210))
    ojo(img, 900, 1760, 0.5, "surprise", t=t)


def car_side(Lr, x, y, s, col):
    d = K.D(Lr)
    d.rounded_rectangle([x, y - 70 * s, x + 380 * s, y], radius=int(30 * s), fill=col, outline=INK, width=5)
    d.polygon([(x + 80 * s, y - 70 * s), (x + 130 * s, y - 130 * s), (x + 270 * s, y - 130 * s), (x + 320 * s, y - 70 * s)], fill=col, outline=INK)
    d.polygon([(x + 100 * s, y - 72 * s), (x + 140 * s, y - 118 * s), (x + 260 * s, y - 118 * s), (x + 300 * s, y - 72 * s)], fill=(200, 230, 250))
    for wx in (x + 80 * s, x + 300 * s):
        d.ellipse([wx - 40 * s, y - 30 * s, wx + 40 * s, y + 50 * s], fill=(40, 40, 46), outline=INK, width=4)


def sh_lejos(img, t, T, L):
    """Regla de 0 a 8 metros con dos coches en fila; la nube avanza hasta el final."""
    d = K.D(img)
    y0 = 1260
    d.line([(60, y0 + 70), (1020, y0 + 70)], fill=WHITE, width=6)
    for m in range(9):
        x = 60 + m * 120
        d.line([(x, y0 + 55), (x, y0 + 85)], fill=WHITE, width=5)
        FL.big(img, x, y0 + 125, f"{m} m", 34, WHITE, 1.0)
    solid(img, lambda Lr: car_side(Lr, 90, y0 + 40, 1.15, (230, 80, 70)), sh=0.2)
    solid(img, lambda Lr: car_side(Lr, 560, y0 + 40, 1.15, (70, 130, 220)), sh=0.2)
    k = ease(clamp((t - 0.3) / max(1.0, T - 0.8)))
    x = 60 + 960 * k
    for j in range(7):
        glow(img, x - j * 70, 980 + 30 * math.sin(t * 2 + j), 110, 90, (200, 225, 255), 0.4)
    FL.big(img, x if x < 900 else 900, 800, f"{8 * k:0.1f} m", 90, (255, 214, 60), 1.0)
    ojo(img, 160, 1760, 0.5, "surprise" if k > 0.8 else "point", t=t)


def sh_grandes(img, t, T, L):
    """Las gotas grandes caen en un par de metros (parábolas que tocan el suelo)."""
    d = K.D(img)
    solid(img, lambda Lr: head_side(Lr, 200, 900, 0.8, 1.0, 1.0))
    d.line([(0, 1400), (W, 1400)], fill=WHITE, width=6)
    for j in range(10):
        u = (t * 0.7 + j / 10) % 1
        x = 330 + 520 * u
        y = 960 + 440 * u * u
        r = 18 + (j % 3) * 6
        d.ellipse([x - r, y - r, x + r, y + r], fill=DROP + (230,), outline=(40, 90, 140))
    d.line([(330, 1440), (850, 1440)], fill=(255, 214, 60), width=8)
    FL.big(img, 590, 1500, "1-2 METROS", 64, (255, 214, 60), clamp((t - 0.3) / 0.3))
    FL.pill(img, 640, 640, "GOTAS GRANDES", clamp(t / 0.3), col=(60, 140, 210))
    ojo(img, 920, 1760, 0.5, "point", t=t)


def sh_pequenas(img, t, T, L):
    """Las gotitas pequeñas flotan en el aire durante minutos (polvo brillante + reloj)."""
    d = K.D(img)
    for i in range(60):
        x = (i * 83 + 40 * math.sin(t * 0.7 + i)) % W
        y = 500 + (i * 157) % 900 + 30 * math.sin(t * 0.9 + i * 2)
        r = 4 + i % 4
        d.ellipse([x - r, y - r, x + r, y + r], fill=(210, 235, 255, 200))
    m = int(lerp(0, 10, ease(clamp(t / max(1.0, T - 0.5)))))
    D.clock(img, 540, 900, m, clamp(t / 0.3))
    FL.pill(img, 540, 560, "FLOTAN MINUTOS", clamp((t - lt(L, 0, 0.5)) / 0.3), col=(150, 90, 200))
    ojo(img, 200, 1760, 0.55, "surprise", t=t)


def sh_codo(img, t, T, L):
    """Estornudar en el codo: la nube choca contra el brazo y se frena."""
    solid(img, lambda Lr: head_side(Lr, 300, 950, 1.0, 1.0, 1.0))
    d = K.D(img)
    k = ease(clamp(t / 0.6))
    D.capsule(d, (300, 1180), (lerp(300, 520, k), lerp(1180, 1010, k)), 46, (90, 150, 220), INK, 7)
    spray(img, 470, 1025, t, 0.18, n=60, reach=120)
    kk = clamp((t - lt(L, 0, 0.4)) / 0.3)
    if kk > 0:
        r = 70 * pop(kk)
        d.line([(760 - r * 0.6, 1020), (760, 1020 + r * 0.5), (760 + r, 1020 - r * 0.6)], fill=GREEN, width=18)
        FL.pill(img, 640, 640, "AL CODO", kk, col=GREEN)
    ojo(img, 900, 1760, 0.55, "smirk", t=t)


def _a_bici(Lr, x, y, s):
    bike(Lr, x, y + 40 * s, 0.4 * s + 0.01, 0)


def _a_nube(Lr, x, y, s):
    d = K.D(Lr)
    for j in range(5):
        d.ellipse([x - 90 * s + j * 30 * s, y - 50 * s - (j % 2) * 30 * s, x - 10 * s + j * 30 * s, y + 30 * s], fill=(200, 225, 255), outline=INK, width=3)


def _a_lejos(Lr, x, y, s):
    d = K.D(Lr)
    d.line([(x - 100 * s, y + 40 * s), (x + 100 * s, y + 40 * s)], fill=INK, width=6)
    d.polygon([(x + 100 * s, y + 20 * s), (x + 130 * s, y + 40 * s), (x + 100 * s, y + 60 * s)], fill=INK)
    d.text((x, y - 30 * s), "8 m", font=F(FL.INTER_X, int(60 * s) + 1), fill=RED, anchor="mm")


GREEN = D.GREEN


def sh_answer(img, t, T, L):
    ks = [clamp((t - lt(L, 0, 0.15)) / 0.35), clamp((t - lt(L, 0, 0.45)) / 0.35), clamp((t - lt(L, 0, 0.7)) / 0.35)]
    pro.chain(img, t, [("NO ES RÁPIDO", (120, 120, 130)), ("ES UNA NUBE", (60, 140, 210)), ("LLEGA LEJOS", RED)], ks, y=1000,
              drawers=[_a_bici, _a_nube, _a_lejos])
    hook_text(img, [("¿160 KM/H?", False), ("LO PELIGROSO ES LA DISTANCIA", True)], clamp((t - 0.1) / 0.4), y=480, size=62)
    ojo(img, 540, 1760, 0.6, "smirk", t=t)


# ------------------------------------------------------------------ subtítulos, emojis y montaje (de c20_dedos)
D.CAP_POS.update({"q": 1760, "lenta": 330, "nariz": 330, "aire": 1600, "ojos": 330, "golpe": 1600, "salida": 330, "mito": 330,
                  "bici": 330, "nube": 1600, "lejos": 330, "grandes": 330, "pequenas": 1500, "codo": 1600, "answer": 1390})
D.EMOJI.update({"q": ["🤧"], "lenta": ["🎥", "⏱️"], "nariz": ["👃", "🌫️"], "aire": ["🫁"], "ojos": ["🙈"], "golpe": ["💥"],
                "salida": ["👃", "👄"], "mito": ["❌"], "bici": ["🚲"], "nube": ["☁️"], "lejos": ["📏"], "grandes": ["💧"],
                "pequenas": ["🌫️", "⏳"], "codo": ["💪"], "answer": ["😷"]})
CAPTION = D.CAPTION
NO_EMOJI = set(NAMES)
NARR = None
D.SCENE_BG.clear()
D.SCENE_BG.update({"q": estudio, "lenta": estudio, "nariz": estudio, "aire": D.lab, "ojos": estudio, "golpe": D.lab, "salida": estudio,
                   "mito": estudio, "bici": D.lluvia, "nube": estudio, "lejos": D.lluvia, "grandes": estudio, "pequenas": estudio,
                   "codo": estudio, "answer": D.lab})
pro.setup(globals(), OJO_TRAJE, estudio().resize((W, H)), NAMES)


def _wrap(fn, name):
    def run(img, t, T, L):
        T_ = pro.NOW[0]
        D._bg(img, name, T_)
        if D.SCENE_BG[name] is D.lluvia:
            D._rain(img, T_)
        elif D.SCENE_BG[name] is estudio:
            dd = K.D(img)
            for i in range(14):
                x = (i * 97 + 30 * math.sin(T_ * 0.6 + i)) % W
                y = (i * 181 + T_ * (14 + i % 5 * 4)) % H
                dd.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(200, 220, 255, 140))
        else:
            D._air(img, name, T_)
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
AUDIO = {"music": [("q", "exp")], "gains": {}, "amb": {},
         "sfx": [(0.05, "whoosh", 0.05), ("lenta+0.2", "click", 0.05), ("nariz+0.4", "pop", 0.05), ("aire+0.3", "whoosh", 0.04),
                 ("ojos+0.3", "pop", 0.05), ("golpe+0.5", "pop", 0.07),
                 ("mito+0.05", "pop", 0.05), ("nube+0.05", "pop", 0.07), ("lejos+0.3", "whoosh", 0.04), ("codo+0.4", "ding", 0.05),
                 ("answer+0.5", "ding", 0.06)], "bpm": 110}
