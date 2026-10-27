"""03 · La llave del Titanic — estilo 7 «minimal blanco» con el formato nuevo (21/10): pregunta de gancho que se
responde al final, Ojo de narrador (científico profe, tema historia), palabras clave con marcador rojo y cierre de
«Ojo al dato». Voz: Fernando Martinez (eleven_flash_v2_5, atemporal). Fuentes en la ficha del Plan de subidas
(Wikipedia: David Blair · Sailors' Society)."""
import os
import math
from gadgets import *            # noqa: F401,F403  (valores por defecto del motor)
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED, SOFT, txt

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "03_Llave_Titanic_estilo7"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c03_titanic")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Una *llave* pudo haber salvado el *Titanic*?",
    "Southampton, 10 de abril de *1912*: zarpa el barco más grande del mundo en su *primer viaje*.",
    "Muchos lo llamaban *insumergible*.",
    "Pero justo antes de zarpar hubo un cambio: el oficial *David Blair* se quedó en tierra.",
    "Y, sin darse cuenta, se llevó algo *en el bolsillo*.",
    "14 de abril. Noche *sin luna* y un frío helador.",
    "En lo alto del mástil, dos vigías buscan icebergs… *a simple vista*.",
    "A las *23:40*, el vigía Frederick Fleet ve una sombra en el agua.",
    "Toca la campana *tres veces*: ¡iceberg justo delante!",
    "Menos de un minuto después… *el choque*.",
    "En menos de tres horas el Titanic se hunde, y mueren *más de 1.500* personas.",
    "¿Y la llave? Según la historia más conocida, abría el armario de los *prismáticos* de los vigías.",
    "Fleet dijo después que, con prismáticos, lo habrían visto *a tiempo*.",
    "Aunque muchos expertos lo dudan: de noche, unos prismáticos *no hacen milagros*.",
    "En 2007, esa llave se subastó por *90.000 libras*.",
    "Así que… ¿una llave pudo salvarlo? Quizá no… pero nunca sabremos *qué habría pasado*.",
]
OUTRO_LINE = "Una llave pequeña, para una historia gigante… ¡Ojo al dato!"
NAMES = ["q", "port", "unsink", "blair", "pocket", "night", "nest", "shadow", "bell", "crash", "sink", "key", "fleet",
         "doubt", "auction", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("bell", 2.2)            # banner de seguir hacia la mitad (~36 s de ~72)
HEAD = {
    0: ("¿Una llave?", "¿PUDO SALVAR EL TITANIC?"),
    1: ("Southampton", "10 DE ABRIL DE 1912 · PRIMER VIAJE"),
    2: ("Insumergible", "ASÍ LO LLAMABAN"),
    3: ("Un cambio", "EL OFICIAL DAVID BLAIR SE QUEDA EN TIERRA"),
    4: ("En el bolsillo", "SE LLEVÓ ALGO SIN DARSE CUENTA"),
    5: ("14 de abril", "NOCHE SIN LUNA Y FRÍO HELADOR"),
    6: ("A simple vista", "DOS VIGÍAS EN LO ALTO DEL MÁSTIL"),
    7: ("23:40", "UNA SOMBRA EN EL AGUA"),
    8: ("¡Iceberg!", "TRES CAMPANADAS"),
    9: ("El choque", "MENOS DE UN MINUTO DESPUÉS"),
    10: ("Más de 1.500", "PERSONAS MUEREN"),
    11: ("La llave", "ABRÍA EL ARMARIO DE LOS PRISMÁTICOS"),
    12: ("A tiempo", "LO QUE DIJO FLEET"),
    13: ("¿Seguro?", "MUCHOS EXPERTOS LO DUDAN"),
    14: ("90.000 libras", "SUBASTA DE 2007"),
    15: ("¿La respuesta?", "QUIZÁ NO… NUNCA LO SABREMOS"),
}
NARRATOR = {}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {}
FL.use("minimal", HEAD)

# estilo 7 + formato nuevo
FRAME = vid2.frame
FPS = 60
BG = (248, 248, 246)
TRANS_POOL = ["push", "whip", "zoom_in", "iris", "whip_r", "spin"]
TRANS_SEED = 13
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
FL.TH["narr"] = True
OJO_TRAJE = "c_profe"
OJO_POSES = {"q": "think", "port": "point", "unsink": "smirk", "blair": "point", "pocket": "surprise", "night": "think",
             "nest": "point", "shadow": "surprise", "bell": "surprise", "crash": "surprise", "sink": "think",
             "key": "point", "fleet": "point", "doubt": "smirk", "auction": "surprise", "answer": "think"}
NARR = FL.NARR
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
IDX = {n: i for i, n in enumerate(NAMES)}
WL = 880                          # línea del mar


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def _h(img, name, t):
    FL.head(img, t, IDX[name])


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    K.water(img, WL + 60, t)
    K.ship(img, 640, WL + 60, 0.75)
    k = clamp((t - 0.2) / 0.4)
    if k > 0:
        K.key(img, 540, 560, 0.9 * pop(k), a=0.15 * math.sin(t * 3))
    FL.big(img, 860, 470, "?", 200, RED, clamp((t - 1.0) / 0.3))
    _h(img, "q", t)


def sh_port(img, t, T, L):
    d = K.D(img)
    q = ease(clamp(t / 2.2))
    FL.pill(img, 540, 450, "10 · 04 · 1912", clamp((t - 0.2) / 0.3))
    # ruta Southampton → Nueva York (de derecha a izquierda)
    y = 640
    d.line([(180, y), (900, y)], fill=K.PALE, width=10)
    FL.dotted_arc(img, 540, y + 520, 560, -math.pi * 0.86, -math.pi * (0.86 - 0.72 * ease(clamp((t - 2.6) / 2.5))), 1.0)
    for x, lab in ((900, "Southampton"), (180, "Nueva York")):
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=RED if x > 500 else INK)
        txt(img, (x, y + 50), lab, 38, INK)
    K.water(img, WL + 80, t)
    K.ship(img, lerp(1300, 560, q), WL + 80, 0.8, flip=-1)
    if t > 4.0:
        FL.pill(img, 540, 1250, "EL BARCO MÁS GRANDE DEL MUNDO", ease(clamp((t - 4.0) / 0.3)))
    _h(img, "port", t)


