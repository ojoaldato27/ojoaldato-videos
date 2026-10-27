"""T01 · ¿Qué cambia de ir a 100 o a 140? — v2 con el estilo del microondas:
objetos grandes y detallados, vistas por dentro (rayos X) y etiquetas con flecha."""
from gadgets import *
import t02_microondas as T2
import t04_qr as T4

xf, callout, glow_line, top_shade, check = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T4.check

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
FOCUS = {"fall": (540, 900, 1.1), "verdict": (540, 1000, 1.08)}
NOTIF = ("react", 1.2)
KW_OVERRIDE = {3: ["39 METROS"]}
KW_ZONES = {"open": [1, 4], "meters": [1, 8, 10, 9], "react": [9, 4, 10, 1], "rule": [10, 8, 9, 5], "energy": [1, 4, 10, 9],
            "fall": [5, 9, 4], "air": [8, 1, 10, 9], "fine": [4, 9, 5], "time": [5, 8, 9], "verdict": [0, 3, 10]}
HYPE = {"line": 0, "text": ['¿QUÉ CAMBIA', 'DE IR A 100 O A 140?'], "delay": [0, 0.75]}
NOTIF_TEXT = "Suscríbete para más cosas que no sabías"

RED = (196, 30, 36)
CY_ = (110, 210, 255)
ORANGE = (255, 150, 60)


# ------------------------------------------------------------------ objetos detallados
def speedo_face(maxv=240):
    c = Cv(800, 800)
    cx = cy = 400
    c.shadow((40, 60, 760, 790), 180, 18)
    c.ellipse((10, 10, 790, 790), radial=((236, 238, 244), (90, 94, 104)), power=0.7, center=(0.38, 0.3))
    c.ellipse((34, 34, 766, 766), radial=((60, 62, 70), (20, 20, 24)), power=1.0)
    c.ellipse((48, 48, 752, 752), radial=((26, 30, 40), (6, 7, 10)), power=1.1, center=(0.5, 0.42))
    a0, a1 = 135, 405
    for v in range(0, maxv + 1, 5):
        a = math.radians(a0 + (a1 - a0) * v / maxv)
        major = v % 20 == 0
        r0, r1 = (300, 352) if major else ((322, 352) if v % 10 == 0 else (334, 352))
        col = (255, 80, 70) if v >= 200 else (220, 236, 255)
        c.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1)], col, 7 if major else 3)
        if major:
            c.text((cx + math.cos(a) * 252, cy + math.sin(a) * 252), str(v), 40, col)
    c.arc((60, 60, 740, 740), a0 + (a1 - a0) * 200 / maxv, a1, (255, 60, 50, 160), 10)
    c.arc((90, 90, 710, 710), 200, 250, (255, 255, 255, 40), 6)
    c.text((cx, cy + 120), "km/h", 34, (150, 170, 200))
    return c.done()


def speedo(img, x, y, s, v, glow_k=1.0):
    paste(img, spr(speedo_face), x, y, s)
    a = math.radians(135 + 270 * clamp(v / 240))
    r = 330 * s
    tip = (x + math.cos(a) * r, y + math.sin(a) * r)
    tail = (x - math.cos(a) * 50 * s, y - math.sin(a) * 50 * s)
    glow_line(img, [tail, tip], (255, 80, 60), int(10 * s) + 2, 10, 255)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([x - 44 * s, y - 44 * s, x + 44 * s, y + 44 * s], fill=(40, 42, 50, 255), outline=(150, 154, 166, 255), width=4)
    d.rounded_rectangle([x - 130 * s, y + 170 * s, x + 130 * s, y + 250 * s], radius=14, fill=(4, 8, 14, 240), outline=(60, 90, 130, 255), width=3)
    d.text((x, y + 210 * s), f"{int(round(v))}", font=f(F_MONO, int(64 * s)), fill=CY_ + (255,), anchor="mm")
    paste(img, glow(int(260 * s), (60, 140, 255), 0.25), x, y, 1.0, glow_k)


def _dash():
    c = Cv(W, H, 2)
    c.poly([(0, 760), (240, 700), (540, 680), (840, 700), (1080, 760), (1080, H), (0, H)], grad=((40, 40, 46), (10, 10, 12)))
    c.poly([(0, 760), (240, 700), (540, 680), (840, 700), (1080, 760), (1080, 790), (840, 730), (540, 712), (240, 730), (0, 790)],
           fill=(70, 72, 82))
    c.ellipse((90, 760, 990, 1400), radial=((30, 32, 40), (14, 14, 18)))
    c.arc((90, 760, 990, 1400), 190, 350, (120, 130, 150, 120), 4)
    for x0 in (60, 880):
        c.ellipse((x0, 980, x0 + 140, 1120), radial=((40, 42, 50), (16, 16, 20)))
        for k in range(8):
            c.line([(x0 + 20 + k * 14, 1000), (x0 + 20 + k * 14, 1100)], (60, 62, 70), 3)
    c.arc((-260, 1420, 1340, 2600), 200, 340, (70, 72, 80), 70)
    for k in range(40):
        a = math.radians(200 + k * 3.5)
        x, y = 540 + math.cos(a) * 800, 2010 + math.sin(a) * 590
        c.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(120, 110, 100))
    return c.done().convert("RGBA")


