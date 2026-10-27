"""T08 · ¿Cómo sabe el GPS dónde estás? (estilo Titanic, ilustración detallada)."""
from gadgets import *
import t02_microondas as T2
import t04_qr as T4

xf, callout, glow_line, top_shade, check = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T4.check

TITLE = "Como_sabe_el_GPS_donde_estas"
LINES = [
    "Tu móvil sabe dónde estás *aunque no tengas internet*.",
    "¿Cómo lo hace… y qué pinta *Einstein* en todo esto?",
    "Sobre tu cabeza hay *31 satélites* GPS, a unos 20.200 km de altura.",
    "Cada uno lleva un *reloj atómico* y emite sin parar una señal con la hora exacta.",
    "Tu móvil escucha esas señales… y mira *cuánto han tardado* en llegar.",
    "Como viajan a la velocidad de la luz, ese tiempo le dice *a qué distancia* está cada satélite.",
    "Con un satélite, sabes que estás en algún punto de *una esfera enorme*.",
    "Con dos y tres, *las esferas se cruzan*… y el punto se va acotando.",
    "Y con un *cuarto*, corrige el error del reloj de tu móvil.",
    "Pero en una milmillonésima de segundo, la luz recorre *30 centímetros*.",
    "Un error minúsculo en los relojes… y te sitúa en *otra calle*.",
    "Y aquí entra Einstein: allí arriba, los relojes adelantan *38 microsegundos* al día.",
    "La *gravedad* más débil los acelera… y la *velocidad* los frena un poco. Al final, *adelantan*.",
    "Si no se corrigiera, el GPS se desviaría unos *10 kilómetros cada día*.",
    "Así que cada vez que abres el mapa… estás usando *la relatividad*.",
]
SHOTS = [("open", 0, 1, 0.3), ("sats", 2, 3, 0.3), ("signal", 4, 5, 0.3), ("tri", 6, 8, 0.3), ("nano", 9, 10, 0.3),
         ("einstein", 11, 12, 0.3), ("drift", 13, 13, 0.3), ("final", 14, 14, 1.8)]
FOCUS = {"tri": (540, 880, 1.1), "drift": (540, 880, 1.1)}
NOTIF = ("signal", 1.0)
HYPE = {"line": 1, "text": ['¿CÓMO LO HACE?', '¿Y QUÉ PINTA EINSTEIN?'], "delay": [0, 1.1]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

SIG = (120, 220, 255)
GOLD = (240, 190, 80)


# ------------------------------------------------------------------ piezas
def satellite():
    c = Cv(620, 300)
    for x0 in (10, 390):
        c.rect((x0, 100, x0 + 220, 200), grad=((40, 70, 160), (20, 30, 80)), r=6)
        for k in range(1, 6):
            c.line([(x0 + k * 37, 100), (x0 + k * 37, 200)], (120, 160, 230, 160), 2)
        c.line([(x0, 150), (x0 + 220, 150)], (120, 160, 230, 160), 2)
        c.rect((x0 + 4, 104, x0 + 216, 112), fill=(255, 255, 255, 40), r=3)
    c.line([(230, 150), (390, 150)], (160, 160, 170), 8)
    c.rect((250, 70, 370, 230), grad=((255, 220, 120), (170, 120, 40)), horizontal=True, r=8)
    for k in range(6):
        c.line([(250, 90 + k * 24), (370, 84 + k * 26)], (200, 150, 60, 140), 2)
    c.ellipse((280, 220, 340, 290), radial=((240, 240, 246), (150, 154, 160)), center=(0.4, 0.3))
    c.line([(310, 70), (310, 20)], (200, 200, 206), 5)
    c.ellipse((300, 10, 320, 30), fill=(255, 90, 80))
    return c.done()


def _mountains():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((6, 10, 28), (40, 40, 70)))
    rr = random.Random(3)
    for i in range(300):
        x, y = rr.uniform(0, W), rr.uniform(0, 1000)
        r = rr.uniform(0.8, 2.4)
        c.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, rr.randint(90, 230)))
    c.poly([(0, 1100), (200, 880), (380, 980), (600, 760), (820, 940), (1080, 820), (1080, H), (0, H)], grad=((40, 44, 70), (14, 14, 22)))
    c.poly([(0, 1300), (300, 1120), (560, 1220), (860, 1080), (1080, 1180), (1080, H), (0, H)], grad=((24, 26, 40), (6, 6, 10)))
    return c.done().convert("RGBA")


