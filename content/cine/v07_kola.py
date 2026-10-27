"""V07 · El agujero más profundo del mundo (pozo superprofundo de Kola)."""
from cine import *

TITLE = "El_agujero_mas_profundo_del_mundo"
LINES = [
    "Los soviéticos hicieron el agujero *más profundo* jamás perforado.",
    "¿Hasta dónde llegaron… y por qué tuvieron que *parar*?",
    "Península de Kola, cerca del Ártico. Año 1970.",
    "Empieza una carrera… pero *hacia abajo*.",
    "El objetivo: perforar la corteza terrestre lo más hondo posible.",
    "El agujero mide solo *23 centímetros* de ancho.",
    "Menos que un plato.",
    "Año tras año, la broca baja y baja.",
    "A pocos kilómetros, encuentran algo inesperado: *agua*.",
    "A 6 kilómetros, *fósiles microscópicos* de plancton.",
    "Y el lodo salía *burbujeando*, lleno de hidrógeno.",
    "En 1989 llegan a los *12.262 metros*.",
    "Más que la altura del Everest… y más que la fosa de las Marianas.",
    "Pero allí abajo pasa algo que no esperaban.",
    "La roca está a *180 grados*.",
    "Las herramientas sufren… y el dinero *se acaba*.",
    "Y tras más de 12 kilómetros, solo habían cruzado *un tercio* de la corteza.",
    "Hoy, el lugar está abandonado… y el agujero, tapado con una placa de metal.",
    "El agujero más profundo del mundo… cabe *bajo una tapa*.",
]
SHOTS = [("open", 0, 1, 0.3), ("kola", 2, 3, 0.3), ("goal", 4, 4, 0.2), ("width", 5, 6, 0.3), ("drill", 7, 8, 0.3),
         ("fossils", 9, 10, 0.3), ("record", 11, 12, 0.4), ("heat", 13, 15, 0.4), ("crust", 16, 16, 0.4), ("today", 17, 18, 1.8)]
FOCUS = {"open": (540, 640), "kola": (540, 640), "goal": (540, 900), "width": (540, 900), "drill": (540, 900),
         "fossils": (540, 880), "record": (540, 960), "heat": (540, 960), "crust": (540, 900), "today": (540, 1060)}
NOTIF = ("width", 1.2)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿HASTA DÓNDE LLEGARON?', '¿POR QUÉ TUVIERON QUE PARAR?'], "delay": [0, 1.1]}
STICKER_EXTRA = [('sovietico', '🚩'), ('agujero', '🕳️'), ('profundo', '⬇️'), ('perfora', '🛠️'), ('artico', '🧊'), ('carrera', '🏁'), ('abajo', '⬇️'), ('corteza', '🌍'), ('centimetro', '📏'), ('plato', '🍽️'), ('broca', '🛠️'), ('fosiles', '🦠'), ('plancton', '🦠'), ('burbuje', '🫧'), ('hidrogeno', '🧪'), ('metros', '📏'), ('everest', '🏔️'), ('marianas', '🌊'), ('roca', '🪨'), ('grados', '🔥'), ('herramienta', '🔧'), ('dinero', '💸'), ('abandonado', '🏚️'), ('=tapa', '🔩'), ('placa', '🔩')]

def derrick(lit=True):
    def fn(d, s):
        c = (40, 44, 56)
        d.polygon(sc([(120, 900), (380, 900), (270, 60), (230, 60)], s), fill=(0, 0, 0, 0))
        for sgn in (-1, 1):
            d.line(sc([(250 + sgn * 130, 900), (250 + sgn * 18, 60)], s), fill=c, width=int(10 * s))
        for k in range(12):
            y1 = 900 - k * 70
            y2 = y1 - 70
            w1 = 130 - (130 - 18) * (900 - y1) / 840
            w2 = 130 - (130 - 18) * (900 - y2) / 840
            d.line(sc([(250 - w1, y1), (250 + w2, y2)], s), fill=c, width=int(4 * s))
            d.line(sc([(250 + w1, y1), (250 - w2, y2)], s), fill=c, width=int(4 * s))
            d.line(sc([(250 - w1, y1), (250 + w1, y1)], s), fill=c, width=int(4 * s))
        d.rectangle(sb([200, 30, 300, 70], s), fill=c)
        d.rectangle(sb([0, 860, 500, 960], s), fill=(60, 64, 76))
        for x in range(30, 480, 70):
            d.rectangle(sb([x, 880, x + 40, 920], s), fill=(255, 210, 140) if lit else (40, 40, 50))
        if lit:
            for y in (200, 450, 700):
                d.ellipse(sb([240, y, 260, y + 20], s), fill=(255, 80, 60))
    return sprite(("derrick", lit), 500, 960, fn)


