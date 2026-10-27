"""N07 · ¿Por qué la inducción calienta la olla y no el cristal?"""
from neon import *

TITLE = "Por_que_la_induccion_no_calienta_el_cristal"
LINES = [
    "La placa de inducción calienta la olla… pero *no el cristal*.",
    "¿Cómo puede ser… y por qué con algunas sartenes *no funciona*?",
    "Debajo del cristal hay una *bobina de cobre*.",
    "Por ella pasa una corriente que cambia de sentido *decenas de miles de veces por segundo*.",
    "Eso crea un *campo magnético* que sube y baja sin parar.",
    "El cristal no reacciona a ese campo… pero el metal de la olla, sí.",
    "El campo crea dentro del metal unas corrientes en remolino.",
    "Y esas corrientes calientan la olla *desde su propio fondo*.",
    "El cristal solo se calienta porque la olla caliente está encima.",
    "Por eso, al quitarla, deja de calentar *al momento*.",
    "¿Y las sartenes que no funcionan?",
    "Necesitan *hierro* en el fondo: el campo solo agarra bien en metales magnéticos.",
    "Truco: si un *imán* se pega al fondo, sirve.",
    "Además, aprovecha alrededor del *75 %* de la energía.",
    "El gas, solo un *40 %*: el resto se escapa calentando la cocina.",
    "En la inducción, *la olla es el fuego*.",
]
SHOTS = [("open", 0, 1, 0.3), ("coil", 2, 3, 0.3), ("field", 4, 5, 0.3), ("eddy", 6, 7, 0.3), ("glass", 8, 9, 0.3),
         ("pans", 10, 12, 0.3), ("eff", 13, 14, 0.3), ("final", 15, 15, 1.8)]
FOCUS = {"open": (540, 1000, 1.12), "coil": (540, 980, 1.12), "field": (540, 980, 1.12), "eddy": (540, 960, 1.15),
         "glass": (540, 1000, 1.12), "pans": (540, 980, 1.12), "eff": (540, 960, 1.12), "final": (540, 1000, 1.12)}
NOTIF = ("field", 1.0)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon

GY = 1180


def hob(d, col=CY, k=1.0):
    rrect(d, 100, GY, 980, GY + 60, 16, col, 6, k)


def pot(d, x=540, y=GY, col=WH, heat=0.0, w=300, h=260):
    c = tuple(int(lerp(a, b, heat)) for a, b in zip(col, OR))
    line(d, [(x - w / 2, y - h), (x - w / 2, y - 8), (x + w / 2, y - 8), (x + w / 2, y - h)], c, 7)
    d.line([(x - w / 2 - 50, y - h + 20), (x - w / 2, y - h + 20)], fill=c, width=8)
    d.line([(x + w / 2, y - h + 20), (x + w / 2 + 50, y - h + 20)], fill=c, width=8)
    if heat > 0.3:
        for j in range(4):
            u = (heat * 3 + j / 4) % 1.0
            xx = x - 90 + j * 60
            pts = [(xx + math.sin(yy / 24 + j) * 12, yy) for yy in range(int(y - h - 40 - u * 120), int(y - h - u * 120), 6)]
            line(d, pts, tuple(int(cc * (1 - u)) for cc in WH), 4)


def spiral(d, cx, cy, r, turns, col, w=6, k=1.0, flat=0.35):
    pts = []
    n = int(turns * 40)
    for i in range(n + 1):
        u = i / n
        a = u * turns * 2 * math.pi
        rr_ = r * (0.12 + 0.88 * u)
        pts.append((cx + math.cos(a) * rr_, cy + math.sin(a) * rr_ * flat))
    line(d, pts, col, w, k)
    return pts


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    hob(d, BL)
    spiral(d, 540, GY + 120, 280, 6, tuple(int(c * 0.6) for c in OR), 4)
    heat = clamp(t / 2.0)
    pot(d, 540, GY, WH, heat)
    finish(img, lay)
    chip(t, 1.0, "CRISTAL: TEMPLADO", 540, GY + 180, BL, 32)
    gtitle2(t, 0.2, "CALIENTA LA OLLA", "PERO NO EL CRISTAL", 250, 60, 84, WH, OR, hold=max(1.6, L[1][0] - 0.2))
    if t > L[1][0]:
        chip(t, L[1][0] + 0.2, "¿Y LAS SARTENES QUE NO VALEN?", 540, 330, MG, 36)
    vignette(img, 150)


