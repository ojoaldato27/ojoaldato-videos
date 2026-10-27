"""V09 · Cleopatra vivió más cerca de la llegada a la Luna que de las pirámides."""
from cine import *
from v05_apolo import lem, astronaut, moon_ground

TITLE = "Cleopatra_la_Luna_y_las_piramides"
LINES = [
    "¿Quién vivió más cerca de la llegada a la Luna: *Cleopatra*… o los constructores de las pirámides?",
    "Piénsalo bien, porque la respuesta *no es la que parece*.",
    "Egipto, hacia el año 2560 antes de Cristo.",
    "Miles de trabajadores terminan la *Gran Pirámide* de Guiza.",
    "Es la tumba del faraón *Keops*.",
    "Medía unos *146 metros*: durante más de 3.800 años, fue lo más alto construido por el ser humano.",
    "Pasan los siglos… y los faraones siguen reinando *durante milenios*.",
    "Hasta que llega la última reina de Egipto: *Cleopatra*.",
    "Y ni siquiera era de origen egipcio: su familia venía de *Macedonia*.",
    "Cleopatra muere en el año 30 antes de Cristo.",
    "Para entonces, la Gran Pirámide ya tenía *más de 2.500 años*.",
    "Para Cleopatra, ya era *una antigüedad*.",
    "Ahora, salta hasta el 20 de julio de 1969.",
    "El ser humano pisa *la Luna*.",
    "De Cleopatra a la Luna pasan unos *2.000 años*.",
    "Así que la respuesta es…",
    "Cleopatra vivió *más cerca* de la llegada a la Luna… que de la construcción de la Gran Pirámide.",
    "Hay cosas tan antiguas… que ya eran antiguas *para los antiguos*.",
]
SHOTS = [("open", 0, 1, 0.3), ("build", 2, 4, 0.3), ("tallest", 5, 5, 0.3), ("centuries", 6, 6, 0.3), ("queen", 7, 8, 0.3),
         ("death", 9, 11, 0.4), ("moon", 12, 14, 0.4), ("answer", 15, 16, 0.4), ("final", 17, 17, 1.8)]
FOCUS = {"open": (540, 1050), "build": (560, 1050), "tallest": (540, 900), "queen": (600, 900), "death": (540, 1000),
         "moon": (520, 1100), "final": (540, 1050)}
NOTIF = ("tallest", 1.0)

SAND = (214, 170, 110)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 0, "text": ['¿CLEOPATRA O LAS PIRÁMIDES?', '¿QUIÉN ESTÁ MÁS CERCA DE LA LUNA?'], "delay": [0, 1.8]}
KW_OVERRIDE = {12: [], 15: [], 17: []}
NARRATOR = {"open": ("wave", "left"), "build": ("point", "left"), "tallest": ("surprise", "left"), "centuries": ("think", "left"),
            "queen": ("point", "left"), "death": ("point", "right"), "moon": ("flag", "left"), "answer": ("surprise", "left"),
            "final": ("think", "left")}
STICKER_EXTRA = [('luna', '🌕'), ('cleopatra', '👑'), ('piramide', '🔺'), ('piensalo', '🤔'), ('egipto', '🐫'), ('trabajadores', '👷'), ('tumba', '⚰️'), ('faraon', '👑'), ('keops', '🔺'), ('metros', '📏'), ('anos', '⏳'), ('siglos', '⏳'), ('milenios', '⏳'), ('reina', '👑'), ('macedonia', '🏛️'), ('muere', '⚱️'), ('antiguedad', '🏺'), ('pisa', '👣'), ('humano', '🚀'), ('cerca', '📍'), ('antiguos', '🏺')]

def pyramid(unfinished=0.0, night=False, w=900, h=600):
    def fn(d, s):
        lit, dark = ((236, 206, 150), (180, 140, 90)) if not night else ((90, 80, 90), (50, 44, 54))
        apex = (w * 0.46, h * 0.02)
        mid = w * 0.62
        d.polygon(sc([(0, h), apex, (mid, h)], s), fill=lit)
        d.polygon(sc([apex, (w, h), (mid, h)], s), fill=dark)
        for k in range(1, 18):
            y = h * k / 18
            u = (y - apex[1]) / (h - apex[1])
            d.line(sc([(apex[0] - apex[0] * u, y), (apex[0] + (mid - apex[0]) * u, y)], s),
                   fill=tuple(max(0, c - 18) for c in lit), width=int(2 * s))
            d.line(sc([(apex[0] + (mid - apex[0]) * u, y), (apex[0] + (w - apex[0]) * u, y)], s),
                   fill=tuple(max(0, c - 14) for c in dark), width=int(2 * s))
        if unfinished > 0:
            d.rectangle(sb([0, 0, w, h * unfinished], s), fill=(0, 0, 0, 0))
    return sprite(("pyr", round(unfinished, 2), night, w, h), w, h, fn)


