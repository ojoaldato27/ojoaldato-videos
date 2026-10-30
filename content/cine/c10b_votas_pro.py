"""10b · ¿Votas al presidente? No: así se elige — FORMATO PRO (referencia 09b · Microondas, Iker 30/10).
Política fácil y neutral, sin partidos. Datos: Constitución art. 68 (Congreso de 350 diputados, circunscripción provincial,
Ceuta y Melilla 1 cada una) y art. 99 (el Rey, tras consultar a los grupos, propone candidato; 1.ª votación mayoría absoluta
= 176; 2.ª votación 48 h después, mayoría simple; si en dos meses desde la primera votación nadie es investido, se disuelven
las Cortes y hay nuevas elecciones). Francia: presidente elegido por sufragio directo."""
import os
import math
from gadgets import *            # noqa: F401,F403
import flat3 as FL
import vid2
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED, SOFT, txt
from PIL import Image
import pro
from pro import solid, glow, ojo, hook_text, lt, WHITE

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "10b_Votas_presidente_pro"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c10b_votas")
VOICE = _VZ + ".mp3"
LINES = [
    "¿En España votas al presidente del Gobierno? *No*.",
    "En tu papeleta no hay ningún presidente: hay una *lista* de candidatos a diputado.",
    "Con todos los votos se reparten los *350 escaños* del Congreso.",
    "Y cada *provincia* elige sus propios diputados.",
    "Después, el Rey habla con los grupos y propone a un *candidato*.",
    "Ese candidato cuenta su plan en el Congreso: es el *debate de investidura*.",
    "Pero ojo: no le basta con ganar las elecciones. En la primera votación necesita *176 síes*.",
    "Si no llega, 48 horas después le vale con *más síes que noes*.",
    "Por eso muchas veces hay que *ponerse de acuerdo*… y si en *dos meses* nadie lo consigue, se repiten las elecciones.",
    "En otros países, como Francia, sí se vota *directamente* al presidente.",
    "Así que… ¿votas al presidente? No: votas a *diputados*… y ellos lo eligen.",
]
OUTRO_LINE = "Ahora ya sabes lo que haces de verdad con tu papeleta… ¡Ojo al dato!"
NAMES = ["q", "ballot", "congress", "prov", "king", "debate", "vote1", "vote2", "deals", "compare", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("vote1", 0.5)
HEAD = {i: ("", "") for i in range(len(NAMES))}
NARRATOR = {}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {}
FL.use("minimal", HEAD)

FRAME = vid2.frame
FPS = 60
BG = (246, 238, 226)
TRANS_POOL = ["suave"]
TRANS_PLAN = ["suave", "suave_out", "deriva", "suave", "suave_out", "deriva_r", "suave", "suave_out", "deriva", "suave"]
TRANS_SEED = 43
TD = 0.9
CAM_PUSH = 0.08
SHAKE = 0
CUT_SFX = False
FL.TH["narr"] = True
OJO_TRAJE = "c_profe"
OJO_POSES = {}
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
GRAY = (196, 196, 204)
GREEN = (60, 170, 100)
GOLD = (236, 190, 60)
BLUE = (70, 130, 220)

# ------------------------------------------------------------------ piezas
_SEATS = {}


def seats(n=350, rows=10):
    if n in _SEATS:
        return _SEATS[n]
    radii = [0.42 + 0.58 * r / (rows - 1) for r in range(rows)]
    tot = sum(radii)
    cnt = [round(n * r / tot) for r in radii]
    cnt[-1] += n - sum(cnt)
    out = []
    for r, c in zip(radii, cnt):
        for j in range(c):
            out.append((math.pi * (1 - (j + 0.5) / c), r))
    out.sort(key=lambda p: -p[0])
    _SEATS[n] = out
    return out


def hemicycle(img, cx, cy, R, k=1.0, n=350, col=lambda i: GRAY, dot=None):
    d = K.D(img)
    dot = dot or max(3, R * 0.024)
    S = seats(n)
    m = int(len(S) * clamp(k))
    d.pieslice([cx - R * 1.08, cy - R * 1.08, cx + R * 1.08, cy + R * 1.08], 180, 360, fill=(250, 246, 238), outline=INK, width=5)
    for i, (a, r) in enumerate(S[:m]):
        x, y = cx + math.cos(a) * R * r, cy - math.sin(a) * R * r
        d.ellipse([x - dot, y - dot, x + dot, y + dot], fill=col(i))
    d.line([(cx - R * 1.08, cy), (cx + R * 1.08, cy)], fill=INK, width=6)


def ballot(img, cx, cy, s=1.0, ang=0.0, k=1.0):
    if s < 0.08:
        return
    lay = Image.new("RGBA", (int(360 * s), int(480 * s)), (0, 0, 0, 0))
    d = K.D(lay)
    d.rounded_rectangle([4, 4, lay.width - 4, lay.height - 4], radius=int(12 * s), fill=WHITE, outline=INK, width=max(2, int(6 * s)))
    d.rectangle([24 * s, 24 * s, lay.width - 24 * s, 80 * s], fill=(230, 230, 236))
    txt(lay, (lay.width / 2, 52 * s), "CONGRESO", int(30 * s), INK)
    for j in range(int(6 * clamp(k))):
        y = 120 * s + j * 54 * s
        d.ellipse([34 * s, y + 6 * s, 52 * s, y + 24 * s], outline=INK, width=max(1, int(3 * s)))
        d.text((64 * s, y), f"Candidato/a {j + 1}", font=F(FL.INTER_X, max(2, int(26 * s))), fill=INK)
    if abs(ang) > 0.01:
        lay = lay.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    x, y = int(cx - lay.width / 2), int(cy - lay.height / 2)
    if img.mode == "RGBA":
        img.alpha_composite(lay, (max(0, x), max(0, y)))
    else:
        img.paste(lay, (x, y), lay)


def urn(img, cx, cy, s=1.0):
    d = K.D(img)
    d.rounded_rectangle([cx - 150 * s, cy - 120 * s, cx + 150 * s, cy + 150 * s], radius=int(14 * s), fill=(214, 232, 248, 235), outline=INK, width=max(2, int(7 * s)))
    d.rectangle([cx - 160 * s, cy - 140 * s, cx + 160 * s, cy - 110 * s], fill=WHITE, outline=INK, width=max(2, int(6 * s)))
    d.rectangle([cx - 70 * s, cy - 131 * s, cx + 70 * s, cy - 119 * s], fill=INK)


def crown(img, cx, cy, s=1.0):
    d = K.D(img)
    pts = [(-90, 40), (-90, -30), (-50, 10), (0, -50), (50, 10), (90, -30), (90, 40)]
    d.polygon([(cx + x * s, cy + y * s) for x, y in pts], fill=GOLD, outline=INK, width=max(2, int(6 * s)))
    for x, y in [(-90, -30), (0, -50), (90, -30)]:
        d.ellipse([cx + (x - 12) * s, cy + (y - 12) * s, cx + (x + 12) * s, cy + (y + 12) * s], fill=RED, outline=INK, width=3)


def bubble(img, cx, cy, w, h, s, k=1.0):
    if k <= 0:
        return
    d = K.D(img)
    sc = pop(k)
    w, h = w * sc, h * sc
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(h / 3), fill=WHITE, outline=INK, width=5)
    d.polygon([(cx - 20, cy + h / 2 - 2), (cx + 10, cy + h / 2 - 2), (cx - 30, cy + h / 2 + 34)], fill=WHITE, outline=INK)
    if sc > 0.6:
        txt(img, (cx, cy), s, int(40 * sc), INK)