def sh_coil(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    pts = spiral(d, 540, 960, 380, 7, OR, 7, ease(clamp(t / 1.4)), 0.8)
    if t > a1:
        sgn = 1 if (t * 2) % 1.0 < 0.5 else -1
        for k in range(24):
            s_ = ((k / 24) + sgn * t * 0.25) % 1.0
            p = partial(pts, s_)[-1]
            dot(d, p[0], p[1], 9, YE)
        arrow(d, (300, 1360), (780, 1360), YE, 6, 1.0) if sgn > 0 else arrow(d, (780, 1360), (300, 1360), YE, 6, 1.0)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "BOBINA DE COBRE", 300, 90, OR)
    else:
        gtitle(t, a1 + 0.2, "25.000-50.000", 290, 96, YE, pop=False)
        chip(t, a1 + 0.8, "CAMBIOS POR SEGUNDO", 540, 450, WH, 34)
    vignette(img, 150)


def sh_field(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    hob(d, BL)
    spiral(d, 540, GY + 120, 280, 6, OR, 4)
    if t > a1:
        pot(d, 540, GY, WH, clamp((t - a1) / 2.0))
    ph = math.sin(t * 6)
    for k in range(5):
        w_ = 100 + k * 70
        hgt = (260 + k * 60) * (0.6 + 0.4 * abs(ph))
        col = tuple(int(c * (0.35 + 0.65 * abs(ph))) for c in GR)
        d.arc([540 - w_, GY + 120 - hgt, 540 + w_, GY + 120 + hgt * 0.2], 180, 360, fill=col, width=4)
    arrow(d, (540, GY + 80), (540, GY - 300 if ph > 0 else GY + 160), GR, 6, 1.0)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "CAMPO MAGNÉTICO", 300, 88, GR)
    else:
        chip(t, a1 + 0.2, "EL CRISTAL NI SE ENTERA", 540, 330, BL, 38)
    vignette(img, 150)


def sh_eddy(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    rect(d, 140, 820, 940, 1100, WH, 6)
    heat = clamp((t - a1) / 2.0) if t > a1 else 0.0
    for cx in (300, 540, 780):
        for r in (50, 90):
            circle(d, cx, 960, r, tuple(int(c * 0.35) for c in YE), 3)
            for j in range(6):
                a = t * (4 if r == 50 else -3) + j / 6 * 2 * math.pi
                dot(d, cx + math.cos(a) * r, 960 + math.sin(a) * r * 0.6, 7, YE)
    if heat > 0:
        overlay(img, (255, 110, 30), 0.1 * heat)
        for j in range(6):
            u = (t * 0.6 + j / 6) % 1.0
            x = 200 + j * 130
            pts = [(x + math.sin(yy / 26 + t * 4 + j) * 14, yy) for yy in range(int(780 - u * 260), int(830 - u * 260), 6)]
            line(d, pts, tuple(int(c * heat) for c in OR), 5)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "REMOLINOS", 300, 104, YE)
        chip(t, 1.0, "CORRIENTES DE FOUCAULT", 540, 460, WH, 34)
    else:
        gtitle(t, a1 + 0.2, "CALOR DESDE DENTRO", 300, 84, OR, pop=False)
    vignette(img, 150)


def sh_glass(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    hob(d, BL)
    on = t < a1 + 0.6
    spiral(d, 540, GY + 120, 280, 6, OR if on else DIM, 4)
    lift = ease(clamp((t - a1) / 0.6)) if t > a1 else 0.0
    pot(d, 540 + 360 * lift, GY - 300 * lift, WH, 1.0 - lift * 0.3)
    if t < a1:
        for j in range(5):
            u = (t * 0.5 + j / 5) % 1.0
            dot(d, 440 + j * 50, GY - 4 + u * 30, 7, tuple(int(c * (1 - u)) for c in OR))
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "CALOR PRESTADO", 300, 96, OR, pop=False)
    else:
        gtitle(t, a1 + 0.3, "SE APAGA AL MOMENTO", 300, 80, CY, pop=False)
    vignette(img, 150)


