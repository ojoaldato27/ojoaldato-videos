"""N05 · ¿Cómo se infla un airbag más rápido que un parpadeo?"""
from neon import *

TITLE = "Como_se_infla_un_airbag"
LINES = [
    "En un choque, el airbag se infla *más rápido que un parpadeo*.",
    "¿Cómo sabe que estás chocando… y de dónde sale tanto gas?",
    "Todo empieza con un sensor: un *acelerómetro*.",
    "Vigila sin parar cuánto frena el coche.",
    "Si frena de golpe, mucho más que en cualquier frenazo… detecta *un choque*.",
    "Al instante, manda una señal eléctrica a un *detonador*.",
    "El detonador prende una pastilla química.",
    "Durante años se usó *azida de sodio*: al reaccionar, suelta *nitrógeno*.",
    "El mismo gas que forma casi el *80 %* del aire que respiras.",
    "Unos 130 gramos dan para *67 litros* de gas.",
    "Y la bolsa se llena en unos *30 milisegundos*.",
    "Un parpadeo tarda varias veces más.",
    "Pero el airbag no es un cojín duro: tiene *agujeros*.",
    "Cuando tu cuerpo choca contra él, se va desinflando… y te frena *poco a poco*.",
    "Y está pensado para funcionar *junto al cinturón*: sin él, puede hacerte daño.",
    "Treinta milésimas de segundo… que *te pueden salvar la vida*.",
]
SHOTS = [("open", 0, 1, 0.3), ("sensor", 2, 4, 0.3), ("signal", 5, 6, 0.3), ("chem", 7, 9, 0.3), ("timing", 10, 11, 0.3),
         ("vents", 12, 13, 0.3), ("belt", 14, 15, 1.8)]
FOCUS = {"open": (560, 960, 1.12), "sensor": (540, 960, 1.12), "signal": (540, 960, 1.12), "chem": (540, 960, 1.12),
         "timing": (540, 960, 1.12), "vents": (560, 960, 1.15), "belt": (560, 960, 1.12)}
NOTIF = ("signal", 0.6)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon


def cabin(d, t, col=CY, k=1.0):
    """Puesto de conducción de perfil (mirando a la izquierda)."""
    dim = tuple(int(c * 0.55) for c in col)
    line(d, [(60, 640), (200, 660), (420, 740), (470, 820)], dim, 6, k)
    line(d, [(60, 1300), (1020, 1300)], dim, 4, k)
    line(d, [(470, 800), (330, 870)], col, 9, k)
    d.ellipse([268, 740, 340, 1000], outline=col, width=11)
    line(d, [(860, 560), (800, 1150), (560, 1160)], col, 8, k)
    line(d, [(800, 1150), (840, 1300)], dim, 6, k)


def driver(d, x, y, col=WH, lean=0.0):
    dx = -lean * 140
    circle(d, 690 + dx, 690, 56, col, 7)
    line(d, [(700 + dx * 0.8, 750), (740, 1110)], col, 9)
    line(d, [(740, 1110), (520, 1130), (470, 1290)], col, 9)
    line(d, [(705 + dx * 0.8, 820), (560 + dx * 0.4, 890), (335, 880)], col, 8)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    cabin(d, t, CY, ease(clamp(t / 1.0)))
    hit = 1.6
    lean = ease(clamp((t - hit) / 0.5)) * 0.4
    driver(d, 700, 720, WH, lean)
    if t > hit:
        q = clamp((t - hit) / 0.25)
        r = 30 + 170 * ease(q)
        circle(d, 330 + 150 * ease(q), 850, r, YE, 8)
        if q > 0.99:
            circle(d, 480, 850, r - 22, tuple(int(c * 0.4) for c in YE), 3)
    finish(img, lay)
    if t > hit:
        overlay(img, (255, 255, 255), 0.5 * math.exp(-(t - hit) * 8))
    gtitle2(t, 0.2, "MÁS RÁPIDO QUE", "UN PARPADEO", 250, 60, 104, WH, YE, hold=max(1.6, L[1][0] + 0.6))
    vignette(img, 150)


