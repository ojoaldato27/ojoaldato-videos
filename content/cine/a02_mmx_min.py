"""⚡ A2 · MMX, a por una luna de Marte — estilo 7 «minimal blanco» con el formato nuevo (21/10): pregunta de gancho
respondida al final, Ojo de narrador (científico astrónomo), palabras clave con marcador rojo y cierre «Ojo al dato».
Voz: Fernando Martinez (eleven_v4 con etiquetas, actualidad).
Datos comprobados: lanzamiento el 20/10/2026 a las 04:41 (hora de Japón) en un H3 desde Tanegashima, llegada en
agosto de 2027, al menos 10 g de muestra, rover IDEFIX (CNES + DLR), cápsula en Australia en 2031.
Fuentes: ESA «MMX from launch to Phobos» · Wikipedia «Martian Moons eXploration» · CRHoy / SDP Noticias (AFP, 19-20/10)."""
import os
import math
from gadgets import *            # noqa: F401,F403
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED, SOFT, txt

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "A2_MMX_luna_de_Marte_estilo7"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "a02_mmx")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Se puede traer un trozo de *Marte*… sin pisar Marte?",
    "Japón lo va a intentar con la misión *MMX*.",
    "Despegó el *20 de octubre* desde Tanegashima, en un cohete *H3*.",
    "Va hacia *Fobos*, una de las dos lunas de Marte.",
    "Una roca con forma de patata de unos *22 kilómetros*…",
    "que da la vuelta a Marte *tres veces al día*.",
    "La nave llegará en *agosto de 2027*.",
    "Soltará un pequeño rover, *IDEFIX*, hecho por Francia y Alemania.",
    "Y después se posará en Fobos para coger *al menos 10 gramos* de su suelo.",
    "Nadie sabe si Fobos es un *asteroide* que Marte atrapó…",
    "o un trozo del propio planeta, arrancado por un *choque gigante*.",
    "Y se cree que su polvo esconde algo más: *restos de Marte*, salpicados por meteoritos durante millones de años.",
    "En *2031*, una cápsula caerá en paracaídas en el desierto de *Australia*.",
    "Así que sí: para traer un poco de Marte… puede que baste con ir a *su luna*.",
]
OUTRO_LINE = "Apunta la fecha: 2031… ¡y ojo al dato!"
NAMES = ["q", "japan", "launch", "phobos", "potato", "orbit3", "arrive", "rover", "sample", "asteroid", "impact", "dust",
         "capsule", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("sample", 2.4)          # banner de seguir hacia la mitad (~30 s de ~62)
HEAD = {
    0: ("¿Un trozo de Marte?", "SIN PISAR MARTE"),
    1: ("Misión MMX", "LA AGENCIA ESPACIAL DE JAPÓN"),
    2: ("20 de octubre", "TANEGASHIMA · COHETE H3"),
    3: ("Fobos", "UNA DE LAS DOS LUNAS DE MARTE"),
    4: ("22 km", "UNA ROCA CON FORMA DE PATATA"),
    5: ("3 vueltas al día", "ALREDEDOR DE MARTE"),
    6: ("Agosto de 2027", "LLEGADA A MARTE"),
    7: ("IDEFIX", "EL ROVER DE FRANCIA Y ALEMANIA"),
    8: ("10 gramos", "COMO MÍNIMO, DEL SUELO DE FOBOS"),
    9: ("¿Un asteroide?", "ATRAPADO POR MARTE"),
    10: ("¿O un trozo de Marte?", "ARRANCADO POR UN CHOQUE GIGANTE"),
    11: ("Polvo de Marte", "SALPICADO POR METEORITOS"),
    12: ("2031", "UNA CÁPSULA CAE EN AUSTRALIA"),
    13: ("La respuesta", "IR A SU LUNA"),
}
NARRATOR = {}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {}
FL.use("minimal", HEAD)

FRAME = vid2.frame
FPS = 60
BG = (248, 248, 246)
TRANS_POOL = ["push", "whip", "zoom_in", "iris", "whip_r", "spin"]
TRANS_SEED = 21
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
FL.TH["narr"] = True
OJO_TRAJE = "c_astronomo"
OJO_POSES = {"q": "think", "japan": "point", "launch": "surprise", "phobos": "point", "potato": "smirk", "orbit3": "surprise",
             "arrive": "point", "rover": "point", "sample": "point", "asteroid": "think", "impact": "surprise",
             "dust": "think", "capsule": "point", "answer": "smirk"}
NARR = FL.NARR
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
IDX = {n: i for i, n in enumerate(NAMES)}


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def _h(img, name, t):
    FL.head(img, t, IDX[name])


def earth(img, cx, cy, r):
    d = K.D(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 150, 230), outline=INK, width=max(3, int(r / 18)))
    for dx, dy, rr in ((-0.3, -0.2, 0.35), (0.35, 0.3, 0.28), (0.2, -0.45, 0.18)):
        d.ellipse([cx + (dx - rr) * r, cy + (dy - rr * 0.7) * r, cx + (dx + rr) * r, cy + (dy + rr * 0.7) * r], fill=(110, 190, 110))


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    K.stars(img, seed=3, n=26)
    K.mars(img, 560, 760, 250, rot=t * 0.05)
    q = ease(clamp((t - 0.6) / 1.6))
    K.phobos(img, lerp(720, 880, q), lerp(600, 480, q), 40, ang=t)
    FL.big(img, 880, 760, "?", 180, RED, clamp((t - 0.9) / 0.3))
    _h(img, "q", t)


