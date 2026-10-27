"""N01 · ¿Qué cambia de ir a 100 o a 140 km/h? (estilo neón explicativo)."""
from neon import *

TITLE = "Que_cambia_de_ir_a_100_o_a_140"
LINES = [
    "¿Qué cambia *de verdad* entre ir a 100 o a 140 por la autopista?",
    "Quédate, que al final te digo *cuánto tiempo ganas*.",
    "Primero, lo fácil: a 100 recorres *28 metros* cada segundo.",
    "A 140, casi *39*.",
    "Ahora imagina que algo se cruza delante.",
    "Tardas casi un segundo en reaccionar… y el coche sigue *a toda velocidad*.",
    "Truco del RACE: quita la última cifra y multiplícala por sí misma.",
    "A 100: diez por diez, *100 metros* de distancia de seguridad.",
    "A 140: catorce por catorce, *196 metros*.",
    "¿Casi el doble, si solo vas un 40 % más rápido?",
    "Sí: la energía crece *con el cuadrado* de la velocidad.",
    "A 140 llevas casi *el doble de energía*.",
    "Chocar a 100 es como caer desde *un piso 13*.",
    "A 140, como caer desde *un piso 26*.",
    "Y el aire te frena más: también crece con el cuadrado.",
    "Por eso gastas más: solo de 120 a 140, entre un *20 y un 25 %*.",
    "Y en una autovía de 120, ir a 140 son *100 euros* de multa.",
    "Entonces… ¿cuánto tiempo ganas?",
    "En un viaje de 100 kilómetros: *unos 17 minutos*.",
    "17 minutos… por casi el doble de frenada y de golpe.",
    "Tú decides si *merece la pena*.",
]
SHOTS = [("open", 0, 1, 0.3), ("meters", 2, 3, 0.3), ("react", 4, 5, 0.3), ("squares", 6, 8, 0.3), ("energy", 9, 11, 0.3),
         ("fall", 12, 13, 0.4), ("air", 14, 15, 0.3), ("fine", 16, 16, 0.3), ("time", 17, 18, 0.3), ("verdict", 19, 20, 1.8)]
FOCUS = {"open": (540, 1000, 1.15), "meters": (540, 900, 1.15), "react": (600, 900, 1.15), "squares": (540, 900, 1.12),
         "energy": (600, 900, 1.15), "fall": (540, 900, 1.12), "air": (540, 900, 1.15), "time": (540, 900, 1.15),
         "verdict": (540, 900, 1.12)}
NOTIF = ("react", 1.2)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon


def road(d, t, speed=1.0, col=CY, hz=760, skip=None):
    vx = 540
    for sx in (-700, 700):
        d.line([(vx, hz), (vx + sx * 1.6, H)], fill=col, width=5)
    for k in range(10):
        u = ((k / 10) + t * 0.6 * speed) % 1.0
        z0 = u ** 2.2
        z1 = min(1.0, (u + 0.05) ** 2.2)
        y0, y1 = hz + (H - hz) * z0, hz + (H - hz) * z1
        if skip and (skip[0] < y0 < skip[1] or skip[0] < y1 < skip[1]):
            continue
        d.line([(vx, y0), (vx, y1)], fill=YE, width=max(3, int(4 + 20 * z0)))
    d.line([(0, hz), (W, hz)], fill=DIM, width=3)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    road(d, t, 1.0 + 0.4 * clamp(t / 3), skip=(860, 1420))
    v = 100 + 40 * (0.5 - 0.5 * math.cos(t * 1.6))
    speedo(d, 540, 1120, 230, v, 200, CY, MG if v > 120 else YE)
    label(d, 540, 1290, f"{v:.0f}", 70, WH, F_POP)
    label(d, 540, 1350, "KM/H", 30, DIM)
    finish(img, lay)
    gtitle2(t, 0.2, "¿QUÉ CAMBIA DE IR A", "100 O A 140?", 250, 56, 112, WH, CY, hold=max(1.6, L[1][0] - 0.2))
    if t > L[1][0]:
        chip(t, L[1][0] + 0.2, "AL FINAL: CUÁNTO TIEMPO GANAS", 540, 330, YE, 38)
    vignette(img, 160)