def podium(img, cx, gy, s=1.0):
    d = K.D(img)
    d.polygon([(cx - 110 * s, gy), (cx + 110 * s, gy), (cx + 85 * s, gy - 200 * s), (cx - 85 * s, gy - 200 * s)], fill=(170, 110, 70), outline=INK, width=6)
    d.rectangle([cx - 100 * s, gy - 220 * s, cx + 100 * s, gy - 196 * s], fill=(140, 86, 50), outline=INK, width=5)


def person(img, x, y, s=1.0, col=(120, 120, 130)):
    d = K.D(img)
    d.ellipse([x - 22 * s, y - 120 * s, x + 22 * s, y - 76 * s], fill=col, outline=INK, width=4)
    d.rounded_rectangle([x - 34 * s, y - 70 * s, x + 34 * s, y], radius=int(20 * s), fill=col, outline=INK, width=4)


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    """GANCHO, fotograma 1: Ojo ya metiendo la papeleta en la urna, pregunta gigante y un NO rotundo."""
    u = ease(clamp(t / 1.4))

    def scene(Lr):
        urn(Lr, 660, 1060, 1.15)
        ballot(Lr, 660, lerp(760, 930, u), 0.5, ang=0.12 * (1 - u))
        urn(Lr, 660, 1060, 1.15) if u > 0.97 else None
    solid(img, scene)
    ojo(img, 300, 1420, 0.92, "point" if t < 1.6 else "think", t=t)
    hook_text(img, [("¿VOTAS AL", False), ("PRESIDENTE?", True)], 1.0 if t < T - 0.7 else clamp((T - t) / 0.7), y=440, size=112)
    k = clamp((t - lt(L, 0, 0.75)) / 0.3)
    if k > 0:
        FL.stamp(img, 840, 820, "NO", k, col=RED)


