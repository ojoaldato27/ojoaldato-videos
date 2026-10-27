"""06 · Un agujero que atraviesa la Tierra — estilo 7 «minimal blanco» con el formato nuevo (pregunta de gancho respondida
al final, Ojo de narrador físico, marcador rojo, cierre «Ojo al dato»). Elegido por Iker el 21/10 («Agujero por la Tierra»).
Datos: Wikipedia «Gravity train» (42,2 min con densidad uniforme; unos 38 min con la densidad real, modelo PREM);
velocidad en el centro ≈ √(g·R) ≈ 7,9 km/s ≈ 28.400 km/h con densidad uniforme (más con la real); núcleo a unos
5.000-6.000 °C; pozo superprofundo de Kola: 12,26 km (1989); antípodas de España en Nueva Zelanda."""
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
TITLE = "06_Agujero_Tierra_estilo7"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "c06_agujero")
VOICE = _VZ + ".mp3"
LINES = [
    "¿Qué pasaría si saltaras a un *agujero* que atraviesa la Tierra?",
    "Imagina un túnel recto desde España… hasta el otro lado del planeta.",
    "Saldrías en *Nueva Zelanda*.",
    "Al saltar, caes cada vez más rápido…",
    "Y en el centro irías a más de *28.000 km/h*.",
    "Pero ahí, la gravedad tira igual hacia todos lados: en el centro *no pesas nada*.",
    "Luego empiezas a frenar… y llegas justo a la superficie del otro lado.",
    "¿Cuánto tardas? Unos *38 minutos*.",
    "Y si no te agarras… vuelves a caer, y vas y vienes *para siempre*.",
    "Bueno… eso sin aire. Con aire, rozas, frenas… y te quedas parado *en el centro*.",
    "Donde hace unos *5.000 grados*, casi como en la superficie del Sol.",
    "Y el agujero más profundo que hemos hecho, el de Kola, en Rusia, solo llega a *12 kilómetros*.",
    "Ni el *0,2 %* del camino hasta el centro.",
    "Así que… ¿qué pasaría? Que en 38 minutos cruzarías el planeta… o acabarías *flotando en su centro*.",
]
OUTRO_LINE = "Mejor quédate en la superficie… ¡Ojo al dato!"
NAMES = ["q", "tunnel", "nz", "fall", "speed", "zero", "brake", "time", "yoyo", "air", "hot", "kola", "pct", "answer"]
SHOTS = [(n, i, i, 0) for i, n in enumerate(NAMES)]
FOCUS = {}
HYPE = None
FOLLOW = None
NOTIF = ("time", 0.8)
HEAD = {
    0: ("¿Un agujero?", "QUE ATRAVIESA LA TIERRA"),
    1: ("Desde España", "UN TÚNEL RECTO HASTA EL OTRO LADO"),
    2: ("Nueva Zelanda", "LAS ANTÍPODAS DE ESPAÑA"),
    3: ("Caída libre", "CADA VEZ MÁS RÁPIDO"),
    4: ("28.000 km/h", "AL PASAR POR EL CENTRO"),
    5: ("0 kilos", "EN EL CENTRO NO PESAS NADA"),
    6: ("Frenada", "HASTA LA SUPERFICIE DEL OTRO LADO"),
    7: ("38 minutos", "LO QUE TARDAS EN CRUZAR"),
    8: ("Para siempre", "VAS Y VIENES"),
    9: ("Con aire", "TE QUEDAS EN EL CENTRO"),
    10: ("5.000 °C", "CASI COMO LA SUPERFICIE DEL SOL"),
    11: ("12 km", "EL POZO DE KOLA, RUSIA"),
    12: ("0,2 %", "DEL CAMINO HASTA EL CENTRO"),
    13: ("La respuesta", "38 MINUTOS… O FLOTAR EN EL CENTRO"),
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
TRANS_SEED = 37
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
FL.TH["narr"] = True
OJO_TRAJE = "c_fisico"
OJO_POSES = {"q": "think", "tunnel": "point", "nz": "smirk", "fall": "surprise", "speed": "surprise", "zero": "think",
             "brake": "point", "time": "point", "yoyo": "smirk", "air": "think", "hot": "surprise", "kola": "point",
             "pct": "smirk", "answer": "think"}
NARR = FL.NARR
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
IDX = {n: i for i, n in enumerate(NAMES)}
CX, CY, R = 540, 960, 500          # la Tierra cortada (más grande: Iker, 21/10 «se ve muy pequeño»)


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def _h(img, name, t):
    FL.head(img, t, IDX[name])


def _earth(img, hole=1.0, glow=0.0):
    K.earth_cut(img, CX, CY, R, glow)
    if hole > 0:
        d = K.D(img)
        y1 = CY - R + 2 * R * ease(clamp(hole))
        d.rectangle([CX - 16, CY - R - 10, CX + 16, y1], fill=(70, 70, 78))


def _pos(u):
    """u = 0 arriba (España), 0.5 centro, 1 abajo (Nueva Zelanda)."""
    return CX, CY - R + 2 * R * u


# ------------------------------------------------------------------ Ojo actor (21/10: «que la mascota excave y caiga al vacío»)
import ojo as OJ
from PIL import Image, ImageDraw
LAYERS = [(0.0, (150, 110, 80)), (0.06, (236, 140, 70)), (0.55, (246, 190, 70)), (0.81, (255, 236, 130))]   # corteza…núcleo


def ojo_c(img, cx, cy, sc, pose="surprise", ang=0.0, lid=0.0, tint=0.0):
    f = OJ.figure(pose, OJO_TRAJE, lid, (0.05, 0.0), 0.0)
    if tint > 0:
        r, g, b, a = f.split()
        r = r.point(lambda v: int(v + (255 - v) * 0.5 * tint))
        f = Image.merge("RGBA", (r, g, b, a))
    ff = f.resize((max(1, int(f.width * sc)), max(1, int(f.height * sc))), Image.BILINEAR)
    if abs(ang) > 0.01:
        ff = ff.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    img.paste(ff, (int(cx - ff.width / 2), int(cy - ff.height / 2)), ff)


def ojo_feet(img, x, y, sc, pose="point", ang=0.0):
    f = OJ.figure(pose, OJO_TRAJE, 0.0, (0.05, 0.0), 0.0)
    ojo_c(img, x, y - f.height * sc * 0.45, sc, pose, ang)


def layer_col(depth):
    """depth 0 = superficie, 1 = centro."""
    col = LAYERS[0][1]
    for d0, c in LAYERS:
        if depth >= d0:
            col = c
    return col


def tunnel_bg(img, depth, scroll, glow=0.0):
    """Primer plano del túnel: paredes del color de la capa y estratos que pasan hacia arriba."""
    d = K.D(img)
    col = layer_col(depth)
    if glow > 0:
        col = tuple(int(lerp(c, t, glow)) for c, t in zip(col, (255, 110, 50)))
    d.rectangle([0, 380, W, 1150], fill=col)
    for k in range(12):
        y = 380 + ((k * 110 - scroll) % 880)
        d.line([(0, y), (W, y + 30)], fill=tuple(max(0, c - 28) for c in col), width=6)
        d.ellipse([90 + (k * 137) % 200, y + 30, 130 + (k * 137) % 200, y + 56], fill=tuple(max(0, c - 40) for c in col))
        d.ellipse([820 + (k * 91) % 160, y + 50, 850 + (k * 91) % 160, y + 70], fill=tuple(max(0, c - 40) for c in col))
    d.rectangle([380, 380, 700, 1150], fill=(58, 58, 66))
    d.line([(380, 380), (380, 1150)], fill=INK, width=8)
    d.line([(700, 380), (700, 1150)], fill=INK, width=8)
    _clip(img)


def _clip(img, y1=1151):
    """Recorta lo que se sale de la franja de la escena (cabecera arriba y subtítulos abajo)."""
    d = K.D(img)
    d.rectangle([0, 0, W, 379], fill=BG)
    d.rectangle([0, y1, W, H], fill=BG)


def depth_meter(img, km):
    d = K.D(img)
    d.rounded_rectangle([760, 400, 1050, 480], radius=20, fill=(255, 255, 255), outline=INK, width=5)
    txt(img, (905, 440), f"{int(km):,} km".replace(",", "."), 44, INK)


def _earth(img, hole=1.0, glow=0.0, cx=CX, cy=CY, r=R):
    K.earth_cut(img, cx, cy, r, glow)
    if hole > 0:
        d = K.D(img)
        y1 = cy - r + 2 * r * ease(clamp(hole))
        d.rectangle([cx - r * 0.05, cy - r - 10, cx + r * 0.05, y1], fill=(70, 70, 78))


def _pos(u, cx=CX, cy=CY, r=R):
    return cx, cy - r + 2 * r * u


# ------------------------------------------------------------------ planos
def sh_q(img, t, T, L):
    """Ojo cava con su pala en la superficie; la cámara se acerca."""
    d = K.D(img)
    gy = 900
    d.rectangle([0, gy, W, 1150], fill=(150, 110, 80))
    d.rectangle([0, gy, W, gy + 40], fill=(110, 190, 110))
    d.line([(0, gy), (W, gy)], fill=INK, width=6)
    hole = 60 + 140 * ease(clamp(t / 2.6))
    d.ellipse([560 - hole / 2, gy - 14, 560 + hole / 2, gy + 26], fill=(40, 40, 46))
    dig = math.sin(t * 9)
    ojo_feet(img, 400, gy, 0.75, "point", ang=0.12 * dig)
    # pala
    hx, hy = 470, gy - 245 + 20 * dig
    bx, by_ = 560, gy - 10 + 16 * dig
    d.line([(hx, hy), (bx, by_)], fill=(150, 96, 50), width=14)
    d.polygon([(bx - 30, by_ - 10), (bx + 30, by_ - 10), (bx + 20, by_ + 50), (bx - 20, by_ + 50)], fill=(170, 170, 180), outline=INK)
    for k in range(7):
        ph = (t * 1.6 + k / 7) % 1.0
        x = 600 + 260 * ph
        y = gy - 40 - 300 * ph + 380 * ph * ph
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(120, 84, 60))
    FL.big(img, 900, 560, "?", 170, RED, clamp((t - 1.4) / 0.3))
    _h(img, "q", t)