def cleopatra(col=(20, 16, 22), gold=(214, 166, 70)):
    def fn(d, s):
        d.polygon(sc([(120, 380), (300, 380), (360, 600), (60, 600)], s), fill=col)
        d.rectangle(sb([170, 300, 230, 390], s), fill=col)
        prof = [(190, 120), (240, 110), (268, 150), (274, 185), (292, 210), (278, 222), (282, 240), (272, 252), (276, 266),
                (258, 280), (230, 300), (190, 300)]
        d.polygon(sc(prof, s), fill=col)
        d.ellipse(sb([96, 50, 262, 220], s), fill=col)
        d.polygon(sc([(96, 140), (240, 140), (236, 200), (228, 340), (92, 340)], s), fill=col)
        d.chord(sb([96, 50, 262, 220], s), 200, 340, fill=gold)
        d.chord(sb([104, 62, 254, 210], s), 200, 340, fill=col)
        d.polygon(sc([(246, 104), (268, 78), (276, 104), (258, 118)], s), fill=gold)
        d.chord(sb([110, 330, 310, 470], s), 0, 180, fill=gold)
        d.chord(sb([130, 330, 290, 440], s), 0, 180, fill=col)
        d.ellipse(sb([236, 168, 250, 178], s), fill=gold)
    return sprite(("cleo", col), 400, 600, fn)


def palm2(h=500):
    def fn(d, s):
        c = (30, 26, 24)
        d.line(sc([(150, h), (170, 100)], s), fill=c, width=int(18 * s))
        for a in (-160, -130, -100, -60, -30, -5):
            r = math.radians(a)
            d.line(sc([(170, 100), (170 + math.cos(r) * 150, 100 + math.sin(r) * 60 + 50)], s), fill=c, width=int(12 * s))
    return sprite(("palm2", h), 340, h, fn)


# ------------------------------------------------------------------ planos
def desert(img, t, hz=1200, night=False, sunset=False):
    if night:
        night_sky(img, t, hz, 1.0, (6, 8, 24), (40, 34, 60))
    elif sunset:
        sky(img, (60, 50, 110), (255, 150, 80), 1.3)
        paste(img, glow(420, (255, 180, 110), 0.8), 760, hz - 40)
    else:
        sky(img, (90, 150, 220), (250, 220, 170), 1.3)
        paste(img, glow(260, (255, 250, 220), 0.9), 820, 380)
    mountains(img, hz, 60, (200, 150, 96) if not night else (40, 34, 40), 5, 0.3, peaks=2)
    ground(img, hz, SAND if not night else (60, 50, 50), (170, 126, 76) if not night else (24, 20, 22))


def sh_open(img, t, T, L):
    desert(img, t, 1200, True)
    paste(img, glow(140, (240, 240, 230), 1.0), 905, 700)     # luna algo más a la derecha: no toca el texto final
    ImageDraw.Draw(img).ellipse([865, 660, 945, 740], fill=(240, 240, 230))
    paste(img, pyramid(0, True), 380, 1200 - 300 + 4, 0.8)
    paste(img, pyramid(0, True, 600, 400), 800, 1200 - 200 + 4, 0.7)
    paste(img, cleopatra(), 760, 1330, 0.9)
    a1 = L[1][0]
    title2(t, a1 + 0.3, "CLEOPATRA, LA LUNA", "Y LAS PIRÁMIDES", 290, 52, 80, hold=max(1.5, T - a1 - 0.8))
    vignette(img, 170)


def sh_build(img, t, T, L):
    desert(img, t)
    q = clamp(t / T)
    paste(img, pyramid(round(0.3 - 0.25 * q, 2)), 540, 1200 - 300 + 4)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(80, 1200), (300, 1000), (340, 1000), (180, 1200)], fill=(190, 150, 96, 255))
    for i in range(6):
        x = (160 + i * 70 + t * 30) % 900 + 60
        paste(img, spr(person, 200, 520, (60, 40, 30), None, False, False, -1.4, round((t * 5 + i) % 6.28, 1)), x, 1290, 0.5)
    bx = (100 + t * 30) % 900 + 520
    d.rectangle([bx - 60, 1250, bx + 60, 1320], fill=(220, 190, 130, 255))
    date_stamp(t, 0.3, "GUIZA · ~2560 A. C.", 300, max(1.8, L[2][0] - 0.4))
    lower_third(img, t, L[2][0] + 0.1, "KEOPS", "FARAÓN DE EGIPTO", 300, 2.4)
    vignette(img, 150)


