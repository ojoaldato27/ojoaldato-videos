"""02 · ¿Qué cambia de ir a 100 o a 140? — estilo 7 «minimal blanco» con el formato nuevo (21/10): Ojo de narrador
(científico físico), palabras clave con marcador rojo, banner de seguir de «Ojo al dato» y cierre con Ojo.
Mismo guion y voz que t01_velocidad_v2."""
import math
from PIL import Image, ImageDraw
from t01_velocidad_v2 import *          # noqa: F401,F403  (guion, voz, planos, titulares)
import t01_velocidad_v2 as BASE
import flat3 as FL
import vid2
FL.use("minimal", BASE.HEAD)
from flat3 import TH, W, H, F, lt, pop, car
from render import ease, clamp, lerp

TITLE = "02_Velocidad_estilo7"
FRAME = vid2.frame
FPS = 60
BG = (248, 248, 246)
TRANS_POOL = ["push", "whip", "zoom_in", "iris", "whip_r", "spin"]
TRANS_SEED = 9
CAM_PUSH = 0.04
SHAKE = 8
CUT_SFX = True
FL.TH["narr"] = True
OJO_TRAJE = "c_fisico"
NARR = FL.NARR
CAPTION = FL.CAPTION
OUTRO_FN = FL.make_outro(OJO_TRAJE)
HANDLE = FL.BRAND["handle"]
NOTIF_ICON = FL.brand_icon()
NOTIF_TEXT = "Sígueme para un dato nuevo cada día"
OUTRO_LINE = BASE.OUTRO_LINE
INK, RED, SOFT = (28, 28, 32), (230, 40, 40), (160, 160, 168)
FIRST = {nm: a for nm, a, b, _ in BASE.SHOTS}


def _li(name, t, L):
    """Índice de la frase que suena en el plano (para el titular de cada frase)."""
    j = 0
    for k, (a, b) in enumerate(L):
        if t >= a - 0.15:
            j = k
    return FIRST[name] + j


def _head(img, name, t, L, hide=None):
    j = _li(name, t, L)
    a = L[j - FIRST[name]][0]
    FL.head(img, max(0.0, t - max(0.0, a - 0.15)) if j != FIRST[name] else t, j, hide)


def _road(img, y, x0=0, x1=W, dash_off=0.0):
    d = ImageDraw.Draw(img)
    d.line([(x0, y), (x1, y)], fill=INK, width=5)
    for k in range(-1, 14):
        x = (k * 120 - dash_off) % (W + 120) - 60
        d.line([(x, y + 60), (x + 60, y + 60)], fill=SOFT, width=5)
    d.line([(x0, y + 120), (x1, y + 120)], fill=INK, width=5)


def _txt(img, xy, s, size, col=INK, anchor="mm", font=None):
    ImageDraw.Draw(img).text(xy, s, font=F(font or FL.INTER_X, size), fill=col, anchor=anchor)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    for k, (y, v, lab) in enumerate(((620, 100, "100"), (900, 140, "140"))):
        _road(img, y + 90, dash_off=t * v * 4)
        u = clamp(t / 4.5)
        x = 300 + (v - 100) * 6 * u
        car(img, x, y + 150, 46, 0, 1, spin=-t * v / 12)
        FL.big(img, 150, y + 20, lab, 100, RED if v == 140 else INK, clamp((t - 0.3 - k * 0.4) / 0.35))
        _txt(img, (150, y + 80), "km/h", 32, SOFT)
    k2 = clamp((t - lt(L, 1, 0.3)) / 0.35)
    if k2 > 0:
        FL.clock(img, 860, 470, 95 * pop(k2), t * 2)
        FL.big(img, 860, 470, "?", 110, RED, k2)
    _head(img, "open", t, L)