def earth_section(r=420):
    def fn(d, s):
        c = r + 20
        for rad, col in ((r, (110, 90, 70)), (r * 0.97, (210, 110, 50)), (r * 0.55, (240, 160, 60)), (r * 0.19, (255, 230, 140))):
            d.ellipse(sb([c - rad, c - rad, c + rad, c + rad], s), fill=col)
        d.ellipse(sb([c - r, c - r, c + r, c + r], s), outline=(40, 80, 140), width=int(6 * s))
    return sprite(("esec", r), int(r * 2 + 40), int(r * 2 + 40), fn)


def plate():
    def fn(d, s):
        d.ellipse(sb([0, 0, 400, 400], s), fill=(236, 236, 240))
        d.ellipse(sb([60, 60, 340, 340], s), fill=(222, 222, 228))
    return sprite("plate", 400, 400, fn)


def plankton(kind=0):
    def fn(d, s):
        c = (230, 220, 190)
        if kind == 0:
            for k in range(7):
                r = 20 + k * 14
                d.ellipse(sb([150 - r + k * 6, 150 - r, 150 + r + k * 6, 150 + r], s), outline=c, width=int(5 * s))
        else:
            for k in range(6):
                a = k * 1.05
                x, y = 150 + math.cos(a) * 60, 150 + math.sin(a) * 60
                d.ellipse(sb([x - 45, y - 45, x + 45, y + 45], s), outline=c, width=int(5 * s))
            d.ellipse(sb([110, 110, 190, 190], s), outline=c, width=int(5 * s))
    return sprite(("plank", kind), 320, 300, fn)


def cap():
    def fn(d, s):
        d.ellipse(sb([0, 0, 600, 300], s), fill=(110, 70, 40))
        d.ellipse(sb([30, 20, 570, 270], s), fill=(140, 86, 46))
        d.ellipse(sb([170, 80, 430, 210], s), fill=(120, 76, 42))
        rr = random.Random(2)
        for k in range(12):
            a = k / 12 * 2 * math.pi
            x, y = 300 + math.cos(a) * 240, 145 + math.sin(a) * 110
            d.ellipse(sb([x - 14, y - 9, x + 14, y + 9], s), fill=(80, 50, 30))
        for _ in range(30):
            x, y, r = rr.uniform(60, 540), rr.uniform(40, 250), rr.uniform(6, 20)
            d.ellipse(sb([x - r, y - r * 0.5, x + r, y + r * 0.5], s), fill=(170, 100, 50))
    return sprite("cap", 600, 300, fn)


# ------------------------------------------------------------------ planos
def snowfield(img, t, hz, night=True):
    if night:
        night_sky(img, t, hz, 1.0, (4, 8, 22), (30, 50, 80))
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(5):
            pts = [(x, 380 + k * 40 + math.sin(x / 160 + t * 0.5 + k) * 60) for x in range(-40, W + 60, 40)]
            d.line(pts, fill=(80, 255, 160, 40 - k * 6), width=40 - k * 6)
    else:
        sky(img, (150, 170, 200), (230, 234, 240), 1.2)
    mountains(img, hz, 200, (190, 200, 216) if not night else (60, 70, 90), 8, 0.4)
    ground(img, hz, (220, 228, 240) if not night else (110, 120, 140), (180, 190, 206) if not night else (60, 66, 80))


def sh_open(img, t, T, L):
    snowfield(img, t, 1250)
    paste(img, glow(300, (255, 210, 150), 0.5), 540, 1150)
    paste(img, derrick(True), 540, 1250 - 384, 0.8)
    particles(img, t, 80, 5, (255, 255, 255), 50, (1.5, 3.5), 170, 30)
    title2(t, 0.25, "EL AGUJERO MÁS", "PROFUNDO DEL MUNDO", 290, 60, 80, hold=max(1.5, L[1][0] - 0.4))
    vignette(img, 170)