def sh_tallest(img, t, T, L):
    desert(img, t)
    paste(img, glow(400, (255, 250, 230), 0.5), 540, 760)
    paste(img, pyramid(0), 540, 1200 - 300 + 4, 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    k = ease(clamp((t - 0.4) / 1.0))
    top = 1200 - 600 * 0.98
    d.line([(980, 1200), (980, lerp(1200, top, k))], fill=(255, 255, 255, 230), width=5)
    d.line([(950, top), (1010, top)], fill=(255, 255, 255, int(230 * k)), width=5)
    dd = td()
    if k > 0.5:
        dd.text((860, top - 70), "146 M", font=f(F_SER, 50), fill=(255, 255, 255, 255))
    big(t, L[0][0] + 2.6, "3.800 AÑOS", 300, 110, YEL, sub="LO MÁS ALTO DEL MUNDO")
    vignette(img, 150)


def sh_centuries(img, t, T, L):
    cyc = (t * 1.6) % 1.0
    day = math.sin(cyc * math.pi)
    top = tuple(int(lerp(a, b, day)) for a, b in zip((8, 10, 26), (90, 150, 220)))
    bot = tuple(int(lerp(a, b, day)) for a, b in zip((40, 34, 60), (250, 220, 170)))
    sky(img, top, bot, 1.3)
    sx = lerp(-100, W + 100, cyc)
    sy = 900 - math.sin(cyc * math.pi) * 500
    paste(img, glow(160, (255, 240, 200), 1.0), sx, sy)
    mountains(img, 1200, 60, (200, 150, 96), 5, 0.3, peaks=2)
    ground(img, 1200, SAND, (170, 126, 76))
    paste(img, pyramid(0), 540, 1200 - 300 + 4)
    yr = int(lerp(2560, 30, clamp(t / (T - 0.3))))
    big(t, 0.2, f"{yr:,} A. C.".replace(",", "."), 300, 104, YEL, pop=False)
    vignette(img, 150)


def sh_queen(img, t, T, L):
    sky(img, (40, 30, 60), (220, 140, 90), 1.2)
    d = ImageDraw.Draw(img, "RGBA")
    for x in (80, 300, 780, 1000):
        d.rectangle([x - 40, 400, x + 40, 1300], fill=(220, 196, 150))
        d.rectangle([x - 60, 380, x + 60, 420], fill=(200, 176, 130))
    d.rectangle([0, 1300, W, H], fill=(120, 90, 60))
    paste(img, palm2(), 540, 1050, 1.2)
    paste(img, glow(400, (255, 200, 120), 0.6), 560, 900)
    paste(img, cleopatra(), 560, 1000, 1.6)
    lower_third(img, t, 0.4, "CLEOPATRA VII", "LA ÚLTIMA REINA DE EGIPTO", 300, max(2.4, L[1][0] - 0.8))
    a1 = L[1][0]
    if t > a1:
        big(t, a1 + 0.6, "MACEDONIA", 300, 104, YEL, sub="SU FAMILIA ERA GRIEGA", pop=False)
    vignette(img, 170)


def sh_death(img, t, T, L):
    desert(img, t, 1200, False, True)
    paste(img, pyramid(0), 620, 1200 - 300 + 4, 1.0)
    paste(img, cleopatra(), 220, 1300, 0.8)
    a1, a2 = L[1][0], L[2][0]
    if t < a1:
        date_stamp(t, 0.3, "AÑO 30 A. C.", 300)
    elif t < a2:
        big(t, a1 + 0.2, counter(t, a1 + 0.2, a1 + 1.6, 0, 2530) + " AÑOS", 300, 110, YEL, sub="TENÍA YA LA PIRÁMIDE")
    else:
        big(t, a2 + 0.1, "UNA ANTIGÜEDAD", 300, 96, WHITE, pop=False)
    vignette(img, 170)


def sh_moon(img, t, T, L):
    space_bg(img, t, 4, ((30, 30, 60), (20, 30, 50)), 300)
    paste(img, spr(globe_sprite, 30.0, 25.0, 110, ()), 880, 880)
    paste(img, moon_ground(), 540, 1520)
    paste(img, lem(), 360, 1150, 0.8)
    paste(img, astronaut(True), 700, 1200, 0.85)
    a1, a2 = L[1][0], L[2][0]
    if t < a2:
        date_stamp(t, 0.3, "20 · 07 · 1969", 300)
    else:
        big(t, a2 + 0.2, "≈ 2.000 AÑOS", 300, 110, YEL, sub="DESDE CLEOPATRA")
    vignette(img, 170)


def sh_answer(img, t, T, L):
    sky(img, (14, 14, 22), (6, 6, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y = 90, 990, 1000

    def X(yr):
        return x0 + (yr + 2560) / (1969 + 2560) * (x1 - x0)

    k = ease(clamp((t - 0.2) / 1.2))
    d.line([(x0, y), (x0 + (x1 - x0) * k, y)], fill=(255, 255, 255, 230), width=6)
    dd = td()
    for yr, lab, icon, t0 in ((-2560, "PIRÁMIDE", "pyr", 0.4), (-30, "CLEOPATRA", "cleo", 1.0), (1969, "LUNA", "moon", 1.6)):
        kk = ease(clamp((t - t0) / 0.5))
        if kk <= 0:
            continue
        x = X(yr)
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=YEL + (int(255 * kk),))
        tw = dd.textlength(lab, font=f(F_SER, 36))
        dd.text((min(max(10, x - tw / 2), W - tw - 10), y + 40), lab, font=f(F_SER, 36), fill=(255, 255, 255, int(255 * kk)))
        if icon == "pyr":
            paste(img, pyramid(0, False, 300, 200), x + 40, y - 140, 0.8, kk)
        elif icon == "cleo":
            paste(img, cleopatra((40, 34, 44)), x, y - 170, 0.5, kk)
        else:
            paste(img, glow(60, (240, 240, 230), 1.0), x - 30, y - 130, 1.0, kk)
            d.ellipse([x - 70, y - 170, x + 10, y - 90], fill=(236, 236, 228, int(255 * kk)))
    a1 = L[1][0]
    if t > a1:
        kk = ease(clamp((t - a1) / 0.8))
        d.line([(X(-2560), y + 140), (X(-2560) + (X(-30) - X(-2560)) * kk, y + 140)], fill=(200, 200, 210, 255), width=14)
        d.line([(X(-30), y + 190), (X(-30) + (X(1969) - X(-30)) * kk, y + 190)], fill=YEL + (255,), width=14)
        dd.text((X(-2560) + 10, y + 150), "2.530 AÑOS", font=f(F_SER, 32), fill=(220, 220, 230, int(255 * kk)))
        dd.text((X(-30) + 10, y + 200), "1.998 AÑOS", font=f(F_SER, 32), fill=YEL + (int(255 * kk),))
        big(t, a1 + 0.8, "MÁS CERCA", 300, 110, YEL, sub="DE LA LUNA")
    vignette(img, 180)


def sh_final(img, t, T, L):
    desert(img, t, 1200, True)
    paste(img, glow(140, (240, 240, 230), 1.0), 905, 700)     # luna algo más a la derecha: no toca el texto final
    ImageDraw.Draw(img).ellipse([865, 660, 945, 740], fill=(240, 240, 230))
    paste(img, pyramid(0, True), 380, 1200 - 300 + 4, 0.8)
    paste(img, pyramid(0, True, 600, 400), 800, 1200 - 200 + 4, 0.7)
    vignette(img, 170)
    # la reflexión final, en pantalla
    title2(t, 0.4, "HAY COSAS TAN ANTIGUAS…", "QUE YA ERAN ANTIGUAS", 250, 52, 76, hold=max(2.0, T - 0.8), c1=WHITE, c2=YEL)
    a, b = L[0]
    title2(t, a + (b - a) * 0.6, "PARA LOS ANTIGUOS", None, 420, 60, hold=max(1.5, T - 2.0), c1=WHITE)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "drone"), ("build", "epic"), ("queen", "premium"), ("death", "doc"), ("moon", "space"), ("answer", "epic"),
              ("final", "space")],
    "amb": {"wind": ["open", "build", "tallest", "centuries", "death", "final"], "space": ["moon"]},
    "sfx": [("open@L1+0.2", "pop", 0.2), ("build+0.3", "thud", 0.2), ("build+1.5", "thud", 0.2), ("build@L2+0.1", "chime", 0.05),
            ("tallest+0.4", "riser", 0.12), ("tallest@L0+2.6", "impact", 0.25),
            ("centuries", "whoosh", 0.15), ("centuries+1.0", "whoosh", 0.12), ("centuries+2.0", "whoosh", 0.12),
            ("queen+0.3", "chime", 0.06), ("queen@L1+0.6", "impact", 0.2),
            ("death@L1+0.2", "riser", 0.12), ("death@L1+1.6", "impact", 0.25),
            ("moon+0.2", "static", 0.1), ("moon@L2+0.2", "impact", 0.25),
            ("answer+0.2", "whoosh_up", 0.12), ("answer+0.4", "pop", 0.2), ("answer+1.0", "pop", 0.2), ("answer+1.6", "pop", 0.2),
            ("answer@L1", "riser_long", 0.14), ("answer@L1+0.8", "impact", 0.3), ("final+0.3", "chime", 0.06)],
    "bed": [("build", "death"), ("answer", "end")],
    "bpm": 90,
}
