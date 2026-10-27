"""T01 · ¿Qué cambia de ir a 100 o a 140? (estilo Titanic, ilustración detallada)."""
from objs import *

TITLE = "Que_cambia_de_ir_a_100_o_a_140"
LINES = [
    "¿Qué cambia *de verdad* entre ir a 100 o a 140 por la autopista?",
    "Quédate, que al final te digo *cuánto tiempo ganas*.",
    "Primero, lo fácil: a 100 recorres *28 metros* cada segundo.",
    "A 140, casi *39*.",
    "Ahora imagina que algo *se cruza delante*.",
    "Tardas casi un segundo en reaccionar… y el coche sigue *a toda velocidad*.",
    "*Truco del RACE*: quita la última cifra y multiplícala por sí misma.",
    "A 100: diez por diez, *100 metros* de distancia de seguridad.",
    "A 140: catorce por catorce, *196 metros*.",
    "¿Casi el doble, si solo vas un *40 % más rápido*?",
    "Sí: la energía crece *con el cuadrado* de la velocidad.",
    "A 140 llevas casi *el doble de energía*.",
    "Chocar a 100 es como caer desde *un piso 13*.",
    "A 140, como caer desde *un piso 26*.",
    "Y *el aire te frena* más: también crece con el cuadrado.",
    "Por eso gastas más: solo de 120 a 140, entre un *20 y un 25 %*.",
    "Y en una autovía de 120, ir a 140 son *100 euros* de multa.",
    "Entonces… *¿cuánto tiempo ganas?*",
    "En un viaje de 100 kilómetros: *unos 17 minutos*.",
    "*17 minutos*… por casi el doble de frenada y de golpe.",
    "Tú decides si *merece la pena*.",
]
SHOTS = [("open", 0, 1, 0.3), ("meters", 2, 3, 0.3), ("react", 4, 5, 0.3), ("rule", 6, 8, 0.3), ("energy", 9, 11, 0.3),
         ("fall", 12, 13, 0.4), ("air", 14, 15, 0.3), ("fine", 16, 16, 0.3), ("time", 17, 18, 0.3), ("verdict", 19, 20, 1.8)]
FOCUS = {"open": (540, 1100), "meters": (500, 1050), "react": (640, 1050), "rule": (540, 1050), "energy": (600, 1050),
         "fall": (540, 1000), "air": (540, 1000), "fine": (540, 900), "time": (540, 1000), "verdict": (540, 1000)}
NOTIF = ("react", 1.2)
HYPE = {"line": 0, "text": ['¿QUÉ CAMBIA', 'DE IR A 100 O A 140?'], "delay": [0, 0.75]}
NOTIF_TEXT = "Suscríbete para más cosas que no sabías"

RED = (196, 30, 36)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    highway_night(img, t, 1.3, 760)
    bob = math.sin(t * 9) * 2
    paste(img, car_rear(RED, 0.0), 540, 1200 + bob, 1.05)
    paste(img, glow(300, (255, 40, 40), 0.25), 540, 1200)
    lower_third(img, t, L[1][0] + 0.2, "AL FINAL", "CUÁNTO TIEMPO GANAS DE VERDAD", 300, max(1.6, T - L[1][0] - 0.6))
    vignette(img, 200)


def sh_meters(img, t, T, L):
    a1 = L[1][0]
    sp = 1.0 if t < a1 else 1.4
    hz = 900
    highway_day(img, t, hz, sp)
    ry = hz + 300
    d = ImageDraw.Draw(img, "RGBA")
    m = 28 if t < a1 else 39
    k = ease(clamp(((t if t < a1 else t - a1) - 0.2) / 0.8))
    x0 = 470
    px = 14
    xe = x0 + m * px * k
    d.rounded_rectangle([x0, ry - 36, xe, ry - 10], radius=10, fill=(255, 210, 63, 230))
    for mm in range(0, m + 1, 5):
        x = x0 + mm * px
        if x <= xe:
            d.line([(x, ry - 40), (x, ry - 6)], fill=(255, 255, 255, 230), width=3)
    paste_car(img, 300, ry, 0.62, RED, False, -t * 14 * sp)
    smoke(img, t, [(120, ry - 30, 0.4)], col=(230, 230, 230), alpha=40, spread=(200, 10), grow=30, speed=1.4)
    if t < a1:
        big(t, 0.3, "28 M", 300, 130, YEL, sub="CADA SEGUNDO A 100")
    else:
        big(t, a1 + 0.1, "39 M", 300, 130, RED, sub="CADA SEGUNDO A 140")
    vignette(img, 160)


