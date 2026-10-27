"""N02 · ¿Cómo funciona un microondas? (estilo neón explicativo)."""
from neon import *

TITLE = "Como_funciona_un_microondas"
LINES = [
    "Un microondas calienta la comida sin fuego y sin resistencias al rojo.",
    "¿Cómo lo hace… y para qué sirve *la rejilla* de la puerta?",
    "Todo empieza aquí dentro: en el *magnetrón*.",
    "Unos electrones giran atrapados por un imán…",
    "…y al pasar por estas cavidades, generan *microondas*.",
    "Son ondas de radio, como las del wifi, que oscilan *2.450 millones de veces por segundo*.",
    "Una guía las conduce hasta la comida.",
    "Y la comida está llena de *agua*.",
    "Cada molécula de agua tiene un lado negativo… y otro positivo.",
    "Las microondas tiran de ellas a un lado y a otro, sin parar.",
    "Giran, chocan entre sí… y ese roce se convierte en *calor*.",
    "Por eso el hielo cuesta tanto: sus moléculas están atrapadas y casi *no pueden girar*.",
    "Y no calienta de dentro hacia fuera: las ondas solo entran *un par de centímetros*.",
    "Dentro hay zonas frías y calientes… por eso el plato *gira*.",
    "¿Y la rejilla?",
    "Sus agujeros miden alrededor de *un milímetro*.",
    "Pero las microondas miden *12 centímetros*: no caben.",
    "La luz es mucho más pequeña: pasa, y puedes ver tu comida.",
    "Se inventó en los años 40, cuando a Percy Spencer se le *derritió una chocolatina* junto a un magnetrón.",
    "Un invento nacido de *un accidente*.",
]
SHOTS = [("open", 0, 1, 0.3), ("magnetron", 2, 4, 0.3), ("wave", 5, 6, 0.3), ("water", 7, 8, 0.3), ("spin", 9, 10, 0.3),
         ("ice", 11, 11, 0.3), ("depth", 12, 12, 0.3), ("hotspots", 13, 13, 0.3), ("mesh", 14, 17, 0.3), ("spencer", 18, 19, 1.8)]
FOCUS = {"open": (520, 900, 1.15), "magnetron": (540, 900, 1.15), "wave": (540, 900, 1.12), "water": (540, 900, 1.15),
         "spin": (540, 900, 1.12), "depth": (540, 900, 1.12), "mesh": (540, 880, 1.15), "spencer": (540, 900, 1.12)}
NOTIF = ("wave", 1.0)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon


# ------------------------------------------------------------------ dibujos de línea
def oven(d, t, k=1.0, col=CY, glow_in=0.0, plate_rot=0.0, mesh=True):
    x0, y0, x1, y1 = 120, 640, 960, 1200
    rrect(d, x0, y0, x1, y1, 30, col, 7, k)
    if k < 0.5:
        return
    kk = clamp((k - 0.5) / 0.5)
    rrect(d, 160, 680, 720, 1160, 18, col, 5, kk)
    if mesh and kk > 0.9:
        for yy in range(710, 1140, 26):
            for xx in range(190, 700, 26):
                d.point((xx, yy), fill=tuple(int(c * 0.55) for c in col))
    if glow_in > 0:
        g = tuple(int(c * glow_in) for c in (255, 190, 90))
        d.ellipse([300, 1040, 580, 1110], outline=g, width=5)
    d.ellipse([280, 1060, 600, 1120], outline=YE, width=5)
    for j in range(6):
        a = plate_rot + j * math.pi / 3
        d.point((440 + math.cos(a) * 130, 1090 + math.sin(a) * 20), fill=YE)
    rect(d, 380, 940, 500, 1060, WH, 5, kk)
    d.arc([490, 970, 540, 1030], -90, 90, fill=WH, width=5)
    rrect(d, 760, 700, 920, 790, 12, GR, 4, kk)
    label(d, 840, 745, "0:30", 40, GR, F_MONO)
    for yy in (880, 1000):
        circle(d, 840, yy, 44, col, 5, kk)
        a = t * 2 + yy
        d.line([(840, yy), (840 + math.cos(a) * 30, yy + math.sin(a) * 30)], fill=col, width=5)