def sh_japan(img, t, T, L):
    K.japan_flag(img, 540, 620, 420, clamp((t - 0.1) / 0.35))
    K.probe(img, 540, 980, 0.9, ang=0.08 * math.sin(t * 2))
    FL.pill(img, 640, 1250, "MMX · MARTIAN MOONS EXPLORATION", clamp((t - 0.8) / 0.3))
    _h(img, "japan", t)


def sh_launch(img, t, T, L):
    d = K.D(img)
    q = ease(clamp((t - 0.9) / 2.8)) ** 1.5
    yb = 1100 - 160 * q
    if t > 0.6:
        FL.puff(img, 520, 1100, math.pi, clamp((t - 0.6) / 0.3), size=60, n=6, seed=2)
        FL.puff(img, 520, 1100, 0.0, clamp((t - 0.6) / 0.3), size=60, n=6, seed=3)
    d.line([(60, 1110), (W - 60, 1110)], fill=INK, width=6)
    K.rocket(img, 520, yb, 0.85, flame=clamp((t - 0.6) / 0.3), t=t)
    FL.big(img, 840, 620, "H3", 150, RED, clamp((t - lt(L, 0, 0.7)) / 0.3))
    FL.pill(img, 640, 1250, "20 OCT · TANEGASHIMA", clamp((t - 0.3) / 0.3))
    _h(img, "launch", t)


def sh_phobos(img, t, T, L):
    K.stars(img, seed=5, n=26)
    K.mars(img, 140, 780, 330, rot=t * 0.04)
    K.orbit(img, 140, 780, 560, 300)
    K.orbit(img, 140, 780, 860, 420, col=(214, 214, 220))
    a = -0.5 + t * 0.35
    px, py = 140 + math.cos(a) * 560, 780 + math.sin(a) * 300
    K.phobos(img, px, py, 46, ang=t)
    b = -0.25 + t * 0.12
    dx, dy = 140 + math.cos(b) * 860, 780 + math.sin(b) * 420
    K.phobos(img, dx, dy, 24, ang=-t)
    if t > 0.5:
        txt(img, (px, py - 80), "Fobos", 46, RED)
    if t > lt(L, 0, 0.5):
        txt(img, (dx, dy - 56), "Deimos", 36, SOFT)
    _h(img, "phobos", t)


def sh_potato(img, t, T, L):
    K.phobos(img, 540, 760, 300, ang=0.15 * math.sin(t * 0.8))
    k = ease(clamp((t - lt(L, 0, 0.6)) / 0.5))
    if k > 0:
        d = K.D(img)
        y = 1080
        d.line([(240, y), (240 + 600 * k, y)], fill=RED, width=8)
        d.line([(240, y - 26), (240, y + 26)], fill=RED, width=8)
        if k >= 1:
            d.line([(840, y - 26), (840, y + 26)], fill=RED, width=8)
        FL.big(img, 540, y + 90, "22 km", 90, RED, k)
    _h(img, "potato", t)