def sh_meters(img, t, T, L):
    d = ImageDraw.Draw(img)
    X0, SC = 140, 20.0                                         # 20 px por metro
    for k, (yy, m, lab, col, fr) in enumerate(((700, 28, "28 m", INK, 0.35), (1000, 39, "39 m", RED, 1.15))):
        a = lt(L, k, 0.0)
        q = ease(clamp((t - a - 0.2) / 1.0))
        if t < a - 0.1:
            continue
        d.line([(X0, yy), (X0 + m * SC, yy)], fill=(225, 225, 228), width=26)
        d.line([(X0, yy), (X0 + m * SC * q, yy)], fill=col, width=26)
        for mm in range(0, m + 1, 5):
            d.line([(X0 + mm * SC, yy + 22), (X0 + mm * SC, yy + 40)], fill=SOFT, width=3)
        car(img, X0 + m * SC * q, yy - 14, 24, 0, 1)
        FL.big(img, X0 + m * SC * q, yy - 130, lab, 90, col, clamp((t - a - 0.6) / 0.35))
    _txt(img, (540, 1160), "en 1 segundo", 46, SOFT)
    _head(img, "meters", t, L)


def sh_react(img, t, T, L):
    _road(img, 900, dash_off=t * 160)
    x = 260
    car(img, x, 960, 50, 0, 1, spin=-t * 12)
    k1 = clamp((t - lt(L, 0, 0.55)) / 0.25)
    if k1 > 0:
        d = ImageDraw.Draw(img)
        s = pop(k1)
        cx, cy = 880, 900
        d.polygon([(cx, cy - 120 * s), (cx + 110 * s, cy + 70 * s), (cx - 110 * s, cy + 70 * s)], fill=RED)
        _txt(img, (cx, cy + 10), "!", int(120 * s) + 1, (255, 255, 255))
    a = lt(L, 1, 0.0)
    run = clamp((t - a - 0.2) / 1.0)
    if t > a:
        FL.stopwatch(img, 540, 560, 150, run, f"{run:.1f} s".replace(".", ","))
        d = ImageDraw.Draw(img)
        q = ease(clamp((t - a - 0.2) / 1.2))
        d.line([(x + 150, 1080), (x + 150 + 430 * q, 1080)], fill=RED, width=12)
        d.polygon([(x + 150 + 430 * q, 1060), (x + 150 + 430 * q + 30, 1080), (x + 150 + 430 * q, 1100)], fill=RED)
        FL.pill(img, 640, 1170, "SIN FRENAR TODAVÍA", ease(clamp((t - a - 1.4) / 0.3)), col=RED)
    _head(img, "react", t, L)


def sh_rule(img, t, T, L):
    rows = [(1, "100", "10 × 10", "100 m", INK), (2, "140", "14 × 14", "196 m", RED)]
    k0 = clamp((t - 0.3) / 0.4)
    if t < lt(L, 1, 0.0) - 0.1:
        if k0 > 0:
            d = ImageDraw.Draw(img)
            fo = F(FL.INTER_X, 130)
            w14 = d.textlength("14", font=fo)
            w0 = d.textlength("0", font=fo)
            x0 = 230
            d.text((x0, 640), "14", font=fo, fill=INK, anchor="lm")
            d.text((x0 + w14, 640), "0", font=fo, fill=SOFT, anchor="lm")
            if t > 1.0:
                d.line([(x0 + w14 - 6, 700), (x0 + w14 + w0 + 6, 580)], fill=RED, width=12)
            d.text((x0 + w14 + w0 + 50, 640), "→", font=F(FL.DJ, 110), fill=INK, anchor="lm")
            d.text((x0 + w14 + w0 + 190, 640), "14", font=fo, fill=RED, anchor="lm")
        FL.pill(img, 540, 860, "QUITA LA ÚLTIMA CIFRA Y ELÉVALA AL CUADRADO", ease(clamp((t - 1.4) / 0.4)))
    else:
        for k, (li, v, op, res, col) in enumerate(rows):
            a = lt(L, li, 0.0)
            if t < a - 0.1:
                continue
            q = clamp((t - a) / 0.35)
            y = 560 + k * 330
            _txt(img, (150, y), v, 90, SOFT, "lm")
            FL.big(img, 520, y, op, 96, INK, q)
            FL.big(img, 860, y, res, 96, col, clamp((t - a - 0.9) / 0.35))
            d = ImageDraw.Draw(img)
            bw = 900 * (100 if k == 0 else 196) / 196 * ease(clamp((t - a - 1.1) / 0.8))
            d.rounded_rectangle([90, y + 90, 90 + bw, y + 130], radius=20, fill=col)
    _head(img, "rule", t, L)