def sh_react(img, t, T, L):
    a1 = L[1][0]
    hz = 820
    night_sky(img, t, hz, 0.7, (4, 6, 14), (26, 26, 44))
    mountains(img, hz, 90, (14, 14, 22), 7, 0.5)
    ground(img, hz, (14, 14, 18), (4, 4, 6))
    pine_row(img, hz + 150, (10, 14, 14), 30, 160, 320, 5)
    pine_row(img, hz + 200, (6, 8, 8), 22, 220, 380, 9)
    d = ImageDraw.Draw(img, "RGBA")
    ry = 1200
    d.rectangle([0, ry - 120, W, ry + 40], fill=(30, 30, 36))
    off = (t * 600) % 220
    for x in range(-220, W + 220, 220):
        d.rectangle([x - off, ry - 46, x - off + 110, ry - 38], fill=(220, 214, 190))
    light_cone(img, 420, ry - 90, 1180, ry - 120, 20, 260, (255, 244, 210), 110, 22)
    dx = 840 + math.sin(t * 2) * 6
    lit = 0.7
    paste(img, glow(260, (255, 240, 200), 0.22), dx, ry - 250, 1.0, lit)
    paste(img, spr(deer, 0.85), dx, ry - 250, 0.95)
    d.ellipse([dx - 170, ry - 50, dx + 170, ry - 20], fill=(0, 0, 0, 90))
    paste_car(img, 230, ry, 0.6, RED, True, -t * 18)
    if t < a1:
        big(t, 0.6, "¡CUIDADO!", 300, 110, RED)
    else:
        q = clamp((t - a1 - 0.2) / 1.6)
        dd = td()
        cx, cy = 540, 420
        dd.arc([cx - 110, cy - 110, cx + 110, cy + 110], -90, -90 + 360 * q, fill=YEL + (255,), width=10)
        dd.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], outline=(255, 255, 255, 60), width=3)
        spaced(dd, cx, cy - 30, f"{0.75 * q:.2f}".replace(".", ",") + " S", f(F_SER, 50), (255, 255, 255, 255), 2)
        lower_third(img, t, a1 + 1.0, "SIN TOCAR EL FRENO", "21 M A 100 · 29 M A 140", 600, 3.0)
    vignette(img, 220)