def sh_kola(img, t, T, L):
    snowfield(img, t, 1250, False)
    paste(img, derrick(False), 540 + t * 6, 1250 - 384, 0.8)
    particles(img, t, 60, 6, (255, 255, 255), 40, (1.5, 3), 200, 30)
    date_stamp(t, 0.3, "KOLA · URSS · 1970", 300, max(1.8, L[1][0] - 0.3))
    a1 = L[1][0]
    if t > a1:
        big(t, a1 + 0.2, "HACIA ABAJO", 300, 104, YEL)
        d = ImageDraw.Draw(img, "RGBA")
        k = ease(clamp((t - a1 - 0.4) / 0.8))
        y = 1350 + 300 * k
        d.line([(540, 1300), (540, y)], fill=(255, 210, 63, 255), width=14)
        d.polygon([(500, y), (580, y), (540, y + 60)], fill=(255, 210, 63, 255))
    vignette(img, 150)


def sh_goal(img, t, T, L):
    space_bg(img, t, 2)
    r = 420
    paste(img, earth_section(r), 540, 960)
    d = ImageDraw.Draw(img, "RGBA")
    c = (540, 960)
    k = ease(clamp((t - 0.6) / 1.0))
    a = math.radians(-60)
    x0, y0 = c[0] + math.cos(a) * r, c[1] + math.sin(a) * r
    d.line([(x0, y0), (x0 - math.cos(a) * 14 * k, y0 - math.sin(a) * 14 * k)], fill=(255, 255, 255), width=6)
    paste(img, glow(40, (255, 255, 255), 1.0), x0, y0, 1.0, 0.8)
    for txt, rad in (("CORTEZA", 1.04), ("MANTO", 0.76), ("NÚCLEO", 0.3)):
        dd = td()
        dd.text((c[0] + 20 + rad * r * 0.0, c[1] - rad * r * 0.95), txt, font=f(F_SER, 34), fill=(255, 255, 255, 220))
    big(t, 0.3, "ATRAVESAR", 290, 80, WHITE, sub="LA CORTEZA", subcol=YEL, pop=False)
    vignette(img, 170)


def sh_width(img, t, T, L):
    sky(img, (60, 62, 70), (30, 30, 34), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, H], fill=(110, 110, 116))
    rr = random.Random(3)
    for _ in range(300):
        x, y = rr.uniform(0, W), rr.uniform(0, H)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(90, 90, 96))
    a1 = L[1][0]
    cx, cy = 540 if t < a1 else 380, 900
    d.ellipse([cx - 160, cy - 160, cx + 160, cy + 160], fill=(10, 10, 12))
    d.ellipse([cx - 175, cy - 175, cx + 175, cy + 175], outline=(70, 70, 76), width=14)
    d.line([(cx - 160, cy + 230), (cx + 160, cy + 230)], fill=YEL + (255,), width=6)
    for x in (cx - 160, cx + 160):
        d.line([(x, cy + 210), (x, cy + 250)], fill=YEL + (255,), width=6)
    big(t, 0.4, "23 CM", 300, 130, YEL)
    if t > a1:
        k = ease(clamp((t - a1) / 0.5))
        paste(img, plate(), 780, 900, 0.95, k)
        dd = td()
        spaced(dd, 780, 1130, "PLATO · ~26 CM", f(F_SER, 40), (255, 255, 255, int(255 * k)), 4)
    vignette(img, 190)


LAYERS = [((150, 120, 90), 0), ((120, 96, 76), 1.2), ((96, 84, 80), 2.5), ((80, 70, 74), 4.0), ((70, 60, 68), 6.0),
          ((90, 60, 50), 8.0), ((110, 64, 44), 10.0), ((140, 70, 40), 11.5)]


def strata(img, depth_km, scale_px_per_km=520, top_y=400):
    d = ImageDraw.Draw(img, "RGBA")
    for i, (col, z) in enumerate(LAYERS):
        z2 = LAYERS[i + 1][1] if i + 1 < len(LAYERS) else 99
        y1 = top_y + (z - depth_km) * scale_px_per_km
        y2 = top_y + (z2 - depth_km) * scale_px_per_km
        if y2 < 0 or y1 > H:
            continue
        d.rectangle([0, max(0, y1), W, min(H, y2)], fill=col)
        for k in range(int(max(0, y1)), int(min(H, y2)), 46):
            d.line([(0, k), (W, k + 10)], fill=tuple(max(0, c - 14) for c in col), width=3)