def sh_ballot(img, t, T, L):
    """La papeleta en grande: una lupa busca al presidente… y solo hay candidatos a diputado."""
    z = ease(clamp(t / 1.0))
    solid(img, lambda Lr: ballot(Lr, 600, 860, lerp(0.7, 1.45, z), k=clamp((t - 0.4) / 1.2)))
    a = t * 1.8
    lx, ly = 600 + 170 * math.cos(a), 840 + 140 * math.sin(a * 1.3)

    def lens(Lr):
        d = K.D(Lr)
        d.ellipse([lx - 84, ly - 84, lx + 84, ly + 84], fill=(220, 236, 250, 90), outline=INK, width=12)
        d.line([(lx + 60, ly + 60), (lx + 136, ly + 136)], fill=INK, width=20)
    solid(img, lens)
    ojo(img, 170, 1430, 0.78, "think", t=t)
    FL.pill(img, 640, 1360, "LISTA DE DIPUTADOS", clamp((t - lt(L, 0, 0.6)) / 0.3), col=RED)


def sh_congress(img, t, T, L):
    """El hemiciclo se llena escaño a escaño hasta 350, con contador."""
    z = ease(clamp(t / 1.4))
    k = clamp((t - 0.2) / 2.2)
    solid(img, lambda Lr: hemicycle(Lr, 540, 1080, lerp(700, 470, z), k))
    FL.big(img, 540, 980, f"{int(350 * k)}", 130, RED, clamp(t / 0.3))
    FL.pill(img, 540, 1250, "ESCAÑOS", clamp((t - 0.3) / 0.3))


SPAIN = [(-0.95, -0.55), (-0.2, -0.75), (0.45, -0.62), (0.9, -0.42), (0.85, -0.05), (0.55, 0.2), (0.45, 0.6), (0.0, 0.85),
         (-0.55, 0.75), (-0.75, 0.35), (-0.7, -0.05), (-1.0, -0.3)]
