"""07 · ¿Por qué los aviones no vuelan en línea recta? — estilo 7 con el formato nuevo (pregunta de gancho respondida al
final, Ojo físico actuando en algunas escenas, marcador rojo, transiciones variadas). Elegido por Iker el 21/10
(«Aviones en curva»). Distancias calculadas (círculo máximo vs loxodrómica, R = 6.371 km): Madrid–Los Ángeles 9.388 km
frente a 10.186 km (≈ 800 km menos); Madrid–Tokio 10.768 frente a 12.561 (≈ 1.800 km menos, la ruta corta sube hasta
68° N, por encima del Círculo Polar). África ≈ 30,4 millones de km² y Groenlandia ≈ 2,2 → unas 14 veces."""
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
TITLE = "07_Aviones_curva_estilo7"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c07_aviones")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Por qué los aviones no vuelan en *línea recta*?",
    "Mira en el mapa un vuelo de Madrid a Los Ángeles: en vez de ir recto… hace *una curva* hacia el norte.",
    "Sube por encima de Canadá, cerca de *Labrador*… y luego baja hasta California.",
    "Parece un rodeo. Pero es justo al revés: es *el camino más corto*.",
    "El truco está en el mapa: la Tierra es una *bola*, y para dibujarla plana hay que estirarla.",
    "Por eso en el mapa Groenlandia parece casi tan grande como África… y África es *14 veces* más grande.",
    "Coge una pelota y un hilo: el camino más corto entre dos puntos es un *círculo máximo*.",
    "Y al aplastarlo en el mapa… se ve *curvado*.",
    "Ir «recto» por el mapa de Madrid a Los Ángeles serían unos *10.200 kilómetros*.",
    "Por la curva, unos 9.400: casi *800 kilómetros menos*.",
    "A Tokio la diferencia es aún mayor: la ruta más corta cruza el *Círculo Polar*… y ahorra unos *1.800 kilómetros*.",
    "Además, los pilotos buscan el *viento*: hacia el este aprovechan la corriente en chorro, y hacia el oeste la esquivan.",
    "Así que… ¿por qué no vuelan en línea recta? Sí que lo hacen… pero *sobre una bola*, no sobre un papel.",
]
OUTRO_LINE = "La próxima vez que mires la pantalla del avión, ya sabes por qué hace la curva… ¡Ojo al dato!"
NAMES = ["q", "route", "labrador", "shortest", "stretch", "greenland", "thread", "flat", "straight", "curve", "tokyo",
         "wind", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("thread", 0.8)
HEAD = {
    0: ("¿En línea recta?", "POR QUÉ LOS AVIONES HACEN CURVAS"),
    1: ("Madrid → Los Ángeles", "EN EL MAPA HACE UNA CURVA"),
    2: ("Por Canadá", "CERCA DE LABRADOR"),
    3: ("¿Un rodeo?", "NO: EL CAMINO MÁS CORTO"),
    4: ("El mapa miente", "UNA BOLA ESTIRADA EN PLANO"),
    5: ("África ×14", "GROENLANDIA ENGAÑA"),
    6: ("Pelota e hilo", "EL CÍRCULO MÁXIMO"),
    7: ("Aplastado", "EN EL MAPA SE CURVA"),
    8: ("10.200 km", "«RECTO» POR EL MAPA"),
    9: ("−800 km", "POR LA CURVA"),
    10: ("Madrid → Tokio", "CRUZA EL CÍRCULO POLAR"),
    11: ("El viento", "LA CORRIENTE EN CHORRO"),
    12: ("La respuesta", "RECTO… PERO SOBRE UNA BOLA"),
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
TRANS_PLAN = ["zoom_in", "whip", "flash", "zoom_out", "spin", "iris", "flash", "whip_r", "drop", "zoom_out", "glitch", "iris"]
TRANS_SEED = 41
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
FL.TH["narr"] = True
OJO_TRAJE = "c_fisico"
OJO_POSES = {"q": "think", "route": "point", "labrador": "point", "shortest": "smirk", "stretch": "point",
             "greenland": "surprise", "thread": "point", "flat": "point", "straight": "point", "curve": "smirk",
             "tokyo": "surprise", "wind": "point", "answer": "smirk"}
ACT = ("thread", "answer")         # escenas en las que Ojo actúa (se esconde el narrador de la esquina)
NARR = (lambda img, V, t, shots, si: None if shots[si]["name"] in ACT else FL.NARR(img, V, t, shots, si))
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
OUTRO_MIN = 5.0
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
IDX = {n: i for i, n in enumerate(NAMES)}
MAD, LAX, TYO = (40.47, -3.56), (33.94, -118.41), (35.55, 139.78)
BOX = (40, 420, 1040, 1120, -150, 30, 72, 18)          # mapa del Atlántico norte (Madrid–Los Ángeles)
BOXW = (40, 440, 1040, 1100, -180, 180, 80, -60)       # mapamundi


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def _h(img, name, t):
    FL.head(img, t, IDX[name])


def _route(img, box, a, b, k, col=RED, w=8, plane=True):
    pts = [K.merc(lo, la, box) for lo, la in K.gc_points(a, b, 80)]
    n = max(2, int(len(pts) * clamp(k)))
    d = K.D(img)
    d.line(pts[:n], fill=col, width=w)
    if plane and n >= 2:
        (x0, y0), (x1, y1) = pts[n - 2], pts[n - 1]
        K.plane_top(img, x1, y1, math.atan2(y1 - y0, x1 - x0), 1.3)


def _straight(img, box, a, b, k, col=INK, w=6):
    p0, p1 = K.merc(a[1], a[0], box), K.merc(b[1], b[0], box)
    d = K.D(img)
    n = 30
    for i in range(int(n * clamp(k))):
        if i % 2 == 0:
            d.line([(lerp(p0[0], p1[0], i / n), lerp(p0[1], p1[1], i / n)), (lerp(p0[0], p1[0], (i + 1) / n), lerp(p0[1], p1[1], (i + 1) / n))],
                   fill=col, width=w)


def _dots(img, box, *pts):
    d = K.D(img)
    for la, lo, lab in pts:
        x, y = K.merc(lo, la, box)
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=INK)
        txt(img, (x, y + 36), lab, 34, INK)


def _ojo(img, cx, cy, sc, pose="point", ang=0.0):
    import ojo as OJ
    from PIL import Image
    f = OJ.figure(pose, OJO_TRAJE, 0.0, (0.05, 0.0), 0.0)
    ff = f.resize((max(1, int(f.width * sc)), max(1, int(f.height * sc))), Image.BILINEAR)
    if abs(ang) > 0.01:
        ff = ff.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    img.paste(ff, (int(cx - ff.width / 2), int(cy - ff.height / 2)), ff)


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    K.world_map(img, BOX)
    _dots(img, BOX, (MAD[0], MAD[1], "Madrid"), (LAX[0], LAX[1], "Los Ángeles"))
    _straight(img, BOX, MAD, LAX, clamp(t / 1.0))
    _route(img, BOX, MAD, LAX, clamp((t - 0.8) / 1.6), plane=False)
    FL.big(img, 930, 500, "?", 150, RED, clamp((t - 1.0) / 0.3))
    _h(img, "q", t)


def sh_route(img, t, T, L):
    K.world_map(img, BOX)
    _dots(img, BOX, (MAD[0], MAD[1], "Madrid"), (LAX[0], LAX[1], "Los Ángeles"))
    _route(img, BOX, MAD, LAX, clamp(t / max(1.0, T - 0.5)))
    _h(img, "route", t)


def sh_labrador(img, t, T, L):
    z = 1 + 0.25 * ease(clamp(t / 2.5))
    box = (40 - 300 * (z - 1), 420 - 160 * (z - 1), 1040 + 300 * (z - 1), 1120 + 160 * (z - 1), -150, 30, 72, 18)
    K.world_map(img, box, clip=(40, 420, 1040, 1120))
    _route(img, box, MAD, LAX, 1.0, plane=False)
    x, y = K.merc(-62, 54.5, box)
    k = pop(clamp((t - 0.4) / 0.4))
    if k > 0:
        d = K.D(img)
        d.ellipse([x - 70 * k, y - 70 * k, x + 70 * k, y + 70 * k], outline=RED, width=8)
        FL.pill(img, x + 40, y - 120, "LABRADOR", clamp((t - 0.6) / 0.3), col=RED)
    d = K.D(img)
    d.rectangle([0, 0, W, 418], fill=BG)
    d.rectangle([0, 1123, W, H], fill=BG)
    d.rectangle([0, 0, 38, H], fill=BG)
    d.rectangle([1042, 0, W, H], fill=BG)
    d.rectangle([40, 420, 1040, 1120], outline=INK, width=5)
    _h(img, "labrador", t)


def sh_shortest(img, t, T, L):
    K.world_map(img, BOX)
    _straight(img, BOX, MAD, LAX, 1.0)
    _route(img, BOX, MAD, LAX, 1.0, plane=False)
    FL.stamp(img, 640, 1240, "EL MÁS CORTO", clamp((t - lt(L, 0, 0.55)) / 0.3))
    _h(img, "shortest", t)


def sh_stretch(img, t, T, L):
    """La bola se «pela» y se estira en un rectángulo."""
    q = ease(clamp((t - 0.6) / 2.2))
    d = K.D(img)
    if q < 0.98:
        r = 300
        w = lerp(r, 520, q)
        h_ = lerp(r, 360, q)
        d.rounded_rectangle([540 - w, 760 - h_, 540 + w, 760 + h_], radius=int(lerp(r, 10, q)), fill=K.SEA, outline=INK, width=8)
        for k in range(-2, 3):
            yy = 760 + k * h_ / 3
            d.line([(540 - w * (1 - 0.3 * (1 - q) * abs(k) / 2), yy), (540 + w * (1 - 0.3 * (1 - q) * abs(k) / 2), yy)], fill=(190, 206, 224), width=3)
    else:
        K.world_map(img, BOXW)
    for n in range(4):
        a = n * math.pi / 2 + math.pi / 4
        k = clamp((t - 0.8) / 0.4)
        x0, y0 = 540 + math.cos(a) * 340, 760 + math.sin(a) * 260
        d.line([(x0, y0), (x0 + math.cos(a) * 120 * k, y0 + math.sin(a) * 120 * k)], fill=RED, width=10)
    _h(img, "stretch", t)


def sh_greenland(img, t, T, L):
    a = lt(L, 0, 0.55)
    if t < a:
        K.world_map(img, BOXW, hi=("gl", "af"))
    else:
        # tamaños reales: África ~14 veces Groenlandia (área) → lado ~3,7 veces
        d = K.D(img)
        k = ease(clamp((t - a) / 0.6))
        sa, sg = 260, 70 * lerp(2.2, 1.0, k)
        af = [(x, -y) for x, y in [(-17, 21), (-10, 30), (-5, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 12),
                                   (40, -5), (40, -15), (35, -25), (28, -34), (18, -35), (12, -18), (9, -2), (9, 4), (-8, 5), (-15, 11)]]
        d.polygon([(380 + x / 35 * sa, 760 + y / 35 * sa) for x, y in af], fill=RED, outline=INK)
        gl = [(x + 45, -(y - 72)) for x, y in [(-73, 78), (-40, 83), (-20, 80), (-20, 70), (-43, 60), (-55, 65), (-60, 75)]]
        d.polygon([(860 + x / 25 * sg, 700 + y / 25 * sg) for x, y in gl], fill=(120, 170, 220), outline=INK)
        txt(img, (380, 1110), "África", 44, INK)
        txt(img, (860, 1110), "Groenlandia", 44, INK)
        FL.big(img, 860, 520, "×14", 110, RED, clamp((t - a - 0.4) / 0.3))
    _h(img, "greenland", t)


def sh_thread(img, t, T, L):
    """Ojo tensa un hilo rojo sobre una pelota."""
    K.globe(img, 600, 760, 300, rot=t * 0.3)
    k = ease(clamp((t - 0.4) / 1.4))
    d = K.D(img)
    pts = []
    for i in range(41):
        u = i / 40
        a = math.pi * (0.85 - 0.7 * u)
        pts.append((600 + math.cos(a) * 300 * 0.98, 760 - math.sin(a) * 300 * 0.55 - 60))
    n = max(2, int(41 * k))
    d.line(pts[:n], fill=RED, width=9)
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - 14, p[1] - 14, p[0] + 14, p[1] + 14], fill=INK)
    _ojo(img, 200, 1000, 0.75, "point", ang=0.05 * math.sin(t * 2))
    _h(img, "thread", t)


