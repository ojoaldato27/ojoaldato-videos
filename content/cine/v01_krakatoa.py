"""V01 · El sonido más fuerte de la historia (Krakatoa, 1883)."""
from cine import *

TITLE = "El_sonido_mas_fuerte_de_la_historia"
LINES = [
    "En 1883 se oyó el sonido *más fuerte* de la historia.",
    "¿Qué pudo hacer un ruido capaz de dar *la vuelta al mundo*?",
    "Isla Rodrigues, en medio del océano Índico.",
    "Allí, la gente oye algo parecido a *cañonazos* lejanos.",
    "Pero el origen estaba a casi *4.800 kilómetros*.",
    "Más lejos que de Madrid a Moscú.",
    "Mucho más cerca, a 64 kilómetros, navegaba el barco *Norham Castle*.",
    "Su capitán escribió que más de la mitad de su tripulación tenía *los tímpanos reventados*.",
    "A 160 kilómetros, se calcula que superó los *172 decibelios*.",
    "Más que un avión despegando a tu lado.",
    "Y la onda de presión no se detuvo ahí.",
    "Los barómetros de todo el planeta la registraron durante *cinco días*.",
    "Dio la vuelta a la Tierra *tres o cuatro veces*.",
    "Entonces… ¿qué la provocó?",
    "Un volcán en una isla entre Java y Sumatra: *Krakatoa*.",
    "El 27 de agosto de 1883, a las 10:02, explotó.",
    "Dos tercios de la isla *desaparecieron*.",
    "Y los tsunamis dejaron más de *36.000 muertos*.",
    "Hoy, en su lugar, crece un volcán nuevo: *el hijo de Krakatoa*.",
    "Un sonido que *dio la vuelta al mundo*… y aún se recuerda.",
]
SHOTS = [("open", 0, 1, 0.3), ("rodrigues", 2, 3, 0.2), ("distance", 4, 5, 0.3), ("ship", 6, 7, 0.4),
         ("db", 8, 9, 0.3), ("barometer", 10, 11, 0.2), ("wave", 12, 12, 0.3), ("question", 13, 13, 0.3),
         ("volcano", 14, 14, 0.4), ("eruption", 15, 16, 0.6), ("tsunami", 17, 17, 0.9), ("anak", 18, 19, 1.8)]
FOCUS = {"open": (540, 900), "rodrigues": (600, 1000), "distance": (560, 900), "ship": (540, 1000),
         "barometer": (380, 760), "volcano": (540, 900), "eruption": (540, 820), "tsunami": (560, 1000),
         "anak": (600, 1050)}
NOTIF = ("db", 1.4)

EXTRA = tuple(tuple(p) for p in SE_ASIA)
KRAK = (105.42, -6.10)
RODR = (63.42, -19.70)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿QUÉ HIZO UN RUIDO', 'QUE DIO LA VUELTA AL MUNDO?'], "delay": [0, 1.4]}
STICKER_EXTRA = [('sonido', '🔊'), ('mundo', '🌍'), ('oceano', '🌊'), ('isla', '🏝️'), ('canonazo', '💥'), ('kilometro', '📏'), ('barco', '🚢'), ('capitan', '⚓'), ('timpano', '👂'), ('decibelio', '🔊'), ('avion', '✈️'), ('despeg', '✈️'), ('presion', '🌊'), ('barometro', '📈'), ('dias', '📅'), ('tierra', '🌍'), ('volcan', '🌋'), ('krakatoa', '🌋'), ('explot', '💥'), ('desaparec', '💨'), ('tsunami', '🌊'), ('muertos', '🕯️'), ('hijo', '🌋')]