def tape_case():
    c = Cv(300, 300)
    c.shadow((20, 250, 290, 300), 160, 10)
    c.rect((20, 30, 280, 270), grad=((255, 214, 60), (200, 150, 20)), r=50)
    c.rect((40, 50, 260, 250), grad=((40, 40, 44), (14, 14, 16)), r=40)
    c.ellipse((90, 90, 210, 210), radial=((200, 200, 206), (110, 114, 122)), center=(0.4, 0.35))
    c.text((150, 150), "50 m", 30, (30, 30, 34))
    c.rect((40, 60, 120, 76), fill=(255, 255, 255, 70), r=6)
    return c.done()


def tape(img, x0, y, length_px, px_per_m, maxm):
    if length_px <= 4:
        return
    d = ImageDraw.Draw(img, "RGBA")
    x1 = x0 + length_px
    d.rectangle([x0, y - 26, x1, y + 26], fill=(255, 210, 50, 255))
    d.rectangle([x0, y - 26, x1, y - 20], fill=(255, 240, 160, 255))
    d.rectangle([x0, y + 20, x1, y + 26], fill=(190, 140, 20, 255))
    for m in range(0, maxm + 1):
        x = x0 + m * px_per_m
        if x > x1:
            break
        hh = 22 if m % 5 == 0 else 10
        d.line([(x, y - 26), (x, y - 26 + hh)], fill=(20, 20, 20, 255), width=3)
        if m % 5 == 0 and m > 0:
            d.text((x, y + 6), str(m), font=f(F_CAP, 22), fill=(20, 20, 20), anchor="mm")
    d.rectangle([x1 - 4, y - 40, x1 + 8, y + 30], fill=(170, 174, 184, 255))


def stopwatch():
    c = Cv(380, 440)
    c.shadow((40, 390, 340, 440), 160, 12)
    c.rect((160, 0, 220, 50), grad=((220, 224, 232), (120, 124, 132)), horizontal=True, r=10)
    c.rect((130, 36, 250, 60), grad=((200, 204, 212), (110, 114, 122)), r=8)
    c.line([(300, 90), (330, 60)], (150, 154, 162), 22)
    c.ellipse((20, 60, 360, 400), radial=((240, 242, 248), (110, 114, 124)), power=0.7, center=(0.36, 0.3))
    c.ellipse((44, 84, 336, 376), radial=((255, 255, 255), (220, 222, 228)), center=(0.45, 0.4))
    for k in range(60):
        a = math.radians(k * 6 - 90)
        r0 = 122 if k % 5 == 0 else 132
        c.line([(190 + math.cos(a) * r0, 230 + math.sin(a) * r0), (190 + math.cos(a) * 140, 230 + math.sin(a) * 140)], (40, 40, 44), 5 if k % 5 == 0 else 2)
    c.ellipse((60, 100, 320, 220), fill=(255, 255, 255, 50))
    return c.done()


def stopwatch_at(img, x, y, s, secs, label=None, col=RED):
    paste(img, spr(stopwatch), x, y, s)
    cy = y + (230 - 220) * s
    a = math.radians(secs * 360 - 90)
    d = ImageDraw.Draw(img, "RGBA")
    if secs > 0.005:
        d.pieslice([x - 128 * s, cy - 128 * s, x + 128 * s, cy + 128 * s], -90, secs * 360 - 90, fill=col + (60,))
    d.line([(x, cy), (x + math.cos(a) * 128 * s, cy + math.sin(a) * 128 * s)], fill=col + (255,), width=int(8 * s) + 1)
    d.ellipse([x - 12 * s, cy - 12 * s, x + 12 * s, cy + 12 * s], fill=(40, 40, 44, 255))
    if label:
        d.text((x, cy + 70 * s), label, font=f(F_MONO, int(40 * s)), fill=(30, 30, 34), anchor="mm")