def sh_rule(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    hz = 900
    highway_day(img, t, hz, 0.6, True)
    ry = hz + 300
    paste_car(img, 170, ry, 0.5, RED, False, -t * 8)
    d = ImageDraw.Draw(img, "RGBA")
    if t >= a1:
        m = 100 if t < a2 else 196
        k = ease(clamp(((t - a1) if t < a2 else (t - a2)) / 1.2))
        x0, px = 400, 3.2
        xe = x0 + m * px * k
        col = (255, 210, 63) if t < a2 else (230, 60, 66)
        d.rounded_rectangle([x0, ry - 34, xe, ry - 12], radius=8, fill=col + (220,))
        if k > 0.95:
            d.line([(xe, ry - 70), (xe, ry)], fill=(255, 255, 255, 230), width=4)
    if t < a1:
        big(t, 0.3, "140 → 14", 300, 120, YEL, sub="QUITA LA ÚLTIMA CIFRA")
    elif t < a2:
        big(t, a1 + 0.1, "10 × 10 = 100 M", 300, 92, YEL)
    else:
        big(t, a2 + 0.1, "14 × 14 = 196 M", 300, 92, RED)
    vignette(img, 160)


def sh_energy(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    sky(img, (24, 26, 34), (8, 8, 12), 1.0)
    for x in (180, 540, 900):
        spotlight(img, t, x, 0, 1400, 40, 260, 40, dust=False)
    d = ImageDraw.Draw(img, "RGBA")
    ry = 1180
    d.rectangle([0, ry, W, H], fill=(40, 40, 46))
    for x in range(0, W, 120):
        d.rectangle([x, ry, x + 60, ry + 14], fill=(230, 200, 40))
    d.rectangle([880, ry - 380, 1080, ry], fill=(120, 120, 124))
    for y in range(int(ry - 380), ry, 60):
        d.line([(880, y), (1080, y)], fill=(90, 90, 96), width=4)
    hit = a2 + 0.6
    if t < hit:
        x = lerp(-200, 560, clamp(t / hit))
    else:
        x = 560
    sx, sy = shake(t, hit, 20, 5)
    paste_car(img, x + sx, ry + sy, 0.7, RED, False, -t * 12)
    if t > hit:
        overlay(img, (255, 255, 255), 0.8 * math.exp(-(t - hit) * 6))
    if t < a1:
        big(t, 0.3, "+40 %", 300, 130, WHITE, sub="DE VELOCIDAD")
    elif t < a2:
        big(t, a1 + 0.1, "E = ½ · M · V²", 300, 96, YEL, pop=False)
    else:
        big(t, a2 + 0.1, "×1,96", 300, 140, RED, sub="DE ENERGÍA")
    vignette(img, 200)


def tower(img, x, base, floors, col=(26, 28, 40), lit=(255, 214, 140), w=220, fh=36, seed=1):
    d = ImageDraw.Draw(img, "RGBA")
    top = base - floors * fh
    d.rectangle([x - w / 2, top, x + w / 2, base], fill=col)
    rr = random.Random(seed)
    for i in range(floors):
        y = base - (i + 1) * fh + 8
        for wx in range(int(x - w / 2 + 16), int(x + w / 2 - 20), 34):
            if rr.random() < 0.7:
                d.rectangle([wx, y, wx + 18, y + 20], fill=lit + (230,))
    return top


def sh_fall(img, t, T, L):
    a1 = L[1][0]
    night_sky(img, t, 1500, 0.8, (6, 8, 22), (40, 30, 60))
    city_lights(img, t, 1420, 3, 200)
    base = 1450
    k1 = ease(clamp((t - 0.2) / 1.0))
    top13 = tower(img, 320, base, int(13 * k1) or 1, seed=2)
    top26 = base
    if t > a1:
        k2 = ease(clamp((t - a1) / 1.4))
        top26 = tower(img, 760, base, max(1, int(26 * k2)), seed=3)
    ground(img, base, (12, 12, 16), (4, 4, 6))
    d = td()
    if t < a1:
        paste_car(img, 320, top13, 0.22, RED, True)
        lower_third(img, t, 1.0, "PISO 13 · ≈ 39 M", "CHOCAR A 100 KM/H", int(top13 - 260), 3.0)
        big(t, 0.3, "PISO 13", 300, 120, YEL)
    else:
        paste_car(img, 760, top26, 0.22, RED, True)
        big(t, a1 + 0.2, "PISO 26", 250, 120, RED, sub="≈ 77 M · A 140 KM/H")
    vignette(img, 200)


def sh_air(img, t, T, L):
    a1 = L[1][0]
    sky(img, (20, 24, 30), (6, 8, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(8):
        r = 1400 - k * 160
        d.ellipse([540 - r, 1000 - r * 0.7, 540 + r, 1000 + r * 0.7], outline=(60, 70, 86, 200), width=6)
    d.rectangle([0, 1150, W, H], fill=(30, 32, 38))
    paste_car(img, 560, 1150, 0.95, RED, False, 0)
    strength = 1.0 if t < a1 else 1.6
    for i in range(9):
        y = 680 + i * 52
        pts = []
        for x in range(0, W, 12):
            yy = y
            if 150 < x < 980 and y < 1080:
                prof = math.exp(-((x - 560) / 330) ** 2) * (1080 - y) * 0.22
                yy -= prof
            pts.append((x, yy + math.sin(x / 50 - t * 10 * strength + i) * 3 * strength))
        d.line(pts, fill=(235, 240, 255, 150), width=3)
    if t < a1:
        big(t, 0.3, "RESISTENCIA ×1,96", 300, 84, WHITE, pop=False)
    else:
        big(t, a1 + 0.2, "+20-25 %", 300, 130, YEL, sub="DE CONSUMO (DE 120 A 140)")
    vignette(img, 200)


def sh_fine(img, t, T, L):
    highway_night(img, t, 1.0, 900, True)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([60, 520, 90, 1100], fill=(70, 74, 84))
    d.rectangle([990, 520, 1020, 1100], fill=(70, 74, 84))
    d.rectangle([60, 520, 1020, 580], fill=(60, 64, 74))
    d.rectangle([460, 580, 620, 680], fill=(40, 42, 50))
    d.ellipse([510, 600, 570, 660], fill=(20, 20, 26))
    if t > 0.9:
        fl = math.exp(-(t - 0.9) * 5)
        paste(img, glow(300, (255, 255, 255), 1.0), 540, 630, 1.0, fl)
        overlay(img, (255, 255, 255), 0.5 * fl)
    if t > 1.4:
        k = ease(clamp((t - 1.4) / 0.6))
        tk = spr(paper, 520, 640, "MULTA", 0, (244, 240, 228), (40, 30, 30), 3,
                 ("Exceso de velocidad", "", "Vía: autovía 120 km/h", "Medido: 140 km/h", "", "Importe: 100 EUR", "Puntos: 0"))
        paste(img, tk, 540, lerp(1700, 1000, k), 0.85, 1.0, -4)
    big(t, 1.6, "100 € · SIN PUNTOS", 300, 84, YEL)
    vignette(img, 200)


def sh_time(img, t, T, L):
    a1 = L[1][0]
    hz = 900
    highway_day(img, t, hz, 1.0, True)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([700, 640, 716, hz + 140], fill=(120, 124, 130))
    d.rectangle([900, 640, 916, hz + 140], fill=(120, 124, 130))
    d.rounded_rectangle([640, 540, 980, 740], radius=14, fill=(24, 70, 160), outline=(255, 255, 255), width=5)
    d.text((810, 640), "100 km", font=f(F_CAP, 74), fill=(255, 255, 255), anchor="mm")
    paste_car(img, 300, hz + 300, 0.55, RED, False, -t * 12)
    dd = td()
    if t < a1:
        big(t, 0.3, "¿CUÁNTO GANAS?", 300, 92, WHITE, pop=False)
    else:
        k = ease(clamp((t - a1 - 0.2) / 0.8))
        spaced(dd, W / 2, 260, "A 100: 60 MIN", f(F_SER, 56), (255, 255, 255, int(255 * k)), 4)
        spaced(dd, W / 2, 340, "A 140: 43 MIN", f(F_SER, 56), (255, 255, 255, int(255 * k)), 4)
        big(t, a1 + 1.2, "17 MINUTOS", 440, 110, YEL)
    vignette(img, 160)


def sh_verdict(img, t, T, L):
    hz = 860
    sky(img, (40, 40, 100), (255, 150, 90), 1.4, 0, hz)
    paste(img, glow(460, (255, 190, 120), 0.9), 540, hz - 20)
    mountains(img, hz, 90, (60, 40, 70), 4, 0.5)
    ground(img, hz, (40, 30, 40), (10, 8, 12))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    dd.polygon([(530, hz), (550, hz), (W + 500, H), (-500, H)], fill=(36, 32, 40, 255))
    for k in range(12):
        u = ((k / 12) + t * 0.35) % 1.0
        z0, z1 = u ** 2.4, min(1.0, (u + 0.03) ** 2.4)
        y0, y1 = hz + (H - hz) * z0, hz + (H - hz) * z1
        dd.polygon([(540 - 2 - 16 * z0, y0), (540 + 2 + 16 * z0, y0), (540 + 2 + 16 * z1, y1), (540 - 2 - 16 * z1, y1)], fill=(240, 220, 180, 255))
    AC(img, im)
    q = clamp(t / T)
    s_ = lerp(1.0, 0.45, ease(q))
    paste(img, car_rear(RED, 0.0), 540, lerp(1260, 1060, ease(q)), s_)
    title2(t, 0.4, "17 MINUTOS", "¿MERECE LA PENA?", 300, 60, 84, hold=max(2.0, T - 3.4), c1=YEL, c2=WHITE)
    vignette(img, 180)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "tension"), ("meters", "epic"), ("fall", "drone"), ("air", "doc"), ("time", "premium")],
    "duck": [("energy@L2+0.4", "fall+1.0", 0.5)],
    "amb": {"road": ["open", "meters", "react", "rule", "fine", "time", "verdict"], "wind": ["air"], "city": ["fall"]},
    "sfx": [("open+0.2", "whoosh", 0.15), ("open@L1+0.2", "chime", 0.05), ("meters+0.3", "riser", 0.1), ("meters@L1", "whoosh_up", 0.15),
            ("react+0.6", "heart", 0.35), ("react+1.35", "heart", 0.35), ("react@L1+0.2", "tick", 0.15), ("react@L1+0.9", "tick", 0.15),
            ("rule+0.3", "pop", 0.18), ("rule@L1", "whoosh_up", 0.12), ("rule@L2", "whoosh_up", 0.14),
            ("energy@L2+0.6", "boom", 0.45), ("energy@L2+0.6", "impact", 0.4),
            ("fall+0.2", "riser", 0.1), ("fall@L1", "riser_long", 0.12), ("fall@L1+1.4", "impact", 0.3),
            ("air", "whoosh", 0.18), ("air@L1+0.2", "impact", 0.2),
            ("fine+0.9", "shutter", 0.35), ("fine+1.4", "paper", 0.25),
            ("time@L1+0.2", "tick", 0.15), ("time@L1+1.2", "chime", 0.06), ("verdict+0.4", "swell", 0.15)],
    "bed": [("meters", "energy"), ("air", "time")],
    "bpm": 100,
}