def palm(h=700, lean=0.15, col=(10, 12, 20)):
    def fn(d, s):
        bx, by = 200, h - 10
        tx, ty = 200 + lean * h, 120
        pts = []
        for k in range(21):
            u = k / 20
            x = bx + (tx - bx) * u + math.sin(u * 3.1) * 30 * lean * 3
            y = by + (ty - by) * u
            pts.append((x, y))
        for k in range(20):
            (x1, y1), (x2, y2) = pts[k], pts[k + 1]
            wdt = 22 - 12 * k / 20
            d.line(sc([(x1, y1), (x2, y2)], s), fill=col, width=int(wdt * s))
        for ang in (-170, -140, -110, -60, -30, 0, 25):
            a = math.radians(ang)
            L = 230
            ex, ey = tx + math.cos(a) * L, ty + math.sin(a) * L * 0.5 + 60
            mx, my = tx + math.cos(a) * L * 0.5, ty + math.sin(a) * L * 0.25 - 30
            d.line(sc([(tx, ty), (mx, my), (ex, ey)], s), fill=col, width=int(14 * s), joint="curve")
            for j in range(1, 8):
                u = j / 8
                px, py = tx + (ex - tx) * u, ty + (ey - ty) * u - 30 * math.sin(u * 3.1)
                d.line(sc([(px, py), (px + 30 * math.cos(a + 1.2), py + 40)], s), fill=col, width=int(6 * s))
        d.ellipse(sb([tx - 22, ty - 10, tx + 22, ty + 30], s), fill=col)
    return sprite(("palm", h, lean, col), 520, h, fn)


def steamer():
    def fn(d, s):
        hull = (20, 20, 26)
        d.polygon(sc([(40, 300), (900, 300), (860, 380), (90, 380)], s), fill=hull)
        d.polygon(sc([(60, 380), (870, 380), (850, 400), (80, 400)], s), fill=(120, 30, 28))
        d.rectangle(sb([300, 240, 640, 300], s), fill=(200, 196, 186))
        for x in range(320, 630, 26):
            d.rectangle(sb([x, 258, x + 12, 272], s), fill=(60, 60, 70))
        d.polygon(sc([(440, 240), (500, 240), (490, 120), (450, 120)], s), fill=(30, 30, 34))
        d.rectangle(sb([446, 120, 494, 140], s), fill=(180, 40, 36))
        for mx in (180, 760):
            d.line(sc([(mx, 300), (mx, 40)], s), fill=(30, 30, 34), width=int(8 * s))
            d.line(sc([(mx - 70, 90), (mx + 70, 90)], s), fill=(30, 30, 34), width=int(5 * s))
        d.line(sc([(180, 40), (760, 40)], s), fill=(50, 50, 56), width=int(2 * s))
        d.line(sc([(760, 40), (900, 300)], s), fill=(50, 50, 56), width=int(2 * s))
        d.line(sc([(180, 40), (40, 300)], s), fill=(50, 50, 56), width=int(2 * s))
    return sprite("steamer", 940, 420, fn)


def volcano_island(collapsed=0.0, night=False):
    def fn(d, s):
        rock, rock2 = ((50, 40, 38), (70, 56, 50)) if not night else ((22, 18, 20), (34, 26, 26))
        green = (40, 70, 44) if not night else (16, 26, 18)
        cut = 900 * collapsed
        pts = [(0, 520), (150, 470), (330, 220), (420, 120), (480, 110), (560, 210), (720, 420), (900, 500), (1000, 520)]
        d.polygon(sc(pts + [(1000, 560), (0, 560)], s), fill=rock)
        d.polygon(sc([(420, 120), (480, 110), (560, 210), (640, 330), (560, 560), (430, 560)], s), fill=rock2)
        d.polygon(sc([(0, 520), (150, 470), (250, 380), (300, 520)], s), fill=green)
        d.polygon(sc([(720, 420), (900, 500), (1000, 520), (700, 530)], s), fill=green)
        if collapsed > 0:
            x0 = 1000 - cut
            rr = random.Random(7)
            edge = [(x0 + rr.uniform(-40, 40), y) for y in range(0, 600, 60)]
            d.polygon(sc(edge + [(1100, 600), (1100, 0)], s), fill=(0, 0, 0, 0))
    return sprite(("vol", round(collapsed, 2), night), 1000, 560, fn)