def sh_tunnel(img, t, T, L):
    """Zoom out desde la pala hasta ver el planeta entero con el túnel recto."""
    z = ease(clamp(t / 1.6))
    r = lerp(1900, R, z)
    cy = lerp(900 + 1900, CY, z)
    _earth(img, hole=0, cx=CX, cy=cy, r=r)
    d = K.D(img)
    k = ease(clamp((t - 1.4) / 2.2))
    top = cy - r
    d.line([(CX, top - 30), (CX, top - 30 + (2 * r + 60) * k)], fill=RED, width=8)
    d.ellipse([CX - 18, top - 18, CX + 18, top + 18], fill=RED)
    ojo_feet(img, CX - 60, top, lerp(0.75, 0.26, z), "point")
    if z > 0.9:
        txt(img, (CX + 170, top + 10), "España", 46, INK)
    _h(img, "tunnel", t)


def sh_nz(img, t, T, L):
    _earth(img, r=R * (1 + 0.05 * t))
    d = K.D(img)
    d.ellipse([CX - 18, CY - R - 18, CX + 18, CY - R + 18], fill=RED)
    d.ellipse([CX - 18, CY + R - 18, CX + 18, CY + R + 18], fill=RED)
    ojo_feet(img, CX - 60, CY - R, 0.26, "surprise", ang=-0.3 * ease(clamp(t / 0.8)))
    FL.pill(img, CX + 300, CY + R - 30, "NUEVA ZELANDA", clamp((t - 0.2) / 0.3), col=RED)
    _h(img, "nz", t)