def sh_orbit3(img, t, T, L):
    K.stars(img, seed=9, n=20)
    K.mars(img, 540, 760, 200, rot=t * 0.1)
    K.orbit(img, 540, 760, 360, 190)
    turns = 3 * clamp(t / max(0.5, T - 0.4))
    a = -math.pi / 2 + turns * 2 * math.pi
    K.phobos(img, 540 + math.cos(a) * 360, 760 + math.sin(a) * 190, 40, ang=a)
    n = min(3, int(turns + 0.02))
    FL.big(img, 860, 470, f"×{max(1, n)}", 110, RED, 1.0 if turns > 0.15 else 0)
    FL.pill(img, 640, 1250, "EN 24 HORAS", clamp((t - 0.5) / 0.3))
    _h(img, "orbit3", t)


def sh_arrive(img, t, T, L):
    K.stars(img, seed=11, n=24)
    earth(img, 200, 1000, 90)
    K.mars(img, 860, 560, 130)
    q = ease(clamp(t / 2.4))
    FL.dotted_arc(img, 530, 1060, 520, -math.pi * 0.95, -math.pi * (0.95 - 0.62 * q), 1.0, col=SOFT)
    a = -math.pi * (0.95 - 0.62 * q)
    K.probe(img, 530 + math.cos(a) * 520, 1060 + math.sin(a) * 520, 0.4, ang=a + math.pi / 2)
    FL.pill(img, 640, 1250, "AGOSTO 2027", clamp((t - 0.6) / 0.3), col=RED)
    _h(img, "arrive", t)


def _ground(img, y=1000):
    d = K.D(img)
    d.rectangle([0, y, W, 1150], fill=K.PHOB)
    d.line([(0, y), (W, y)], fill=INK, width=6)
    for x, r in ((200, 50), (620, 70), (920, 40)):
        d.chord([x - r, y + 10, x + r, y + 10 + r * 0.6], 0, 180, fill=K.PHOB_D, outline=INK, width=4)


def sh_rover(img, t, T, L):
    K.stars(img, seed=13, n=18, y1=900)
    K.mars(img, 820, 560, 150)
    _ground(img)
    q = ease(clamp((t - 0.2) / 2.8))
    K.rover(img, lerp(380, 700, q), 1000, 1.2, t=t)
    FL.pill(img, 640, 1250, "FRANCIA + ALEMANIA", clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "rover", t)


def sh_sample(img, t, T, L):
    K.stars(img, seed=17, n=16, y1=800)
    _ground(img, 1060)
    q = ease(clamp(t / 1.8))
    K.probe(img, 400, lerp(500, 980, q), 0.7, flame=1.0 - q)
    k = clamp((t - lt(L, 0, 0.6)) / 0.8)
    if k > 0:
        K.scale_10g(img, 790, 700, k)
    _h(img, "sample", t)


def sh_asteroid(img, t, T, L):
    K.stars(img, seed=19, n=24)
    K.mars(img, 540, 800, 170)
    q = ease(clamp(t / 2.6))
    # el asteroide llega en línea recta y Marte lo «atrapa» en órbita
    if q < 0.6:
        u = q / 0.6
        x, y = lerp(1100, 860, u), lerp(420, 700, u)
    else:
        u = (q - 0.6) / 0.4
        a = -0.35 + u * 2.4
        x, y = 540 + math.cos(a) * 330, 800 + math.sin(a) * 180
    K.orbit(img, 540, 800, 330, 180, col=(214, 214, 220))
    K.phobos(img, x, y, 44, ang=t * 2)
    FL.big(img, 540, 1240, "¿ASTEROIDE?", 80, INK, clamp((t - 0.4) / 0.3))
    _h(img, "asteroid", t)