PROV = [(-0.75, -0.4, 4), (-0.45, -0.45, 3), (-0.1, -0.5, 5), (0.3, -0.45, 3), (0.65, -0.25, 12), (0.6, 0.05, 6), (-0.55, -0.1, 3),
        (-0.15, -0.1, 37), (0.2, -0.15, 2), (0.35, 0.3, 8), (-0.45, 0.35, 5), (-0.1, 0.45, 12), (0.25, 0.6, 5), (-0.25, 0.7, 3)]


def sh_prov(img, t, T, L):
    """Mapa: cada provincia se ilumina con sus escaños (círculos más o menos grandes)."""
    cx, cy, s = 560, 850, 430 * (1 + 0.06 * ease(clamp(t / max(1, T))))
    solid(img, lambda Lr: K.D(Lr).polygon([(cx + x * s, cy + y * s) for x, y in SPAIN], fill=(240, 236, 228), outline=INK, width=8))
    d = K.D(img)
    for i, (x, y, n) in enumerate(PROV):
        k = clamp((t - 0.2 - i * 0.1) / 0.3)
        if k <= 0:
            continue
        r = (14 + 6 * math.sqrt(n)) * pop(k)
        d.ellipse([cx + x * s - r, cy + y * s - r, cx + x * s + r, cy + y * s + r], fill=RED if n > 10 else (240, 140, 140), outline=INK, width=3)
    ojo(img, 170, 1430, 0.72, "point", t=t)
    FL.pill(img, 640, 1360, "CADA PROVINCIA ELIGE", clamp((t - lt(L, 0, 0.45)) / 0.3))


def sh_king(img, t, T, L):
    """La corona escucha a los grupos (bocadillos grises, sin colores de partido) y señala a un candidato: Ojo."""
    glow(img, 540, 560, 260, 160, GOLD, 0.5)
    solid(img, lambda Lr: crown(Lr, 540, 560 + 8 * math.sin(t * 2), 1.3))
    for j in range(4):
        x = 200 + j * 230
        k = clamp((t - 0.25 - j * 0.22) / 0.3)
        bubble(img, x, 760, 160, 80, "…", k)
        solid(img, lambda Lr, x=x: person(Lr, x, 980, 1.2), sh=0.2)
    k = ease(clamp((t - lt(L, 0, 0.55)) / 0.4))
    if k > 0:
        glow(img, 540, 1250, 200, 160, GOLD, 0.6 * k)
        ojo(img, 540, 1440, 0.82 * pop(k) + 0.01, "wave", t=t)
        FL.pill(img, 820, 1360, "CANDIDATO", k, col=RED)


def sh_debate(img, t, T, L):
    """Ojo en la tribuna con el hemiciclo detrás; bocadillo «Mi plan…»."""
    z = ease(clamp(t / max(1, T)))
    solid(img, lambda Lr: hemicycle(Lr, 540, 900 + 40 * z, lerp(470, 540, z)), sh=0.18)
    solid(img, lambda Lr: podium(Lr, 540, 1440, 1.05))
    ojo(img, 540, 1240, 0.72, "point" if (t % 1.6) < 0.8 else "wave", t=t)
    bubble(img, 810, 560, 300, 96, "Mi plan…", clamp((t - 0.5) / 0.3))


def sh_vote1(img, t, T, L):
    """GIRO: «Pero ojo». Los escaños se encienden en verde; barra con la raya roja de 176."""
    k = clamp((t - 1.2) / max(1.5, T - 2.2))
    yes = int(176 * ease(k))
    solid(img, lambda Lr: hemicycle(Lr, 540, 1000, 470, col=lambda i: GREEN if i < yes else GRAY))

    def bar(Lr):
        d = K.D(Lr)
        d.rounded_rectangle([140, 1110, 940, 1170], radius=30, fill=(232, 232, 236), outline=INK, width=5)
        if yes:
            d.rounded_rectangle([140, 1110, 140 + max(60, 800 * yes / 350), 1170], radius=30, fill=GREEN)
        xm = 140 + 800 * 176 / 350
        d.line([(xm, 1090), (xm, 1190)], fill=RED, width=8)
    solid(img, bar)
    if t > 1.2:
        FL.big(img, 540, 880, f"{yes}", 130, GREEN if yes >= 176 else INK, 1.0)
    FL.pill(img, 540, 1270, "176 = MAYORÍA ABSOLUTA", clamp((t - 1.5) / 0.3), col=RED)
    if t < 1.5:
        FL.stamp(img, 540, 760, "PERO OJO", clamp(t / 0.35) * clamp((1.5 - t) / 0.25), col=RED)


