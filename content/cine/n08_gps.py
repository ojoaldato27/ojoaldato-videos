"""N08 · ¿Cómo sabe el GPS dónde estás? (y qué pinta Einstein)."""
from neon import *

TITLE = "Como_sabe_el_GPS_donde_estas"
LINES = [
    "Tu móvil sabe dónde estás *aunque no tengas internet*.",
    "¿Cómo lo hace… y qué pinta *Einstein* en todo esto?",
    "Sobre tu cabeza hay *31 satélites* GPS, a unos 20.200 km de altura.",
    "Cada uno lleva un *reloj atómico* y emite sin parar una señal con la hora exacta.",
    "Tu móvil escucha esas señales… y mira cuánto han tardado en llegar.",
    "Como viajan a la velocidad de la luz, ese tiempo le dice *a qué distancia* está cada satélite.",
    "Con un satélite, sabes que estás en algún punto de una esfera enorme.",
    "Con dos y tres, las esferas se cruzan… y el punto se va acotando.",
    "Y con un *cuarto*, corrige el error del reloj de tu móvil.",
    "Pero en una milmillonésima de segundo, la luz recorre *30 centímetros*.",
    "Un error minúsculo en los relojes… y te sitúa en otra calle.",
    "Y aquí entra Einstein: allí arriba, los relojes adelantan *38 microsegundos* al día.",
    "La gravedad más débil los acelera… y la velocidad los frena un poco. Al final, adelantan.",
    "Si no se corrigiera, el GPS se desviaría unos *10 kilómetros cada día*.",
    "Así que cada vez que abres el mapa… estás usando *la relatividad*.",
]
SHOTS = [("open", 0, 1, 0.3), ("sats", 2, 3, 0.3), ("signal", 4, 5, 0.3), ("tri", 6, 8, 0.3), ("nano", 9, 10, 0.3),
         ("einstein", 11, 12, 0.3), ("drift", 13, 13, 0.3), ("final", 14, 14, 1.8)]
FOCUS = {"open": (540, 960, 1.12), "sats": (540, 900, 1.12), "signal": (540, 960, 1.12), "tri": (540, 960, 1.12),
         "nano": (540, 960, 1.12), "einstein": (540, 960, 1.12), "drift": (540, 960, 1.12), "final": (540, 960, 1.12)}
NOTIF = ("signal", 1.0)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon


def satellite(d, x, y, s=1.0, col=WH, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)

    def R_(px, py):
        return (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)
    body = [R_(-26, -26), R_(26, -26), R_(26, 26), R_(-26, 26), R_(-26, -26)]
    line(d, body, col, 5)
    for sg in (-1, 1):
        pan = [R_(sg * 34, -18), R_(sg * 110, -18), R_(sg * 110, 18), R_(sg * 34, 18), R_(sg * 34, -18)]
        line(d, pan, CY, 4)
        for k in range(1, 4):
            a, b = R_(sg * (34 + k * 19), -18), R_(sg * (34 + k * 19), 18)
            d.line([a, b], fill=CY, width=2)
        d.line([R_(sg * 26, 0), R_(sg * 34, 0)], fill=col, width=4)


def pin(d, x, y, col=MG, s=1.0):
    pts = [(x, y)] + [(x + math.cos(a) * 40 * s, y - 70 * s + math.sin(a) * 40 * s) for a in
                      [math.radians(v) for v in range(150, 391, 15)]] + [(x, y)]
    line(d, pts, col, 6)
    circle(d, x, y - 70 * s, 14 * s, col, 5)


def map_grid(d, t, col=(30, 50, 90), off=(0, 0)):
    for k in range(-2, 14):
        x = k * 100 + off[0] % 100
        d.line([(x, 500), (x + 60, 1420)], fill=col, width=3)
    for k in range(-2, 12):
        y = 500 + k * 90 + off[1] % 90
        d.line([(60, y), (1020, y + 40)], fill=col, width=3)


def phone_mini(d, x, y, col=WH, s=1.0):
    rrect(d, x - 110 * s, y - 200 * s, x + 110 * s, y + 200 * s, 30 * s, col, 6)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone_mini(d, 540, 960, WH, 1.9)
    map_grid(d, t, (30, 60, 110))
    pin(d, 540, 1000, MG, 1.4)
    if t > 0.8:
        cx, cy = 820, 640
        for j in range(3):
            d.arc([cx - 30 - j * 30, cy - 30 - j * 30, cx + 30 + j * 30, cy + 30 + j * 30], 225, 315, fill=DIM, width=6)
        line(d, [(cx - 110, cy - 110), (cx + 110, cy + 60)], RD, 8, ease(clamp((t - 0.8) / 0.4)))
    finish(img, lay)
    gtitle2(t, 0.2, "¿CÓMO SABE DÓNDE ESTÁS", "SIN INTERNET?", 250, 54, 100, WH, CY, hold=max(1.6, L[1][0] - 0.2))
    if t > L[1][0]:
        chip(t, L[1][0] + 0.3, "¿Y QUÉ PINTA EINSTEIN?", 540, 330, YE, 40)
    vignette(img, 150)