def _map(w=1080, h=1920, seed=4):
    c = Cv(w, h, 1)
    c.rect((0, 0, w, h), fill=(238, 234, 226))
    rr = random.Random(seed)
    c.poly([(0, 1200), (300, 1140), (700, 1260), (w, 1180), (w, 1300), (700, 1380), (300, 1260), (0, 1320)], fill=(150, 196, 230))
    for i in range(6):
        x, y = rr.uniform(0, w), rr.uniform(0, h)
        c.ellipse((x - 140, y - 90, x + 140, y + 90), fill=(196, 226, 176))
    for k in range(-2, 14):
        x = k * 120 + 40
        c.line([(x, 0), (x + 200, h)], (255, 255, 255), 18 if k % 3 else 30)
    for k in range(-2, 22):
        y = k * 110
        c.line([(0, y), (w, y - 160)], (255, 255, 255), 18 if k % 4 else 30)
    c.line([(0, 600), (w, 900)], (255, 214, 120), 34)
    return c.done().convert("RGBA")


def map_bg(img):
    AC(img, cached("map", _map))


def pin(img, x, y, s=1.0, col=(230, 60, 66)):
    c = spr(_pin, col)
    paste(img, glow(60, (0, 0, 0), 0.8), x + 10 * s, y + 6, 1.0, 0.5)
    paste(img, c, x, y - 60 * s, s)


def _pin(col):
    c = Cv(100, 130)
    c.poly([(50, 128), (14, 64), (86, 64)], fill=shade(col, 0.8))
    c.ellipse((10, 10, 90, 90), radial=(shade(col, 1.3), shade(col, 0.7)), center=(0.38, 0.3))
    c.ellipse((34, 34, 66, 66), fill=(255, 255, 255))
    return c.done()