def sh_fall(img, t, T, L):
    """Primer plano: Ojo cae de cabeza por el túnel; las capas pasan hacia arriba cada vez más rápido."""
    q = clamp(t / max(0.6, T))
    depth = 0.45 * q * q
    tunnel_bg(img, depth, scroll=900 * t * t)
    FL.speed_lines(img, 470, 380, 610, 700, clamp(t / 0.4), n=5)
    ojo_c(img, 540, 860 + 20 * math.sin(t * 6), 0.85, "surprise", ang=math.pi * ease(clamp(t / 0.9)) + 0.15 * math.sin(t * 5))
    depth_meter(img, 6371 * depth)
    _h(img, "fall", t)


def sh_speed(img, t, T, L):
    q = clamp(t / max(0.6, T))
    depth = 0.45 + 0.55 * q
    sh = 10 * math.sin(t * 50)
    tunnel_bg(img, depth, scroll=2600 * t + 1000)
    FL.speed_lines(img, 450, 380, 630, 760, 1.0, n=8, seed=int(t * 20) % 5)
    ojo_c(img, 540 + sh, 860, 0.85, "surprise", ang=math.pi + 0.1 * math.sin(t * 9))
    depth_meter(img, 6371 * depth)
    FL.big(img, 650, 1250, "28.000 km/h", 110, RED, clamp((t - lt(L, 0, 0.5)) / 0.3))
    _h(img, "speed", t)


