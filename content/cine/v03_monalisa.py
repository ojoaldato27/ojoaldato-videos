"""V03 · Por qué la Mona Lisa es tan famosa (el robo de 1911)."""
from cine import *

TITLE = "Por_que_la_Mona_Lisa_es_tan_famosa"
LINES = [
    "Hasta 1911, la Mona Lisa *no era* el cuadro más famoso del mundo.",
    "¿Qué pasó para que de repente *todo el mundo* quisiera verla?",
    "París. Lunes, 21 de agosto de 1911.",
    "El Louvre está *cerrado* al público.",
    "Un hombre con bata blanca, como los trabajadores del museo, entra en la sala.",
    "Se llama *Vincenzo Peruggia*, y había trabajado allí.",
    "Descuelga el cuadro… y deja el marco en una escalera.",
    "Lo envuelve en su bata… y *sale tan tranquilo*.",
    "Hasta un fontanero le abre una puerta, creyendo que es un empleado.",
    "Nadie se da cuenta hasta *el día siguiente*.",
    "Y entonces… *escándalo mundial*.",
    "Los periódicos lo cuentan en medio planeta.",
    "El poeta Apollinaire fue detenido… y hasta *Picasso* fue interrogado.",
    "Y la gente hacía cola para ver… *el hueco vacío* en la pared.",
    "Pasan *más de dos años*.",
    "Peruggia la tenía escondida en un baúl, en su piso de París.",
    "En 1913 intenta venderla en Florencia… y *lo pillan*.",
    "Allí, *30.000 personas* corrieron a verla.",
    "Cuando volvió al Louvre, ya era *el cuadro más famoso del planeta*.",
    "Un robo la hizo famosa… *para siempre*.",
]
SHOTS = [("open", 0, 1, 0.3), ("louvre", 2, 3, 0.3), ("smock", 4, 5, 0.3), ("take", 6, 6, 0.2), ("exit", 7, 8, 0.3),
         ("empty", 9, 9, 0.2), ("scandal", 10, 11, 0.3), ("suspects", 12, 12, 0.3), ("queue", 13, 13, 0.3),
         ("years", 14, 15, 0.3), ("florence", 16, 17, 0.3), ("famous", 18, 19, 1.8)]
FOCUS = {"open": (540, 860), "louvre": (540, 900), "smock": (520, 1000), "take": (540, 860), "exit": (560, 980),
         "empty": (540, 860), "scandal": (540, 900), "queue": (540, 900), "years": (620, 1060), "florence": (540, 900),
         "famous": (540, 860)}
NOTIF = ("take", 0.6)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿QUÉ PASÓ', 'PARA QUE TODOS QUISIERAN VERLA?'], "delay": [0, 0.9]}
STICKER_EXTRA = [('cuadro', '🖼️'), ('famos', '⭐'), ('lunes', '📅'), ('louvre', '🏛️'), ('cerrado', '🔒'), ('bata', '🥼'), ('peruggia', '🕵️'), ('descuelga', '🖼️'), ('marco', '🖼️'), ('envuelve', '🥼'), ('tranquilo', '😎'), ('fontanero', '🔧'), ('puerta', '🚪'), ('escandalo', '😱'), ('periodico', '📰'), ('poeta', '✍️'), ('detenido', '🚓'), ('picasso', '🎨'), ('cola', '👥'), ('hueco', '🕳️'), ('anos', '⏳'), ('baul', '🧳'), ('pillan', '🚨'), ('personas', '👥'), ('planeta', '🌍'), ('robo', '🦹'), ('siempre', '♾️')]