def sh_energy(img, t, T, L):
    d = ImageDraw.Draw(img)
    a1, a2 = lt(L, 1, 0.0), lt(L, 2, 0.0)
    if t < a1 - 0.1:
        for k, (v, lab, col) in enumerate(((100, "100", INK), (140, "140", RED))):
            q = ease(clamp((t - 0.2 - k * 0.5) / 0.6))
            y = 640 + k * 260
            d.rounded_rectangle([140, y, 140 + 5.4 * v * q, y + 90], radius=20, fill=col)
            _txt(img, (120, y + 45), lab, 60, col, "rm")
        FL.big(img, 860, 1220, "+40 %", 120, RED, clamp((t - 1.6) / 0.35))
    else:
        ox, oy, sw, shh = 160, 1180, 780, 560
        d.line([(ox, oy), (ox + sw, oy)], fill=INK, width=5)
        d.line([(ox, oy), (ox, oy - shh)], fill=INK, width=5)
        q = ease(clamp((t - a1) / 1.4))
        pts = [(ox + sw * u, oy - shh * u * u) for u in [i / 60 * q for i in range(61)]]
        if len(pts) > 1:
            d.line(pts, fill=RED, width=10, joint="curve")
        _txt(img, (ox + sw, oy + 40), "velocidad", 32, SOFT, "rm")
        _txt(img, (ox - 20, oy - shh), "energía", 32, SOFT, "rm")
        for (u, lab) in ((100 / 140, "100"), (1.0, "140")):
            if q >= u:
                x, y = ox + sw * u, oy - shh * u * u
                d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=INK if lab == "100" else RED)
                _txt(img, (x, oy + 40), lab, 40, INK)
        if t > a2:
            FL.big(img, 420, 560, "× 2", 200, RED, clamp((t - a2 - 0.2) / 0.35))
    _head(img, "energy", t, L)


def sh_fall(img, t, T, L):
    d = ImageDraw.Draw(img)
    bx, by, fh = 620, 1440, 38                                 # edificio de 26 pisos
    for k in range(26):
        y = by - (k + 1) * fh
        col = (235, 235, 238) if k % 2 else (226, 226, 230)
        d.rectangle([bx, y, bx + 260, y + fh - 2], fill=col)
        for wx in range(bx + 24, bx + 250, 54):
            d.rectangle([wx, y + 10, wx + 26, y + fh - 12], fill=(200, 205, 214))
    d.rectangle([bx, by - 26 * fh, bx + 260, by], outline=INK, width=5)
    d.line([(60, by), (1040, by)], fill=INK, width=5)
    for k, (fl, col) in enumerate(((13, INK), (26, RED))):
        a = lt(L, k, 0.0)
        if t < a:
            continue
        y = by - fl * fh
        q = ease(clamp((t - a - 0.1) / 0.5))
        d.line([(bx - 40, y), (bx - 40 - 200 * q, y)], fill=col, width=8)
        car(img, bx - 160, y - 4, 22, 0, 1, alpha=int(255 * q))
        FL.big(img, bx - 160, y - 90, f"piso {fl}", 64, col, clamp((t - a - 0.3) / 0.35))
        if q >= 1:
            for yy in range(int(y + 20), by - 10, 36):
                d.line([(bx - 160, yy), (bx - 160, yy + 18)], fill=col, width=5)
    _head(img, "fall", t, L)


def sh_air(img, t, T, L):
    a1 = lt(L, 1, 0.0)
    d = ImageDraw.Draw(img)
    if t < a1 - 0.1:
        g = car(img, 640, 1020, 70, 0, 1)
        n = 3 + int(5 * clamp(t / 2.5))
        for i in range(n):
            y = 760 + i * 40
            x0 = 120 + ((t * 600 + i * 90) % 300)
            d.line([(x0, y), (x0 + 160, y)], fill=(90, 170, 230), width=8)
            d.polygon([(x0 + 160, y - 12), (x0 + 190, y), (x0 + 160, y + 12)], fill=(90, 170, 230))
        FL.pill(img, 640, 1180, "EL AIRE FRENA COMO EL CUADRADO", ease(clamp((t - 1.2) / 0.4)))
    else:
        cx, cy = 600, 760
        d.rounded_rectangle([cx - 150, cy - 200, cx + 90, cy + 260], radius=24, fill=(240, 240, 242), outline=INK, width=8)
        d.rounded_rectangle([cx - 110, cy - 160, cx + 50, cy - 40], radius=10, fill=INK)
        _txt(img, (cx - 30, cy - 100), "120→140", 34, (255, 255, 255))
        d.line([(cx + 90, cy), (cx + 160, cy + 40), (cx + 160, cy + 220)], fill=INK, width=12, joint="curve")
        FL.big(img, cx - 30, cy + 110, "+20-25 %", 76, RED, clamp((t - a1 - 0.6) / 0.35))
    _head(img, "air", t, L)