def sh_meters(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    x0, x1 = 90, 990
    px = (x1 - x0) / 40.0
    for m in range(0, 41, 5):
        x = x0 + m * px
        d.line([(x, 1240), (x, 1270 if m % 10 else 1290)], fill=DIM, width=4)
        if m % 10 == 0:
            label(d, x, 1320, f"{m} m", 30, DIM)
    d.line([(x0, 1240), (x1, 1240)], fill=DIM, width=4)
    a1 = L[1][0]
    for i, (sp, col, y, t0) in enumerate(((27.8, CY, 900, 0.3), (38.9, MG, 1110, a1))):
        if t < t0:
            continue
        q = clamp((t - t0) / 1.0)
        xe = x0 + sp * px * ease(q)
        d.rounded_rectangle([x0, y - 16, max(x0 + 2, xe), y + 16], radius=14, outline=col, width=5)
        car(d, xe - 120, y - 30, 0.55, col, 1.0, -t * 9)
        label(d, x0, y - 120, "100 KM/H" if i == 0 else "140 KM/H", 40, col, F_POP, "lm")
        if q > 0.6:
            label(d, min(xe, x1 - 80), y + 70, f"{sp:.1f} m/s".replace(".", ","), 46, col, F_MONO, "mm")
    finish(img, lay)
    gtitle(t, 0.3, "CADA SEGUNDO", 300, 90, YE, pop=False)
    vignette(img, 160)


def sh_react(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    hz = 1240
    d.line([(0, hz), (W, hz)], fill=DIM, width=4)
    for k in range(14):
        x = (k * 90 - t * 300) % (W + 90) - 45
        d.line([(x, hz + 40), (x + 40, hz + 40)], fill=DIM, width=4)
    car(d, 300, hz - 6, 0.9, CY, 1.0, -t * 14)
    ox = 900
    blink = 0.6 + 0.4 * math.sin(t * 10) ** 2
    tri = [(ox, hz - 260), (ox + 90, hz - 100), (ox - 90, hz - 100), (ox, hz - 260)]
    line(d, tri, tuple(int(c * blink) for c in RD), 8, ease(clamp((t - 0.2) / 0.5)))
    if t > 0.6:
        label(d, ox, hz - 160, "!", 70, RD, F_POP)
    if t > a1:
        q = clamp((t - a1 - 0.2) / 1.6)
        cx, cy = 300, 640
        circle(d, cx, cy, 120, DIM, 6)
        circle(d, cx, cy, 120, YE, 10, q * 0.75 / 1.0)
        label(d, cx, cy, f"{0.75 * q:.2f} s".replace(".", ","), 48, YE)
        for i, (dist, col, y) in enumerate(((20.8, CY, 900), (29.2, MG, 1000))):
            xe = 520 + dist * 14 * ease(q)
            d.line([(520, y), (xe, y)], fill=col, width=14)
            label(d, 520, y - 40, ("A 100: " if i == 0 else "A 140: ") + f"{dist * ease(q):.0f} m", 32, col, F_MONO, "lm")
        chip(t, a1 + 0.2, "SIN TOCAR EL FRENO", 540, 330, RD, 40)
    else:
        gtitle(t, 0.4, "¡OBSTÁCULO!", 300, 100, RD)
    finish(img, lay)
    vignette(img, 160)


def grid_sq(d, x0, y0, n, cell, col, k, w=3):
    tot = n * n
    show = int(tot * k)
    for i in range(show):
        r, c = divmod(i, n)
        x, y = x0 + c * cell, y0 + r * cell
        d.rectangle([x + 2, y + 2, x + cell - 2, y + cell - 2], outline=col, width=w)


def sh_squares(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    if t < a1:
        label(d, 470, 820, "14", 220, WH, F_POP)
        k = ease(clamp((t - 0.8) / 0.5))
        label(d, 700, 820, "0", 220, RD if k > 0 else WH, F_POP)
        if k > 0:
            line(d, [(630, 930), (770, 700)], RD, 14, k)
        label(d, 540, 1100, "14 × 14", 110, YE, F_MONO) if t > 1.8 else None
        gtitle(t, 0.3, "EL TRUCO", 300, 100, YE)
    else:
        cell = 54
        x0, y0 = 540 - 7 * cell, 560
        k1 = clamp((t - a1) / 1.4)
        grid_sq(d, x0, y0, 10, cell, CY, k1)
        if t > a2:
            k2 = clamp((t - a2) / 1.6)
            extra = [(r, c) for r in range(14) for c in range(14) if r >= 10 or c >= 10]
            for i, (r, c) in enumerate(extra[: int(len(extra) * k2)]):
                d.rectangle([x0 + c * cell + 2, y0 + r * cell + 2, x0 + (c + 1) * cell - 2, y0 + (r + 1) * cell - 2], outline=MG, width=3)
        if t < a2:
            gtitle(t, a1 + 0.2, "10 × 10 = 100 M", 300, 84, CY, pop=False)
        else:
            gtitle(t, a2 + 0.2, "14 × 14 = 196 M", 300, 84, MG, pop=False)
    finish(img, lay)
    vignette(img, 150)


def sh_energy(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    ox, oy, gw, gh = 140, 1300, 820, 700
    d.line([(ox, oy), (ox + gw, oy)], fill=DIM, width=4)
    d.line([(ox, oy), (ox, oy - gh)], fill=DIM, width=4)
    label(d, ox + gw, oy + 40, "VELOCIDAD", 28, DIM, F_MONO, "rm")
    label(d, ox - 10, oy - gh - 30, "ENERGÍA", 28, DIM, F_MONO, "lm")
    vmax = 160
    pts = [(ox + gw * v / vmax, oy - gh * (v / vmax) ** 2) for v in range(0, vmax + 1, 4)]
    k = ease(clamp((t - 0.3) / 1.6))
    line(d, pts, YE, 8, k)
    a1, a2 = L[1][0], L[2][0]
    for v, col, t0 in ((100, CY, a1 + 0.4), (140, MG, a1 + 1.4)):
        if t > t0:
            kk = ease(clamp((t - t0) / 0.5))
            x, y = ox + gw * v / vmax, oy - gh * (v / vmax) ** 2
            dashed(d, (x, oy), (x, y), col, 4)
            dashed(d, (ox, y), (x, y), col, 4)
            dot(d, x, y, 14 * kk, col)
            label(d, x, oy + 44, str(v), 40, col, F_MONO)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "+40 % VELOCIDAD", 300, 84, CY, pop=False)
    elif t < a2:
        chip(t, a1 + 0.1, "E = ½ · m · v²", 540, 330, YE, 50)
    else:
        gtitle(t, a2 + 0.1, "×1,96 ENERGÍA", 300, 96, MG)
    vignette(img, 150)


def sh_fall(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    base = 1420
    a1 = L[1][0]
    k1 = ease(clamp((t - 0.2) / 1.6))
    building(d, 320, base, 13, CY, 3, k1, 38, 170)
    if t > a1:
        building(d, 760, base, 26, MG, 3, ease(clamp((t - a1) / 1.8)), 38, 170)
    d.line([(60, base), (W - 60, base)], fill=DIM, width=4)
    fy = base - 13 * 38 - 40 + ((t * 2.0) % 1.0) * 0 if t < a1 else None
    finish(img, lay)
    if t < a1:
        chip(t, 1.4, "100 KM/H ≈ 39 M", 320, base - 13 * 38 - 70, CY, 34)
        gtitle(t, 0.3, "PISO 13", 300, 104, CY)
    else:
        chip(t, 1.4 + a1, "140 KM/H ≈ 77 M", 760, base - 26 * 38 - 60, MG, 34)
        gtitle(t, a1 + 0.2, "PISO 26", 230, 104, MG)
    vignette(img, 150)


def sh_air(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    cy = 900
    car(d, 600, cy + 80, 1.3, CY, 1.0, -t * 14, 7)
    strength = 1.0 if t < a1 else 1.7
    for i in range(7):
        y = 560 + i * 70
        ph = t * 8 * strength + i
        pts = []
        for x in range(0, 380, 10):
            bend = 0
            if 200 < x:
                bend = -((x - 200) / 180) ** 2 * (cy + 40 - y) * 0.25 if y < cy + 40 else 0
            pts.append((x, y + bend + math.sin(x / 40 + ph) * 6 * strength))
        line(d, pts, WH if i % 2 else BL, 4)
    if t > a1:
        cx, cyy = 540, 1300
        d.arc([cx - 150, cyy - 150, cx + 150, cyy + 150], 180, 360, fill=DIM, width=8)
        q = ease(clamp((t - a1) / 2.0))
        a = math.radians(180 + 160 * (1 - q * 0.6))
        d.line([(cx, cyy), (cx + math.cos(a) * 130, cyy + math.sin(a) * 130)], fill=OR, width=10)
        label(d, cx - 160, cyy + 30, "E", 34, RD, F_POP)
        label(d, cx + 160, cyy + 30, "F", 34, GR, F_POP)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "RESISTENCIA × 1,96", 300, 80, BL, pop=False)
    else:
        gtitle(t, a1 + 0.3, "+20-25 % CONSUMO", 300, 84, OR)
        chip(t, a1 + 0.9, "SOLO DE 120 A 140", 540, 470, WH, 34)
    vignette(img, 150)


def sh_fine(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    rrect(d, 200, 620, 520, 840, 24, CY, 6, ease(clamp(t / 0.8)))
    circle(d, 360, 730, 70, CY, 6, ease(clamp((t - 0.3) / 0.6)))
    circle(d, 360, 730, 30, CY, 5)
    d.line([(360, 840), (360, 1100)], fill=CY, width=8)
    fl = math.exp(-max(0, t - 1.0) * 6) if t > 1.0 else 0
    if fl > 0.02:
        dot(d, 360, 730, 80 * fl, (255, 255, int(255 * fl)))
    k = ease(clamp((t - 1.2) / 0.6))
    if k > 0:
        tk = [(620, 560), (920, 560), (920, 1180), (620, 1180), (620, 560)]
        line(d, tk, YE, 6, k)
        for j in range(5):
            d.line([(660, 760 + j * 60), (880 - (j % 2) * 60, 760 + j * 60)], fill=DIM, width=4)
        label(d, 770, 640, "MULTA", 36, YE, F_POP)
        if k > 0.9:
            label(d, 770, 1100, "100 €", 64, YE, F_POP)
    finish(img, lay)
    gtitle(t, 1.4, "100 € · SIN PUNTOS", 300, 84, YE)
    vignette(img, 150)


def sh_time(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    x0, x1 = 120, 960
    for i, (mins, col, y, lab) in enumerate(((60.0, CY, 820, "A 100"), (42.9, MG, 1060, "A 140"))):
        q = ease(clamp((t - 0.3 - i * 0.4) / 1.6))
        xe = x0 + (x1 - x0) * mins / 60 * q
        rrect(d, x0, y - 40, x1, y + 40, 20, DIM, 4)
        if xe > x0 + 40:
            d.rounded_rectangle([x0 + 6, y - 34, xe - 6, y + 34], radius=16, fill=tuple(int(c * 0.35) for c in col), outline=col, width=5)
        label(d, x0, y - 80, lab, 34, col, F_POP, "lm")
        label(d, x1, y - 80, f"{mins * q:.0f} MIN", 36, col, F_MONO, "rm")
    if t > a1:
        kk = ease(clamp((t - a1) / 0.6))
        xa = x0 + (x1 - x0) * 42.9 / 60
        dashed(d, (xa, 760), (xa, 1120), YE, 4, off=t * 40)
        d.line([(xa, 1180), (x1, 1180)], fill=YE, width=6)
        label(d, (xa + x1) / 2, 1230, "17 MIN", 44, YE, F_POP)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "100 KM DE VIAJE", 300, 84, WH, pop=False)
    else:
        gtitle(t, a1 + 0.2, "≈ 17 MINUTOS", 300, 104, YE)
    vignette(img, 150)


def sh_verdict(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    tilt = math.radians(-12 * ease(clamp((t - 0.8) / 1.2)))
    cx, cy = 540, 760
    d.line([(cx, cy), (cx, 1300)], fill=DIM, width=8)
    d.line([(cx - 160, 1300), (cx + 160, 1300)], fill=DIM, width=8)
    L_ = 360
    lx, ly = cx - math.cos(tilt) * L_, cy - math.sin(tilt) * L_
    rx, ry = cx + math.cos(tilt) * L_, cy + math.sin(tilt) * L_
    d.line([(lx, ly), (rx, ry)], fill=WH, width=8)
    dot(d, cx, cy, 16, WH)
    for x, y, col, txt in ((lx, ly, YE, "17 MIN"), (rx, ry, MG, "×2")):
        d.line([(x, y), (x - 90, y + 200)], fill=col, width=4)
        d.line([(x, y), (x + 90, y + 200)], fill=col, width=4)
        d.arc([x - 110, y + 140, x + 110, y + 260], 0, 180, fill=col, width=6)
        label(d, x, y + 160, txt, 46, col, F_POP)
    finish(img, lay)
    chip(t, 0.6, "FRENADA Y GOLPE", rx, ry + 320, MG, 30)
    if t > L[1][0]:
        gtitle(t, L[1][0] + 0.2, "¿MERECE LA PENA?", 300, 92, WH, pop=False)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "exp"), ("squares", "creative"), ("fall", "tension"), ("air", "creative"), ("time", "premium")],
    "gains": {"exp": 0.75, "creative": 0.9},
    "amb": {"road": ["open", "meters", "react", "air"], "hum": ["squares", "energy", "fine", "time", "verdict"]},
    "sfx": [("open+0.2", "draw", 0.2), ("open+0.6", "riser", 0.1), ("open@L1+0.2", "blip", 0.15),
            ("meters+0.3", "whoosh_up", 0.12), ("meters@L1", "whoosh_up", 0.14),
            ("react+0.2", "beep", 0.12), ("react+0.45", "beep", 0.12), ("react@L1+0.2", "heart", 0.3), ("react@L1+1.0", "heart", 0.3),
            ("squares+0.8", "glitch", 0.15), ("squares+1.6", "blip", 0.15), ("squares+2.4", "blip", 0.15),
            ("squares@L1", "draw", 0.2), ("squares@L2", "draw", 0.22),
            ("energy+0.3", "draw", 0.2), ("energy@L1+0.4", "pop", 0.2), ("energy@L1+1.4", "pop", 0.2), ("energy@L2+0.1", "impact", 0.25),
            ("fall+0.2", "riser", 0.1), ("fall+1.8", "thud", 0.3), ("fall@L1", "riser_long", 0.12), ("fall@L1+1.8", "impact", 0.35),
            ("air", "whoosh", 0.15), ("air@L1+0.3", "blip_down", 0.15),
            ("fine+1.0", "shutter", 0.3), ("fine+1.4", "zap", 0.12),
            ("time+0.3", "tick", 0.15), ("time+1.0", "tick", 0.15), ("time@L1+0.2", "chime", 0.06),
            ("verdict+0.8", "thud", 0.2)],
    "bed": [("meters", "fall"), ("air", "time")],
    "bpm": 110,
}