def sh_impact(img, t, T, L):
    K.stars(img, seed=23, n=20)
    K.mars(img, 540, 800, 220)
    d = K.D(img)
    q = clamp(t / 1.0)
    if q < 1:
        K.phobos(img, lerp(1000, 700, q), lerp(420, 650, q), 70, ang=t)
    else:
        u = ease(clamp((t - 1.0) / 1.6))
        for i in range(16):
            a = -0.9 + i * 0.12
            r = 240 + 200 * u + (i % 3) * 20
            x, y = 540 + math.cos(a) * r, 800 + math.sin(a) * r * 0.8
            d.ellipse([x - 12, y - 10, x + 12, y + 10], fill=K.MARS_D, outline=INK, width=2)
        FL.big(img, 720, 640, "¡BUM!", 90, RED, clamp((t - 1.0) / 0.2))
    FL.pill(img, 640, 1250, "¿CHOQUE GIGANTE?", clamp((t - lt(L, 0, 0.6)) / 0.3), col=RED)
    _h(img, "impact", t)


def sh_dust(img, t, T, L):
    K.stars(img, seed=29, n=18)
    K.mars(img, 330, 860, 230)
    K.phobos(img, 850, 540, 90, ang=0.2)
    d = K.D(img)
    for n in range(3):
        tk = 0.6 + n * 1.3
        if t < tk:
            continue
        u = clamp((t - tk) / 1.6)
        sx, sy = 330 + 150, 860 - 160 + n * 40
        d.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], outline=RED, width=int(6 * (1 - u)) + 1)
        for i in range(8):
            p = clamp(u * 1.2 - i * 0.05)
            x, y = lerp(sx, 850 + (i - 4) * 14, p), lerp(sy, 560 + (i % 3) * 14, p) - 120 * math.sin(p * math.pi)
            d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=K.MARS)
    if t > lt(L, 0, 0.35):
        FL.pill(img, 640, 1250, "RESTOS DE MARTE", ease(clamp((t - lt(L, 0, 0.35)) / 0.3)), col=RED)
    _h(img, "dust", t)


def sh_capsule(img, t, T, L):
    K.australia(img, 560, 960, 330, clamp(t / 0.4))
    q = ease(clamp(t / 3.2))
    K.capsule(img, 600, lerp(460, 900, q), 0.9, chute=clamp((t - 0.4) / 0.5))
    FL.big(img, 860, 480, "2031", 120, RED, clamp((t - 0.2) / 0.3))
    _h(img, "capsule", t)


def sh_answer(img, t, T, L):
    K.stars(img, seed=31, n=20)
    K.mars(img, 300, 820, 200)
    K.phobos(img, 760, 620, 110, ang=0.1 * math.sin(t))
    d = K.D(img)
    k = ease(clamp((t - lt(L, 0, 0.6)) / 0.4))
    if k > 0:
        r = 170 * pop(k)
        d.ellipse([760 - r, 620 - r, 760 + r, 620 + r], outline=RED, width=10)
        FL.pill(img, 760, 860, "SU LUNA", k, col=RED)
    _h(img, "answer", t)


FNS = {n: globals()["sh_" + n] for n in NAMES}
FOCUS_PT = {n: (540, 800) for n in NAMES}

AUDIO = {
    "music": [("q", "mystery"), ("japan", "epic"), ("phobos", "exp"), ("arrive", "premium"), ("asteroid", "tension"),
              ("capsule", "epic"), ("answer", "premium")],
    "gains": {"exp": 0.6, "epic": 0.8, "tension": 0.75},
    "amb": {"space": ["q", "phobos", "potato", "orbit3", "arrive", "asteroid", "impact", "dust", "answer"],
            "hum": ["rover", "sample"], "crowd": ["launch"]},
    "sfx": [("q+0.3", "swell", 0.08), ("japan+0.2", "pop", 0.06), ("launch+0.9", "rumble", 0.35),
            ("launch+1.0", "whoosh_up", 0.1), ("phobos+0.4", "whoosh", 0.07), ("potato+0.6", "tick", 0.06),
            ("orbit3+0.3", "whoosh", 0.07), ("arrive+0.5", "chime", 0.05), ("rover+0.4", "click", 0.1),
            ("sample+1.6", "pop", 0.08), ("impact+1.0", "boom", 0.4), ("dust+0.6", "whoosh", 0.07),
            ("capsule+0.5", "swell", 0.08), ("answer+0.5", "ding", 0.06)],
    "bpm": 100,
}