def monalisa(w=420, h=600):
    def fn(d, s):
        for y in range(h):
            u = y / h
            c = (int(lerp(110, 50, u)), int(lerp(120, 60, u)), int(lerp(90, 40, u)))
            d.line([(0, y * s), (w * s, y * s)], fill=c, width=int(s) + 1)
        d.polygon(sc([(0, 210), (60, 180), (120, 220), (90, 260), (0, 270)], s), fill=(90, 110, 100))
        d.polygon(sc([(w, 170), (w - 70, 160), (w - 120, 210), (w - 40, 240), (w, 250)], s), fill=(90, 110, 100))
        cx = w / 2
        dress = (44, 34, 24)
        d.polygon(sc([(cx - 70, 300), (cx + 70, 300), (cx + 190, h), (cx - 190, h)], s), fill=dress)
        d.polygon(sc([(cx - 52, 300), (cx + 52, 300), (cx, 390)], s), fill=(214, 170, 120))
        d.ellipse(sb([cx - 68, 120, cx + 68, 300], s), fill=(40, 28, 20))
        d.ellipse(sb([cx - 50, 140, cx + 50, 270], s), fill=(222, 178, 126))
        d.polygon(sc([(cx - 70, 170), (cx - 50, 160), (cx - 56, 330), (cx - 88, 330)], s), fill=(40, 28, 20))
        d.polygon(sc([(cx + 70, 170), (cx + 50, 160), (cx + 56, 330), (cx + 88, 330)], s), fill=(40, 28, 20))
        d.arc(sb([cx - 16, 222, cx + 16, 238], s), 20, 160, fill=(150, 90, 70), width=int(3 * s))
        for ex in (cx - 20, cx + 20):
            d.ellipse(sb([ex - 7, 195, ex + 7, 203], s), fill=(70, 50, 40))
        sleeve = (110, 84, 44)
        d.polygon(sc([(cx - 170, 430), (cx - 120, 420), (cx - 20, 490), (cx - 60, 530), (cx - 190, 520)], s), fill=sleeve)
        d.polygon(sc([(cx + 160, 440), (cx + 120, 430), (cx + 20, 480), (cx + 40, 520), (cx + 180, 520)], s), fill=sleeve)
        d.rounded_rectangle(sb([cx - 70, 478, cx + 30, 512], s), radius=int(16 * s), fill=(214, 170, 120))
        d.rounded_rectangle(sb([cx - 30, 466, cx + 70, 500], s), radius=int(16 * s), fill=(224, 180, 130))
    return sprite("mona", w, h, fn)


def frame(w=520, h=700, inner=(420, 600)):
    def fn(d, s):
        g1, g2, g3 = (150, 104, 40), (214, 166, 74), (250, 214, 130)
        d.rectangle(sb([0, 0, w, h], s), fill=g1)
        d.rectangle(sb([14, 14, w - 14, h - 14], s), fill=g2)
        d.rectangle(sb([30, 30, w - 30, h - 30], s), fill=g1)
        ix, iy = (w - inner[0]) / 2, (h - inner[1]) / 2
        d.rectangle(sb([ix - 6, iy - 6, ix + inner[0] + 6, iy + inner[1] + 6], s), fill=g3)
        d.rectangle(sb([ix, iy, ix + inner[0], iy + inner[1]], s), fill=(0, 0, 0, 0))
        for x, y in ((22, 22), (w - 22, 22), (22, h - 22), (w - 22, h - 22)):
            d.ellipse(sb([x - 16, y - 16, x + 16, y + 16], s), fill=g3)
    return sprite(("frame", w, h, inner), w, h, fn)


def painting_framed():
    im = frame().copy()
    m = monalisa()
    im.alpha_composite(m, (50, 50))
    return im


def gallery_wall(img, t, light=1.0):
    sky(img, (60, 44, 36), (28, 20, 16), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 270):
        d.rectangle([x + 10, 200, x + 260, 1260], outline=(90, 66, 52, 255), width=4)
    d.rectangle([0, 1260, W, 1300], fill=(70, 50, 40))
    d.rectangle([0, 1300, W, H], fill=(46, 30, 22))
    for x in range(-200, W + 200, 120):
        d.line([(540 + (x - 540) * 0.4, 1300), (x, H)], fill=(60, 40, 30), width=3)