def sh_unsink(img, t, T, L):
    K.water(img, WL, t)
    K.ship(img, 540, WL, 1.05, a=0.02 * math.sin(t * 1.5))
    FL.stamp(img, 540, 520, "INSUMERGIBLE", clamp((t - 0.5) / 0.35))
    _h(img, "unsink", t)


def sh_blair(img, t, T, L):
    d = K.D(img)
    K.water(img, WL + 120, t, x0=0, x1=W)
    d.rectangle([0, WL - 40, 330, WL + 120], fill=(214, 206, 196), outline=INK, width=5)  # muelle
    K.ship(img, 800, WL + 120, 0.9)
    q = ease(clamp((t - lt(L, 0, 0.55)) / 1.6))
    x = lerp(560, 200, q)
    y = lerp(WL - 60, WL - 40, q)
    d.line([(600, WL - 50), (330, WL - 40)], fill=INK, width=6)                          # pasarela
    K.stick(img, x, y, 1.1)
    if q > 0.6:
        txt(img, (x, y - 170), "David Blair", 40, RED)
        FL.pill(img, 640, 1250, "SE QUEDA EN TIERRA", ease(clamp((q - 0.6) / 0.3)), col=RED)
    _h(img, "blair", t)


def sh_pocket(img, t, T, L):
    K.pocket(img, 540, 800, 1.3)
    q = ease(clamp((t - 0.9) / 0.8))
    K.key(img, 540, lerp(430, 790, q), 0.75, a=lerp(-0.6, 1.4, q))
    d = K.D(img)
    d.chord([540 - 195, 800 - 221 - 110, 540 + 195, 800 + 221], 0, 180, fill=(54, 68, 98), outline=INK, width=8)
    if t > 1.8:
        FL.big(img, 830, 520, "?", 150, RED, clamp((t - 1.8) / 0.3))
    _h(img, "pocket", t)