def sh_vote2(img, t, T, L):
    """Reloj de 48 h y después una balanza: síes contra noes."""
    if t < 1.3:
        FL.clock(img, 540, 840, 230, t * 6)
        FL.big(img, 540, 1180, "48 h", 120, RED, clamp(t / 0.3))
    else:
        u = ease(clamp((t - 1.3) / 0.8))
        tilt = -0.18 * u

        def scale(Lr):
            d = K.D(Lr)
            cx, cy = 540, 700
            d.polygon([(cx - 70, 1260), (cx + 70, 1260), (cx, 720)], fill=(206, 206, 216), outline=INK, width=6)
            x1, y1 = cx - 330 * math.cos(tilt), cy + 330 * math.sin(-tilt)
            x2, y2 = cx + 330 * math.cos(tilt), cy - 330 * math.sin(-tilt)
            d.line([(x1, y1), (x2, y2)], fill=INK, width=12)
            for (x, y, lab, col) in [(x1, y1, "SÍ", GREEN), (x2, y2, "NO", RED)]:
                d.line([(x, y), (x - 80, y + 160)], fill=INK, width=4)
                d.line([(x, y), (x + 80, y + 160)], fill=INK, width=4)
                d.chord([x - 130, y + 90, x + 130, y + 230], 0, 180, fill=col, outline=INK, width=5)
                txt(Lr, (x, y + 185), lab, 50, WHITE)
        solid(img, scale)
        ojo(img, 170, 1430, 0.72, "smirk", t=t)


def sh_deals(img, t, T, L):
    """Piezas de puzle grises que se juntan hasta pasar la raya de 176; luego un calendario de 2 meses y la urna otra vez."""
    widths = [0.3, 0.14, 0.06, 0.05]
    mid = lt(L, 0, 0.5)
    if t < mid:
        def puzzle(Lr):
            d = K.D(Lr)
            x = 140
            for j, w in enumerate(widths):
                k = ease(clamp((t - j * 0.45) / 0.6))
                ww = 800 * w
                xx = lerp(x + 400 * (j % 2 * 2 - 1) * 0.6, x, k) if j else x
                yy = lerp(620, 820, k) if j else 820
                d.rounded_rectangle([xx, yy, xx + ww - 8, yy + 130], radius=18, fill=(150 + 25 * j, 150 + 25 * j, 162 + 20 * j), outline=INK, width=5)
                x += ww
            xm = 140 + 800 * 176 / 350
            d.line([(xm, 760), (xm, 1010)], fill=RED, width=8)
        solid(img, puzzle)
        txt(img, (140 + 800 * 176 / 350, 1050), "176", 46, RED)
        ojo(img, 300, 1430, 0.78, "point", t=t)
        FL.pill(img, 720, 1360, "PONERSE DE ACUERDO", clamp((t - 0.6) / 0.3), col=RED)
    else:
        u = t - mid
        pages = int(clamp(u / 1.3) * 60)

        def cal(Lr):
            d = K.D(Lr)
            d.rounded_rectangle([300, 560, 780, 1040], radius=24, fill=WHITE, outline=INK, width=8)
            d.rectangle([300, 560, 780, 660], fill=RED)
            txt(Lr, (540, 610), "DÍA", 44, WHITE)
            txt(Lr, (540, 860), f"{pages}", 180, INK)
        solid(img, cal)
        if u > 1.4:
            k = ease(clamp((u - 1.4) / 0.4))
            solid(img, lambda Lr: urn(Lr, 860, 1180, 0.6 * pop(k) + 0.01))
            FL.stamp(img, 600, 1170, "OTRA VEZ A VOTAR", clamp((u - 1.6) / 0.3))
        ojo(img, 150, 1440, 0.66, "think", t=t)