def sh_sensor(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    rrect(d, 340, 520, 740, 820, 20, CY, 6)
    for k in range(8):
        d.line([(360 + k * 50, 820), (360 + k * 50, 860)], fill=CY, width=6)
        d.line([(360 + k * 50, 480), (360 + k * 50, 520)], fill=CY, width=6)
    shake_ = 0
    if t > a2 + 0.8:
        shake_ = math.exp(-(t - a2 - 0.8) * 3) * math.sin(t * 40) * 60
    mx = 540 + math.sin(t * 3) * 10 + shake_
    pts = []
    for k in range(13):
        x = 380 + (mx - 60 - 380) * k / 12
        pts.append((x, 670 + (20 if k % 2 else -20)))
    line(d, pts, YE, 4)
    rect(d, mx - 60, 620, mx + 60, 720, YE, 6)
    ox, oy, gw, gh = 120, 1380, 840, 380
    d.line([(ox, oy), (ox + gw, oy)], fill=DIM, width=3)
    d.line([(ox, oy), (ox, oy - gh)], fill=DIM, width=3)
    thr = oy - gh * 0.6
    dashed(d, (ox, thr), (ox + gw, thr), RD, 3, off=t * 30)
    label(d, ox + gw, thr - 26, "UMBRAL", 26, RD, F_MONO, "rm")
    q = clamp(t / (T - 0.3))
    pts = []
    for i in range(int(120 * q) + 1):
        u = i / 120
        x = ox + gw * u
        v = 0.12 + 0.05 * math.sin(u * 40)
        if t > a1:
            v += 0.18 * math.exp(-((u - 0.45) * 12) ** 2)
        if t > a2:
            v += 0.9 * math.exp(-((u - 0.85) * 18) ** 2)
        pts.append((x, oy - gh * min(1.0, v)))
    line(d, pts, GR, 5)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "ACELERÓMETRO", 300, 92, CY)
    elif t < a2:
        chip(t, a1 + 0.2, "FRENAZO NORMAL", 540, 330, GR, 44)
    else:
        gtitle(t, a2 + 0.8, "¡CHOQUE!", 300, 110, RD)
    vignette(img, 150)


