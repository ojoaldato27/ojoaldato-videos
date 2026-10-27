"""N10 · ¿Por qué explotan las palomitas?"""
from neon import *

TITLE = "Por_que_explotan_las_palomitas"
LINES = [
    "Cada palomita es una pequeña *bomba de vapor*.",
    "¿Qué pasa dentro del grano… y de dónde sale el *¡pop!*?",
    "Un grano de maíz tiene una cáscara muy dura… y dentro, *almidón y un poco de agua*.",
    "Al calentarlo, esa agua se convierte en *vapor*.",
    "Pero la cáscara no le deja salir… y la presión sube y sube.",
    "Cerca de los *180 grados*, dentro hay unas *10 atmósferas* de presión.",
    "Diez veces la presión del aire que te rodea.",
    "Hasta que la cáscara *revienta*.",
    "El almidón, blando por el calor, se hincha de golpe… y se enfría convertido en *espuma*.",
    "Eso blanco que te comes es *almidón inflado*.",
    "¿Y el ruido? En 2015, unos científicos lo grabaron a *3.000 imágenes por segundo*.",
    "Y descubrieron que el pop no es la cáscara rompiéndose…",
    "…es el *vapor* escapando de golpe.",
    "Al salir disparado, el grano *salta*… como un pequeño cohete.",
    "Con una aceleración de unas *20 veces la gravedad*.",
    "Así que cada palomita es una explosión… *que te comes*.",
]
SHOTS = [("open", 0, 1, 0.3), ("kernel", 2, 3, 0.3), ("pressure", 4, 6, 0.3), ("burst", 7, 9, 0.3), ("camera", 10, 12, 0.3),
         ("jump", 13, 14, 0.3), ("final", 15, 15, 1.8)]
FOCUS = {"open": (540, 960, 1.12), "kernel": (540, 960, 1.15), "pressure": (540, 960, 1.12), "burst": (540, 960, 1.15),
         "camera": (540, 960, 1.12), "jump": (540, 960, 1.12), "final": (540, 960, 1.12)}
NOTIF = ("pressure", 0.8)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon


def kernel(d, x, y, s=1.0, col=YE, crack=0.0):
    pts = []
    for k in range(41):
        a = k / 40 * 2 * math.pi
        r = 120 * s * (1 + 0.22 * math.cos(a) - 0.08 * math.cos(2 * a))
        pts.append((x + math.sin(a) * r * 0.78, y - math.cos(a) * r))
    line(d, pts, col, 7)
    line(d, [(x - 30 * s, y + 90 * s), (x, y + 125 * s), (x + 30 * s, y + 90 * s)], OR, 6)
    if crack > 0:
        line(d, [(x - 10 * s, y - 120 * s), (x + 12 * s, y - 70 * s), (x - 8 * s, y - 30 * s), (x + 10 * s, y + 10 * s)], WH, 5, crack)


def popcorn(d, x, y, s=1.0, col=WH, seed=1):
    rr = random.Random(seed)
    for k in range(7):
        a = k / 7 * 2 * math.pi + rr.uniform(-0.3, 0.3)
        r = rr.uniform(40, 70) * s
        cx, cy = x + math.cos(a) * 55 * s, y + math.sin(a) * 45 * s
        circle(d, cx, cy, r, col, 5)
    circle(d, x, y, 60 * s, col, 5)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    rr = random.Random(3)
    for k in range(9):
        x, y = rr.uniform(160, 920), rr.uniform(640, 1320)
        tk = 0.5 + k * 0.25
        if t < tk:
            kernel(d, x, y, 0.35)
        else:
            u = clamp((t - tk) / 0.25)
            popcorn(d, x, y - 40 * u, 0.4 + 0.3 * ease(u), WH, k)
            if u < 1:
                circle(d, x, y, 40 + 140 * u, tuple(int(c * (1 - u)) for c in YE), 4)
    finish(img, lay)
    gtitle2(t, 0.2, "¿POR QUÉ EXPLOTAN", "LAS PALOMITAS?", 250, 60, 96, WH, YE, hold=max(1.6, L[1][0] + 1.0))
    vignette(img, 150)