def louvre():
    def fn(d, s):
        c, c2 = (190, 176, 150), (150, 136, 112)
        d.rectangle(sb([0, 200, 1080, 700], s), fill=c)
        d.polygon(sc([(300, 200), (540, 60), (780, 200)], s), fill=c2)
        d.rectangle(sb([0, 190, 1080, 210], s), fill=c2)
        for x in range(30, 1060, 90):
            d.rectangle(sb([x, 260, x + 50, 380], s), fill=(60, 56, 60))
            d.rectangle(sb([x, 460, x + 50, 600], s), fill=(60, 56, 60))
            d.rectangle(sb([x + 60, 220, x + 74, 690], s), fill=c2)
        d.rectangle(sb([470, 470, 610, 700], s), fill=(40, 34, 30))
    return sprite("louvre", 1080, 700, fn)


def trunk(glow_=0.0):
    def fn(d, s):
        d.rounded_rectangle(sb([20, 120, 580, 400], s), radius=int(16 * s), fill=(96, 60, 34))
        d.rounded_rectangle(sb([20, 40, 580, 150], s), radius=int(40 * s), fill=(116, 74, 42))
        for x in (90, 300, 510):
            d.rectangle(sb([x - 14, 40, x + 14, 400], s), fill=(60, 40, 24))
        d.rectangle(sb([270, 150, 330, 210], s), fill=(200, 160, 70))
        d.line(sc([(20, 150), (580, 150)], s), fill=(40, 26, 16), width=int(6 * s))
    return sprite("trunk", 600, 420, fn)


def florence():
    def fn(d, s):
        c = (34, 26, 36)
        rr = random.Random(4)
        x = 0
        while x < W:
            bw = rr.uniform(70, 140)
            bh = rr.uniform(120, 220)
            d.rectangle(sb([x, 500 - bh, x + bw, 500], s), fill=c)
            d.polygon(sc([(x - 8, 500 - bh), (x + bw / 2, 500 - bh - 30), (x + bw + 8, 500 - bh)], s), fill=c)
            x += bw
        d.ellipse(sb([380, 120, 640, 400], s), fill=c)
        d.rectangle(sb([360, 260, 660, 420], s), fill=c)
        d.rectangle(sb([495, 70, 525, 130], s), fill=c)
        d.rectangle(sb([760, 40, 810, 420], s), fill=c)
        d.rectangle(sb([750, 30, 820, 60], s), fill=c)
    return sprite("florence", W, 500, fn)


def hooks(d, cx, cy, a=255):
    for dx, dy in ((-150, -230), (150, -230), (-150, 230), (150, 230)):
        x, y = cx + dx, cy + dy
        d.line([(x, y - 18), (x, y + 10)], fill=(30, 26, 24, a), width=8)
        d.line([(x, y + 10), (x + 14, y + 10)], fill=(30, 26, 24, a), width=8)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    gallery_wall(img, t)
    spotlight(img, t, 540, 0, 1300, 120, 520, 60)
    paste(img, glow(420, (255, 220, 160), 0.5), 540, 860)
    paste(img, spr(painting_framed), 540, 860, 1.12 + 0.03 * ease(clamp(t / T)))
    title2(t, 0.25, "LA MONA LISA", "¿POR QUÉ ES TAN FAMOSA?", 230, 64, 62, hold=max(1.5, L[1][0] - 0.4))
    vignette(img, 200)


