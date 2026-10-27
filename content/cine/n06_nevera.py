"""N06 · Tu nevera no fabrica frío (ciclo de refrigeración)."""
from neon import *

TITLE = "Tu_nevera_no_fabrica_frio"
LINES = [
    "Tu nevera *no fabrica frío*.",
    "Entonces… ¿cómo enfría la comida?",
    "Lo que hace es *sacar el calor* de dentro… y echarlo fuera.",
    "Por sus tubos circula un líquido especial: el *refrigerante*.",
    "Dentro de la nevera, ese líquido *hierve*… a temperaturas bajísimas.",
    "Y para hervir necesita calor: se lo *roba a tu comida*.",
    "Igual que el sudor te enfría al evaporarse.",
    "Ese gas viaja hasta el *compresor*: el zumbido que oyes.",
    "Al comprimirlo, el gas se calienta mucho.",
    "Luego pasa por los tubos de atrás… y suelta el calor en tu cocina.",
    "Por eso la parte de atrás está *caliente*.",
    "Al enfriarse, el gas vuelve a ser líquido.",
    "Cruza un tubo estrechísimo, pierde presión… y vuelve dentro, listo para *hervir* otra vez.",
    "Un ciclo que se repite *todo el día*.",
    "Por eso, si dejas la nevera abierta para refrescar la cocina… *la calientas*.",
    "Tu nevera es, en realidad, *una bomba de calor*.",
]
SHOTS = [("open", 0, 1, 0.3), ("move", 2, 3, 0.3), ("boil", 4, 6, 0.3), ("compress", 7, 8, 0.3), ("back", 9, 11, 0.3),
         ("valve", 12, 13, 0.3), ("door", 14, 14, 0.3), ("final", 15, 15, 1.8)]
FOCUS = {"open": (540, 960, 1.12), "move": (540, 960, 1.12), "boil": (540, 960, 1.15), "compress": (540, 960, 1.12),
         "back": (540, 960, 1.12), "valve": (540, 960, 1.12), "door": (540, 960, 1.12), "final": (540, 960, 1.12)}
NOTIF = ("boil", 1.0)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon

FX0, FY0, FX1, FY1 = 300, 520, 700, 1380


def fridge(d, col=CY, k=1.0, door_open=0.0):
    rrect(d, FX0, FY0, FX1, FY1, 30, col, 7, k)
    d.line([(FX0 + 10, 820), (FX1 - 10, 820)], fill=col, width=5)
    d.line([(FX0 + 40, 600), (FX0 + 40, 740)], fill=col, width=8)
    d.line([(FX0 + 40, 900), (FX0 + 40, 1100)], fill=col, width=8)
    if door_open > 0:
        x = FX0 - 260 * door_open
        line(d, [(FX0, FY0), (x, FY0 + 60), (x, FY1 - 60), (FX0, FY1)], col, 6)


def snow(d, x, y, r, col):
    for a in range(3):
        aa = math.radians(a * 60)
        d.line([(x - math.cos(aa) * r, y - math.sin(aa) * r), (x + math.cos(aa) * r, y + math.sin(aa) * r)], fill=col, width=6)


def heat_dots(d, t, src, dst, n=10, col=OR, seed=1):
    rr = random.Random(seed)
    for k in range(n):
        u = (t * 0.5 + k / n) % 1.0
        x = lerp(src[0], dst[0], u) + math.sin(u * 8 + k) * 30
        y = lerp(src[1], dst[1], u) + rr.uniform(-60, 60)
        dot(d, x, y, 8 * (1 - u * 0.5), col)


LOOP = [(380, 600), (620, 600), (620, 680), (380, 680), (380, 760), (620, 760), (780, 760), (780, 1300), (880, 1300),
        (880, 1220), (980, 1220), (980, 560), (1040, 560), (1040, 520), (300, 520), (300, 600), (380, 600)]


def loop_flow(d, t, n=40, k=1.0):
    pts = partial(LOOP, k)
    line(d, pts, DIM, 5)
    if k < 0.99:
        return
    label(d, 500, 720, "EVAPORADOR", 24, BL, F_MONO)
    rrect(d, 840, 1260, 1000, 1340, 16, CY, 4)
    label(d, 920, 1380, "COMPRESOR", 24, CY, F_MONO)
    label(d, 1010, 900, "TUBOS DE ATRÁS", 24, OR, F_MONO, "rm")
    for i in range(n):
        s_ = ((i / n) + t * 0.08) % 1.0
        p = partial(LOOP, s_)[-1]
        hot = 0.32 < s_ < 0.75
        dot(d, p[0], p[1], 9, OR if hot else BL)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    fridge(d, CY, ease(clamp(t / 1.0)))
    snow(d, 500, 1000, 70, BL)
    k = ease(clamp((t - 1.0) / 0.5))
    if k > 0:
        line(d, [(400, 900), (600, 1100)], RD, 12, k)
    finish(img, lay)
    gtitle2(t, 0.2, "TU NEVERA", "NO FABRICA FRÍO", 250, 64, 96, WH, CY, hold=max(1.6, L[1][0] + 0.8))
    vignette(img, 150)