def blue_dot(img, x, y, t):
    d = ImageDraw.Draw(img, "RGBA")
    r = 40 + 26 * ((t * 1.2) % 1.0)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(60, 140, 255, int(110 * (1 - (t * 1.2) % 1.0))))
    d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(255, 255, 255, 255))
    d.ellipse([x - 19, y - 19, x + 19, y + 19], fill=(40, 120, 255, 255))


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    AC(img, cached("mount", _mountains))
    if t < a1:
        def extra(scr):
            m = cached("map_small", lambda: _map(428, 928, 7))
            scr.alpha_composite(m)
            dd = ImageDraw.Draw(scr, "RGBA")
            x, y = 214, 520
            r = 30 + 22 * ((t * 1.2) % 1.0)
            dd.ellipse([x - r, y - r, x + r, y + r], fill=(60, 140, 255, int(110 * (1 - (t * 1.2) % 1.0))))
            dd.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(255, 255, 255))
            dd.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(40, 120, 255))
            dd.rounded_rectangle([60, 90, 368, 150], radius=26, fill=(30, 30, 34, 230))
            dd.text((214, 120), "Sin conexión", font=f(F_CAP, 28), fill=(255, 255, 255), anchor="mm")
        phone(img, 540, 880, 0.9, "off", 0, 1.0, extra)
    else:
        sky(img, (20, 30, 24), (8, 12, 10), 1.0)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([90, 460, 990, 1240], radius=20, fill=(30, 52, 40, 255), outline=(120, 90, 50, 255), width=26)
        k = ease(clamp((t - a1 - 0.2) / 1.2))
        lines_ = ["t' = t · √(1 − v²/c²)", "E = mc²", "g → el tiempo va más rápido"]
        for i, ln in enumerate(lines_):
            kk = clamp(k * 3 - i)
            if kk > 0:
                d.text((540, 640 + i * 170), ln, font=f(F_SER, 64 if i < 2 else 46), fill=(240, 240, 230, int(230 * kk)), anchor="mm")
    top_shade(img)
    if t < a1:
        title2(t, 0.3, "SIN INTERNET", "SABE DÓNDE ESTÁS", 250, 60, 84, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def space(img, t, earth_y=1700, r=640):
    sky(img, (2, 4, 12), (10, 14, 34), 1.0)
    stars(img, t, H, 0.9, 260, 11)
    paste(img, glow(r * 2, (60, 140, 255), 0.35), 540, earth_y)
    paste(img, spr(globe_sprite, -4.0, 30.0, r), 540, earth_y)


def sh_sats(img, t, T, L):
    a1 = L[1][0]
    if t < a1 + 0.3:
        space(img, t)
        d = ImageDraw.Draw(img, "RGBA")
        sat = spr(satellite)
        for k in range(6):
            rx, ry = 980 + k * 30, 300 + k * 40
            cy = 1700 - 60
            d.ellipse([540 - rx, cy - ry - 520, 540 + rx, cy + ry - 520], outline=(150, 190, 255, 60), width=2)
        rr = random.Random(5)
        kk = ease(clamp((t - 0.3) / 1.6))
        for i in range(31):
            if i / 31 > kk:
                continue
            k = i % 6
            rx, ry = 980 + k * 30, 300 + k * 40
            a = rr.uniform(0, 6.28) + t * 0.12 * (1 if k % 2 else -1)
            x, y = 540 + math.cos(a) * rx / 2, 1120 + math.sin(a) * ry / 2 - 220
            if y < 1200:
                paste(img, sat, x, y, 0.13)
                paste(img, glow(30, (255, 230, 160), 1.0), x, y, 1.0, 0.7)
        if t > 1.6:
            k2 = ease(clamp((t - 1.6) / 0.6))
            d = ImageDraw.Draw(img, "RGBA")
            d.line([(960, 1080), (960, 560)], fill=(255, 255, 255, int(220 * k2)), width=4)
            for y in (1080, 560):
                d.line([(940, y), (980, y)], fill=(255, 255, 255, int(220 * k2)), width=4)
            spaced(d, 880, 800, "20.200 KM", f(F_SER, 36), (255, 255, 255, int(255 * k2)), 3)
    else:
        sky(img, (2, 4, 12), (8, 10, 24), 1.0)
        stars(img, t, H, 0.9, 260, 11)
        paste(img, spr(satellite), 540, 760, 1.4)
        for i in range(4):
            u = ((t - a1) * 0.8 + i * 0.25) % 1.0
            r = 140 + u * 700
            d = ImageDraw.Draw(img, "RGBA")
            d.arc([540 - r, 760 - r * 0.6, 540 + r, 760 + r * 0.6], 20, 160, fill=SIG + (int(200 * (1 - u)),), width=6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([250, 1040, 830, 1130], radius=20, fill=(0, 0, 0, 200), outline=GOLD + (255,), width=3)
        ms = int(((t - a1) * 1000) % 1000)
        d.text((540, 1085), f"12:00:0{int(t - a1) % 10}.{ms:03d}421", font=f(F_MONO, 44), fill=(120, 255, 170), anchor="mm")
        spaced(d, 540, 1170, "RELOJ ATÓMICO", f(F_SER, 36), GOLD + (230,), 6)
    if t < a1:
        big(t, 0.3, "31 SATÉLITES", 290, 100, WHITE)
    else:
        big(t, a1 + 0.4, "LA HORA EXACTA", 290, 92, YEL, pop=False)
    vignette(img, 180)


def sh_signal(img, t, T, L):
    a1 = L[1][0]
    sky(img, (2, 4, 14), (20, 24, 50), 1.0)
    stars(img, t, H, 0.8, 200, 4)
    paste(img, spr(satellite), 540, 470, 0.5)
    AC(img, cached("mount", _mountains).crop((0, 900, W, H)).resize((W, 1020)), (0, 900))
    phone(img, 540, 1180, 0.32, "home")
    k = (t * 0.7) % 1.0
    y = lerp(520, 1080, k)
    glow_line(img, [(540, 520), (540, y)], SIG, 4, 8, 160)
    paste(img, glow(60, SIG, 1.0), 540, y)
    d = ImageDraw.Draw(img, "RGBA")
    spaced(d, 790, 560, "SALE: 12:00:00,000", f(F_MONO, 30), (200, 230, 255, 230), 1)
    if t > 1.6:
        spaced(d, 290, 1060, "LLEGA: 12:00:00,067", f(F_MONO, 30), (120, 255, 170, 230), 1)
    if t > a1:
        kk = ease(clamp((t - a1 - 0.3) / 0.6))
        d.rounded_rectangle([140, 720, 940, 880], radius=20, fill=(0, 0, 0, int(200 * kk)), outline=(120, 220, 255, int(255 * kk)), width=3)
        d.text((540, 770), "0,067 s × 300.000 km/s", font=f(F_MONO, 40), fill=(255, 255, 255, int(255 * kk)), anchor="mm")
        d.text((540, 830), "≈ 20.200 km", font=f(F_MONO, 48), fill=YEL + (int(255 * kk),), anchor="mm")
    if t < a1:
        big(t, 0.3, "¿CUÁNTO TARDA?", 290, 92, WHITE, pop=False)
    else:
        big(t, a1 + 0.2, "TIEMPO = DISTANCIA", 290, 76, YEL, pop=False)
    vignette(img, 190)


def sh_tri(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    map_bg(img)
    overlay(img, (10, 14, 30), 0.35)
    d = ImageDraw.Draw(img, "RGBA")
    P = (560, 900)
    sats = [((80, 300), 760), ((1040, 360), 720), ((300, 1500), 670), ((960, 1450), 690)]
    for i, ((sx, sy), r_) in enumerate(sats):
        st = 0.4 if i == 0 else (a1 + 0.2 + (i - 1) * 0.7 if i < 3 else a2 + 0.2)
        k = ease(clamp((t - st) / 1.0))
        if k <= 0:
            continue
        r = math.hypot(P[0] - sx, P[1] - sy)
        rr_ = r * k
        col = [(120, 220, 255), (255, 210, 63), (255, 120, 120), (140, 255, 170)][i]
        d.ellipse([sx - rr_, sy - rr_, sx + rr_, sy + rr_], outline=col + (220,), width=7)
        d.ellipse([sx - rr_, sy - rr_, sx + rr_, sy + rr_], fill=col + (18,))
        paste(img, spr(satellite), sx, sy, 0.16)
        d = ImageDraw.Draw(img, "RGBA")
    if t > a1 + 1.8:
        k = ease(clamp((t - a1 - 1.8) / 0.4))
        pin(img, P[0], P[1], 1.0 * k + 0.01)
    if t > a2 + 1.0:
        k = ease(clamp((t - a2 - 1.0) / 0.4))
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([660, 960, 980, 1040], radius=18, fill=(0, 0, 0, int(200 * k)))
        d.text((820, 1000), "RELOJ OK", font=f(F_CAP, 40), fill=(140, 255, 170, int(255 * k)), anchor="mm")
    top_shade(img, 230, 660)
    if t < a1:
        big(t, 0.3, "1 SATÉLITE: UNA ESFERA", 290, 62, (120, 220, 255), pop=False)
    elif t < a2:
        big(t, a1 + 0.3, "2… Y 3", 290, 110, YEL)
    else:
        big(t, a2 + 0.2, "EL CUARTO", 290, 100, (140, 255, 170), sub="CORRIGE TU RELOJ")
    vignette(img, 190)


def ruler(img, t, t0):
    sky(img, (12, 14, 24), (4, 4, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y = 90, 990, 860
    d.rounded_rectangle([x0 - 20, y - 70, x1 + 20, y + 70], radius=12, fill=(232, 200, 120, 255))
    for k in range(31):
        x = x0 + k * (x1 - x0) / 30
        h_ = 46 if k % 10 == 0 else (32 if k % 5 == 0 else 20)
        d.line([(x, y - 70), (x, y - 70 + h_)], fill=(60, 40, 20, 255), width=3)
        if k % 10 == 0:
            d.text((x, y), str(k), font=f(F_SER, 34), fill=(60, 40, 20), anchor="mm")
    u = clamp(((t - t0) % 2.2) / 1.6)
    x = lerp(x0, x1, ease(u))
    glow_line(img, [(x0, y - 160), (x, y - 160)], (255, 250, 210), 5, 10, 230)
    paste(img, glow(90, (255, 250, 220), 1.0), x, y - 160)
    d.text((540, y + 150), "1 NANOSEGUNDO", font=f(F_SER, 50), fill=(255, 255, 255), anchor="mm")


def wrong_street(img, t, t0):
    map_bg(img)
    k = ease(clamp((t - t0 - 0.6) / 0.8))
    blue_dot(img, 540, 900, t)
    x, y = lerp(540, 820, k), lerp(900, 640, k)
    pin(img, x, y, 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    if k > 0.2:
        d.line([(540, 900), (x, y)], fill=(230, 60, 66, 200), width=5)


def sh_nano(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: ruler(im, t, 0), lambda im: wrong_street(im, t, a1), 0.6)
    if t < a1:
        big(t, 0.3, "30 CM", 290, 130, YEL, sub="LO QUE RECORRE LA LUZ")
    else:
        top_shade(img, 235, 660)
        big(t, a1 + 0.2, "OTRA CALLE", 290, 104, (255, 90, 90))
    vignette(img, 190)


def clock_face(img, x, y, r, t, label, col, speed=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([x - r - 14, y - r - 14, x + r + 14, y + r + 14], fill=shade(col, 0.6) + (255,))
    d.ellipse([x - r, y - r, x + r, y + r], fill=(246, 244, 236, 255))
    for k in range(12):
        a = k * math.pi / 6
        d.line([(x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82), (x + math.cos(a) * r * 0.94, y + math.sin(a) * r * 0.94)], fill=(40, 40, 44), width=5)
    a = -math.pi / 2 + t * speed * 2
    d.line([(x, y), (x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)], fill=(200, 40, 40), width=6)
    a2 = -math.pi / 2 + t * speed * 0.2
    d.line([(x, y), (x + math.cos(a2) * r * 0.55, y + math.sin(a2) * r * 0.55)], fill=(30, 30, 34), width=10)
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(30, 30, 34))
    spaced(d, x, y + r + 40, label, f(F_SER, 34), (255, 255, 255, 230), 5)


def well(img, t, t0):
    sky(img, (4, 6, 16), (10, 12, 30), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = 540, 1150
    for i in range(-9, 10):
        pts = []
        for j in range(0, 60):
            x = cx + i * 60
            y = 500 + j * 14
            r = math.hypot(x - cx, (y - cy) * 1.0)
            dip = 260 * math.exp(-(r / 220) ** 2)
            pts.append((x, y + dip * 0.6))
        d.line(pts, fill=(90, 140, 255, 90), width=2)
    for j in range(0, 60, 4):
        pts = []
        for i in range(-12, 13):
            x = cx + i * 46
            y = 500 + j * 14
            r = math.hypot(x - cx, y - cy)
            dip = 260 * math.exp(-(r / 220) ** 2)
            pts.append((x, y + dip * 0.6))
        d.line(pts, fill=(90, 140, 255, 90), width=2)
    paste(img, spr(globe_sprite, -4.0, 30.0, 120), cx, cy + 120)
    paste(img, spr(satellite), 820, 600, 0.22)
    k1 = ease(clamp((t - t0 - 0.3) / 0.5))
    k2 = ease(clamp((t - t0 - 2.0) / 0.5))
    k3 = ease(clamp((t - t0 - 3.6) / 0.5))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([600, 680, 1040, 760], radius=16, fill=(0, 0, 0, int(200 * k1)))
    d.text((820, 720), "GRAVEDAD: +45 μs", font=f(F_MONO, 36), fill=(140, 255, 170, int(255 * k1)), anchor="mm")
    d.rounded_rectangle([600, 780, 1040, 860], radius=16, fill=(0, 0, 0, int(200 * k2)))
    d.text((820, 820), "VELOCIDAD: −7 μs", font=f(F_MONO, 36), fill=(255, 140, 120, int(255 * k2)), anchor="mm")
    d.rounded_rectangle([600, 880, 1040, 960], radius=16, fill=(0, 0, 0, int(220 * k3)), outline=YEL + (int(255 * k3),), width=3)
    d.text((820, 920), "TOTAL: +38 μs/día", font=f(F_MONO, 36), fill=YEL + (int(255 * k3),), anchor="mm")


def clocks(img, t, t0):
    sky(img, (6, 8, 20), (14, 18, 40), 1.0)
    stars(img, t, 900, 0.8, 160, 6)
    clock_face(img, 300, 820, 190, t * 1.06, "SATÉLITE", GOLD, 1.0)
    clock_face(img, 780, 820, 190, t, "TIERRA", (120, 160, 220), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    k = ease(clamp((t - t0 - 1.4) / 0.5))
    d.rounded_rectangle([140, 1110, 460, 1190], radius=18, fill=(0, 0, 0, int(200 * k)), outline=GOLD + (int(255 * k),), width=3)
    d.text((300, 1150), "+38 μs/día", font=f(F_MONO, 40), fill=YEL + (int(255 * k),), anchor="mm")


def sh_einstein(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: clocks(im, t, 0), lambda im: well(im, t, a1), 0.7)
    if t < a1:
        big(t, 0.3, "ADELANTAN", 290, 110, YEL, sub="38 MICROSEGUNDOS AL DÍA")
    else:
        big(t, a1 + 0.2, "GRAVEDAD VS VELOCIDAD", 290, 64, WHITE, pop=False)
    vignette(img, 190)


def sh_drift(img, t, T, L):
    map_bg(img)
    overlay(img, (0, 0, 0), 0.15)
    k = ease(clamp((t - 0.5) / (T - 1.2)))
    blue_dot(img, 300, 1160, t)
    x, y = lerp(300, 860, k), lerp(1160, 520, k)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(300, 1160), (x, y)], fill=(230, 60, 66, 220), width=6)
    pin(img, x, y, 1.0)
    km = 10 * k
    d.rounded_rectangle([560, 1060, 980, 1150], radius=18, fill=(0, 0, 0, 200))
    d.text((770, 1105), f"{km:.1f} km".replace(".", ","), font=f(F_MONO, 50), fill=YEL, anchor="mm")
    top_shade(img, 235, 660)
    big(t, 0.3, "10 KM CADA DÍA", 280, 96, (255, 90, 90), sub="SIN CORREGIR")
    vignette(img, 190)


def sh_final(img, t, T, L):
    AC(img, cached("mount", _mountains))

    def extra(scr):
        m = cached("map_small", lambda: _map(428, 928, 7))
        scr.alpha_composite(m)
        dd = ImageDraw.Draw(scr, "RGBA")
        x, y = 214, 520
        r = 30 + 22 * ((t * 1.2) % 1.0)
        dd.ellipse([x - r, y - r, x + r, y + r], fill=(60, 140, 255, int(110 * (1 - (t * 1.2) % 1.0))))
        dd.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(255, 255, 255))
        dd.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(40, 120, 255))
    phone(img, 540, 900, 0.85, "off", 0, 1.0, extra)
    top_shade(img)
    title2(t, 0.3, "CADA VEZ QUE ABRES EL MAPA", "USAS LA RELATIVIDAD", 250, 44, 76, hold=max(2.0, T - 1.2))
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "space"), ("sats", "epic"), ("signal", "exp"), ("tri", "creative"), ("nano", "tension"), ("einstein", "mystery"),
              ("drift", "tension"), ("final", "premium")],
    "gains": {"exp": 0.7, "mystery": 0.8},
    "amb": {"wind": ["open"], "space": ["sats", "signal", "einstein"], "city": ["tri", "drift"]},
    "sfx": [("open+0.6", "blip", 0.12), ("open@L1", "whoosh", 0.14), ("open@L1+0.4", "paper", 0.1),
            ("sats+0.3", "whoosh_up", 0.14), ("sats+1.6", "tick", 0.15), ("sats@L1+0.2", "beep", 0.06), ("sats@L1+1.0", "beep", 0.05),
            ("signal+0.3", "blip", 0.12), ("signal+1.7", "blip_down", 0.12), ("signal@L1+0.3", "type", 0.12),
            ("tri+0.4", "swell", 0.1), ("tri@L1+0.2", "pop", 0.14), ("tri@L1+0.9", "pop", 0.14), ("tri@L1+1.8", "ding", 0.08),
            ("tri@L2+1.0", "chime", 0.06),
            ("nano+0.3", "zap", 0.08), ("nano@L1+0.6", "glitch", 0.1),
            ("einstein+1.4", "tick", 0.15), ("einstein@L1+0.3", "blip", 0.1), ("einstein@L1+2.0", "blip_down", 0.1), ("einstein@L1+3.6", "ding", 0.08),
            ("drift+0.5", "riser_long", 0.1), ("final+0.3", "swell", 0.14)],
    "bed": [("signal", "tri")],
    "bpm": 100,
}