def magnetron(d, t, cx, cy, R_=300, k=1.0, electrons=True):
    circle(d, cx, cy, R_, CY, 8, k)
    circle(d, cx, cy, R_ * 0.55, CY, 6, k)
    n = 8
    for i in range(n):
        a = i / n * 2 * math.pi
        px, py = cx + math.cos(a) * R_ * 0.78, cy + math.sin(a) * R_ * 0.78
        circle(d, px, py, R_ * 0.12, CY, 5, k)
        d.line([(cx + math.cos(a) * R_ * 0.55, cy + math.sin(a) * R_ * 0.55), (cx + math.cos(a) * R_ * 0.66, cy + math.sin(a) * R_ * 0.66)],
               fill=CY, width=8)
    circle(d, cx, cy, R_ * 0.12, OR, 6, k)
    if electrons and k > 0.9:
        rr = random.Random(3)
        for j in range(70):
            spoke = j % 4
            u = (rr.random() + t * 0.4) % 1.0
            rad = R_ * (0.14 + 0.38 * u)
            a = t * 3.0 + spoke * math.pi / 2 + u * 1.6 + rr.uniform(-0.12, 0.12)
            dot(d, cx + math.cos(a) * rad, cy + math.sin(a) * rad, 5, YE)


def molecules(d, t, n, area, seed, mode="random", field=0.0, heat=0.0, s=1.0):
    rr = random.Random(seed)
    x0, y0, x1, y1 = area
    for i in range(n):
        x, y = rr.uniform(x0, x1), rr.uniform(y0, y1)
        base = rr.uniform(0, 2 * math.pi)
        if mode == "random":
            ang = base + math.sin(t * 0.8 + i) * 0.3
        elif mode == "field":
            target = 0 if field >= 0 else math.pi
            ang = target + math.sin(i) * 0.25 + heat * math.sin(t * 20 + i) * 0.4
            x += heat * math.sin(t * 17 + i * 3) * 10
            y += heat * math.cos(t * 13 + i * 5) * 10
        else:
            ang = base + math.sin(t * 25 + i) * 0.06
        water(d, x, y, s, ang)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    k = ease(clamp(t / 1.4))
    hum = 0.6 + 0.4 * math.sin(t * 6) ** 2
    oven(d, t, k, CY, hum, t * 1.5)
    if t > 1.0:
        for j in range(4):
            sine(d, 200, 690, 760 + j * 90, 16, 120, t * 10 + j, tuple(int(c * 0.6) for c in YE), 3)
    a1 = L[1][0]
    if t > a1:
        kk = ease(clamp((t - a1 - 0.4) / 0.6))
        circle(d, 440, 900, 200 * kk, MG, 6)
        label(d, 440, 900 + 240, "REJILLA", 40, MG, F_POP) if kk > 0.9 else None
    finish(img, lay)
    gtitle2(t, 0.2, "¿CÓMO FUNCIONA", "UN MICROONDAS?", 260, 60, 100, WH, CY, hold=max(1.6, L[1][0] - 0.2))
    vignette(img, 160)