def sh_fine(img, t, T, L):
    d = ImageDraw.Draw(img)
    s = pop(clamp(t / 0.4))
    cx, cy, r = 380, 720, 190 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=RED, width=max(1, int(36 * s)))
    _txt(img, (cx, cy), "120", max(1, int(130 * s)))
    k = clamp((t - lt(L, 0, 0.62)) / 0.35)
    if k > 0:
        d.rounded_rectangle([600, 860, 980, 1180], radius=20, fill=(255, 255, 255), outline=INK, width=6)
        _txt(img, (790, 920), "MULTA", 44, SOFT)
        FL.big(img, 790, 1050, "100 €", 110, RED, k)
    _head(img, "fine", t, L)


def sh_time(img, t, T, L):
    d = ImageDraw.Draw(img)
    a1 = lt(L, 1, 0.0)
    if t < a1 - 0.1:
        FL.big(img, 540, 760, "¿?", 300, SOFT, clamp(t / 0.3))
        FL.clock(img, 540, 760, 0, 0)
    else:
        ys = (620, 920)
        for k, (y, mins, lab, col) in enumerate(((620, 60, "a 100 · 60 min", INK), (920, 43, "a 140 · 43 min", RED))):
            q = ease(clamp((t - a1 - 0.2 - k * 0.3) / 1.0))
            d.line([(140, y), (940, y)], fill=(225, 225, 228), width=20)
            d.line([(140, y), (140 + 800 * q * mins / 60, y)], fill=col, width=20)
            _txt(img, (140, y - 60), lab, 44, col, "lm")
            car(img, 140 + 800 * q * mins / 60, y - 12, 22, 0, 1)
        _txt(img, (940, 1010), "100 km", 34, SOFT, "rm")
        FL.big(img, 540, 1210, "17 min", 150, RED, clamp((t - a1 - 1.4) / 0.35))
    _head(img, "time", t, L)


def sh_verdict(img, t, T, L):
    d = ImageDraw.Draw(img)
    tilt = 10 * ease(clamp((t - 1.0) / 1.2))
    cx, cy = 560, 780
    d.line([(cx, cy), (cx, cy + 480)], fill=INK, width=12)
    d.polygon([(cx - 120, cy + 480), (cx + 120, cy + 480), (cx, cy + 420)], fill=INK)
    ang = math.radians(tilt)
    lx, ly = cx - 330 * math.cos(ang), cy - 330 * math.sin(ang) * -1
    rx, ry = cx + 330 * math.cos(ang), cy - 330 * math.sin(ang)
    ly = cy + 330 * math.sin(ang)
    d.line([(lx, ly), (rx, ry)], fill=INK, width=10)
    for (x, y, lab, col) in ((lx, ly, "17 min", INK), (rx, ry, "×2 frenada\n×2 golpe", RED)):
        d.line([(x, y), (x - 90, y + 160), (x + 90, y + 160), (x, y)], fill=INK, width=5)
        d.chord([x - 120, y + 110, x + 120, y + 210], 0, 180, fill=(235, 235, 238), outline=INK, width=5)
        for i, ln in enumerate(lab.split("\n")):
            _txt(img, (x, y + 70 - (len(lab.split("\n")) - 1) * 26 + i * 52), ln, 44, col)
    k2 = clamp((t - lt(L, 1, 0.0)) / 0.35)
    if k2 > 0:
        FL.pill(img, 540, 560, "¿MERECE LA PENA?", ease(k2), col=RED)
    _head(img, "verdict", t, L)


FNS = {k: globals()["sh_" + k] for k in ("open", "meters", "react", "rule", "energy", "fall", "air", "fine", "time", "verdict")}
FOCUS_PT = {"open": (540, 800), "meters": (540, 860), "react": (540, 900), "rule": (540, 760), "energy": (540, 900),
            "fall": (700, 1000), "air": (600, 900), "fine": (540, 800), "time": (540, 900), "verdict": (560, 900)}