def asphalt(img, y0, y1, t, speed=1.0):
    def mk():
        rr = random.Random(3)
        im = Image.new("RGBA", (W * 2, 400), (48, 48, 54, 255))
        d = ImageDraw.Draw(im)
        for i in range(6000):
            x, y = rr.uniform(0, W * 2), rr.uniform(0, 400)
            v = rr.randint(30, 90)
            d.point((x, y), fill=(v, v, v + 4, 255))
        return im
    tex = cached("asphalt", mk)
    off = int((t * 900 * speed) % W)
    crop = tex.crop((off, 0, off + W, 400)).resize((W, int(y1 - y0)))
    img.paste(crop.convert("RGB"), (0, int(y0)))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, y0, W, y0 + 10], fill=(230, 230, 220, 255))
    o2 = (t * 900 * speed) % 300
    for x in range(-300, W + 300, 300):
        d.rectangle([x - o2, (y0 + y1) / 2 - 6, x - o2 + 160, (y0 + y1) / 2 + 6], fill=(240, 236, 220, 255))


def sky_day(img, hz):
    sky(img, (90, 150, 220), (210, 228, 240), 1.3, 0, hz)
    clouds(img, 0, hz - 520, (255, 255, 255), 130, 6, 8, 1.2)
    mountains(img, hz - 10, 150, (120, 140, 160), 3, 0.5)
    mountains(img, hz, 70, (90, 120, 96), 5, 0.6)
    ground(img, hz, (110, 130, 86), (70, 90, 56))


def _footwell():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((30, 30, 36), (10, 10, 12)))
    c.poly([(0, 1300), (1080, 1300), (1080, H), (0, H)], grad=((40, 40, 46), (20, 20, 24)))
    c.poly([(0, 1300), (1080, 1300), (1080, 1330), (0, 1330)], fill=(70, 70, 76))
    c.poly([(0, 400), (1080, 300), (1080, 560), (0, 640)], grad=((50, 52, 60), (26, 26, 30)))
    for k in range(18):
        x = 60 * k
        c.line([(x, 1340), (x + 40, H)], (34, 34, 38), 4)
    return c.done().convert("RGBA")


def shoe():
    c = Cv(460, 260)
    c.shadow((40, 200, 440, 260), 150, 10)
    c.poly([(30, 190), (60, 100), (180, 70), (260, 30), (340, 30), (400, 90), (440, 160), (440, 200), (30, 210)], grad=((250, 250, 252), (200, 204, 212)))
    c.poly([(20, 200), (450, 196), (450, 230), (20, 236)], grad=((240, 90, 60), (180, 50, 30)))
    for k in range(5):
        c.line([(200 + k * 24, 70 + k * 6), (230 + k * 24, 110 + k * 4)], (120, 124, 132), 5)
    c.poly([(330, 40), (400, 90), (370, 110), (300, 60)], fill=(230, 60, 66))
    c.line([(60, 160), (420, 150)], (180, 184, 192), 3)
    return c.done()


def pedals(img, t, press):
    """Corte del hueco de los pies: acelerador, freno y la zapatilla que pasa de uno a otro."""
    AC(img, cached("footwell", _footwell))
    d = ImageDraw.Draw(img, "RGBA")
    ax, bx = 760, 360
    for px, hgt, w_, lbl, down in ((ax, 420, 110, "ACELERADOR", 1 - press), (bx, 260, 220, "FRENO", press)):
        yb = 1240
        top = yb - hgt + 40 * down
        d.line([(px, top + hgt * 0.4), (px + 60, 560)], fill=(70, 72, 80, 255), width=14)
        d.rounded_rectangle([px - w_ / 2, top, px + w_ / 2, top + hgt * 0.55], radius=22, fill=(40, 40, 46, 255), outline=(110, 114, 124, 255), width=4)
        for k in range(5):
            yy = top + 24 + k * hgt * 0.09
            d.line([(px - w_ / 2 + 16, yy), (px + w_ / 2 - 16, yy)], fill=(80, 82, 92, 255), width=5)
        spaced(d, px, yb + 60, lbl, f(F_SER, 36), (220, 224, 235, 230), 5)
    p = ease(clamp(press))
    sx = lerp(ax, bx, p)
    lift = math.sin(math.pi * p) * 140
    sy = lerp(1240 - 420 - 10, 1240 - 260 - 10 + 40, p) - lift
    paste(img, spr(shoe), sx + 60, sy - 60, 1.0)


def squares(img, cx, cy, n, cell, k, col, label):
    d = ImageDraw.Draw(img, "RGBA")
    shown = int(n * n * k)
    x0, y0 = cx - n * cell / 2, cy - n * cell / 2
    d.rounded_rectangle([x0 - 14, y0 - 14, x0 + n * cell + 14, y0 + n * cell + 14], radius=16, fill=(0, 0, 0, 140), outline=col + (200,), width=4)
    for i in range(shown):
        r, cc = i // n, i % n
        x, y = x0 + cc * cell, y0 + r * cell
        d.rounded_rectangle([x + 2, y + 2, x + cell - 2, y + cell - 2], radius=3, fill=col + (230,))
        d.rectangle([x + 3, y + 3, x + cell - 4, y + 6], fill=(255, 255, 255, 70))
    spaced(d, cx, y0 + n * cell + 64, label, f(F_SER, 44), (255, 255, 255, 240), 3)