def sh_louvre(img, t, T, L):
    sky(img, (120, 140, 180), (230, 200, 170), 1.2)
    clouds(img, t, 420, (255, 255, 255), 110, 8, 7, 1.2)
    paste(img, louvre(), 540, 1250 - 350)
    ground(img, 1250, (150, 140, 120), (90, 84, 70))
    date_stamp(t, 0.3, "LUNES · 21 · 08 · 1911", 300, max(2.0, L[1][0] - 0.2))
    a1 = L[1][0] + 0.3
    if t > a1:
        k = ease(clamp((t - a1) / 0.3))
        st = Image.new("RGBA", (520, 200), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([10, 20, 510, 180], radius=16, fill=(200, 40, 40, 235))
        tw = sd.textlength("FERMÉ", font=f(F_SER, 96))
        sd.text(((520 - tw) / 2, 36), "FERMÉ", font=f(F_SER, 96), fill=(255, 255, 255, 255))
        paste(img, st, 540, 1080, lerp(1.4, 1.0, k), k, -4)
        big(t, a1, "CERRADO", 300, 100, WHITE)
    vignette(img, 160)


def sh_smock(img, t, T, L):
    gallery_wall(img, t)
    d = ImageDraw.Draw(img, "RGBA")
    for x in (120, 960):
        d.rectangle([x - 110, 520, x + 110, 900], fill=(150, 110, 50))
        d.rectangle([x - 90, 540, x + 90, 880], fill=(80, 70, 60))
    x = lerp(120, 560, ease(clamp(t / (T * 0.8))))
    paste(img, spr(person, 240, 600, (232, 230, 222), "cap", True, False, 0.0, round((t * 6) % 6.28, 1)), x, 1010, 1.15)
    lower_third(img, t, L[1][0] + 0.2, "VINCENZO PERUGGIA", "ANTIGUO TRABAJADOR DEL LOUVRE", 300, 3.2)
    vignette(img, 200)


def sh_take(img, t, T, L):
    gallery_wall(img, t)
    spotlight(img, t, 540, 0, 1300, 120, 520, 50)
    q = ease(clamp((t - 0.6) / 1.4))
    d = ImageDraw.Draw(img, "RGBA")
    hooks(d, 540, 800)
    paste(img, spr(painting_framed), 540 + 260 * q, 800 + 120 * q, 1.0 - 0.1 * q, 1.0, -8 * q)
    if t > 2.2:
        k = ease(clamp((t - 2.2) / 0.8))
        fr = frame()
        paste(img, fr, 300, 1200, 0.6, k, 30)
    vignette(img, 210)


def sh_exit(img, t, T, L):
    sky(img, (30, 26, 24), (14, 12, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([300, 600, 780, 1300], fill=(60, 44, 34))
    op = ease(clamp((t - L[1][0] - 0.3) / 0.8))
    d.rectangle([320, 620, 760, 1300], fill=(255, 236, 200))
    paste(img, glow(420, (255, 230, 180), 0.6), 540, 980, 1.0, 0.4 + 0.6 * op)
    dw = 440 * (1 - op * 0.85)
    d.rectangle([320, 620, 320 + dw, 1300], fill=(90, 66, 50))
    d.ellipse([300 + dw - 10, 860, 300 + dw + 10, 880], fill=(200, 160, 70))
    d.rectangle([0, 1300, W, H], fill=(30, 22, 18))
    if t > L[1][0]:
        paste(img, spr(person, 240, 600, (20, 18, 18), "cap", True, False, -0.8), 860, 1010, 1.1)
    x = lerp(140, 520, ease(clamp(t / (T * 0.9))))
    paste(img, spr(person, 240, 600, (232, 230, 222), "cap", True, False, -0.9, round((t * 6) % 6.28, 1)), x, 1010, 1.1)
    d2 = ImageDraw.Draw(img, "RGBA")
    d2.rounded_rectangle([x + 10, 880, x + 120, 1030], radius=10, fill=(230, 228, 218))
    lower_third(img, t, L[1][0] + 0.4, "UN FONTANERO", "LE ABRE LA PUERTA", 300, 3.0)
    vignette(img, 210)


def sh_empty(img, t, T, L):
    gallery_wall(img, t)
    spotlight(img, t, 540, 0, 1300, 120, 520, 55)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([540 - 230, 800 - 310, 540 + 230, 800 + 310], fill=(70, 52, 42))
    hooks(d, 540, 800)
    date_stamp(t, 0.3, "22 · 08 · 1911", 300)
    vignette(img, 210)


def sh_scandal(img, t, T, L):
    sky(img, (20, 18, 16), (6, 5, 4), 1.0)
    rays(img, t, 540, 900, 16, (255, 220, 160), 18, 1400, 0.07, 0.06)
    heads = [("LA JOCONDE\nA DISPARU", "PARIS · 1911"), ("MONA LISA\nSTOLEN!", "NEW YORK · 1911"),
             ("RUBATA\nLA GIOCONDA", "ROMA · 1911"), ("¡ROBADA LA\nGIOCONDA!", "MADRID · 1911")]
    for i, (hd, dt) in enumerate(heads):
        t0 = 0.3 + i * 0.7
        if t < t0:
            continue
        k = ease(clamp((t - t0) / 0.5))
        im = spr(newspaper, hd, "", dt, 560, 720, i)
        ang = (1 - k) * 360 * (1 if i % 2 else -1) + (-8, 6, -4, 9)[i]
        x = 540 + (-200, 190, -150, 170)[i] * k
        y = 900 + (-200, -90, 160, 260)[i] * k
        paste(img, im, x, y, lerp(0.2, 0.8, k), 1.0, ang)
    big(t, 0.2, "ESCÁNDALO", 280, 104, YEL, sub="MUNDIAL")
    vignette(img, 200)


def sh_suspects(img, t, T, L):
    gallery_wall(img, t)
    for i, (x, nm, st) in enumerate(((290, "APOLLINAIRE", "DETENIDO"), (790, "PICASSO", "INTERROGADO"))):
        t0 = 0.2 if i == 0 else L[0][0] + 2.2
        k = ease(clamp((t - t0) / 0.5))
        if k <= 0:
            continue
        fr = Image.new("RGBA", (380, 500), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fr)
        fd.rectangle([0, 0, 379, 499], fill=(150, 104, 40, 255))
        fd.rectangle([20, 20, 359, 479], fill=(70, 64, 60, 255))
        paste(fr, spr(person, 240, 600, (20, 18, 20), "bowler" if i == 0 else None, True), 190, 380, 0.9)
        paste(img, fr, x, 840, 1.0, k)
        d = td()
        spaced(d, x, 1130, nm, f(F_SER, 46), (255, 255, 255, int(255 * k)), 5)
        spaced(d, x, 1190, st, f(F_SER, 40), YEL + (int(255 * k),), 6)
    big(t, 0.2, "SOSPECHOSOS", 300, 90, WHITE, pop=False)
    vignette(img, 200)


def sh_queue(img, t, T, L):
    gallery_wall(img, t)
    spotlight(img, t, 540, 0, 1300, 120, 520, 55)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([540 - 180, 700 - 240, 540 + 180, 700 + 240], fill=(70, 52, 42))
    for dx, dy in ((-120, -180), (120, -180), (-120, 180), (120, 180)):
        d.line([(540 + dx, 700 + dy - 14), (540 + dx, 700 + dy + 8)], fill=(30, 26, 24), width=7)
    rr = random.Random(3)
    for i in range(9):
        x = 60 + i * 120 + math.sin(t + i) * 4
        hat = ("bowler", "top", None, "cap")[i % 4]
        paste(img, spr(person, 220, 560, (16, 12, 12) if i % 2 else (24, 18, 18), hat, True, i % 3 == 2), x, 1260, 0.9 + (i % 2) * 0.08)
    big(t, L[0][0] + 1.8, "UN HUECO VACÍO", 300, 92, YEL, pop=False)
    vignette(img, 200)


def sh_years(img, t, T, L):
    sky(img, (24, 20, 30), (8, 6, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(0, 300), (540, 120), (1080, 300), (1080, 0), (0, 0)], fill=(14, 12, 16))
    d.rectangle([0, 1300, W, H], fill=(40, 28, 20))
    for x in range(0, W, 90):
        d.line([(x, 1300), (x, H)], fill=(30, 20, 14), width=3)
    paste(img, glow(300, (255, 200, 140), 0.5), 820, 560)
    d.rectangle([760, 460, 880, 640], fill=(40, 50, 80))
    d.line([(820, 460), (820, 640)], fill=(20, 16, 20), width=6)
    d.line([(760, 550), (880, 550)], fill=(20, 16, 20), width=6)
    if t < L[1][0]:
        yrs = ["1911", "1912", "1913"]
        k = int(clamp((t - 0.3) / (max(0.6, L[0][1] - 0.6)), 0, 0.999) * 3)
        big(t, 0.3, yrs[k], 360, 170, YEL, pop=False)
    else:
        paste(img, glow(240, (255, 200, 120), 0.5), 600, 1180, 1.0, 0.5 + 0.2 * math.sin(t * 3))
        big(t, L[1][0], "UN BAÚL", 330, 110, WHITE, sub="EN SU PISO DE PARÍS")
    paste(img, trunk(), 600, 1180, 1.0)
    vignette(img, 210)


def sh_florence(img, t, T, L):
    sky(img, (60, 50, 90), (250, 160, 110), 1.3)
    paste(img, glow(360, (255, 190, 130), 0.7), 300, 1000)
    paste(img, florence(), 540, 1240 - 250)
    ground(img, 1240, (30, 24, 30), (10, 8, 10))
    date_stamp(t, 0.3, "FLORENCIA · 1913", 300, max(1.6, L[1][0] - 0.8))
    if t > L[1][0]:
        rr = random.Random(5)
        for i in range(16):
            x = 30 + i * 66
            paste(img, spr(person, 200, 520, (14, 10, 14), (None, "cap", "bowler")[i % 3], i % 2 == 0, i % 4 == 1), x, 1400 + (i % 2) * 30, 0.62)
        big(t, L[1][0] + 0.2, counter(t, L[1][0] + 0.2, L[1][0] + 1.8, 0, 30000), 300, 124, YEL, sub="PERSONAS")
    vignette(img, 170)


def sh_famous(img, t, T, L):
    gallery_wall(img, t)
    spotlight(img, t, 540, 0, 1300, 120, 520, 70)
    paste(img, glow(440, (255, 220, 160), 0.6), 540, 760)
    paste(img, spr(painting_framed), 540, 760, 0.95)
    rr = random.Random(int(t * 5))
    for _ in range(3):
        if rr.random() < 0.5:
            x, y = rr.uniform(100, 980), rr.uniform(1050, 1250)
            paste(img, glow(120, (255, 255, 255), 1.0), x, y, 1.0, 0.9)
    for i in range(10):
        x = 40 + i * 112
        paste(img, spr(person, 200, 520, (12, 10, 14), (None, "cap")[i % 2], True, i % 3 == 0, -2.6 if i % 4 == 1 else 0.0), x, 1330, 0.8)
    lower_third(img, t, 0.3, "EL CUADRO MÁS FAMOSO", "DEL PLANETA", 300, max(2.5, L[0][1] + 0.4))
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "premium"), ("smock", "tension"), ("scandal", "doc"), ("years", "drone"), ("florence", "doc")],
    "gains": {"premium": 0.9},
    "amb": {"room": ["open", "smock", "take", "empty", "suspects", "famous", "years"], "city": ["louvre", "florence"],
            "crowd": ["queue", "famous"]},
    "sfx": [("open+0.2", "chime", 0.06), ("louvre@L1+0.3", "thud", 0.45),
            ("smock", "heart", 0.3), ("smock+0.8", "heart", 0.3), ("smock+1.6", "heart", 0.3),
            ("take+0.6", "whoosh", 0.12), ("take+2.2", "thud", 0.3),
            ("exit@L1+0.3", "knock", 0.3), ("empty+0.3", "riser", 0.12), ("empty+1.5", "impact", 0.3),
            ("scandal+0.3", "paper", 0.3), ("scandal+1.0", "paper", 0.3), ("scandal+1.7", "paper", 0.3), ("scandal+2.4", "paper", 0.3),
            ("suspects+0.2", "shutter", 0.3), ("suspects@L0+2.2", "shutter", 0.3),
            ("years+0.3", "tick", 0.2), ("years+1.3", "tick", 0.2), ("years+2.3", "tick", 0.2),
            ("florence@L1+0.2", "riser", 0.1),
            ("famous+0.2", "swell", 0.2), ("famous+0.6", "shutter", 0.2), ("famous+1.4", "shutter", 0.2), ("famous+2.3", "shutter", 0.2)],
    "bed": [("louvre", "years"), ("florence", "end")],
    "bpm": 90,
}