def barometer():
    def fn(d, s):
        c, r = 260, 240
        d.ellipse(sb([c - r, c - r, c + r, c + r], s), fill=(150, 110, 50))
        d.ellipse(sb([c - r + 18, c - r + 18, c + r - 18, c + r - 18], s), fill=(220, 180, 100))
        d.ellipse(sb([c - r + 34, c - r + 34, c + r - 34, c + r - 34], s), fill=(244, 238, 222))
        for k in range(41):
            a = math.radians(135 + k * 270 / 40)
            r1, r2 = r - 50, r - (80 if k % 5 == 0 else 66)
            d.line(sc([(c + math.cos(a) * r1, c + math.sin(a) * r1), (c + math.cos(a) * r2, c + math.sin(a) * r2)], s),
                   fill=(40, 34, 30), width=int((4 if k % 5 == 0 else 2) * s))
        fnt = f(F_SER, int(34 * s))
        for txt, a in (("LLUVIA", 190), ("VARIABLE", 270), ("BUENO", 350)):
            aa = math.radians(a)
            x, y = c + math.cos(aa) * (r - 125), c + math.sin(aa) * (r - 125)
            tw = d.textlength(txt, font=fnt)
            d.text((x * s - tw / 2, y * s - 18 * s), txt, font=fnt, fill=(60, 50, 40))
    return sprite("baro", 520, 520, fn)


def huts():
    def fn(d, s):
        col = (12, 12, 18)
        for x, w_, h_ in ((40, 160, 120), (230, 200, 150), (470, 150, 110), (650, 190, 140)):
            d.rectangle(sb([x, 300 - h_ * 0.5, x + w_, 300], s), fill=col)
            d.polygon(sc([(x - 25, 300 - h_ * 0.5), (x + w_ / 2, 300 - h_), (x + w_ + 25, 300 - h_ * 0.5)], s), fill=col)
        d.rectangle(sb([0, 300, 900, 320], s), fill=col)
    return sprite("huts", 900, 330, fn)