def car_xray(crush=0.0):
    c = Cv(1000, 420)
    dx = 150 * crush
    body = [(40, 300), (40, 230), (70, 196), (230, 178), (330, 110), (420, 84), (680, 82), (800, 160), (930 - dx, 186), (990 - dx, 220),
            (995 - dx, 290), (970 - dx, 316), (40, 316)]
    c.poly(body, fill=(196, 30, 36, 90), outline=(255, 120, 120), width=4)
    c.poly([(340, 116), (420, 92), (670, 92), (780, 164), (340, 168)], fill=(120, 170, 220, 70), outline=(200, 230, 255), width=3)
    c.rect((720 - dx * 0.5, 190, 900 - dx, 290), grad=((150, 154, 164), (80, 84, 92)), r=10)
    for k in range(5):
        c.rect((735 - dx * 0.5, 200 + k * 18, 885 - dx, 208 + k * 18), fill=(60, 62, 70), r=3)
    c.rect((915 - dx, 196, 950 - dx, 300), grad=((90, 100, 110), (50, 56, 64)), r=6)
    for y in range(200, 300, 10):
        c.line([(918 - dx, y), (948 - dx, y)], (140, 150, 160), 2)
    c.rect((960 - dx, 200, 990 - dx, 300), fill=(200, 200, 206), r=6)
    for k in range(6):
        x = 905 - dx + k * 14
        c.line([(x, 186), (x - 10, 316)], (255, 210, 63, int(150 + 100 * crush)), 3)
    for wx in (230, 760 - dx * 0.4):
        c.ellipse((wx - 80, 316 - 80, wx + 80, 316 + 80), fill=(20, 20, 22))
        c.ellipse((wx - 46, 316 - 46, wx + 46, 316 + 46), radial=((210, 214, 222), (110, 114, 122)))
    c.ellipse((420, 130, 470, 180), fill=(240, 200, 60, 220))
    c.line([(445, 180), (430, 270)], (240, 200, 60, 220), 26)
    c.line([(440, 200), (560, 190)], (240, 200, 60, 220), 16)
    return c.done()


def building(floors, seed=1, w=300):
    fh = 46
    h = floors * fh + 80
    c = Cv(w + 40, h)
    rr = random.Random(seed)
    c.rect((20, 60, w + 20, h), grad=((70, 74, 96), (40, 42, 58)), horizontal=True)
    c.rect((10, 40, w + 30, 64), fill=(50, 52, 70))
    c.rect((w - 60, 0, w - 10, 44), fill=(60, 62, 80))
    for i in range(floors):
        y = h - (i + 1) * fh
        c.rect((14, y + fh - 8, w + 26, y + fh - 2), fill=(90, 94, 116))
        for j in range(5):
            x = 34 + j * (w - 30) / 5
            lit = rr.random() < 0.6
            col = ((255, 214, 140), (220, 170, 90)) if lit else ((50, 56, 80), (30, 34, 50))
            c.rect((x, y + 8, x + 34, y + 32), grad=col, r=3)
    return c.done()


def speed_cam():
    c = Cv(420, 360)
    c.shadow((40, 300, 400, 360), 150, 10)
    c.rect((20, 40, 400, 300), grad=((200, 204, 212), (110, 114, 124)), r=24)
    c.rect((36, 56, 384, 284), grad=((70, 74, 84), (30, 32, 38)), r=18)
    c.ellipse((90, 90, 250, 250), radial=((60, 80, 110), (6, 8, 12)), power=0.8)
    c.ellipse((120, 120, 220, 220), radial=((90, 140, 200), (10, 14, 20)))
    c.ellipse((140, 136, 170, 160), fill=(255, 255, 255, 160))
    for i in range(3):
        for j in range(4):
            c.ellipse((280 + j * 22, 100 + i * 30, 296 + j * 22, 116 + i * 30), fill=(250, 240, 200))
    c.rect((290, 220, 370, 260), fill=(255, 210, 63), r=6)
    c.text((330, 240), "RADAR", 18, (30, 30, 34))
    return c.done()