def sh_pans(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    hob(d, BL)
    spiral(d, 540, GY + 120, 280, 6, OR, 4)
    if t < a1:
        pot(d, 540, GY, (180, 190, 210), 0.0)
        label(d, 540, GY - 140, "?", 120, MG, F_POP)
        gtitle(t, 0.1, "¿POR QUÉ ESTA NO?", 300, 88, MG, pop=False)
    elif t < a2:
        pot(d, 330, GY, (170, 180, 200), 0.0, 260, 200)
        label(d, 330, GY - 260, "ALUMINIO", 30, DIM, F_MONO)
        line(d, [(260, GY - 160), (400, GY - 40)], RD, 10)
        line(d, [(400, GY - 160), (260, GY - 40)], RD, 10)
        pot(d, 760, GY, WH, clamp((t - a1) / 2.0), 260, 200)
        label(d, 760, GY - 260, "HIERRO", 30, WH, F_MONO)
        gtitle(t, a1 + 0.2, "NECESITA HIERRO", 300, 90, GR, pop=False)
    else:
        py = GY - 300
        pot(d, 540, py, WH, 0.0)
        k = ease(clamp((t - a2 - 0.2) / 0.6))
        my = lerp(py + 460, py + 140, k)
        line(d, [(470, my - 140), (470, my), (610, my), (610, my - 140)], RD, 26)
        d.line([(456, my - 120), (484, my - 120)], fill=WH, width=26)
        d.line([(596, my - 120), (624, my - 120)], fill=WH, width=26)
        if k > 0.98:
            for xx in (470, 610):
                circle(d, xx, py - 4, 30, GR, 5)
        gtitle(t, a2 + 0.2, "SI SE PEGA, SIRVE", 300, 88, GR)
    finish(img, lay)
    vignette(img, 150)


def sh_eff(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    x0, y = 140, 1300
    for i, (pct, col, lab, t0) in enumerate(((75, GR, "INDUCCIÓN", 0.3), (40, OR, "GAS", a1 + 0.2))):
        if t < t0:
            continue
        q = ease(clamp((t - t0) / 1.2))
        x = 300 + i * 480
        hgt = 700 * pct / 100 * q
        rrect(d, x - 110, y - 700, x + 110, y, 20, DIM, 4)
        if hgt > 30:
            d.rounded_rectangle([x - 104, y - hgt, x + 104, y - 6], radius=16, fill=tuple(int(c * 0.3) for c in col), outline=col, width=5)
        label(d, x, y + 50, lab, 36, col, F_POP)
        label(d, x, y - hgt - 50, f"{pct * q:.0f} %", 52, col, F_MONO)
        if i == 1 and q > 0.5:
            for j in range(5):
                u = (t * 0.7 + j / 5) % 1.0
                d.arc([x + 130 + u * 120 - 26, y - 400 + j * 60 - 26, x + 130 + u * 120 + 26, y - 400 + j * 60 + 26], -60, 60,
                      fill=tuple(int(c * (1 - u)) for c in OR), width=5)
    finish(img, lay)
    gtitle(t, 0.3, "ENERGÍA APROVECHADA", 300, 80, WH, pop=False)
    vignette(img, 150)


def sh_final(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    hob(d, BL)
    spiral(d, 540, GY + 120, 280, 6, OR, 4)
    pot(d, 540, GY, WH, 1.0)
    finish(img, lay)
    gtitle(t, 0.2, "LA OLLA ES EL FUEGO", 300, 88, OR)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "creative"), ("coil", "exp"), ("eddy", "creative"), ("pans", "playful"), ("eff", "premium"), ("final", "space")],
    "gains": {"exp": 0.7},
    "amb": {"hum": ["open", "coil", "field", "eddy", "glass", "pans", "final"]},
    "sfx": [("open+0.2", "hum_on", 0.2), ("open@L1+0.2", "pop", 0.2), ("coil+0.2", "draw", 0.18), ("coil@L1", "zap", 0.12),
            ("field+0.2", "whoosh_up", 0.12), ("field@L1+0.2", "blip", 0.12), ("eddy+0.3", "swell", 0.15),
            ("eddy@L1+0.2", "crackle", 0.12), ("glass@L1", "whoosh", 0.15), ("glass@L1+0.6", "blip_down", 0.15),
            ("pans+0.1", "pop", 0.2), ("pans@L1+0.2", "glitch", 0.12), ("pans@L2+0.7", "thud", 0.35), ("pans@L2+0.75", "ding", 0.1),
            ("eff+0.3", "riser", 0.1), ("eff@L1+0.2", "riser", 0.1), ("final+0.2", "chime", 0.06)],
    "bed": [("coil", "pans")],
    "bpm": 106,
}