def sh_flat(img, t, T, L):
    K.world_map(img, BOX)
    _route(img, BOX, MAD, LAX, 1.0, plane=False)
    k = pop(clamp((t - 0.3) / 0.4))
    if k > 0:
        FL.pill(img, 540, 1240, "EN EL MAPA SE VE CURVA", k)
    _h(img, "flat", t)


def sh_straight(img, t, T, L):
    K.world_map(img, BOX)
    _straight(img, BOX, MAD, LAX, clamp(t / 1.2), col=INK, w=8)
    FL.big(img, 640, 1240, "10.200 km", 110, INK, clamp((t - lt(L, 0, 0.6)) / 0.3))
    _h(img, "straight", t)


def sh_curve(img, t, T, L):
    K.world_map(img, BOX)
    _straight(img, BOX, MAD, LAX, 1.0, col=SOFT, w=6)
    _route(img, BOX, MAD, LAX, clamp(t / 1.4))
    FL.big(img, 640, 1240, "9.400 km", 110, RED, clamp((t - 0.5) / 0.3))
    k = clamp((t - lt(L, 0, 0.6)) / 0.3)
    if k > 0:
        FL.pill(img, 760, 470, "−800 km", k, col=RED)
    _h(img, "curve", t)


def sh_tokyo(img, t, T, L):
    K.world_map(img, BOXW)
    d = K.D(img)
    _, y66 = K.merc(0, 66.6, BOXW)
    for x in range(40, 1040, 30):
        d.line([(x, y66), (x + 15, y66)], fill=(80, 140, 220), width=4)
    _dots(img, BOXW, (MAD[0], MAD[1], "Madrid"), (TYO[0], TYO[1], "Tokio"))
    _straight(img, BOXW, MAD, TYO, 1.0, col=SOFT)
    _route(img, BOXW, MAD, TYO, clamp(t / 2.0))
    FL.big(img, 640, 1240, "−1.800 km", 110, RED, clamp((t - lt(L, 0, 0.75)) / 0.3))
    _h(img, "tokyo", t)