def sh_zero(img, t, T, L):
    """En el centro: Ojo flota y gira, la gravedad tira igual desde todos lados."""
    d = K.D(img)
    d.rectangle([0, 380, W, 1150], fill=(255, 236, 130))
    for rr in (700, 560, 420):
        d.ellipse([540 - rr, 770 - rr, 540 + rr, 770 + rr], outline=(240, 200, 90), width=6)
    for a in range(8):
        ang = a * math.pi / 4 + 0.2
        r0, r1 = 300, 300 - 90 * ease(clamp((t - 0.4) / 0.6))
        x0, y0 = 540 + math.cos(ang) * r0, 770 + math.sin(ang) * r0
        x1, y1 = 540 + math.cos(ang) * (r1 + 160), 770 + math.sin(ang) * (r1 + 160)
        d.line([(x0, y0), (x1, y1)], fill=RED, width=10)
    _clip(img)
    ojo_c(img, 540, 770 + 14 * math.sin(t * 2.2), 0.85, "think", ang=t * 0.9)
    FL.big(img, 650, 1250, "0 kg", 120, RED, clamp((t - lt(L, 0, 0.7)) / 0.3))
    _h(img, "zero", t)


def sh_brake(img, t, T, L):
    """Sigue hacia el otro lado frenando: capas al revés, cada vez más despacio, y asoma en Nueva Zelanda."""
    q = clamp(t / max(0.6, T - 0.9))
    if t < T - 0.9:
        depth = 1 - q
        tunnel_bg(img, depth, scroll=1800 * (1 - (1 - q) ** 2))
        ojo_c(img, 540, 860, 0.85, "point", ang=-0.3 + 0.1 * math.sin(t * 3))
        depth_meter(img, 6371 * depth)
    else:
        d = K.D(img)
        gy = 900
        d.rectangle([0, gy, W, 1150], fill=(150, 110, 80))
        d.rectangle([0, gy, W, gy + 40], fill=(110, 190, 110))
        d.ellipse([440, gy - 14, 640, gy + 26], fill=(40, 40, 46))
        u = ease(clamp((t - (T - 0.9)) / 0.5))
        ojo_feet(img, 540, gy + 200 - 200 * u, 0.75, "wave")
        d.rectangle([0, gy + 26, W, 1150], fill=(150, 110, 80))
        d.line([(0, gy), (440, gy)], fill=INK, width=6)
        d.line([(640, gy), (W, gy)], fill=INK, width=6)
        FL.pill(img, 760, 520, "NUEVA ZELANDA", u, col=RED)
    _h(img, "brake", t)