# ------------------------------------------------------------------ utilidades del vídeo
def ring_layer(cx, cy, r_glob, radii, col=(255, 220, 160), width=10, alpha=200):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for rr, a in radii:
        if rr > 2:
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=col + (int(alpha * a),), width=width)
    mask = cached(("gmask", cx, cy, r_glob), lambda: _circle_mask(cx, cy, r_glob))
    im.putalpha(Image.fromarray((np.array(im.getchannel("A")).astype(np.uint16) * np.array(mask) // 255).astype(np.uint8)))
    return im.filter(ImageFilter.GaussianBlur(2))


def _circle_mask(cx, cy, r):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    return m


def ash(img, t, n=90, seed=31, fall=60, col=(150, 140, 130), alpha=150):
    particles(img, t, n, seed, col, fall, (1.5, 4), alpha, 40)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    space_bg(img, t, 3)
    gx, gy, r = 540, 920, 420
    g = spr(globe_sprite, 92.0, -8.0, r, EXTRA)
    paste(img, g, gx, gy)
    kx, ky = proj_point(92.0, -8.0, r, *KRAK)
    kx, ky = gx + kx, gy + ky
    pulse = 0.6 + 0.4 * math.sin(t * 5) ** 2
    paste(img, glow(60, (255, 160, 80), 1.0), kx, ky, 1.0, pulse)
    a0 = L[1][0] + 0.9
    if t > a0:
        u = t - a0
        radii = [((u - k * 0.5) * 300, max(0, 1 - (u - k * 0.5) / 2.6)) for k in range(4) if u - k * 0.5 > 0]
        AC(img, ring_layer(int(kx), int(ky), r, radii))
        flare(img, kx, ky, math.exp(-u * 3), 200, (255, 200, 140))
    title2(t, 0.25, "EL SONIDO MÁS FUERTE", "DE LA HISTORIA", 290, 60, 90, hold=max(1.5, L[1][0] - 0.6))
    vignette(img, 170)


def sh_rodrigues(img, t, T, L):
    hz = 1150
    sky(img, (40, 30, 80), (250, 140, 90), 1.2)
    paste(img, glow(400, (255, 180, 120), 0.8), 760, hz - 60)
    clouds(img, t, 560, (255, 200, 170), 70, 8, 6, 1.2)
    sea(img, t, hz, (60, 50, 100), (16, 14, 34), (200, 150, 170), 0.7)
    ground(img, 1420, (24, 20, 30), (10, 8, 14))
    paste(img, palm(820, 0.18), 150, 1080)
    paste(img, palm(640, -0.12), 940, 1180, flip=True)
    for i, (x, hh) in enumerate(((430, 1.0), (560, 0.9), (690, 0.95))):
        turn = ease(clamp((t - L[1][0] - 0.6 - i * 0.2) / 0.5))
        paste(img, spr(person, 200, 520, (14, 12, 22), None, False, i == 1, round(-0.6 * turn, 1), 0.0), x, 1290, 0.75 * hh)
    a0 = L[1][0] + 0.4
    if t > a0:
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(5):
            ph = ((t - a0) * 0.5 + k / 5) % 1.0
            r = 80 + ph * 900
            d.arc([-200 - r, hz - 120 - r * 0.4, -200 + r, hz - 120 + r * 0.4], -40, 40, fill=(255, 230, 200, int(140 * (1 - ph))), width=5)
        for k, tk in enumerate((0.0, 1.1, 2.0)):
            fl = math.exp(-max(0, t - a0 - tk) * 4) if t > a0 + tk else 0
            paste(img, glow(180, (255, 200, 150), 0.7), 60, hz - 30, 1.0, fl)
    lower_third(img, t, 0.3, "ISLA RODRIGUES", "OCÉANO ÍNDICO · 1883", 300, max(2.4, L[0][1] + 0.6))
    vignette(img, 170)


def sh_distance(img, t, T, L):
    space_bg(img, t, 5)
    gx, gy, r = 540, 1000, 820
    lon0, lat0 = 86.0, -13.0
    paste(img, spr(globe_sprite, lon0, lat0, r, EXTRA), gx, gy)
    pts = []
    for k in range(41):
        u = k / 40
        lo = KRAK[0] + (RODR[0] - KRAK[0]) * u
        la = KRAK[1] + (RODR[1] - KRAK[1]) * u
        x, y = proj_point(lon0, lat0, r, lo, la)
        pts.append((gx + x, gy + y - math.sin(u * math.pi) * 60))
    q = ease(clamp((t - 0.4) / 2.4))
    d = ImageDraw.Draw(img, "RGBA")
    n = max(2, int(len(pts) * q))
    d.line(pts[:n], fill=YEL + (255,), width=8, joint="curve")
    for (x, y), lab in ((pts[0], "KRAKATOA"), (pts[-1], "RODRIGUES")):
        paste(img, glow(40, (255, 220, 120), 1.0), x, y)
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(255, 255, 255))
    dd = td()
    big(t, 0.3, counter(t, 0.4, 2.8, 0, 4800) + " KM", 300, 120, YEL)
    if t > L[1][0]:
        k = ease(clamp((t - L[1][0]) / 0.5))
        spaced(dd, W / 2, 460, "MADRID → MOSCÚ: 3.440 KM", f(F_SER, 46), (230, 230, 240, int(255 * k)), 4)
    vignette(img, 160)


def sh_ship(img, t, T, L):
    hz = 1080
    sky(img, (40, 36, 38), (96, 84, 76), 1.0)
    clouds(img, t, 300, (60, 52, 50), 200, 10, 9, 1.5)
    clouds(img, t * 1.4, 620, (80, 70, 64), 150, 14, 10, 1.2)
    hit = L[1][0] + 0.3
    sx, sy = shake(t, hit, 22, 4)
    bob = math.sin(t * 1.1) * 8
    paste(img, steamer(), 540 + sx + t * 6, hz - 150 + bob + sy, 0.95, 1.0, math.sin(t * 0.9) * 2)
    sea(img, t, hz, (50, 54, 60), (16, 18, 22), (120, 120, 126), 1.6)
    ash(img, t)
    if t > hit:
        overlay(img, (255, 250, 240), 0.85 * math.exp(-(t - hit) * 5))
    lower_third(img, t, 0.3, "NORHAM CASTLE", "A 64 KM DEL ORIGEN", 300, max(2.4, L[0][1]))
    vignette(img, 190)


def sh_db(img, t, T, L):
    sky(img, (12, 10, 16), (4, 4, 6), 1.0)
    spotlight(img, t, 540, 0, 1400, 140, 620, 50)
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, y1 = 300, 1380, 520
    q = ease(clamp((t - 0.3) / 2.6))
    top_db = 172 * q

    def ydb(v):
        return y0 - (y1 - y0) * -1 * 0 - (y0 - y1) * v / 180

    for v in range(0, 181, 10):
        y = ydb(v)
        d.line([(x0 - 30, y), (x0 - 6, y)], fill=(200, 200, 210, 200), width=3)
        if v % 30 == 0:
            d.text((x0 - 120, y - 22), str(v), font=f(F_SER, 40), fill=(220, 220, 230))
    nb = 36
    for i in range(nb):
        v0 = i * 180 / nb
        if v0 > top_db:
            break
        y = ydb(v0)
        col = (80, 200, 120) if v0 < 90 else ((240, 200, 60) if v0 < 140 else (235, 70, 60))
        d.rounded_rectangle([x0, y - 14, x0 + 260, y - 2], radius=4, fill=col + (255,))
    for v, lab in ((150, "AVIÓN AL DESPEGAR, CERCA"), (110, "CONCIERTO DE ROCK")):
        y = ydb(v)
        k = ease(clamp((t - L[1][0] + (0.0 if v == 150 else 0.6)) / 0.4))
        d.line([(x0 + 280, y), (x0 + 330, y)], fill=(255, 255, 255, int(220 * k)), width=3)
        d.text((x0 + 345, y - 20), lab, font=f(F_SER, 34), fill=(235, 235, 240, int(255 * k)))
    big(t, 0.3, counter(t, 0.3, 2.9, 0, 172) + " dB", 260, 130, YEL)
    if q > 0.98:
        paste(img, glow(260, (255, 120, 80), 0.6), x0 + 130, ydb(172), 1.0, 0.6 + 0.4 * math.sin(t * 8))
    vignette(img, 200)


def sh_barometer(img, t, T, L):
    sky(img, (30, 24, 20), (10, 8, 8), 1.0)
    spotlight(img, t, 380, 0, 1200, 120, 480, 45)
    paste(img, barometer(), 380, 760, 1.25)
    c = (380, 760)
    base = math.radians(270)
    wob = 0.0
    for k in range(5):
        tk = 0.6 + k * 0.9
        if t > tk:
            wob += math.exp(-(t - tk) * 3) * math.sin((t - tk) * 12) * 0.5
    a = base + wob
    d = ImageDraw.Draw(img, "RGBA")
    d.line([c, (c[0] + math.cos(a) * 230, c[1] + math.sin(a) * 230)], fill=(30, 26, 24), width=9)
    d.ellipse([c[0] - 18, c[1] - 18, c[0] + 18, c[1] + 18], fill=(150, 110, 50))
    # banda de registro
    py0 = 1180
    d.rectangle([0, py0, W, py0 + 200], fill=(236, 230, 214))
    for x in range(0, W, 60):
        d.line([(x, py0), (x, py0 + 200)], fill=(200, 190, 170), width=1)
    off = t * 120
    pts = []
    for x in range(0, W, 6):
        u = (x + off) / 300.0
        spike = sum(math.exp(-((u - k * 1.6) ** 2) * 30) * (1.0 - k * 0.15) for k in range(1, 9))
        pts.append((x, py0 + 120 - spike * 80 + math.sin(u * 7) * 3))
    d.line(pts, fill=(170, 30, 40), width=4)
    if t > L[1][0] + 1.0:
        big(t, L[1][0] + 1.0, "5 DÍAS", 300, 130, YEL)
    vignette(img, 190)


def sh_wave(img, t, T, L):
    space_bg(img, t, 8)
    gx, gy, r = 540, 920, 520
    paste(img, spr(globe_sprite, KRAK[0], KRAK[1], r, EXTRA), gx, gy)
    radii = []
    period = 2.2
    for k in range(6):
        u = (t - k * period / 2) / period
        if u > 0:
            ph = u % 1.0
            rr = r * math.sin(ph * math.pi)
            radii.append((rr, 0.9))
    AC(img, ring_layer(gx, gy, r, radii, (255, 210, 140), 12, 210))
    paste(img, glow(50, (255, 160, 80), 1.0), gx, gy, 1.0, 0.8)
    laps = min(4, int(t / period) + 1)
    big(t, 0.3, "3 O 4 VUELTAS", 280, 104, YEL, sub="AL PLANETA ENTERO")
    vignette(img, 170)


def sh_question(img, t, T, L):
    hz = 1150
    night_sky(img, t, hz, 0.7, (6, 6, 12), (40, 20, 24))
    paste(img, glow(460, (200, 70, 40), 0.7), 540, hz)
    smoke(img, t, [(560, hz - 20, 1.8)], col=(40, 34, 36), alpha=140, spread=(-40, 420), grow=120, speed=0.15)
    sea(img, t, hz, (30, 18, 22), (6, 4, 6), (120, 60, 50), 0.6)
    fog(img, t, hz + 60, 50, 16)
    big(t, 0.2, "¿QUÉ LA PROVOCÓ?", 320, 92, WHITE, pop=False)
    vignette(img, 220)


def sh_volcano(img, t, T, L):
    hz = 1180
    sky(img, (70, 64, 70), (180, 140, 110), 1.1)
    paste(img, glow(300, (255, 210, 160), 0.5), 800, 500)
    col_h = 300 + 500 * ease(clamp(t / T))
    smoke(img, t, [(560, hz - 420, 1.4), (540, hz - 460, 1.0)], col=(90, 84, 84), alpha=150, spread=(-60, col_h), grow=150, speed=0.2)
    paste(img, volcano_island(), 540, hz - 230 + 10)
    sea(img, t, hz, (60, 80, 96), (20, 28, 36), (150, 170, 180), 0.8)
    big(t, L[0][0] + 2.6, "KRAKATOA", 300, 130, YEL)
    lower_third(img, t, 0.4, "ESTRECHO DE LA SONDA", "ENTRE JAVA Y SUMATRA", 470, max(2.0, L[0][0] + 2.0))
    vignette(img, 170)


def sh_eruption(img, t, T, L):
    hz = 1180
    hit = max(0.8, L[0][1] - 0.6)
    sx, sy = shake(t, hit, 26, 3)
    pre = t < hit
    sky(img, (60, 40, 40), (160, 90, 60), 1.1) if not pre else sky(img, (70, 64, 70), (180, 140, 110), 1.1)
    if not pre:
        u = t - hit
        cr = 200 + 900 * (1 - math.exp(-u * 0.9))
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(4)
        for k in range(46):
            ang = rr.uniform(math.pi * 1.05, math.pi * 1.95)
            dist = rr.uniform(0.1, 1.0) * cr
            x = 540 + math.cos(ang) * dist * 0.8 + sx
            y = hz - 380 + math.sin(ang) * dist * 1.1 + sy
            rad = 60 + dist * 0.35
            g = int(40 + 40 * rr.random())
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(g, g - 6, g - 8, 230))
        paste(img, glow(420, (255, 120, 50), 0.9), 540 + sx, hz - 380 + sy, 1.0, 0.7 + 0.3 * math.sin(t * 9))
        particles(img, t, 60, 41, (255, 150, 60), -120, (2, 5), 220, 30, (200, 300, 880, hz))
    col = clamp((t - L[1][0] - 0.4) / 1.6)
    paste(img, volcano_island(round(col * 0.66, 2), not pre), 540 + sx, hz - 230 + 10 + sy)
    sea(img, t, hz, (60, 50, 50), (20, 14, 14), (150, 120, 110), 1.2)
    if not pre:
        overlay(img, (255, 245, 230), 0.9 * math.exp(-(t - hit) * 4))
    date_stamp(t, 0.2, "27 · 08 · 1883 · 10:02", 300, max(1.5, hit - 0.4))
    if t > L[1][0] + 1.0:
        big(t, L[1][0] + 1.0, "2/3 DE LA ISLA", 300, 104, YEL, sub="DESAPARECIERON")
    vignette(img, 190)


def sh_tsunami(img, t, T, L):
    hz = 1100
    sky(img, (40, 40, 48), (110, 100, 96), 1.0)
    clouds(img, t, 420, (70, 66, 70), 170, 10, 12, 1.4)
    sea(img, t, hz, (40, 56, 66), (12, 18, 22), (120, 140, 150), 1.4)
    q = ease(clamp(t / (T - 0.5)))
    wx = -600 + 900 * q
    d = ImageDraw.Draw(img, "RGBA")
    crest = []
    for k in range(60):
        u = k / 59
        x = wx - 700 + u * 1300
        y = hz + 120 - math.sin(min(1, u * 1.3) * math.pi / 2) ** 3 * 420 * (0.5 + 0.5 * q)
        crest.append((x, y))
    d.polygon(crest + [(crest[-1][0], H), (crest[0][0], H)], fill=(36, 60, 74, 255))
    d.line(crest[-20:], fill=(220, 236, 240, 230), width=14)
    ytop = min(y for _, y in crest)
    particles(img, t, 28, 44, (230, 240, 245), -50, (2, 4), 170, 20, (int(wx - 100), int(ytop - 90), int(wx + 500), int(ytop + 30)))
    ground(img, hz + 210, (24, 24, 28), (8, 8, 10))
    paste(img, huts(), 760, hz + 50)
    paste(img, palm(560, -0.2), 1000, hz - 50, 1.0, 1.0, -6 * q, flip=True)
    big(t, L[0][0] + 1.2, "+36.000", 300, 124, WHITE, sub="VÍCTIMAS")
    vignette(img, 200)


def sh_anak(img, t, T, L):
    hz = 1150
    sky(img, (24, 30, 70), (255, 150, 100), 1.3)
    paste(img, glow(380, (255, 190, 120), 0.8), 820, hz - 40)
    clouds(img, t, 520, (255, 190, 170), 60, 6, 15, 1.1)
    smoke(img, t, [(540, hz - 210, 0.7)], col=(140, 120, 120), alpha=110, spread=(-30, 360), grow=60, speed=0.18)
    paste(img, glow(60, (255, 120, 60), 1.0), 540, hz - 205, 1.0, 0.6 + 0.4 * math.sin(t * 3) ** 2)
    paste(img, volcano_island(0.0, True), 540, hz - 105, 0.45)
    sea(img, t, hz, (60, 50, 100), (16, 14, 34), (220, 160, 170), 0.6)
    lower_third(img, t, L[0][0] + 1.2, "ANAK KRAKATAU", "«EL HIJO DE KRAKATOA»", 330, 4.2)
    vignette(img, 170)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "tension"), ("volcano", "epic"), ("tsunami", "drone"), ("anak", "doc")],
    "duck": [("tsunami@L0", "anak+0.5", 0.35)],
    "amb": {"sea": ["rodrigues", "ship", "question", "volcano", "eruption", "tsunami", "anak"],
            "wind": ["ship", "eruption", "tsunami"], "space": ["open", "distance", "wave"]},
    "sfx": [("open@L1+0.85", "riser", 0.15), ("open@L1+0.9", "boom", 0.45),
            ("rodrigues@L1+0.4", "rumble", 0.3), ("rodrigues@L1+1.5", "rumble", 0.25), ("rodrigues@L1+2.4", "rumble", 0.22),
            ("distance+0.4", "whoosh_up", 0.12), ("distance+2.8", "ding", 0.1),
            ("ship@L1+0.3", "impact", 0.5), ("ship@L1+0.3", "ring", 0.25),
            ("db+0.3", "riser_long", 0.16), ("db+2.9", "impact", 0.3),
            ("barometer+0.6", "tick", 0.2), ("barometer+1.5", "tick", 0.2), ("barometer+2.4", "tick", 0.2),
            ("barometer@L1+1.0", "ding", 0.1),
            ("wave+0.2", "swell", 0.2), ("wave+1.5", "rumble", 0.15),
            ("question", "heart", 0.4), ("question+0.75", "heart", 0.4), ("question+1.5", "heart", 0.4),
            ("volcano+0.4", "rumble", 0.25), ("volcano@L0+2.6", "impact", 0.3),
            ("eruption@L0e-0.6", "boom", 0.6), ("eruption@L1+0.4", "rumble", 0.35),
            ("tsunami", "whoosh", 0.2), ("tsunami+0.5", "rumble", 0.3),
            ("anak@L0+1.2", "chime", 0.06)],
    "bed": [("rodrigues", "question")],
    "bpm": 92,
}