def sh_magnetron(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    k = ease(clamp(t / 1.2))
    magnetron(d, t, 540, 920, 300, k, t > L[1][0])
    label(d, 540, 520, "N", 60, RD, F_POP)
    label(d, 540, 1320, "S", 60, BL, F_POP)
    a2 = L[2][0]
    if t > a2:
        for j in range(3):
            u = ((t - a2) * 0.6 + j / 3) % 1.0
            r = 320 + u * 300
            d.arc([540 - r, 920 - r, 540 + r, 920 + r], -30, 30, fill=tuple(int(c * (1 - u)) for c in YE), width=6)
    finish(img, lay)
    gtitle(t, 0.3, "MAGNETRÓN", 300, 100, CY, hold=max(1.2, L[1][0] - 0.6))
    if L[1][0] <= t < a2:
        chip(t, L[1][0] + 0.2, "ELECTRONES + IMÁN", 540, 330, YE, 40)
    if t >= a2:
        gtitle(t, a2 + 0.2, "MICROONDAS", 300, 100, YE)
    vignette(img, 150)


def sh_wave(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    if t < a1:
        sine(d, 60, 1020, 860, 140, 340, -t * 8, YE, 8, ease(clamp(t / 1.0)))
        dashed(d, (60, 860), (1020, 860), DIM, 3, off=t * 30)
        if t > 1.4:
            cx, cy = 540, 1200
            for j in range(3):
                d.arc([cx - 50 - j * 50, cy - 50 - j * 50, cx + 50 + j * 50, cy + 50 + j * 50], 225, 315, fill=CY, width=8)
            dot(d, cx, cy, 14, CY)
            label(d, cx, cy + 80, "WIFI · 2,4 GHz", 40, CY, F_MONO)
    else:
        rrect(d, 120, 760, 960, 1000, 20, CY, 6)
        x = 140 + ((t - a1) * 300) % 760
        sine(d, 140, min(940, x), 880, 70, 180, -t * 10, YE, 7)
        rect(d, 960, 640, 1060, 1120, CY, 6)
        label(d, 540, 1080, "GUÍA DE ONDAS", 38, CY, F_MONO)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.4, "2.450.000.000", 290, 96, YE, pop=False)
        chip(t, 0.9, "VECES POR SEGUNDO", 540, 470, WH, 36)
    vignette(img, 150)


def sh_water(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    if t < a1:
        d.arc([240, 900, 840, 1260], 0, 180, fill=CY, width=8)
        d.line([(240, 1080), (840, 1080)], fill=CY, width=8)
        molecules(d, t, 14, (300, 1000, 780, 1180), 4, "random", s=0.7)
        circle(d, 540, 1100, 260 * ease(clamp((t - 0.8) / 0.6)), DIM, 3)
        gtitle(t, 0.3, "AGUA", 300, 120, MG)
    else:
        cx, cy = 540, 920
        water(d, cx, cy, 3.2, math.radians(90))
        k = ease(clamp((t - a1 - 0.3) / 0.5))
        if k > 0:
            label(d, cx, cy - 190, "δ–", 64, MG, F_POP)
            label(d, cx, cy + 300, "δ+    δ+", 64, WH, F_POP)
        gtitle(t, a1 + 0.1, "UN IMÁN DIMINUTO", 300, 84, WH, pop=False)
    finish(img, lay)
    vignette(img, 150)


def sh_spin(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    period = 0.9
    fsign = 1 if (t % period) < period / 2 else -1
    heat = clamp((t - a1) / 2.0)
    molecules(d, t, 14, (160, 640, 920, 1240), 9, "field", fsign, heat, 0.85)
    ax = 540
    arrow(d, (ax - 300 * fsign, 520), (ax + 300 * fsign, 520), YE, 8, 1.0, 34)
    label(d, ax, 470, "CAMPO", 32, YE, F_MONO)
    if heat > 0:
        for j in range(5):
            u = ((t * 0.5) + j / 5) % 1.0
            x = 220 + j * 160
            pts = [(x + math.sin(yy / 30 + t * 4 + j) * 14, yy) for yy in range(int(1300 - u * 300), int(1360 - u * 300), 6)]
            line(d, pts, tuple(int(c * heat) for c in OR), 5)
    finish(img, lay)
    if heat > 0:
        overlay(img, (255, 110, 30), 0.12 * heat)
        gtitle(t, a1 + 0.4, "ROCE = CALOR", 290, 100, OR)
    else:
        chip(t, 0.3, "A CÁMARA SUPERLENTA", 540, 330, WH, 36)
    vignette(img, 150)


def sh_ice(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    cx, cy, sp = 540, 920, 150
    for r in range(-2, 3):
        for c in range(-2, 3):
            x = cx + c * sp + (sp / 2 if r % 2 else 0)
            y = cy + r * sp * 0.87
            if abs(x - cx) < 420:
                water(d, x, y, 0.8, math.radians(90 + (r + c) * 60 % 180) + math.sin(t * 30 + r + c) * 0.04, BL, WH)
                for a in (0, 60, 120):
                    aa = math.radians(a)
                    d.line([(x + math.cos(aa) * 60, y + math.sin(aa) * 60), (x + math.cos(aa) * 90, y + math.sin(aa) * 90)], fill=DIM, width=3)
    fsign = 1 if (t % 0.9) < 0.45 else -1
    arrow(d, (540 - 300 * fsign, 520), (540 + 300 * fsign, 520), YE, 8, 1.0, 34)
    finish(img, lay)
    gtitle(t, 0.3, "HIELO", 290, 110, BL)
    chip(t, 1.2, "CASI NO GIRAN", 540, 1360, WH, 40)
    vignette(img, 150)


def sh_depth(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    x0, y0, x1, y1 = 260, 640, 820, 1240
    rrect(d, x0, y0, x1, y1, 30, CY, 6)
    pen = 90
    for side in (-1, 1):
        for j in range(5):
            y = y0 + 60 + j * 110
            pts = []
            for k_ in range(0, 260, 6):
                xx = (x0 - 160 + k_) if side < 0 else (x1 + 160 - k_)
                inside = (xx > x0) if side < 0 else (xx < x1)
                depth = (xx - x0) if side < 0 else (x1 - xx)
                amp = 26 * (math.exp(-max(0, depth) / pen) if inside else 1.0)
                pts.append((xx, y + amp * math.sin(k_ / 18 - t * 9)))
            line(d, pts, YE, 4)
    q = clamp((t - 1.2) / 2.0)
    for j in range(8):
        w_ = 60 + j * 30 * q
        col = tuple(int(c * (1 - j / 8) * 0.8) for c in OR)
        d.rectangle([x0 + 10, y0 + 10, x0 + 10 + w_ * 0.4, y1 - 10], outline=col, width=3)
        d.rectangle([x1 - 10 - w_ * 0.4, y0 + 10, x1 - 10, y1 - 10], outline=col, width=3)
    d.line([(x0, y1 + 60), (x0 + pen, y1 + 60)], fill=WH, width=5)
    label(d, x0 + pen / 2, y1 + 110, "~1,4 cm", 40, WH, F_MONO)
    finish(img, lay)
    gtitle(t, 0.3, "DE FUERA A DENTRO", 300, 84, OR, pop=False)
    vignette(img, 150)


def sh_hotspots(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    x0, y0, s_ = 160, 560, 760
    rect(d, x0, y0, x0 + s_, y0 + s_, CY, 6)
    for i in range(6):
        for j in range(6):
            v = abs(math.cos((i + 0.5) / 6 * math.pi * 2) * math.cos((j + 0.5) / 6 * math.pi * 2))
            x, y = x0 + (i + 0.5) * s_ / 6, y0 + (j + 0.5) * s_ / 6
            r = 20 + 40 * v
            col = OR if v > 0.5 else BL
            circle(d, x, y, r, tuple(int(c * (0.4 + 0.6 * v)) for c in col), 4)
    cx, cy = x0 + s_ / 2, y0 + s_ / 2
    circle(d, cx, cy, 300, YE, 5)
    a = t * 1.4
    fx_, fy = cx + math.cos(a) * 200, cy + math.sin(a) * 200
    rect(d, fx_ - 50, fy - 50, fx_ + 50, fy + 50, WH, 5)
    arc_pts = [(cx + math.cos(a - u) * 320, cy + math.sin(a - u) * 320) for u in [k / 20 * 1.2 for k in range(21)]]
    line(d, arc_pts, YE, 4)
    finish(img, lay)
    gtitle(t, 0.3, "EL PLATO GIRA", 300, 96, YE, pop=False)
    vignette(img, 150)


def sh_mesh(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2, a3 = L[1][0], L[2][0], L[3][0]
    gx = 640
    for yy in range(500, 1400, 60):
        for xx in (gx,):
            d.line([(xx, yy + 18), (xx, yy + 60)], fill=CY, width=10)
    d.line([(gx, 480), (gx, 1400)], fill=tuple(int(c * 0.4) for c in CY), width=2)
    if t >= a1:
        k = ease(clamp((t - a1) / 0.4))
        d.line([(gx + 40, 560), (gx + 40, 578)], fill=WH, width=4)
        label(d, gx + 140, 569, "1 mm", 34, WH, F_MONO)
    if t >= a2:
        u = ((t - a2) * 0.5) % 1.0
        xw = lerp(60, gx - 20, min(1, u * 2)) if u < 0.5 else lerp(gx - 20, 60, (u - 0.5) * 2)
        sine(d, 60, xw, 900, 120, 360, -t * 6, YE, 9)
        d.line([(60, 1080), (420, 1080)], fill=YE, width=5)
        label(d, 240, 1130, "12 cm", 40, YE, F_MONO)
    if t >= a3:
        for j, y in enumerate((620, 700, 780, 1220, 1300)):
            x_end = 60 + ((t - a3) * 500 + j * 90) % 960
            sine(d, max(60, x_end - 200), x_end, y, 6, 14, -t * 20, WH, 3)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.1, "¿Y LA REJILLA?", 300, 96, MG)
    elif t < a2:
        gtitle(t, a1 + 0.2, "AGUJEROS DE 1 MM", 300, 84, WH, pop=False)
    elif t < a3:
        gtitle(t, a2 + 0.2, "ONDA DE 12 CM", 300, 90, YE, pop=False)
        chip(t, a2 + 0.8, "NO CABE", 540, 470, RD, 40)
    else:
        gtitle(t, a3 + 0.2, "LA LUZ SÍ PASA", 300, 90, WH, pop=False)
    vignette(img, 150)


def sh_spencer(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    magnetron(d, t, 360, 860, 200, 1.0, True)
    melt = clamp((t - 1.2) / 2.5)
    x0, y0 = 640, 760
    rrect(d, x0, y0, x0 + 300, y0 + 180, 14, OR, 6)
    for i in range(1, 4):
        d.line([(x0 + i * 75, y0 + 10), (x0 + i * 75, y0 + 170)], fill=tuple(int(c * 0.6) for c in OR), width=3)
    for j, dx in enumerate((40, 120, 210, 270)):
        ln = melt * (80 + j * 30)
        if ln > 4:
            line(d, [(x0 + dx, y0 + 180), (x0 + dx + 4, y0 + 180 + ln)], OR, 10)
            dot(d, x0 + dx + 4, y0 + 180 + ln, 10, OR)
    a1 = L[1][0]
    if t > a1:
        k = ease(clamp((t - a1) / 0.8))
        oven(d, t, k, CY, 0.8, t)
    finish(img, lay)
    if t < a1:
        chip(t, 0.4, "PERCY SPENCER · AÑOS 40", 540, 330, YE, 38)
    else:
        gtitle(t, a1 + 0.2, "UN ACCIDENTE", 290, 100, YE)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "space"), ("magnetron", "exp"), ("water", "creative"), ("ice", "space"), ("mesh", "creative"),
              ("spencer", "premium")],
    "gains": {"exp": 0.7},
    "amb": {"hum": ["open", "magnetron", "wave", "spin", "hotspots", "spencer"]},
    "sfx": [("open+0.2", "hum_on", 0.2), ("open+0.4", "draw", 0.2), ("open@L1+0.4", "blip", 0.15),
            ("magnetron+0.2", "draw", 0.2), ("magnetron@L1", "zap", 0.12), ("magnetron@L2+0.2", "whoosh_up", 0.14),
            ("wave+0.2", "draw", 0.18), ("wave+1.4", "blip", 0.12), ("wave@L1", "whoosh", 0.12),
            ("water+0.3", "pop", 0.2), ("water@L1+0.3", "blip", 0.12), ("water@L1+0.6", "blip_down", 0.12),
            ("spin+0.3", "click", 0.3), ("spin+0.75", "click", 0.3), ("spin+1.2", "click", 0.3), ("spin@L1+0.4", "swell", 0.18),
            ("ice+0.3", "glitch", 0.12), ("depth+0.3", "whoosh", 0.12), ("hotspots+0.3", "blip", 0.12),
            ("mesh", "pop", 0.2), ("mesh@L1+0.2", "tick", 0.2), ("mesh@L2+0.2", "thud", 0.25), ("mesh@L3+0.2", "chime", 0.06),
            ("spencer+1.2", "swell", 0.15), ("spencer@L1+0.2", "ding", 0.1)],
    "bed": [("magnetron", "ice"), ("mesh", "spencer")],
    "bpm": 104,
}