def sh_sats(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    d.arc([-600, 1250, 1680, 3000], 200, 340, fill=BL, width=8)
    for k in range(6):
        a = math.radians(236 + k * 14) + t * 0.02
        x = 540 + math.cos(a) * 1150
        y = 2125 + math.sin(a) * 1500
        satellite(d, x, y, 0.8, WH, a + math.pi / 2)
    a1 = L[1][0]
    if t > a1:
        cx, cy = 540, 1120
        circle(d, cx, cy, 120, YE, 6)
        for j in range(12):
            aa = math.radians(j * 30)
            d.line([(cx + math.cos(aa) * 100, cy + math.sin(aa) * 100), (cx + math.cos(aa) * 112, cy + math.sin(aa) * 112)], fill=YE, width=4)
        d.line([(cx, cy), (cx, cy - 80)], fill=YE, width=6)
        d.line([(cx, cy), (cx + math.cos(t * 6) * 90, cy + math.sin(t * 6) * 90)], fill=MG, width=3)
        for j in range(3):
            d.ellipse([cx - 40, cy - 14, cx + 40, cy + 14], outline=CY, width=2) if j == 0 else None
    finish(img, lay)
    gtitle(t, 0.3, "31 SATÉLITES", 300, 100, CY, hold=max(1.4, a1 - 0.5))
    if t < a1:
        chip(t, 1.0, "A 20.200 KM", 540, 460, WH, 40)
    else:
        gtitle(t, a1 + 0.2, "RELOJ ATÓMICO", 300, 92, YE)
    vignette(img, 150)


def sh_signal(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    sx, sy = 540, 600
    satellite(d, sx, sy, 1.0)
    phone_mini(d, 540, 1300, WH, 0.8)
    for k in range(5):
        u = (t * 0.5 + k / 5) % 1.0
        y = lerp(sy + 60, 1140, u)
        d.arc([540 - 60 - u * 80, y - 20, 540 + 60 + u * 80, y + 20], 20, 160, fill=tuple(int(c * (1 - u * 0.6)) for c in YE), width=5)
    label(d, 780, 600, "12:00:00,000000", 32, YE, F_MONO, "lm") if t < a1 else None
    if t > a1:
        label(d, 540, 950, "DISTANCIA = LUZ × TIEMPO", 40, CY, F_MONO)
        label(d, 540, 1020, "≈ 0,07 s", 44, WH, F_MONO)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "¿CUÁNTO TARDA?", 300, 96, YE, pop=False)
    else:
        gtitle(t, a1 + 0.2, "TIEMPO = DISTANCIA", 300, 84, CY, pop=False)
    vignette(img, 150)


def sh_tri(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    target = (560, 1020)
    sats = [(200, 640), (900, 700), (520, 1500)]
    cols = [CY, MG, GR]
    n = 1 if t < a1 else (2 if t < a1 + (L[1][1] - a1) * 0.5 else 3)
    for i in range(n):
        sx, sy = sats[i]
        r = math.hypot(target[0] - sx, target[1] - sy)
        t0 = 0.2 if i == 0 else (a1 if i == 1 else a1 + (L[1][1] - a1) * 0.5)
        k = ease(clamp((t - t0) / 0.8))
        circle(d, sx, sy, r * k, cols[i], 5)
        satellite(d, sx, sy, 0.5, cols[i])
    if n >= 3:
        pin(d, target[0], target[1], YE, 1.0)
    if t > a2:
        jitter = math.exp(-(t - a2) * 2) * 30
        for i in range(3):
            sx, sy = sats[i]
            r = math.hypot(target[0] - sx, target[1] - sy) + jitter * math.sin(t * 10 + i)
            circle(d, sx, sy, r, cols[i], 3)
        satellite(d, 880, 1400, 0.5, OR)
        line(d, [(880, 1400), (target[0] + 20, target[1] + 10)], OR, 4, ease(clamp((t - a2) / 0.6)))
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "1 SATÉLITE", 300, 96, CY, pop=False)
    elif t < a2:
        gtitle(t, a1 + 0.1, "2… 3 SATÉLITES", 300, 92, GR, pop=False)
    else:
        gtitle(t, a2 + 0.2, "EL 4.º AJUSTA EL RELOJ", 300, 80, OR, pop=False)
    vignette(img, 150)


def sh_nano(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    if t < a1:
        x0, x1, y = 160, 920, 960
        k = ease(clamp((t - 0.3) / 1.0))
        d.line([(x0, y), (x0 + (x1 - x0) * k, y)], fill=YE, width=10)
        for i in range(31):
            x = x0 + (x1 - x0) * i / 30
            if x <= x0 + (x1 - x0) * k:
                d.line([(x, y - 20 - (20 if i % 10 == 0 else 0)), (x, y)], fill=YE, width=3)
        label(d, 540, 1060, "30 cm", 60, YE, F_MONO)
        gtitle(t, 0.3, "1 NANOSEGUNDO", 300, 96, CY, pop=False)
    else:
        map_grid(d, t, (30, 60, 110))
        k = ease(clamp((t - a1 - 0.3) / 0.8))
        pin(d, lerp(480, 760, k), lerp(980, 760, k), MG, 1.3)
        circle(d, 480, 980, 30, DIM, 4)
        gtitle(t, a1 + 0.2, "OTRA CALLE", 300, 100, MG)
    finish(img, lay)
    vignette(img, 150)


def clock(d, x, y, r, col, a):
    circle(d, x, y, r, col, 6)
    for j in range(12):
        aa = math.radians(j * 30)
        d.line([(x + math.cos(aa) * r * 0.82, y + math.sin(aa) * r * 0.82), (x + math.cos(aa) * r * 0.94, y + math.sin(aa) * r * 0.94)], fill=col, width=4)
    d.line([(x, y), (x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)], fill=col, width=6)


def sh_einstein(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    clock(d, 300, 900, 170, CY, t * 2.0)
    clock(d, 780, 900, 170, YE, t * 2.0 * 1.25)
    label(d, 300, 1120, "TIERRA", 36, CY, F_POP)
    label(d, 780, 1120, "SATÉLITE", 36, YE, F_POP)
    if t > a1:
        k = ease(clamp((t - a1) / 0.5))
        label(d, 780, 1200, "+45 µs  GRAVEDAD", 34, GR, F_MONO)
        if t > a1 + (L[1][1] - a1) * 0.45:
            label(d, 780, 1260, "−7 µs  VELOCIDAD", 34, RD, F_MONO)
    finish(img, lay)
    gtitle(t, 0.3, "+38 µs AL DÍA", 300, 100, YE)
    vignette(img, 150)


def sh_drift(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    map_grid(d, t, (30, 60, 110), (-t * 60, -t * 30))
    q = ease(clamp((t - 0.3) / (T - 0.5)))
    circle(d, 400, 1100, 30, GR, 5)
    pin(d, lerp(400, 820, q), lerp(1100, 640, q), RD, 1.3)
    dashed(d, (400, 1100), (lerp(400, 820, q), lerp(1100, 640, q)), RD, 4, off=t * 40)
    finish(img, lay)
    gtitle(t, 0.3, "10 KM CADA DÍA", 300, 96, RD)
    vignette(img, 150)


def sh_final(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    phone_mini(d, 540, 1000, WH, 1.6)
    map_grid(d, t, (30, 60, 110))
    pin(d, 540, 1040, MG, 1.2)
    for k, (x, y) in enumerate(((180, 560), (900, 600), (160, 1360), (920, 1340))):
        satellite(d, x, y, 0.5, WH, t * 0.2 + k)
        dashed(d, (x, y), (540, 970), DIM, 3, off=t * 60)
    finish(img, lay)
    gtitle(t, 0.2, "RELATIVIDAD", 300, 100, YE)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "space"), ("sats", "space"), ("signal", "exp"), ("tri", "creative"), ("einstein", "drone"),
              ("drift", "tension"), ("final", "space")],
    "gains": {"exp": 0.7},
    "amb": {"space": ["sats", "signal", "tri"], "hum": ["open", "nano", "einstein", "final"]},
    "sfx": [("open+0.8", "glitch", 0.12), ("open@L1+0.3", "pop", 0.2), ("sats+0.3", "swell", 0.15), ("sats@L1+0.2", "tick", 0.2),
            ("sats@L1+0.7", "tick", 0.2), ("signal+0.2", "beep", 0.1), ("signal+1.2", "beep", 0.1), ("signal+2.2", "beep", 0.1),
            ("tri+0.2", "draw", 0.18), ("tri@L1", "draw", 0.18), ("tri@L1+1.4", "draw", 0.18), ("tri@L1+2.2", "ding", 0.1),
            ("tri@L2+0.2", "blip", 0.14), ("nano+0.3", "whoosh_up", 0.12), ("nano@L1+0.3", "glitch", 0.15),
            ("einstein+0.3", "tick", 0.15), ("einstein@L1", "blip", 0.12), ("drift+0.3", "riser_long", 0.12),
            ("final+0.2", "chime", 0.06)],
    "bed": [("signal", "einstein")],
    "bpm": 104,
}