def sh_wind(img, t, T, L):
    K.world_map(img, BOX)
    d = K.D(img)
    for k in range(5):
        y = 560 + k * 26
        off = (t * 260 + k * 90) % 1000
        x = 40 + off
        d.line([(x, y), (x + 120, y - 8)], fill=(80, 140, 220), width=8)
        d.polygon([(x + 120, y - 20), (x + 150, y - 10), (x + 120, y + 4)], fill=(80, 140, 220))
    FL.pill(img, 640, 1240, "CORRIENTE EN CHORRO", clamp((t - 0.4) / 0.3))
    _h(img, "wind", t)


def sh_answer(img, t, T, L):
    K.globe(img, 640, 760, 280, rot=t * 0.4)
    d = K.D(img)
    a0 = -2.5 + t * 0.4
    pts = [(640 + math.cos(a0 + u * 0.03) * 280 * 0.96, 760 + math.sin(a0 + u * 0.03) * 280 * 0.4 - 40) for u in range(60)]
    d.line(pts, fill=RED, width=9)
    K.plane_top(img, pts[-1][0], pts[-1][1], a0 + 1.8 + math.pi / 2, 1.6)
    _ojo(img, 210, 1000, 0.75, "smirk")
    FL.pill(img, 700, 1220, "SOBRE UNA BOLA", clamp((t - lt(L, 0, 0.6)) / 0.3), col=RED)
    _h(img, "answer", t)


FNS = {n: globals()["sh_" + n] for n in NAMES}
FOCUS_PT = {n: (540, 780) for n in NAMES}

AUDIO = {
    "music": [("q", "synthwave")],
    "gains": {},
    "amb": {},
    "sfx": [("q+0.3", "swell", 0.08), ("route+0.3", "whoosh", 0.07), ("labrador+0.4", "pop", 0.06), ("shortest+0.6", "ding", 0.06),
            ("stretch+0.6", "whoosh_up", 0.07), ("greenland+0.4", "pop", 0.06), ("thread+0.5", "click", 0.1), ("flat+0.3", "pop", 0.06),
            ("straight+0.3", "tick", 0.06), ("curve+0.5", "ding", 0.06), ("tokyo+0.4", "whoosh", 0.07), ("wind+0.3", "whoosh", 0.07),
            ("answer+0.4", "ding", 0.06)],
    "bpm": 100,
}