def nav_screen(t, k):
    w, h = 900, 620
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w, h], radius=40, fill=(20, 22, 28, 255), outline=(90, 94, 104, 255), width=8)
    m = cached("navmap", lambda: __import__("t08_gps")._map(860, 580, 9))
    im.alpha_composite(m, (20, 20))
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle([20, 20, w - 20, h - 20], radius=30, outline=(20, 22, 28, 255), width=10)
    pts = [(120, 520), (220, 420), (300, 430), (420, 300), (560, 280), (700, 160), (800, 90)]
    n = max(2, int(len(pts) * k))
    d.line(pts[:n], fill=(40, 120, 255, 255), width=18, joint="curve")
    d.line(pts[:n], fill=(120, 190, 255, 255), width=8, joint="curve")
    d.ellipse([105, 505, 135, 535], fill=(255, 255, 255, 255), outline=(40, 120, 255, 255), width=6)
    if k > 0.95:
        d.ellipse([785, 75, 815, 105], fill=(230, 60, 66, 255))
    d.rounded_rectangle([40, 40, 380, 130], radius=20, fill=(255, 255, 255, 235))
    d.text((210, 85), "100 km", font=f(F_CAP, 46), fill=(30, 40, 60), anchor="mm")
    return im


def fuel_gauge(img, x, y, s, lvl):
    d = ImageDraw.Draw(img, "RGBA")
    r = 150 * s
    d.pieslice([x - r, y - r, x + r, y + r], 180, 360, fill=(14, 16, 22, 240))
    d.arc([x - r, y - r, x + r, y + r], 180, 360, fill=(150, 154, 166, 255), width=8)
    for k in range(5):
        a = math.radians(180 + k * 45)
        d.line([(x + math.cos(a) * r * 0.7, y + math.sin(a) * r * 0.7), (x + math.cos(a) * r * 0.9, y + math.sin(a) * r * 0.9)], fill=(220, 220, 230), width=4)
    d.text((x - r * 0.72, y - 22), "E", font=f(F_CAP, int(34 * s)), fill=(255, 90, 80), anchor="mm")
    d.text((x + r * 0.72, y - 22), "F", font=f(F_CAP, int(34 * s)), fill=(220, 220, 230), anchor="mm")
    a = math.radians(180 + 180 * lvl)
    d.line([(x, y), (x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)], fill=(255, 120, 60), width=7)
    d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(60, 62, 70))
    d.text((x, y + 34), "GASOLINA", font=f(F_SER, int(26 * s)), fill=(220, 220, 230), anchor="mm")


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    highway_night(img, t, 1.4, 560)
    AC(img, cached("dash", _dash))
    v = lerp(100, 140, ease(clamp((t - 1.2) / 2.4))) if t < a1 else 140 + math.sin(t * 3) * 1.5
    speedo(img, 540, 1080, 0.82, v)
    for x, col in ((250, (90, 200, 255)), (830, (255, 180, 60))):
        d = ImageDraw.Draw(img, "RGBA")
        d.ellipse([x - 26, 1070, x + 26, 1122], fill=col + (200,))
        paste(img, glow(60, col, 0.8), x, 1096)
    lower_third(img, t, a1 + 0.2, "AL FINAL", "CUÁNTO TIEMPO GANAS DE VERDAD", 300, max(1.6, T - a1 - 0.6))
    vignette(img, 200)


def sh_meters(img, t, T, L):
    a1 = L[1][0]
    hz = 700
    sky_day(img, hz)
    asphalt(img, hz + 380, 1260, t, 1.0 if t < a1 else 1.4)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, hz + 330, W, hz + 380], fill=(150, 154, 160, 255))
    for x in range(0, W, 120):
        d.rectangle([x, hz + 300, x + 10, hz + 380], fill=(120, 124, 130, 255))
    ry = 1200
    paste_car(img, 200, ry, 0.62, RED, False, -t * 16)
    m = 28 if t < a1 else 39
    tl = t if t < a1 else t - a1
    k = ease(clamp((tl - 0.3) / 1.0))
    px, x0 = 15, 460
    paste(img, spr(tape_case), x0 - 30, ry - 120, 0.42)
    tape(img, x0, ry - 120, m * px * k, px, m)
    sw = clamp(tl - 0.3)
    stopwatch_at(img, 840, 690, 0.6, sw, f"{sw:.1f} s".replace(".", ","))
    if t < a1:
        big(t, 0.3, "28 M CADA SEGUNDO", 300, 76, YEL, sub="A 100 KM/H", pop=False)
    else:
        big(t, a1 + 0.1, "39 M CADA SEGUNDO", 300, 76, (255, 120, 100), sub="A 140 KM/H", pop=False)
    vignette(img, 160)