def sh_compare(img, t, T, L):
    """Pantalla partida: España (papeleta → diputados → presidente) contra Francia (papeleta → presidente)."""
    d = K.D(img)
    d.line([(540, 420), (540, 1300)], fill=SOFT, width=4)
    txt(img, (270, 460), "ESPAÑA", 50, INK)
    txt(img, (810, 460), "FRANCIA", 50, INK)
    k1 = ease(clamp((t - 0.2) / 0.8))

    def left(Lr):
        ballot(Lr, 270, 620, 0.3)
        hemicycle(Lr, 270, 940, 150 * pop(k1) + 1, n=120, dot=4)
        if t > 1.0:
            person(Lr, 270, 1250, 1.2, col=GOLD)
    solid(img, left)
    k2 = ease(clamp((t - lt(L, 0, 0.35)) / 0.6))

    def right(Lr):
        ballot(Lr, 810, 620, 0.3)
        K.D(Lr).line([(810, 720), (810, 720 + 380 * k2)], fill=RED, width=12)
        if k2 > 0.95:
            person(Lr, 810, 1250, 1.2, col=GOLD)
    solid(img, right)
    if k2 > 0.95:
        FL.pill(img, 810, 1330, "DIRECTO", 1.0, col=RED)


def _i_ballot(Lr, x, y, s):
    ballot(Lr, x, y, 0.42 * s)


def _i_hemi(Lr, x, y, s):
    hemicycle(Lr, x, y + 50 * s, 105 * s + 1, n=120, dot=3)


def _i_pres(Lr, x, y, s):
    crown(Lr, x, y - 60 * s, 0.6 * s)
    person(Lr, x, y + 90 * s, 1.1 * s, col=GOLD)


def sh_answer(img, t, T, L):
    """Respuesta en 3 pasos: TU PAPELETA → 350 DIPUTADOS → ELIGEN AL PRESIDENTE."""
    ks = [clamp((t - 0.25) / 0.35), clamp((t - lt(L, 0, 0.45)) / 0.35), clamp((t - lt(L, 0, 0.72)) / 0.35)]
    pro.chain(img, t, [("TU VOTO", RED), ("350 DIPUTADOS", BLUE), ("PRESIDENTE", INK)], ks, drawers=[_i_ballot, _i_hemi, _i_pres])
    ojo(img, 540, 1450, 0.62, "smirk", t=t)
    hook_text(img, [("¿VOTAS AL PRESIDENTE?", False), ("VOTAS DIPUTADOS", True)], clamp((t - lt(L, 0, 0.15)) / 0.4), y=440, size=76)


import fondos
NARR = None
pro.setup(globals(), OJO_TRAJE, fondos.congreso(), NAMES)

OUTRO_MIN = 5.5
MUSIC_GAIN = 1.7
MUSIC_DUCK = 0.45
AUDIO = {
    "music": [("q", "playful")],
    "gains": {},
    "amb": {},
    "sfx": [("q+1.3", "pop", 0.06), ("ballot+0.3", "whoosh", 0.05), ("congress+0.3", "whoosh_up", 0.06), ("prov+0.3", "pop", 0.05),
            ("king+0.4", "ding", 0.05), ("debate+0.3", "whoosh", 0.05), ("vote1+0.05", "pop", 0.07), ("vote2+0.3", "tick", 0.05),
            ("deals+0.3", "click", 0.06), ("compare+0.3", "whoosh", 0.05), ("answer+0.5", "ding", 0.06)],
    "bpm": 100,
}