def sh_signal(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    rrect(d, 120, 620, 360, 800, 16, CY, 6)
    label(d, 240, 710, "SENSOR", 32, CY, F_MONO)
    rrect(d, 700, 560, 960, 860, 30, OR, 6)
    label(d, 830, 900, "DETONADOR", 32, OR, F_MONO)
    path_ = [(360, 710), (520, 710), (520, 640), (700, 640)]
    line(d, path_, DIM, 5)
    u = clamp((t - 0.3) / 0.8)
    pp = partial(path_, u)
    if len(pp) > 1:
        line(d, pp, YE, 7)
        dot(d, pp[-1][0], pp[-1][1], 14, WH)
    a1 = L[1][0]
    if t > a1:
        k = clamp((t - a1) / 0.6)
        rrect(d, 760, 660, 900, 760, 20, YE, 6)
        for j in range(10):
            a = j / 10 * 2 * math.pi + t
            r1, r2 = 70, 70 + 90 * k
            d.line([(830 + math.cos(a) * r1, 710 + math.sin(a) * r1), (830 + math.cos(a) * r2, 710 + math.sin(a) * r2)],
                   fill=tuple(int(c * (1 - k * 0.5)) for c in OR), width=6)
    finish(img, lay)
    gtitle(t, 0.3, "SEÑAL ELÉCTRICA", 300, 84, YE, pop=False, hold=max(1.2, a1 - 0.6))
    if t > a1:
        gtitle(t, a1 + 0.1, "¡CHISPA!", 300, 104, OR)
    vignette(img, 150)


def n2(d, x, y, s, col):
    circle(d, x - 26 * s, y, 26 * s, col, 5)
    circle(d, x + 26 * s, y, 26 * s, col, 5)
    label(d, x - 26 * s, y, "N", int(24 * s), col, F_POP)
    label(d, x + 26 * s, y, "N", int(24 * s), col, F_POP)


def sh_chem(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    if t < a1:
        rrect(d, 420, 1100, 660, 1200, 20, OR, 6)
        rr = random.Random(2)
        for k in range(16):
            u = (t * 0.6 + rr.random()) % 1.0
            x = 540 + rr.uniform(-300, 300) * u
            y = 1100 - u * 520
            n2(d, x, y, 0.9, tuple(int(c * (1 - u * 0.6)) for c in BL))
        chip(t, 0.3, "NaN₃  →  Na + N₂", 540, 330, OR, 50)
    elif t < a2:
        x0, x1, y = 120, 960, 920
        rrect(d, x0, y - 60, x1, y + 60, 24, DIM, 5)
        k = ease(clamp((t - a1) / 1.2))
        xe = x0 + (x1 - x0) * 0.78 * k
        if xe > x0 + 30:
            d.rounded_rectangle([x0 + 6, y - 54, xe, y + 54], radius=20, fill=tuple(int(c * 0.3) for c in BL), outline=BL, width=5)
        label(d, (x0 + xe) / 2, y, "N₂", 56, WH, F_POP)
        label(d, x1 - 90, y, "O₂…", 40, DIM, F_POP)
        gtitle(t, a1 + 0.2, "78 % DEL AIRE", 300, 96, BL)
    else:
        rrect(d, 200, 1040, 340, 1110, 16, OR, 6)
        label(d, 270, 1160, "130 g", 40, OR, F_MONO)
        k = ease(clamp((t - a2 - 0.2) / 1.2))
        circle(d, 680, 900, 60 + 220 * k, BL, 7)
        label(d, 680, 900, f"{67 * k:.0f} L", 72, WH, F_POP)
        arrow(d, (360, 1070), (440, 1000), YE, 6, 1.0)
    finish(img, lay)
    vignette(img, 150)


def sh_timing(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    x0, x1 = 120, 960
    scale_ms = 300.0
    y1, y2 = 820, 1100
    q = clamp((t - 0.3) / 1.0)
    xe = x0 + (x1 - x0) * 30 / scale_ms * ease(q)
    d.rounded_rectangle([x0, y1 - 40, max(x0 + 10, xe), y1 + 40], radius=16, fill=tuple(int(c * 0.35) for c in YE), outline=YE, width=5)
    label(d, x0, y1 - 80, "AIRBAG", 36, YE, F_POP, "lm")
    label(d, xe + 20, y1, "30 ms", 44, YE, F_MONO, "lm")
    if t > a1:
        q2 = clamp((t - a1) / 1.6)
        xe2 = x0 + (x1 - x0) * ease(q2)
        d.rounded_rectangle([x0, y2 - 40, max(x0 + 10, xe2), y2 + 40], radius=16, fill=tuple(int(c * 0.35) for c in MG), outline=MG, width=5)
        label(d, x0, y2 - 80, "PARPADEO", 36, MG, F_POP, "lm")
        label(d, x1, y2 + 80, "100-400 ms", 40, MG, F_MONO, "rm")
        cx, cy = 540, 1350
        lid = abs(math.sin(t * 2.2))
        d.arc([cx - 120, cy - 60 * (1 - lid) - 10, cx + 120, cy + 60], 180, 360, fill=WH, width=6)
        d.arc([cx - 120, cy - 60, cx + 120, cy + 60], 0, 180, fill=WH, width=6)
    finish(img, lay)
    gtitle(t, 0.3, "0,03 SEGUNDOS", 300, 96, YE)
    vignette(img, 150)


def sh_vents(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    cx, cy = 440, 900
    press = ease(clamp((t - a1 - 0.2) / 1.6)) if t > a1 else 0.0
    r = 260 - 60 * press
    pts = []
    for k in range(61):
        a = k / 60 * 2 * math.pi
        rr_ = r * (1 - 0.25 * press * max(0, math.cos(a)))
        pts.append((cx + math.cos(a) * rr_, cy + math.sin(a) * rr_))
    line(d, pts, YE, 7)
    for hx, hy in ((cx - 120, cy - 180), (cx - 150, cy + 160)):
        circle(d, hx, hy, 18, OR, 5)
        if press > 0:
            for j in range(5):
                u = (t * 2 + j / 5) % 1.0
                dot(d, hx - u * 160, hy + (u * 60 if hy > cy else -u * 60), 8 * (1 - u), OR)
    hx = lerp(900, cx + r + 40, ease(clamp(t / 1.0)))
    circle(d, hx, 860, 70, WH, 6)
    line(d, [(hx + 30, 930), (hx + 120, 1250)], WH, 8)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "TIENE AGUJEROS", 300, 92, OR, pop=False)
    else:
        gtitle(t, a1 + 0.3, "FRENA POCO A POCO", 300, 84, GR, pop=False)
    vignette(img, 150)


def sh_belt(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    cabin(d, t, DIM)
    driver(d, 700, 720, WH, 0.15)
    k = ease(clamp((t - 0.4) / 1.0))
    line(d, [(820, 620), (650, 1110)], GR, 14, k)
    line(d, [(560, 1110), (790, 1130)], GR, 12, k)
    circle(d, 480, 850, 200, YE, 8, ease(clamp((t - 1.2) / 0.5)))
    finish(img, lay)
    chip(t, 0.3, "CINTURÓN + AIRBAG", 540, 330, GR, 46)
    if t > L[1][0]:
        gtitle(t, L[1][0] + 0.2, "0,03 S QUE SALVAN", 430, 76, YE, pop=False)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "tension"), ("sensor", "exp"), ("chem", "creative"), ("vents", "space"), ("belt", "premium")],
    "gains": {"exp": 0.7},
    "amb": {"road": ["open"], "hum": ["sensor", "signal", "timing"]},
    "sfx": [("open+1.55", "boom", 0.4), ("open+1.6", "impact", 0.35), ("sensor+0.3", "draw", 0.15),
            ("sensor@L1+0.2", "blip", 0.12), ("sensor@L2+0.8", "impact", 0.3), ("sensor@L2+0.8", "beep", 0.12),
            ("signal+0.3", "zap", 0.15), ("signal@L1+0.1", "impact", 0.3), ("chem+0.3", "whoosh_up", 0.15),
            ("chem@L1+0.2", "blip", 0.12), ("chem@L2+0.2", "swell", 0.18), ("timing+0.3", "whoosh_up", 0.15),
            ("timing+1.3", "ding", 0.1), ("timing@L1", "tick", 0.12), ("vents@L1+0.2", "whoosh", 0.18),
            ("belt+0.4", "click", 0.35), ("belt+1.2", "pop", 0.2)],
    "bed": [("sensor", "vents")],
    "bpm": 112,
}