def sh_drill(img, t, T, L):
    a1 = L[1][0]
    depth = lerp(0.0, 3.4, ease(clamp(t / (a1 + 0.6))))
    strata(img, depth)
    d = ImageDraw.Draw(img, "RGBA")
    y_bit = 900
    d.rectangle([520, 0, 560, y_bit], fill=(30, 30, 36))
    d.polygon([(510, y_bit), (570, y_bit), (540, y_bit + 60)], fill=(200, 200, 210))
    if depth < 0.3:
        sky(img, (150, 170, 200), (230, 234, 240), 1.2, 0, int((400 - depth * 520) // 10 * 10))
    if t > a1:
        k = ease(clamp((t - a1 - 0.4) / 0.6))
        rr = random.Random(4)
        for _ in range(9):
            x, y = rr.uniform(100, 980), rr.uniform(1000, 1400)
            r = rr.uniform(30, 70) * k
            d.ellipse([x - r, y - r * 0.5, x + r, y + r * 0.5], fill=(60, 140, 220, 220))
        big(t, a1 + 1.0, "¡AGUA!", 300, 120, (120, 200, 255))
    dd = td()
    km = depth
    dd.rounded_rectangle([60, 230, 420, 330], radius=16, fill=(0, 0, 0, 160))
    dd.text((90, 248), f"{km * 1000:,.0f} m".replace(",", "."), font=f(F_MONO, 54), fill=(255, 255, 255, 255))
    vignette(img, 180)


def sh_fossils(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        sky(img, (10, 12, 16), (4, 4, 6), 1.0)
        d = ImageDraw.Draw(img, "RGBA")
        d.ellipse([140, 500, 940, 1300], fill=(40, 70, 70))
        for i, (x, y, kd, rot) in enumerate(((420, 760, 0, 10), (660, 980, 1, 40), (500, 1100, 0, -30), (720, 700, 1, 0))):
            paste(img, plankton(kd), x + math.sin(t + i) * 6, y, 0.8, 0.9, rot + t * 4)
        d.ellipse([140, 500, 940, 1300], outline=(20, 20, 24), width=40)
        big(t, 0.3, "6 KM", 300, 120, YEL, sub="FÓSILES DE PLANCTON")
    else:
        strata(img, 6.2)
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(9)
        d.rectangle([0, 1100, W, H], fill=(90, 80, 76))
        for k in range(40):
            ph = ((t - a1) * 0.6 + k / 40) % 1.0
            x = rr.uniform(60, 1020)
            y = 1500 - ph * 500
            r = 10 + rr.uniform(0, 26) * (1 - ph * 0.5)
            d.ellipse([x - r, y - r, x + r, y + r], outline=(230, 230, 220, int(220 * (1 - ph))), width=4)
        big(t, a1 + 0.3, "HIDRÓGENO", 300, 104, WHITE)
    vignette(img, 190)


def sh_record(img, t, T, L):
    sky(img, (14, 18, 28), (6, 8, 12), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    base = 820
    px = 0.042
    bars = [("EVEREST", 8849, -1, (220, 230, 240)), ("FOSA DE LAS\nMARIANAS", 10935, 1, (60, 120, 200)), ("KOLA", 12262, 1, YEL)]
    d.line([(0, base), (W, base)], fill=(255, 255, 255, 180), width=3)
    dd = td()
    for i, (nm, m, sgn, col) in enumerate(bars):
        x = 200 + i * 340
        t0 = 0.3 if i == 2 else L[1][0] + (0.0 if i == 0 else 1.6)
        k = ease(clamp((t - t0) / 0.9))
        if k <= 0:
            continue
        hpx = m * px * k
        if sgn < 0:
            d.polygon([(x - 120, base), (x + 120, base), (x, base - hpx)], fill=col + (255,))
            ty = base - hpx - 80
        else:
            d.rectangle([x - 60, base, x + 60, base + hpx], fill=col + (255,))
            ty = base + hpx + 20
        for j, ln in enumerate(nm.split("\n")):
            tw = dd.textlength(ln, font=f(F_SER, 34))
            dd.text((x - tw / 2, ty + j * 40), ln, font=f(F_SER, 34), fill=(255, 255, 255, int(255 * k)))
        val = f"{int(m * k):,} m".replace(",", ".")
        tw = dd.textlength(val, font=f(F_SER, 40))
        dd.text((x - tw / 2, (ty - 50) if sgn < 0 else (ty + 40 * len(nm.split(chr(10))) + 6)), val, font=f(F_SER, 40), fill=col + (int(255 * k),))
    big(t, 0.3, "12.262 M", 220, 100, YEL, pop=False)
    vignette(img, 170)


def sh_heat(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    strata(img, 11.6)
    hot = clamp((t - a1) / 1.6)
    overlay(img, (255, 90, 30), hot * 0.4)
    paste(img, glow(600, (255, 120, 40), 1.0), 540, 1300, 1.0, hot)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([860, 520, 940, 1300], radius=40, fill=(240, 240, 240, 230))
    d.ellipse([830, 1240, 970, 1380], fill=(240, 240, 240, 230))
    lvl = lerp(1240, 600, hot)
    d.rectangle([882, lvl, 918, 1290], fill=(230, 40, 40, 255))
    d.ellipse([850, 1260, 950, 1360], fill=(230, 40, 40, 255))
    if a1 < t < a2:
        big(t, a1 + 0.2, counter(t, a1 + 0.2, a1 + 1.8, 20, 180) + " °C", 300, 124, YEL, pop=False)
    if t >= a2:
        big(t, a2 + 0.2, "SIN DINERO", 300, 104, WHITE, sub="1992-1995", subcol=YEL)
        k = ease(clamp((t - a2 - 0.6) / 1.0))
        d.polygon([(500, 860), (580, 860), (560 + 30 * k, 980), (520 - 30 * k, 980)], fill=(160, 160, 170, 255))
    d.rectangle([520, 0, 560, 860], fill=(30, 30, 36))
    vignette(img, 180)


def sh_crust(img, t, T, L):
    sky(img, (14, 16, 22), (6, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    top, bot = 520, 1420
    d.rectangle([340, top, 740, bot], fill=(110, 90, 70))
    k = ease(clamp((t - 0.5) / 1.2))
    frac = 12.262 / 35
    d.rectangle([340, top, 740, top + (bot - top) * frac * k], fill=(255, 210, 63, 255))
    d.rectangle([520, top, 560, top + (bot - top) * frac * k], fill=(30, 30, 36))
    dd = td()
    dd.text((770, top + (bot - top) * frac - 30), "12 KM", font=f(F_SER, 44), fill=YEL + (int(255 * k),))
    dd.text((770, bot - 40), "~35 KM", font=f(F_SER, 44), fill=(255, 255, 255, 220))
    dd.text((80, (top + bot) / 2 - 30), "CORTEZA", font=f(F_SER, 40), fill=(255, 255, 255, 200))
    big(t, 1.2, "SOLO 1/3", 300, 120, YEL)
    vignette(img, 180)


def sh_today(img, t, T, L):
    a1 = L[1][0]
    if t < a1 - 0.3:
        snowfield(img, t, 1250, False)
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([260, 900, 820, 1260], fill=(120, 116, 112))
        for x in range(290, 800, 90):
            d.rectangle([x, 960, x + 50, 1040], fill=(30, 30, 34))
        d.polygon([(260, 900), (500, 760), (560, 900)], fill=(100, 96, 92))
        particles(img, t, 70, 8, (255, 255, 255), 45, (1.5, 3), 210, 40)
        lower_third(img, t, 0.3, "ABANDONADO", "DESDE LOS AÑOS 90", 300, 3.0)
    else:
        ground(img, 0, (150, 146, 140), (110, 106, 100))
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(5)
        for _ in range(200):
            x, y = rr.uniform(0, W), rr.uniform(0, H)
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(130, 126, 120))
        paste(img, cap(), 540, 1000, 1.25)
        big(t, a1 + 0.2, "BAJO UNA TAPA", 300, 100, YEL, pop=False)
    vignette(img, 180)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "drone"), ("kola", "tension"), ("record", "epic"), ("heat", "tension"), ("today", "drone")],
    "amb": {"wind": ["open", "kola", "today"], "room": ["width", "fossils", "crust"]},
    "sfx": [("open+0.2", "drill", 0.12), ("kola@L1+0.4", "whoosh", 0.15), ("kola@L1+0.6", "impact", 0.25),
            ("goal+0.6", "drill", 0.1), ("width+0.4", "thud", 0.3), ("width@L1", "pop", 0.2),
            ("drill", "drill", 0.16), ("drill+2.6", "drill", 0.14), ("drill@L1+0.4", "swell", 0.15),
            ("fossils+0.3", "ding", 0.08), ("fossils@L1", "crackle", 0.2),
            ("record+0.3", "riser", 0.12), ("record+1.2", "impact", 0.3), ("record@L1", "pop", 0.2), ("record@L1+1.6", "pop", 0.2),
            ("heat@L1", "riser_long", 0.15), ("heat@L1+1.8", "impact", 0.25), ("heat@L2+0.6", "thud", 0.3),
            ("crust+0.5", "swell", 0.15), ("crust+1.2", "impact", 0.2), ("today@L1", "thud", 0.3)],
    "bed": [("width", "heat")],
    "bpm": 94,
}