def sh_kernel(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    kernel(d, 540, 940, 2.6, YE)
    rr = random.Random(5)
    for k in range(40):
        x, y = rr.uniform(400, 680), rr.uniform(720, 1180)
        d.rectangle([x - 8, y - 6, x + 8, y + 6], outline=(140, 120, 80), width=2)
    for k in range(14):
        x, y = rr.uniform(420, 660), rr.uniform(760, 1160)
        if t < a1:
            dot(d, x, y, 9, BL)
        else:
            u = ((t - a1) * 0.8 + k / 14) % 1.0
            circle(d, x + math.sin(t * 5 + k) * 20, y - u * 40, 8 + 10 * u, tuple(int(c * (1 - u * 0.5)) for c in WH), 3)
    if t > a1:
        for j in range(3):
            u = (t * 0.8 + j / 3) % 1.0
            line(d, [(400 + j * 140 + math.sin(yy / 20 + t * 4) * 12, yy) for yy in range(int(1480 - u * 120), int(1540 - u * 120), 6)],
                 tuple(int(c * (1 - u)) for c in OR), 6)
    finish(img, lay)
    if t < a1:
        chip(t, 0.3, "ALMIDÓN + AGUA (~14 %)", 540, 330, YE, 40)
    else:
        gtitle(t, a1 + 0.2, "VAPOR", 300, 110, WH)
    vignette(img, 150)


def sh_pressure(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    q = clamp(t / (T - 0.3))
    kernel(d, 380, 960, 1.9 + 0.08 * q + 0.02 * math.sin(t * 30) * q, YE)
    cx, cy, r = 800, 960, 180
    d.arc([cx - r, cy - r, cx + r, cy + r], 135, 405, fill=DIM, width=10)
    a = math.radians(135 + 270 * min(1, q * 1.05))
    d.line([(cx, cy), (cx + math.cos(a) * (r - 30), cy + math.sin(a) * (r - 30))], fill=RD if q > 0.8 else YE, width=10)
    dot(d, cx, cy, 16, YE)
    label(d, cx, cy + 110, f"{1 + 9 * q:.0f} atm", 48, WH, F_MONO)
    th_y = lerp(1300, 700, q)
    rrect(d, 120, 640, 180, 1320, 30, WH, 5)
    d.rectangle([136, th_y, 164, 1300], fill=RD)
    label(d, 150, 600, f"{lerp(20, 180, q):.0f} °C", 36, RD, F_MONO)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "LA PRESIÓN SUBE", 300, 96, YE, pop=False)
    elif t < a2:
        gtitle(t, a1 + 0.2, "180 °C · 10 ATM", 300, 92, RD)
    else:
        gtitle(t, a2 + 0.2, "×10 EL AIRE", 300, 100, RD, pop=False)
    vignette(img, 150)


def sh_burst(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    hit = 0.5
    if t < hit:
        kernel(d, 540, 960, 2.0 + math.sin(t * 50) * 0.03, YE, ease(t / hit))
    else:
        u = clamp((t - hit) / 0.5)
        s_ = 0.5 + 2.4 * ease(u)
        popcorn(d, 540, 960, s_, WH, 4)
        if u < 1:
            for j in range(12):
                a = j / 12 * 2 * math.pi
                r1, r2 = 200 * u, 200 * u + 120
                d.line([(540 + math.cos(a) * r1, 960 + math.sin(a) * r1), (540 + math.cos(a) * r2, 960 + math.sin(a) * r2)],
                       fill=tuple(int(c * (1 - u)) for c in YE), width=6)
        rr = random.Random(7)
        for k in range(10):
            a = rr.uniform(0, 2 * math.pi)
            dist = 180 + 500 * ease(u)
            line(d, [(540 + math.cos(a) * dist, 960 + math.sin(a) * dist), (540 + math.cos(a) * (dist + 40), 960 + math.sin(a) * (dist + 40) + 20)],
                 OR, 6)
    finish(img, lay)
    if t > hit:
        overlay(img, (255, 250, 230), 0.6 * math.exp(-(t - hit) * 7))
    if t < a1:
        gtitle(t, hit, "¡POP!", 300, 140, YE)
    elif t < a2:
        gtitle(t, a1 + 0.2, "ESPUMA DE ALMIDÓN", 300, 84, WH, pop=False)
    else:
        chip(t, a2 + 0.2, "ALMIDÓN INFLADO", 540, 330, YE, 46)
    vignette(img, 150)


def sh_camera(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    if t < a1:
        rrect(d, 260, 760, 700, 1120, 30, WH, 6)
        circle(d, 480, 940, 120, CY, 7)
        circle(d, 480, 940, 70, CY, 4)
        rrect(d, 700, 860, 840, 1020, 16, WH, 6)
        for k in range(5):
            x = 300 + k * 90
            rect(d, x, 1200, x + 70, 1260, DIM, 3)
            if int(t * 12) % 5 == k:
                d.rectangle([x + 4, 1204, x + 66, 1256], outline=YE, width=4)
        gtitle(t, 0.3, "3.000 FPS", 300, 110, CY)
    else:
        u = ((t - a1) * 0.5) % 1.0
        kernel(d, 540, 1000, 1.6, YE, 1.0)
        if t > a2:
            for k in range(10):
                uu = (t * 1.2 + k / 10) % 1.0
                circle(d, 540 + math.sin(k) * 40 * uu, 820 - uu * 260, 16 + 30 * uu, tuple(int(c * (1 - uu)) for c in WH), 4)
            gtitle(t, a2 + 0.1, "ES EL VAPOR", 300, 104, WH)
        else:
            line(d, [(470, 880), (610, 1080)], RD, 10)
            line(d, [(610, 880), (470, 1080)], RD, 10)
            chip(t, a1 + 0.2, "NO ES LA CÁSCARA", 540, 330, RD, 44)
    finish(img, lay)
    vignette(img, 150)


def sh_jump(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    period = 1.8
    u = (t % period) / period
    y = 1300 - 620 * 4 * u * (1 - u)
    rot = u * 490
    popcorn(d, 540 + (u - 0.5) * 200, y, 0.9, WH, 2)
    d.line([(200, 1400), (880, 1400)], fill=DIM, width=5)
    for k in range(8):
        uu = clamp(u * 3 - k * 0.05)
        if uu < 1:
            dot(d, 540 + math.sin(k) * 30, 1360 + uu * 60, 8 * (1 - uu), WH)
    label(d, 880, 640, f"{rot:.0f}°", 44, CY, F_MONO)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "¡SALTA!", 300, 120, YE)
    else:
        gtitle(t, a1 + 0.2, "≈ 20 G", 300, 120, MG)
        chip(t, a1 + 0.8, "200 m/s²", 540, 460, WH, 40)
    vignette(img, 150)


def sh_final(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    rrect(d, 300, 760, 780, 1360, 30, RD, 7)
    for k in range(5):
        x = 330 + k * 100
        d.line([(x, 780), (x + 40, 1340)], fill=WH, width=14)
    rr = random.Random(8)
    for k in range(7):
        popcorn(d, rr.uniform(360, 720), rr.uniform(640, 800) + math.sin(t * 2 + k) * 10, 0.45, WH, k)
    finish(img, lay)
    gtitle(t, 0.2, "UNA EXPLOSIÓN COMESTIBLE", 300, 72, YE)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "playful"), ("kernel", "creative"), ("pressure", "tension"), ("burst", "playful"), ("camera", "creative"),
              ("final", "playful")],
    "amb": {"fire": ["kernel", "pressure"]},
    "sfx": [("open+0.5", "pop", 0.25), ("open+0.75", "pop", 0.25), ("open+1.0", "pop", 0.25), ("open+1.25", "pop", 0.25),
            ("open+1.5", "pop", 0.25), ("open+1.75", "pop", 0.25), ("open+2.0", "pop", 0.25), ("open+2.25", "pop", 0.25),
            ("kernel@L1", "crackle", 0.15), ("pressure+0.3", "riser_long", 0.12), ("pressure@L1+0.2", "riser", 0.12),
            ("burst+0.5", "impact", 0.3), ("burst+0.5", "pop", 0.45), ("burst@L1+0.2", "swell", 0.12),
            ("camera+0.3", "shutter", 0.25), ("camera+0.6", "shutter", 0.2), ("camera@L1+0.2", "glitch", 0.12),
            ("camera@L2+0.1", "whoosh_up", 0.15), ("jump+0.1", "pop", 0.25), ("jump+1.9", "pop", 0.25), ("jump+3.7", "pop", 0.25),
            ("final+0.2", "pop", 0.2), ("final+0.5", "pop", 0.2)],
    "bed": [("kernel", "camera")],
    "bpm": 112,
}