def sh_time(img, t, T, L):
    ojo_feet(img, 300, 1100, 0.7, "point")
    frac = clamp(t / 2.0)
    FL.stopwatch(img, 720, 720, 200, frac * 0.63, f"{int(38 * frac)} min")
    FL.big(img, 650, 1250, "38 min", 120, RED, clamp((t - lt(L, 0, 0.55)) / 0.3))
    _h(img, "time", t)


def sh_yoyo(img, t, T, L):
    """Vista entera: Ojo va y viene por el túnel, con estela."""
    _earth(img)
    for k in range(4, -1, -1):
        tt_ = t - k * 0.05
        u = 0.5 - 0.5 * math.cos(tt_ * 2.6)
        x, y = _pos(u)
        if k:
            K.D(img).ellipse([x - 16, y - 16, x + 16, y + 16], fill=(230, 40, 40, 60 - k * 10))
    u = 0.5 - 0.5 * math.cos(t * 2.6)
    x, y = _pos(u)
    ojo_c(img, x, y, 0.32, "surprise", ang=math.pi * (u > 0.5))
    FL.big(img, 960, 470, "∞", 150, RED, clamp((t - lt(L, 0, 0.6)) / 0.3), fo=F(FL.DJ, 150))
    _h(img, "yoyo", t)


def sh_air(img, t, T, L):
    zf = 1 + 1.3 * ease(clamp((t - 1.2) / 2.6))           # zoom al centro de la Tierra
    r = R * zf
    _earth(img, r=r)
    _clip(img, 1462)
    A = 0.5 * math.exp(-0.7 * t)
    u = 0.5 - A * math.cos(t * 3)
    x, y = _pos(u, r=r)
    d = K.D(img)
    for k in range(5):
        yy = y - 50 + k * 25
        d.line([(x + 45 * zf, yy), (x + 110 * zf, yy)], fill=(150, 190, 230), width=5)
    ojo_c(img, x, y, 0.32 * zf, "think", ang=0.2 * math.sin(t * 4))
    _h(img, "air", t)


def sh_hot(img, t, T, L):
    """Primer plano en el centro: todo al rojo y Ojo sudando."""
    g = ease(clamp(t / 1.0))
    d = K.D(img)
    col = tuple(int(lerp(c, h, g)) for c, h in zip((255, 236, 130), (255, 110, 50)))
    d.rectangle([0, 380, W, 1150], fill=col)
    for k in range(6):
        x = 120 + k * 170
        pts = [(x + 14 * math.sin(yy / 30 + t * 6 + k), yy) for yy in range(420, 1120, 20)]
        d.line(pts, fill=(255, 170, 90), width=5)
    ojo_c(img, 540, 780, 0.85, "surprise", tint=g)
    for k in range(3):
        ph = (t * 1.2 + k / 3) % 1
        d.ellipse([600 + k * 30, 640 + 140 * ph, 616 + k * 30, 664 + 140 * ph], fill=(120, 180, 255))
    FL.big(img, 650, 1250, "5.000 °C", 120, RED, clamp((t - 0.3) / 0.3))
    k = clamp((t - lt(L, 0, 0.55)) / 0.3)
    if k > 0:
        r = 70 * pop(k)
        d.ellipse([960 - r, 470 - r, 960 + r, 470 + r], fill=(255, 220, 60), outline=INK, width=5)
    _h(img, "hot", t)


def sh_kola(img, t, T, L):
    """La cámara baja por la corteza: el pozo de Kola se queda en nada."""
    d = K.D(img)
    pan = 520 * ease(clamp((t - 1.6) / 2.0))
    gy = 600 - pan
    d.rectangle([0, max(380, gy), W, 1150], fill=(150, 110, 80))
    if gy > 380:
        d.rectangle([0, gy - 40, W, gy], fill=(110, 190, 110))
        d.line([(0, gy - 40), (W, gy - 40)], fill=INK, width=6)
        # torre de perforación
        d.polygon([(500, gy - 40), (580, gy - 40), (550, gy - 260), (530, gy - 260)], outline=INK, width=6)
        for k in range(4):
            yy = gy - 40 - k * 55
            d.line([(505 + k * 7, yy), (575 - k * 7, yy - 55)], fill=INK, width=4)
        ojo_feet(img, 360, gy - 40, 0.5, "point")
    k = ease(clamp((t - 0.6) / 1.0))
    d.rectangle([536, gy, 544, gy + 60 * k], fill=INK)
    FL.big(img, 760, max(560, gy + 60), "12 km", 100, (255, 255, 255), clamp((t - lt(L, 0, 0.55)) / 0.3))
    if pan > 200:
        d.line([(540, 900), (540, 1110)], fill=(255, 255, 255), width=8)
        d.polygon([(515, 1100), (565, 1100), (540, 1140)], fill=(255, 255, 255))
        txt(img, (760, 1060), "6.371 km hasta el centro", 42, (255, 255, 255))
    _h(img, "kola", t)