def sh_react(img, t, T, L):
    a1 = L[1][0]

    def A(im):
        hz = 760
        night_sky(im, t, hz, 0.7, (4, 6, 14), (26, 26, 44))
        mountains(im, hz, 90, (14, 14, 22), 7, 0.5)
        ground(im, hz, (14, 14, 18), (4, 4, 6))
        pine_row(im, hz + 150, (10, 14, 14), 30, 160, 320, 5)
        d = ImageDraw.Draw(im, "RGBA")
        ry = 1140
        d.rectangle([0, ry - 120, W, ry + 40], fill=(30, 30, 36))
        light_cone(im, 420, ry - 90, 1180, ry - 120, 20, 260, (255, 244, 210), 110, 22)
        dx = 840 + math.sin(t * 2) * 6
        paste(im, glow(260, (255, 240, 200), 0.22), dx, ry - 250, 1.0, 0.7)
        paste(im, spr(deer, 0.85), dx, ry - 250, 0.95)
        paste_car(im, 230, ry, 0.6, RED, True, -t * 18)

    def B(im):
        q = clamp((t - a1 - 0.4) / 2.0)
        pedals(im, t, q)
        stopwatch_at(im, 860, 560, 0.55, 0.75 * q, f"{0.75 * q:.2f} s".replace(".", ","))
        callout(im, t, a1 + 1.2, 560, 860, 300, 600, "TU REACCIÓN", YEL, 36)

    xf(img, t, a1, A, B, 0.6)
    if t < a1:
        big(t, 0.4, "¡CUIDADO!", 300, 110, RED)
    else:
        big(t, a1 + 0.5, "SIN TOCAR EL FRENO", 280, 66, WHITE, sub="21 M A 100 · 29 M A 140", pop=False)
    vignette(img, 200)