def sh_move(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    fridge(d, CY)
    if t < a1:
        heat_dots(d, t, (500, 1000), (980, 900), 14, OR)
        arrow(d, (720, 900), (960, 900), OR, 8, ease(clamp(t / 0.8)))
        gtitle(t, 0.3, "SACA EL CALOR", 300, 96, OR)
    else:
        loop_flow(d, t, 40, ease(clamp((t - a1) / 1.4)))
        gtitle(t, a1 + 0.2, "REFRIGERANTE", 300, 96, BL)
    finish(img, lay)
    vignette(img, 150)


def sh_boil(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    if t < a2:
        rrect(d, 160, 560, 920, 1360, 30, CY, 5)
        pts = []
        for k in range(9):
            y = 640 + k * 70
            pts += [(220, y), (860, y)] if k % 2 == 0 else [(860, y), (220, y)]
        line(d, pts, BL, 8)
        rr = random.Random(4)
        for k in range(26):
            u = (t * 0.7 + rr.random()) % 1.0
            x = rr.uniform(240, 840)
            y = 1200 - u * 560
            circle(d, x, y, 6 + 10 * u, tuple(int(c * (1 - u * 0.5)) for c in BL), 3)
        if t > a1:
            rect(d, 360, 1200, 720, 1330, WH, 5)
            label(d, 540, 1265, "COMIDA", 34, WH, F_MONO)
            heat_dots(d, t, (540, 1200), (540, 700), 12, OR, 3)
        chip(t, 0.3, "HIERVE A ≈ -30 °C", 540, 330, BL, 40)
        if t > a1:
            gtitle(t, a1 + 0.2, "ROBA CALOR", 400, 90, OR, pop=False)
    else:
        cx, cy = 540, 960
        line(d, [(200, 1200), (400, 1100), (700, 1120), (900, 1220)], WH, 6)
        for k in range(6):
            u = ((t - a2) * 0.6 + k / 6) % 1.0
            x = 300 + k * 100
            y = 1110 - u * 400
            circle(d, x, y, 18 * (1 - u * 0.5), tuple(int(c * (1 - u)) for c in BL), 4)
            dot(d, x, 1150, 14, BL) if u < 0.1 else None
        gtitle(t, a2 + 0.2, "COMO EL SUDOR", 300, 96, BL, pop=False)
    finish(img, lay)
    vignette(img, 150)


def sh_compress(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    rect(d, 340, 560, 740, 1300, CY, 6)
    stroke = 0.5 + 0.5 * math.sin(t * 5)
    py = lerp(1180, 820, stroke if t > a1 else 0.2)
    d.line([(350, py), (730, py)], fill=WH, width=12)
    d.line([(540, py), (540, 1420)], fill=WH, width=10)
    rr = random.Random(5)
    hot = clamp((t - a1) / 1.5)
    for k in range(30):
        x = rr.uniform(370, 710) + math.sin(t * (3 + hot * 9) + k) * (6 + 14 * hot)
        y = rr.uniform(580, py - 20)
        col = tuple(int(lerp(a, b, hot)) for a, b in zip(BL, OR))
        dot(d, x, y, 9, col)
    hum = 0.5 + 0.5 * math.sin(t * 40)
    for j in range(3):
        d.arc([780, 820 - j * 40, 860 + j * 30, 980 + j * 40], -60, 60, fill=tuple(int(c * hum) for c in DIM), width=4)
    finish(img, lay)
    gtitle(t, 0.3, "COMPRESOR", 300, 100, CY)
    if t > a1:
        chip(t, a1 + 0.3, "+ PRESIÓN = + CALOR", 540, 470, OR, 40)
    vignette(img, 150)


def sh_back(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    rect(d, 220, 520, 860, 1380, DIM, 5)
    pts = []
    for k in range(11):
        y = 600 + k * 70
        pts += [(280, y), (800, y)] if k % 2 == 0 else [(800, y), (280, y)]
    glow_k = 1.0 if t < a2 else 1 - clamp((t - a2) / 1.4) * 0.6
    col = tuple(int(lerp(b, a, glow_k)) for a, b in zip(OR, BL))
    line(d, pts, col, 9)
    for k in range(8):
        u = (t * 0.6 + k / 8) % 1.0
        x = 900 + u * 160
        y = 640 + k * 90
        d.arc([x - 30, y - 30, x + 30, y + 30], -60, 60, fill=tuple(int(c * (1 - u)) for c in OR), width=5)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "SUELTA EL CALOR", 300, 90, OR, pop=False)
    elif t < a2:
        gtitle(t, a1 + 0.2, "¡ATRÁS QUEMA!", 300, 100, RD)
    else:
        chip(t, a2 + 0.2, "VUELVE A SER LÍQUIDO", 540, 330, BL, 40)
    vignette(img, 150)


def sh_valve(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    if t < a1:
        d.line([(80, 900), (440, 900)], fill=CY, width=60)
        d.line([(80, 900), (440, 900)], fill=(4, 8, 18), width=46)
        d.line([(440, 900), (640, 900)], fill=CY, width=14)
        d.line([(640, 900), (1000, 900)], fill=CY, width=80)
        d.line([(640, 900), (1000, 900)], fill=(4, 8, 18), width=66)
        for k in range(14):
            u = (t * 0.6 + k / 14) % 1.0
            x = 90 + u * 900
            if x < 440:
                y = 900 + math.sin(k * 7) * 12
                dot(d, x, y, 9, OR)
            elif x < 640:
                dot(d, x, 900, 6, YE)
            else:
                y = 900 + math.sin(k * 3) * 28
                dot(d, x, y, 9, BL)
        label(d, 540, 1000, "TUBO CAPILAR", 34, CY, F_MONO)
        gtitle(t, 0.3, "PIERDE PRESIÓN", 300, 90, BL, pop=False)
    else:
        fridge(d, CY)
        loop_flow(d, t, 44)
        gtitle(t, a1 + 0.2, "TODO EL DÍA", 300, 100, CY, pop=False)
    finish(img, lay)
    vignette(img, 150)


def sh_door(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    k = ease(clamp((t - 0.3) / 0.8))
    fridge(d, CY, 1.0, k)
    rr = random.Random(2)
    for j in range(10):
        u = (t * 0.5 + j / 10) % 1.0
        dot(d, FX0 - 40 - u * 200, 700 + rr.uniform(0, 600), 8, BL)
    for j in range(16):
        u = (t * 0.6 + j / 16) % 1.0
        x = FX1 + 40 + u * 280
        y = 600 + rr.uniform(0, 760)
        d.arc([x - 26, y - 26, x + 26, y + 26], -60, 60, fill=tuple(int(c * (1 - u)) for c in OR), width=5)
    cx = 940
    rrect(d, cx - 30, 560, cx + 30, 1200, 30, WH, 5)
    lvl = lerp(1100, 760, clamp((t - 0.8) / 2.0))
    d.rectangle([cx - 14, lvl, cx + 14, 1180], fill=RD)
    dot(d, cx, 1230, 46, RD)
    finish(img, lay)
    gtitle(t, 0.6, "LA COCINA SE CALIENTA", 300, 76, RD, pop=False)
    vignette(img, 150)


def sh_final(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    fridge(d, CY)
    loop_flow(d, t, 44)
    finish(img, lay)
    gtitle(t, 0.2, "BOMBA DE CALOR", 300, 100, OR)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "space"), ("move", "creative"), ("compress", "exp"), ("back", "creative"), ("door", "playful"),
              ("final", "space")],
    "gains": {"exp": 0.7},
    "amb": {"hum": ["open", "move", "boil", "compress", "back", "valve", "door", "final"]},
    "sfx": [("open+0.2", "draw", 0.18), ("open+1.0", "glitch", 0.15), ("move+0.2", "whoosh", 0.12), ("move@L1", "draw", 0.18),
            ("boil+0.3", "crackle", 0.12), ("boil@L1+0.2", "blip_down", 0.12), ("boil@L2+0.2", "pop", 0.15),
            ("compress+0.2", "hum_on", 0.2), ("compress@L1", "riser", 0.12), ("back+0.3", "swell", 0.15),
            ("back@L1+0.2", "impact", 0.25), ("valve+0.3", "whoosh", 0.14), ("valve@L1+0.2", "chime", 0.06),
            ("door+0.3", "whoosh", 0.15), ("door+0.8", "riser", 0.12), ("final+0.2", "ding", 0.08)],
    "bed": [("move", "door")],
    "bpm": 104,
}