def sh_night(img, t, T, L):
    d = K.D(img)
    d.rounded_rectangle([60, 400, W - 60, 1120], radius=40, fill=(24, 28, 44))
    K.stars(img, seed=7, n=34, y0=440, y1=760, col=(210, 214, 230))
    K.moon_x(img, 300, 580, 90, clamp((t - 0.8) / 0.4))
    if t > 1.8:
        K.snow(img, 790, 580, 80 * pop(clamp((t - 1.8) / 0.3)))
    K.water(img, 900, t, x0=60, x1=W - 60, y1=1120, waves=2)
    K.ship(img, 560, 900, 0.7, lights=True)
    FL.pill(img, 540, 1250, "SIN LUNA · FRÍO HELADOR", clamp((t - 2.0) / 0.3))
    _h(img, "night", t)


def sh_nest(img, t, T, L):
    d = K.D(img)
    d.line([(440, 1140), (440, 520)], fill=INK, width=18)                                 # mástil
    d.rectangle([340, 600, 540, 690], fill=(255, 255, 255), outline=INK, width=8)         # cofa
    for x in (390, 490):
        K.stick(img, x, 640, 0.9, arm=0.6 + 0.2 * math.sin(t * 4 + x))
    q = ease(clamp((t - 1.2) / 1.0))
    for dy in (-40, 40):
        d.line([(520, 560), (520 + 420 * q, 560 + dy * q * 3)], fill=SOFT, width=4)
    if t > lt(L, 0, 0.6):
        FL.pill(img, 760, 840, "SIN PRISMÁTICOS", ease(clamp((t - lt(L, 0, 0.6)) / 0.3)), col=RED)
    _h(img, "nest", t)


def sh_shadow(img, t, T, L):
    d = K.D(img)
    d.rounded_rectangle([60, 400, W - 60, 1120], radius=40, fill=(24, 28, 44))
    K.water(img, 860, t, x0=60, x1=W - 60, y1=1120, waves=2)
    k = clamp((t - 1.0) / 2.5)
    K.iceberg(img, 600, 860, 0.5 + 0.5 * k, k * 0.85, under=False)
    FL.big(img, 540, 560, "23:40", 160, (255, 255, 255), clamp(t / 0.3))
    _h(img, "shadow", t)


def sh_bell(img, t, T, L):
    for n in range(3):
        tk = 0.2 + n * 0.45
        if t > tk:
            FL.big(img, 280 + n * 260, 1000, "¡DING!", 70, RED, clamp((t - tk) / 0.2))
    K.bell(img, 540, 450, 1.3, ang=18 * math.sin(t * 9) * math.exp(-0.25 * t))
    if t > 1.7:
        FL.stamp(img, 540, 1240, "¡ICEBERG!", clamp((t - 1.7) / 0.3))
    _h(img, "bell", t)


def sh_crash(img, t, T, L):
    q = ease(clamp(t / 2.0))
    K.water(img, WL, t)
    K.iceberg(img, 840, WL, 0.9)
    K.ship(img, lerp(140, 470, q), WL, 0.8)
    if t > 2.0:
        K.crack(img, 735, WL - 40, clamp((t - 2.0) / 0.3), 1.2)
        FL.pill(img, 640, 1250, "MENOS DE 1 MINUTO", 1.0, col=RED)
    FL.stopwatch(img, 860, 520, 90, clamp(t / 2.0) * 0.6, "< 1 min" if t > 2.0 else "")
    _h(img, "crash", t)


def sh_sink(img, t, T, L):
    q = ease(clamp(t / 3.5))
    K.ship(img, 540, WL + 40 + 120 * q, 1.0, a=0.32 * q)
    K.water(img, WL + 20, t)
    FL.clock(img, 860, 520, 80, t * 1.5)
    k = clamp((t - lt(L, 0, 0.6)) / 0.35)
    FL.big(img, 540, 1250, "+1.500", 150, RED, k)
    _h(img, "sink", t)


def sh_key(img, t, T, L):
    d = K.D(img)
    k = clamp((t - lt(L, 0, 0.35)) / 0.5)
    K.key(img, 540, 560, 1.0, a=0.1 * math.sin(t * 2))
    # armario de los prismáticos que se abre
    x0, y0 = 340, 760
    d.rectangle([x0, y0, x0 + 400, y0 + 340], fill=(196, 150, 96), outline=INK, width=8)
    op = ease(k)
    d.polygon([(x0, y0), (x0 + 400 * (1 - op * 0.85), y0 + 30 * op), (x0 + 400 * (1 - op * 0.85), y0 + 340 - 30 * op), (x0, y0 + 340)],
              fill=(170, 124, 74), outline=INK)
    if op > 0.5:
        K.binoculars(img, x0 + 250, y0 + 150, 0.7)
    _h(img, "key", t)