def sh_pct(img, t, T, L):
    d = K.D(img)
    y = 860
    d.rounded_rectangle([140, y - 40, 940, y + 40], radius=40, fill=K.PALE, outline=INK, width=6)
    d.rounded_rectangle([140, y - 40, 162, y + 40], radius=20, fill=RED)
    ojo_feet(img, 175, y - 40, 0.42, "think")
    FL.big(img, 600, 560, "0,2 %", 170, RED, clamp((t - 0.2) / 0.3))
    txt(img, (940, y + 90), "Centro", 40, INK, "rm")
    FL.dotted_arc(img, 560, y + 600, 640, -math.pi * 0.86, -math.pi * (0.86 - 0.72 * ease(clamp((t - 0.6) / 1.4))), 1.0, col=SOFT)
    _h(img, "pct", t)


def sh_answer(img, t, T, L):
    """Pantalla partida: cruzar en 38 minutos… o quedarse flotando en el centro."""
    _earth(img, cx=285, cy=820, r=250)
    u = 0.5 - 0.5 * math.cos(t * 1.6)
    x, y = _pos(u, 285, 820, 250)
    ojo_c(img, x, y, 0.17, "surprise")
    _earth(img, cx=800, cy=820, r=250, glow=0.6)
    ojo_c(img, 800, 820 + 6 * math.sin(t * 3), 0.17, "think", ang=t)
    FL.pill(img, 285, 1120, "38 MINUTOS", clamp((t - lt(L, 0, 0.35)) / 0.3))
    FL.pill(img, 800, 1120, "FLOTAR EN EL CENTRO", clamp((t - lt(L, 0, 0.75)) / 0.3), col=RED)
    _h(img, "answer", t)


# Ojo actúa dentro de la escena: el narrador de la esquina se esconde en este vídeo
NARR = None
TRANS_PLAN = ["zoom_out", "spin", "fall", "fall", "flash", "fall", "whip", "zoom_in", "glitch", "flash", "zoom_out", "whip_r", "iris"]
FNS = {n: globals()["sh_" + n] for n in NAMES}
FOCUS_PT = {n: (540, 800) for n in NAMES}

OUTRO_MIN = 6.6           # el vídeo tiene que durar entre 1:00 y 1:30 (Iker, 21/10)
MUSIC_GAIN = 1.7          # música épica más presente (Iker, 21/10)
MUSIC_DUCK = 0.45
AUDIO = {
    "music": [("q", "epic")],
    "gains": {},
    "amb": {"wind": ["fall", "speed", "brake", "yoyo", "air"], "fire": ["hot"]},
    "sfx": [("q+0.3", "swell", 0.08), ("tunnel+0.2", "whoosh", 0.07), ("nz+0.2", "pop", 0.06), ("fall+0.2", "whoosh_up", 0.08),
            ("speed+0.4", "boom", 0.25), ("zero+0.5", "swell", 0.06), ("brake+0.3", "whoosh", 0.07), ("time+0.4", "tick", 0.06),
            ("yoyo+0.3", "whoosh", 0.07), ("air+0.3", "whoosh", 0.06), ("hot+0.3", "rumble", 0.25), ("kola+0.4", "click", 0.1),
            ("pct+0.3", "pop", 0.06), ("answer+0.4", "ding", 0.06)],
    "bpm": 96,
}