def sh_rule(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    sky(img, (24, 26, 34), (8, 8, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    if t < a1:
        k = ease(clamp((t - 0.8) / 0.6))
        ty = 820
        d.text((540 - 90, ty), "14", font=f(F_SER, 260), fill=YEL + (255,), anchor="mm")
        d.text((540 + 150, ty), "0", font=f(F_SER, 260), fill=(255, 255, 255, int(255 * (1 - 0.7 * k))), anchor="mm")
        if k > 0:
            d.line([(540 + 80, ty + 90), (540 + 80 + 150 * k, ty - 90)], fill=(255, 80, 80, 255), width=16)
        speedo(img, 540, 1330, 0.4, 140, 0.4)
        big(t, 0.3, "TRUCO DEL RACE", 300, 92, YEL)
    else:
        k1 = ease(clamp((t - a1 - 0.2) / 1.6))
        squares(img, 290, 860, 10, 34, k1, (90, 200, 255), "10 × 10 = 100 M")
        if t > a2:
            k2 = ease(clamp((t - a2 - 0.1) / 1.8))
            squares(img, 770, 860, 14, 24, k2, (255, 110, 90), "14 × 14 = 196 M")
        if t < a2:
            big(t, a1 + 0.1, "A 100", 300, 100, CY_)
        else:
            big(t, a2 + 0.1, "A 140", 300, 100, (255, 110, 90))
    vignette(img, 190)


def sh_energy(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    AC(img, cached("labtrack_e", __import__("t05_airbag")._lab_track))
    for x in (180, 540, 900):
        spotlight(img, t, x, 0, 1400, 40, 260, 30, dust=False)
    hit = a2 + 0.6
    crush = ease(clamp((t - hit) / 0.18)) if t > hit else 0.0
    x = lerp(-300, 470, clamp(t / hit)) if t < hit else 470
    sx, sy = shake(t, hit, 20, 5)
    paste(img, spr(car_xray, round(crush, 2)), x + sx, 1180 - 175 + sy, 0.82)
    if t > hit:
        overlay(img, (255, 255, 255), 0.7 * math.exp(-(t - hit) * 6))
        rr = random.Random(int(t * 30))
        dd = ImageDraw.Draw(img, "RGBA")
        u = clamp((t - hit) / 0.6)
        for i in range(14):
            a = rr.uniform(-2.6, -0.6)
            r = 40 + 260 * u
            dd.line([(870 + math.cos(a) * r * 0.6, 1040 + math.sin(a) * r * 0.6), (870 + math.cos(a) * r, 1040 + math.sin(a) * r)],
                    fill=(255, 220, 120, int(255 * (1 - u))), width=5)
    if 0.8 < t < hit:
        callout(img, t, 1.0, x + 300 * 0.82, 1010, 300, 700, "MOTOR", (220, 224, 235), 34)
    k = clamp((t - a1) / 1.0) if t > a1 else 0
    if k > 0:
        d = ImageDraw.Draw(img, "RGBA")
        bx, by = 120, 560
        d.rounded_rectangle([bx, by, bx + 840, by + 70], radius=20, fill=(0, 0, 0, 170), outline=(255, 255, 255, 120), width=3)
        lvl = (0.5 if t < a2 else lerp(0.5, 0.98, ease(clamp((t - a2) / 1.0)))) * ease(k)
        col = (90, 200, 255) if t < a2 else (255, 90, 70)
        d.rounded_rectangle([bx + 8, by + 8, bx + 8 + 824 * lvl, by + 62], radius=14, fill=col + (255,))
        d.text((bx + 20, by - 34), "ENERGÍA DEL CHOQUE", font=f(F_SER, 32), fill=(255, 255, 255, 230))
    if t < a1:
        big(t, 0.3, "+40 %", 300, 130, WHITE, sub="DE VELOCIDAD")
    elif t < a2:
        big(t, a1 + 0.1, "E = ½ · M · V²", 300, 96, YEL, pop=False)
    else:
        big(t, a2 + 0.1, "×1,96", 300, 140, RED, sub="DE ENERGÍA")
    vignette(img, 200)


def sh_fall(img, t, T, L):
    a1 = L[1][0]
    night_sky(img, t, 1500, 0.8, (6, 8, 22), (40, 30, 60))
    city_lights(img, t, 1420, 3, 200)
    base = 1460
    b13 = spr(building, 13, 2)
    k1 = ease(clamp((t - 0.2) / 1.0))
    top13 = base - b13.size[1]
    paste(img, b13, 300, lerp(base + b13.size[1] / 2, base - b13.size[1] / 2, k1), 1.0)
    b26 = spr(building, 26, 3)
    top26 = base - b26.size[1]
    if t > a1:
        k2 = ease(clamp((t - a1) / 1.4))
        paste(img, b26, 770, lerp(base + b26.size[1] / 2, base - b26.size[1] / 2, k2), 1.0)
    ground(img, base, (12, 12, 16), (4, 4, 6))
    d = ImageDraw.Draw(img, "RGBA")
    if k1 > 0.95:
        d.line([(110, base), (110, top13)], fill=(255, 255, 255, 220), width=4)
        for y in (base, top13):
            d.line([(92, y), (128, y)], fill=(255, 255, 255, 220), width=4)
        spaced(d, 110, (base + top13) / 2 - 20, "39 M", f(F_SER, 34), (255, 255, 255, 230), 2)
        paste_car(img, 300, top13 + 20, 0.2, RED, True)
    if t > a1 + 1.4:
        d.line([(980, base), (980, top26)], fill=(255, 255, 255, 220), width=4)
        for y in (base, top26):
            d.line([(962, y), (998, y)], fill=(255, 255, 255, 220), width=4)
        spaced(d, 980, (base + top26) / 2, "77 M", f(F_SER, 34), (255, 255, 255, 230), 2)
        paste_car(img, 770, top26 + 20, 0.2, RED, True)
    if t < a1:
        big(t, 0.3, "PISO 13", 280, 120, YEL, sub="CHOCAR A 100")
    else:
        big(t, a1 + 0.2, "PISO 26", 280, 120, RED, sub="CHOCAR A 140")
    vignette(img, 200)


def sh_air(img, t, T, L):
    a1 = L[1][0]
    sky(img, (22, 26, 32), (8, 9, 12), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    fx, fy = 110, 860
    d.ellipse([fx - 300, fy - 300, fx + 300, fy + 300], fill=(40, 44, 52, 255), outline=(110, 114, 124, 255), width=12)
    for k in range(6):
        a = t * 14 + k * math.pi / 3
        d.polygon([(fx, fy), (fx + math.cos(a - 0.22) * 270, fy + math.sin(a - 0.22) * 270), (fx + math.cos(a + 0.22) * 270, fy + math.sin(a + 0.22) * 270)],
                  fill=(90, 94, 104, 255))
    d.ellipse([fx - 50, fy - 50, fx + 50, fy + 50], fill=(150, 154, 164, 255))
    d.rectangle([0, 1150, W, H], fill=(30, 32, 38, 255))
    for x in range(0, W + 80, 80):
        d.line([(x, 1150), (x - 60, H)], fill=(44, 46, 54, 255), width=3)
    paste_car(img, 640, 1150, 0.9, RED, False, 0)
    strength = 1.0 if t < a1 else 1.6
    for i in range(10):
        y = 640 + i * 50
        pts = []
        for x in range(400, W, 12):
            yy = y
            if 220 < x < 1080 and y < 1100:
                yy -= math.exp(-((x - 660) / 320) ** 2) * (1100 - y) * 0.22
            pts.append((x, yy + math.sin(x / 50 - t * 10 * strength + i) * 3 * strength))
        d.line(pts, fill=(235, 240, 255, 150), width=3)
    if t > a1:
        lvl = lerp(0.8, 0.55, ease(clamp((t - a1 - 0.5) / 2.0)))
        fuel_gauge(img, 820, 560, 1.2, lvl)
        big(t, a1 + 0.2, "+20-25 %", 290, 120, YEL, sub="DE CONSUMO (DE 120 A 140)")
    else:
        callout(img, t, 0.6, 330, 860, 380, 560, "TÚNEL DE VIENTO", CY_, 34)
        big(t, 0.3, "RESISTENCIA ×1,96", 290, 84, WHITE, pop=False)
    vignette(img, 200)


def sh_fine(img, t, T, L):
    highway_night(img, t, 1.0, 900, True)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([520, 380, 560, 640], fill=(80, 84, 92, 255))
    paste(img, spr(speed_cam), 540, 600, 1.2)
    if t > 0.9:
        fl = math.exp(-(t - 0.9) * 5)
        paste(img, glow(360, (255, 255, 255), 1.0), 640, 560, 1.0, fl)
        overlay(img, (255, 255, 255), 0.5 * fl)
    if t > 1.4:
        k = ease(clamp((t - 1.4) / 0.6))
        tk = spr(paper, 520, 640, "MULTA", 0, (244, 240, 228), (40, 30, 30), 3,
                 ("Exceso de velocidad", "", "Vía: autovía 120 km/h", "Medido: 140 km/h", "", "Importe: 100 EUR", "Puntos: 0"))
        paste(img, tk, 540, lerp(1800, 1080, k), 0.82, 1.0, -4)
    big(t, 1.6, "100 € · SIN PUNTOS", 290, 84, YEL)
    vignette(img, 200)


def sh_time(img, t, T, L):
    a1 = L[1][0]
    sky(img, (20, 22, 30), (6, 6, 8), 1.0)
    AC(img, cached("dash", _dash))
    k = ease(clamp((t - 0.3) / 1.4))
    paste(img, nav_screen(t, k), 540, 820, 1.0)
    if t > a1:
        d = ImageDraw.Draw(img, "RGBA")
        kk = ease(clamp((t - a1 - 0.2) / 0.6))
        for i, (lbl, val, col) in enumerate((("A 100", "60 MIN", (90, 200, 255)), ("A 140", "43 MIN", (255, 120, 90)))):
            x = 300 + i * 480
            d.rounded_rectangle([x - 200, 1180, x + 200, 1330], radius=24, fill=(10, 12, 18, int(235 * kk)), outline=col + (int(255 * kk),), width=5)
            d.text((x, 1220), lbl, font=f(F_SER, 40), fill=(255, 255, 255, int(255 * kk)), anchor="mm")
            d.text((x, 1285), val, font=f(F_CAP, 60), fill=col + (int(255 * kk),), anchor="mm")
        big(t, a1 + 1.2, "17 MINUTOS", 300, 120, YEL)
    else:
        big(t, 0.3, "¿CUÁNTO GANAS?", 300, 92, WHITE, pop=False)
    vignette(img, 180)


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
    paste(img, car_rear(RED, 0.0), 540, lerp(1260, 1060, ease(q)), lerp(1.0, 0.45, ease(q)))
    title2(t, 0.4, "17 MINUTOS", "¿MERECE LA PENA?", 300, 60, 84, hold=max(2.0, T - 3.4), c1=YEL, c2=WHITE)
    vignette(img, 180)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "tension"), ("meters", "epic"), ("fall", "drone"), ("air", "doc"), ("time", "premium")],
    "duck": [("energy@L2+0.4", "fall+1.0", 0.5)],
    "amb": {"road": ["open", "meters", "react", "fine", "verdict"], "hum": ["rule", "time"], "wind": ["air"], "city": ["fall"]},
    "sfx": [("open+1.2", "riser", 0.08), ("open@L1+0.2", "chime", 0.05), ("meters+0.3", "tick", 0.12), ("meters@L1", "whoosh_up", 0.12),
            ("react+0.6", "heart", 0.35), ("react+1.35", "heart", 0.35), ("react@L1+0.6", "click", 0.2), ("react@L1+2.2", "thud", 0.2),
            ("rule+0.6", "draw", 0.15), ("rule@L1+0.2", "tick", 0.12), ("rule@L2+0.1", "tick", 0.12),
            ("energy@L2+0.6", "boom", 0.45), ("energy@L2+0.6", "impact", 0.4),
            ("fall+0.2", "riser", 0.1), ("fall@L1", "riser_long", 0.12), ("fall@L1+1.4", "impact", 0.3),
            ("air", "whoosh", 0.18), ("air@L1+0.4", "tick", 0.12),
            ("fine+0.9", "shutter", 0.35), ("fine+1.4", "paper", 0.25),
            ("time+0.3", "blip", 0.1), ("time@L1+0.2", "pop", 0.15), ("time@L1+1.2", "chime", 0.06), ("verdict+0.4", "swell", 0.15)],
    "bed": [("meters", "energy"), ("air", "time")],
    "bpm": 100,
}