def sh_fleet(img, t, T, L):
    d = K.D(img)
    for sx in (-1, 1):
        cx = 540 + sx * 190
        d.ellipse([cx - 220, 520, cx + 220, 960], fill=(24, 28, 44), outline=INK, width=14)
    q = clamp((t - 0.6) / 1.4)
    K.iceberg(img, 540, 840, 0.6 + 0.5 * q, 1.0, under=False)
    for sx in (-1, 1):
        cx = 540 + sx * 190
        d.ellipse([cx - 220, 520, cx + 220, 960], outline=INK, width=22)
    if t > lt(L, 0, 0.75):
        FL.stamp(img, 540, 1240, "¿A TIEMPO?", clamp((t - lt(L, 0, 0.75)) / 0.3))
    _h(img, "fleet", t)


def sh_doubt(img, t, T, L):
    K.binoculars(img, 540, 700, 1.4, view=(24, 28, 44))
    FL.big(img, 540, 700, "?", 160, RED, clamp((t - 0.8) / 0.3))
    if t > lt(L, 0, 0.6):
        FL.pill(img, 540, 1010, "NO HACEN MILAGROS", ease(clamp((t - lt(L, 0, 0.6)) / 0.3)), col=RED)
    _h(img, "doubt", t)


def sh_auction(img, t, T, L):
    d = K.D(img)
    d.rounded_rectangle([200, 840, 880, 920], radius=12, fill=(150, 96, 50), outline=INK, width=6)
    K.key(img, 420, 760, 0.6)
    hit = (t * 1.3) % 1.0
    K.gavel(img, 760, 880, 0.8, ang=lerp(40, 0, ease(clamp(hit / 0.25))))
    FL.big(img, 540, 540, "90.000 £", 140, RED, clamp((t - lt(L, 0, 0.6)) / 0.3))
    FL.pill(img, 640, 1250, "SUBASTA · 2007", clamp((t - 0.3) / 0.3))
    _h(img, "auction", t)


def sh_answer(img, t, T, L):
    K.key(img, 540, 640, 1.1, a=0.08 * math.sin(t * 2))
    k1 = clamp((t - lt(L, 0, 0.4)) / 0.3)
    FL.big(img, 540, 900, "¿Quizá no?", 100, INK, k1)
    k2 = clamp((t - lt(L, 0, 0.72)) / 0.3)
    if k2 > 0:
        FL.pill(img, 640, 1250, "NUNCA LO SABREMOS", ease(k2), col=RED)
    _h(img, "answer", t)


FNS = {n: globals()["sh_" + n] for n in NAMES}
FOCUS_PT = {n: (540, 800) for n in NAMES}

AUDIO = {
    "music": [("q", "mystery"), ("port", "doc"), ("night", "drone"), ("bell", "tension"), ("sink", "epic"),
              ("key", "mystery"), ("auction", "premium")],
    "gains": {"mystery": 0.8},
    "duck": [("crash", "crash+1.6", 0.5)],
    "amb": {"sea": ["night", "nest", "shadow", "bell", "sink"], "crowd": ["port", "blair"], "room": ["key", "auction"]},
    "sfx": [("q+0.2", "chime", 0.06), ("port+0.4", "horn", 0.3), ("unsink+0.5", "pop", 0.08), ("blair+0.3", "paper", 0.12),
            ("pocket+1.0", "click", 0.2), ("shadow+0.6", "heart", 0.3), ("shadow+1.2", "heart", 0.3),
            ("bell+0.2", "bell", 0.35), ("bell+0.65", "bell", 0.35), ("bell+1.1", "bell", 0.35),
            ("crash+2.0", "boom", 0.5), ("crash+2.0", "impact", 0.4), ("sink+0.5", "rumble", 0.3),
            ("key+0.4", "ding", 0.1), ("fleet+0.5", "swell", 0.1), ("auction+0.3", "gavel", 0.4),
            ("answer+0.3", "swell", 0.12)],
    "bpm": 92,
}
