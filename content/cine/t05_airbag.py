"""T05 · ¿Cómo se infla un airbag? (estilo Titanic, ilustración detallada con vista interior)."""
from gadgets import *
import t02_microondas as T2

xf, callout, glow_line, top_shade, wavy = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T2.wavy

TITLE = "Como_se_infla_un_airbag"
LINES = [
    "En un choque, el airbag se infla *más rápido que un parpadeo*.",
    "¿Cómo sabe que estás chocando… y de dónde sale tanto gas?",
    "Todo empieza con un sensor: un *acelerómetro*.",
    "Vigila sin parar *cuánto frena* el coche.",
    "Si frena de golpe, mucho más que en cualquier frenazo… detecta *un choque*.",
    "Al instante, manda una señal eléctrica a un *detonador*.",
    "El detonador prende una *pastilla química*.",
    "Durante años se usó *azida de sodio*: al reaccionar, suelta *nitrógeno*.",
    "El mismo gas que forma casi el *80 %* del aire que respiras.",
    "Unos 130 gramos dan para *67 litros* de gas.",
    "Y la bolsa se llena en unos *30 milisegundos*.",
    "Un parpadeo tarda *varias veces más*.",
    "Pero el airbag no es un cojín duro: tiene *agujeros*.",
    "Cuando tu cuerpo choca contra él, se va desinflando… y te frena *poco a poco*.",
    "Y está pensado para funcionar *junto al cinturón*: sin él, puede hacerte daño.",
    "Treinta milésimas de segundo… que *te pueden salvar la vida*.",
]
SHOTS = [("open", 0, 1, 0.3), ("sensor", 2, 4, 0.3), ("signal", 5, 6, 0.3), ("chem", 7, 9, 0.3), ("timing", 10, 11, 0.3),
         ("vents", 12, 13, 0.3), ("belt", 14, 15, 1.8)]
FOCUS = {"chem": (540, 900, 1.1), "timing": (540, 880, 1.1)}
NOTIF = ("sensor", 1.0)
HYPE = {"line": 1, "text": ['¿CÓMO SABE QUE CHOCAS?', '¿DE DÓNDE SALE EL GAS?'], "delay": [0, 1.8]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

RED = (196, 30, 36)
DUMMY = (240, 200, 60)
OX, OY = 120, 420  # esquina del sprite del maniquí en pantalla
HAND = (600, 330)
BAG_C = (450, 240)
N2C = (90, 140, 255)


# ------------------------------------------------------------------ maniquí, airbag, cabina
def _ik(sx, sy, hx, hy, l1, l2, bend=1):
    dx, dy = hx - sx, hy - sy
    d = min(math.hypot(dx, dy), l1 + l2 - 1)
    a = math.atan2(dy, dx)
    b = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1))
    return sx + math.cos(a + bend * b) * l1, sy + math.sin(a + bend * b) * l1


def dummy(lean=0.0, belt=False):
    c = Cv(720, 760)
    Y, Yd, K = DUMMY, (186, 146, 30), (34, 34, 38)
    hx, hy = 230, 560
    a = math.radians(-8 + lean * 34)
    up = (math.sin(a), -math.cos(a))
    P = lambda d_, s_=0: (hx + up[0] * d_ + math.cos(a) * s_, hy + up[1] * d_ + math.sin(a) * s_)
    knee, ankle = (470, 548), (566, 724)
    c.line([(hx, hy), knee], Yd, 96)
    c.line([(hx, hy - 10), knee], Y, 70)
    c.line([knee, ankle], Yd, 76)
    c.line([knee, (ankle[0] - 6, ankle[1])], Y, 54)
    c.rect((ankle[0] - 30, ankle[1] - 20, ankle[0] + 80, ankle[1] + 26), fill=K, r=12)
    for p, r in ((knee, 40), ((hx, hy), 52)):
        c.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=K)
    sh = P(300)
    c.line([(hx, hy), sh], Yd, 150)
    c.line([P(0, -12), P(300, -12)], Y, 116)
    c.line([P(40, -40), P(270, -40)], (255, 236, 150), 18)
    nk, hd = P(350), P(430)
    c.line([sh, nk], K, 40)
    c.ellipse((hd[0] - 74, hd[1] - 80, hd[0] + 74, hd[1] + 80), radial=((255, 230, 120), Yd), center=(0.38, 0.32))
    c.ellipse((hd[0] - 34, hd[1] - 34, hd[0] + 34, hd[1] + 34), fill=(250, 250, 250))
    c.poly([(hd[0], hd[1] - 34), (hd[0] + 34, hd[1]), (hd[0], hd[1]), ], fill=K)
    c.poly([(hd[0], hd[1] + 34), (hd[0] - 34, hd[1]), (hd[0], hd[1])], fill=K)
    c.ellipse((hd[0] - 34, hd[1] - 34, hd[0] + 34, hd[1] + 34), fill=None)
    c.arc((hd[0] - 34, hd[1] - 34, hd[0] + 34, hd[1] + 34), 0, 360, K, 4)
    el = _ik(sh[0], sh[1], HAND[0], HAND[1], 190, 190, -1)
    c.line([sh, el], Yd, 66)
    c.line([el, HAND], Yd, 58)
    c.line([sh, el], Y, 46)
    c.line([el, HAND], Y, 40)
    c.ellipse((el[0] - 30, el[1] - 30, el[0] + 30, el[1] + 30), fill=K)
    c.ellipse((sh[0] - 44, sh[1] - 44, sh[0] + 44, sh[1] + 44), fill=K)
    c.ellipse((HAND[0] - 30, HAND[1] - 30, HAND[0] + 30, HAND[1] + 30), fill=Yd)
    hip_m = (hx + 10, hy + 6)
    c.ellipse((hip_m[0] - 26, hip_m[1] - 26, hip_m[0] + 26, hip_m[1] + 26), fill=(250, 250, 250))
    c.arc((hip_m[0] - 26, hip_m[1] - 26, hip_m[0] + 26, hip_m[1] + 26), 0, 90, K, 26)
    c.arc((hip_m[0] - 26, hip_m[1] - 26, hip_m[0] + 26, hip_m[1] + 26), 180, 270, K, 26)
    if belt:
        b0, b1 = P(290, -60), P(10, 70)
        c.line([b0, b1], (50, 52, 60), 26)
        c.line([b0, b1], (90, 94, 104), 8)
        c.line([(hx - 60, hy - 10), (hx + 80, hy - 30)], (50, 52, 60), 26)
        c.rect((b1[0] - 18, b1[1] - 14, b1[0] + 18, b1[1] + 14), fill=(190, 194, 200), r=4)
    return c.done()


def airbag(k=1.0, deflate=0.0):
    rx, ry = 180 * k, 168 * k * (1 - 0.25 * deflate)
    w, h = 420, 400
    c = Cv(w, h)
    if k <= 0.02:
        return c.done()
    cx, cy = w / 2, h / 2
    c.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), radial=((255, 255, 255), (178, 182, 192)), power=1.3, center=(0.42, 0.36))
    for i in range(4):
        yy = cy - ry * 0.6 + i * ry * 0.4
        c.arc((cx - rx * 0.8, yy - 20, cx + rx * 0.8, yy + 30), 200, 340, (150, 154, 166, 140), 3)
    c.arc((cx - rx * 0.96, cy - ry * 0.96, cx + rx * 0.96, cy + ry * 0.96), 100, 160, (140, 144, 156, 150), 4)
    return c.done()


def _cabin():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((34, 36, 44), (10, 10, 12)))
    # carrocería cortada
    roof = [(60, 1220), (60, 760), (140, 560), (300, 470), (700, 460), (980, 760), (1080, 800), (1080, 1220)]
    c.poly(roof, grad=(shade(RED, 1.1), shade(RED, 0.5)))
    inner = [(90, 1190), (90, 770), (160, 590), (310, 502), (690, 494), (950, 772), (1080, 820), (1080, 1190)]
    c.poly(inner, grad=((70, 72, 80), (30, 32, 38)))
    c.poly([(700, 494), (950, 772), (930, 790), (690, 520)], fill=(140, 180, 220, 90))
    c.poly([(760, 700), (1080, 760), (1080, 900), (820, 880)], grad=((50, 52, 60), (24, 24, 28)))
    c.rect((90, 1170, 1080, 1220), grad=((60, 60, 66), (20, 20, 24)))
    # asiento
    hx, hy = OX + 230, OY + 560
    a = math.radians(-12)
    up = (math.sin(a), -math.cos(a))
    p0 = (hx - 110, hy + 70)
    p1 = (hx - 70 + up[0] * 380, hy + up[1] * 380)
    c.line([p0, p1], (40, 40, 46), 70)
    c.line([(p0[0] + 10, p0[1]), (p1[0] + 10, p1[1])], (62, 62, 70), 36)
    c.rect((p1[0] - 46, p1[1] - 120, p1[0] + 30, p1[1] - 10), fill=(46, 46, 52), r=22)
    c.poly([(hx - 130, hy + 30), (hx + 230, hy + 10), (hx + 230, hy + 80), (hx - 130, hy + 110)], grad=((62, 62, 70), (36, 36, 42)))
    c.rect((hx - 90, hy + 110, hx + 160, 1170), fill=(30, 30, 34))
    # volante y columna
    wx, wy = OX + HAND[0] + 40, OY + HAND[1] + 20
    c.line([(wx + 10, wy + 40), (wx + 190, wy + 170)], (60, 62, 70), 30)
    c.ellipse((wx - 26, wy - 120, wx + 26, wy + 120), fill=None)
    c.line([(wx - 10, wy - 118), (wx + 14, wy + 118)], (20, 20, 22), 30)
    c.ellipse((wx - 30, wy - 30, wx + 40, wy + 40), radial=((90, 92, 100), (30, 30, 34)))
    # pedales y caja del sensor
    c.rect((470, 1130, 600, 1170), grad=((80, 84, 92), (40, 42, 48)), r=6)
    c.line([(OX + 640, OY + 640), (OX + 700, OY + 740)], (50, 50, 56), 12)
    return c.done().convert("RGBA")


def cabin(img, t, lean=0.0, bag=0.0, deflate=0.0, belt=False, wire=0.0):
    AC(img, cached("cabin", _cabin))
    for x in (200, 860):
        paste(img, glow(300, (255, 240, 210), 0.15), x, 300)
    if wire > 0:
        pts = [(535, 1150), (535, 1100), (700, 1060), (820, 900), (OX + HAND[0] + 50, OY + HAND[1] + 30)]
        glow_line(img, pts, (90, 200, 255), 4, 8, 120)
        segs = wavy(pts, wire, 0, 10, 0)
        if segs:
            x, y = segs[-1]
            paste(img, glow(90, (160, 230, 255), 1.0), x, y)
            glow_line(img, segs[max(0, len(segs) - 30):], (200, 240, 255), 6, 10, 255)
    paste(img, spr(dummy, round(lean, 2), belt), OX + 360, OY + 380, 1.0)
    if bag > 0:
        bx, by = OX + BAG_C[0], OY + BAG_C[1]
        paste(img, spr(airbag, round(bag, 2), round(deflate, 2)), bx + 40 * (1 - bag), by + 10, 1.0)


def _lab_track():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((26, 28, 34), (8, 8, 10)))
    c.rect((0, 1180, W, H), grad=((50, 50, 56), (18, 18, 20)))
    for x in range(0, W, 120):
        c.rect((x, 1180, x + 60, 1194), fill=(230, 200, 40))
    c.rect((880, 800, 1080, 1180), grad=((140, 140, 144), (80, 80, 86)))
    for y in range(800, 1180, 60):
        c.line([(880, y), (1080, y)], (90, 90, 96), 4)
    for y in range(820, 1180, 120):
        c.poly([(880, y), (920, y), (880, y + 40)], fill=(230, 200, 40))
    return c.done().convert("RGBA")


def crash(img, t, hit):
    AC(img, cached("labtrack", _lab_track))
    for x in (180, 540, 900):
        spotlight(img, t, x, 0, 1400, 40, 260, 34, dust=False)
    x = lerp(-300, 450, clamp(t / hit)) if t < hit else 450
    sx, sy = shake(t, hit, 20, 5)
    paste_car(img, x + sx, 1180 + sy, 0.82, RED, False, -t * 12)
    if t > hit:
        overlay(img, (255, 255, 255), 0.85 * math.exp(-(t - hit) * 6))


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    hit = 1.3

    def A(im):
        crash(im, t, hit)

    def B(im):
        q = clamp((t - 1.8) / 1.6)
        cabin(im, t, ease(q) * 0.55, ease(clamp((t - 1.8) / 0.9)))
        if t > a1:
            overlay(im, (6, 10, 20), 0.35 * ease(clamp((t - a1) / 0.6)))
    xf(img, t, 1.7, A, B, 0.5)
    top_shade(img)
    if t < a1:
        big(t, 2.0, "MÁS RÁPIDO", 270, 96, WHITE, sub="QUE UN PARPADEO")
    vignette(img, 200)


def _pcb():
    c = Cv(W, 900, 2)
    c.rect((0, 0, W, 900), grad=((20, 90, 60), (8, 46, 30)))
    rr = random.Random(3)
    for i in range(60):
        x0, y0 = rr.uniform(0, W), rr.uniform(0, 900)
        x1 = x0 + rr.choice([-1, 1]) * rr.uniform(80, 300)
        c.line([(x0, y0), (x1, y0), (x1 + 40, y0 + rr.choice([-40, 40]))], (200, 170, 80), 5)
        c.ellipse((x0 - 9, y0 - 9, x0 + 9, y0 + 9), fill=(220, 190, 100))
    c.rect((360, 260, 720, 620), grad=((40, 40, 46), (14, 14, 16)), r=16)
    for k in range(8):
        y = 290 + k * 42
        c.rect((320, y, 360, y + 16), fill=(200, 200, 206))
        c.rect((720, y, 760, y + 16), fill=(200, 200, 206))
    c.text((540, 440), "ACC", 60, (200, 200, 210))
    c.ellipse((380, 280, 404, 304), fill=(80, 80, 86))
    return c.done().convert("RGBA")


def mems(img, t, dx, cx=540, cy=640):
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([cx - 420, cy - 250, cx + 420, cy + 250], radius=26, fill=(26, 28, 34, 255), outline=(120, 130, 150, 255), width=4)
    for sgn in (-1, 1):
        for k in range(6):
            y = cy - 180 + k * 70
            xa, xb = sorted((cx + sgn * 400, cx + sgn * 230))
            d.rectangle([xa, y, xb, y + 20], fill=(150, 156, 170, 255))
    d.rectangle([cx - 190 + dx, cy - 210, cx + 190 + dx, cy + 210], fill=(190, 196, 210, 255))
    d.rectangle([cx - 190 + dx, cy - 210, cx + 190 + dx, cy - 196], fill=(240, 244, 250, 255))
    for sgn in (-1, 1):
        for k in range(6):
            y = cy - 145 + k * 70
            xa, xb = sorted((cx + sgn * 190 + dx, cx + sgn * 290 + dx))
            d.rectangle([xa, y, xb, y + 20], fill=(190, 196, 210, 255))
    for sgn in (-1, 1):
        pts = []
        for k in range(9):
            pts.append((cx + dx * (k / 8) + (16 if k % 2 else -16), cy + sgn * (210 + k * 4)))
        d.line(pts, fill=(170, 176, 190, 255), width=5)
    spaced(d, cx, cy + 300, "MASA QUE SE MUEVE CON EL FRENAZO", f(F_SER, 30), (200, 210, 230, 220), 3)


def graph(img, t, t0, spike_t=None):
    x0, y0, x1, y1 = 80, 980, 1000, 1330
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=(8, 14, 12, 235), outline=(60, 120, 90, 255), width=3)
    for k in range(1, 6):
        d.line([(x0, y0 + k * (y1 - y0) / 6), (x1, y0 + k * (y1 - y0) / 6)], fill=(60, 120, 90, 60), width=1)
    thr = y0 + 80
    d.line([(x0 + 10, thr), (x1 - 10, thr)], fill=(255, 80, 80, 200), width=3)
    d.text((x1 - 20, thr - 26), "UMBRAL DE CHOQUE", font=f(F_SER, 26), fill=(255, 120, 120, 230), anchor="rm")
    pts = []
    base = y1 - 60
    for i in range(0, 200):
        u = i / 199
        tt = t - (1 - u) * 3.0
        v = 18 * (0.5 + 0.5 * math.sin(tt * 3.1)) + 8 * math.sin(tt * 11) + (40 if (tt % 2.7) < 0.5 else 0)
        if spike_t is not None and tt > spike_t:
            v += 300 * math.exp(-((tt - spike_t - 0.25) / 0.12) ** 2)
        pts.append((x0 + 10 + u * (x1 - x0 - 20), base - v))
    glow_line(img, pts, (90, 255, 160), 3, 6, 230)
    d.text((x0 + 20, y0 + 20), "FRENADA (g)", font=f(F_SER, 28), fill=(140, 230, 180, 220))


def sh_sensor(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    sky(img, (12, 20, 18), (4, 8, 6), 1.0)
    if t < 1.6:
        AC(img, cached("pcb", _pcb), (0, 300))
        k = ease(clamp((t - 0.6) / 0.8))
        callout(img, t, 0.4, 720, 560, 860, 1000, "ACELERÓMETRO", YEL, 40)
        overlay(img, (0, 0, 0), 0.5 * k)
    else:
        k = ease(clamp((t - 1.6) / 0.5))
        dx = math.sin(t * 7) * 6
        if t > a2:
            dx = 70 * math.exp(-((t - a2 - 1.7) / 0.5) ** 2) + math.sin(t * 7) * 6
        mems(img, t, dx)
        overlay(img, (0, 0, 0), 0.5 * (1 - k))
    if t > a1 - 0.3:
        graph(img, t, a1, (a2 + 0.6) if t > a2 else None)
    if t > a2 + 1.9:
        kk = ease(clamp((t - a2 - 1.9) / 0.3))
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([340, 1040, 740, 1120], radius=16, fill=(220, 40, 40, int(230 * kk)))
        d.text((540, 1080), "¡CHOQUE!", font=f(F_CAP, 50), fill=(255, 255, 255, int(255 * kk)), anchor="mm")
    if t < a1:
        big(t, 0.3, "UN ACELERÓMETRO", 290, 80, YEL, pop=False)
    elif t < a2:
        big(t, a1 + 0.2, "VIGILA LA FRENADA", 290, 76, WHITE, pop=False)
    else:
        big(t, a2 + 1.9, "DETECTA EL CHOQUE", 290, 76, (255, 110, 100))
    vignette(img, 200)


def inflator(img, t, t0):
    sky(img, (24, 20, 18), (6, 6, 6), 1.0)
    cx, cy = 540, 860
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([cx - 330, cy - 200, cx + 330, cy + 200], radius=60, fill=(150, 154, 162, 255))
    d.rounded_rectangle([cx - 300, cy - 170, cx + 300, cy + 170], radius=40, fill=(40, 40, 44, 255))
    ign = ease(clamp((t - t0 - 0.6) / 1.4))
    rr = random.Random(5)
    for i in range(26):
        x, y = cx - 260 + (i % 9) * 64 + rr.uniform(-6, 6), cy - 120 + (i // 9) * 100 + rr.uniform(-6, 6)
        dist = math.hypot(x - cx, y - cy) / 300
        lit = clamp((ign - dist * 0.6) / 0.4)
        col = (int(lerp(200, 255, lit)), int(lerp(190, 150, lit)), int(lerp(150, 50, lit)))
        d.rounded_rectangle([x - 26, y - 18, x + 26, y + 18], radius=8, fill=col + (255,))
        if lit > 0:
            paste(img, glow(60, (255, 160, 60), 0.9), x, y, 1.0, lit)
    d.rounded_rectangle([cx - 40, cy - 50, cx + 40, cy + 50], radius=12, fill=(200, 160, 60, 255))
    if t > t0 + 0.5:
        paste(img, glow(200, (255, 230, 150), 1.0), cx, cy, 1.0, clamp(1 - (t - t0 - 0.5) * 1.2) + 0.2 * ign)
    callout(img, t, t0 + 0.2, cx, cy, 540, 520, "DETONADOR", YEL, 38)
    callout(img, t, t0 + 1.0, cx + 230, cy + 100, 820, 1260, "PASTILLAS", (255, 200, 140), 34)


def sh_signal(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: cabin(im, t, 0.0, 0.0, 0.0, False, ease(clamp((t - 0.4) / 1.4))), lambda im: inflator(im, t, a1), 0.6)
    if t < a1:
        big(t, 0.3, "SEÑAL AL DETONADOR", 290, 72, (140, 210, 255), pop=False)
    else:
        big(t, a1 + 0.3, "¡PRENDE!", 290, 104, (255, 160, 60))
    vignette(img, 200)


def n2():
    c = Cv(220, 140)
    for x in (70, 150):
        c.ellipse((x - 56, 14, x + 56, 126), radial=((180, 210, 255), (40, 70, 200)), center=(0.38, 0.32))
    return c.done()


def chem_burst(img, t, t0):
    sky(img, (14, 18, 34), (4, 6, 12), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(2)
    for i in range(14):
        x, y = 260 + i * 42 + rr.uniform(-10, 10), 1180 + rr.uniform(-20, 20)
        d.rounded_rectangle([x - 34, y - 22, x + 34, y + 22], radius=10, fill=(236, 232, 220, 255), outline=(180, 176, 166, 255), width=2)
    spaced(d, 540, 1280, "AZIDA DE SODIO", f(F_SER, 40), (230, 230, 230, 230), 6)
    k = clamp((t - t0 - 0.6) / 2.4)
    m = spr(n2)
    rr = random.Random(9)
    for i in range(40):
        st = rr.uniform(0, 1)
        u = clamp((k - st * 0.6) / 0.6)
        if u <= 0:
            continue
        x = 540 + rr.uniform(-1, 1) * 440 * u
        y = 1160 - u * rr.uniform(400, 760)
        paste(img, m, x, y, 0.42, min(1, u * 3), rr.uniform(0, 360) + t * 60)
    if k > 0.3:
        spaced(d, 540, 470, "NITRÓGENO", f(F_SER, 46), (160, 200, 255, int(255 * clamp((k - 0.3) / 0.3))), 6)


def air_donut(img, t, t0):
    sky(img, (110, 160, 220), (200, 225, 245), 1.0)
    clouds(img, t, 420, (255, 255, 255), 120, 10, 4, 1.0)
    cx, cy, r = 540, 880, 300
    k = ease(clamp((t - t0 - 0.2) / 1.2))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], fill=(255, 255, 255, 120))
    a0 = -90
    for frac, col in ((0.78, (60, 110, 230)), (0.21, (230, 70, 70)), (0.01, (150, 150, 160))):
        a1_ = a0 + 360 * frac * k
        d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a1_, fill=col + (255,))
        a0 = a1_
    d.ellipse([cx - 170, cy - 170, cx + 170, cy + 170], fill=(240, 246, 252, 255))
    d.text((cx, cy - 40), "AIRE", font=f(F_SER, 56), fill=(40, 50, 70), anchor="mm")
    d.text((cx, cy + 30), "NITRÓGENO", font=f(F_SER, 40), fill=(60, 110, 230), anchor="mm")
    d.text((cx, cy + 82), "≈ 78 %", font=f(F_SER, 44), fill=(60, 110, 230), anchor="mm")


def grams(img, t, t0):
    sky(img, (30, 26, 22), (10, 8, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1180, W, H], fill=(60, 44, 32, 255))
    d.rounded_rectangle([140, 1060, 440, 1180], radius=16, fill=(170, 174, 182, 255))
    d.rounded_rectangle([160, 1000, 420, 1070], radius=12, fill=(30, 40, 30, 255))
    d.text((290, 1036), "130 g", font=f(F_MONO, 48), fill=(120, 255, 170), anchor="mm")
    rr = random.Random(3)
    for i in range(10):
        x, y = 200 + (i % 5) * 46, 960 - (i // 5) * 30
        d.rounded_rectangle([x - 22, y - 14, x + 22, y + 14], radius=8, fill=(236, 232, 220, 255))
    k = ease(clamp((t - t0 - 0.6) / 1.4))
    r = 60 + 300 * k
    bx, by = 740, 1170 - r
    bag = spr(airbag, 1.0, 0.0)
    paste(img, bag, bx, by + 20, r / 180, 0.95)
    d = ImageDraw.Draw(img, "RGBA")
    if k > 0.6:
        spaced(d, bx, by, "67 L", f(F_SER, 90), (40, 44, 60, int(255 * clamp((k - 0.6) / 0.3))), 4, shadow=False)


def sh_chem(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a2 - 0.4:
        xf(img, t, a1, lambda im: chem_burst(im, t, 0), lambda im: air_donut(im, t, a1), 0.6)
    else:
        xf(img, t, a2, lambda im: air_donut(im, t, a1), lambda im: grams(im, t, a2), 0.6)
    if t < a1:
        big(t, 0.3, "SUELTA NITRÓGENO", 300, 80, (160, 200, 255), pop=False)
    elif t < a2:
        big(t, a1 + 0.2, "CASI EL 80 %", 300, 100, (30, 60, 140), sub="DEL AIRE", subcol=(40, 60, 100))
    else:
        big(t, a2 + 0.3, "130 g → 67 LITROS", 300, 80, YEL, pop=False)
    vignette(img, 190)


def sh_timing(img, t, T, L):
    a1 = L[1][0]
    sky(img, (20, 22, 30), (6, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    if t < a1:
        for i, (ms, k) in enumerate(((0, 0.05), (10, 0.4), (20, 0.75), (30, 1.0))):
            kk = ease(clamp((t - 0.4 - i * 0.5) / 0.4))
            x = 110 + (i % 2) * 460
            y = 500 + (i // 2) * 440
            d.rounded_rectangle([x, y, x + 400, y + 400], radius=16, fill=(40, 42, 50, int(255 * kk)), outline=(255, 255, 255, int(120 * kk)), width=3)
            if kk > 0:
                d.rounded_rectangle([x + 300, y + 90, x + 360, y + 330], radius=26, fill=(16, 16, 18, int(255 * kk)))
                paste(img, spr(airbag, k, 0.0), x + 300 - 150 * k, y + 200, 0.85, kk)
                d = ImageDraw.Draw(img, "RGBA")
                d.rounded_rectangle([x + 120, y + 344, x + 280, y + 390], radius=10, fill=(0, 0, 0, int(160 * kk)))
                d.text((x + 200, y + 367), f"{ms} ms", font=f(F_MONO, 36), fill=YEL + (int(255 * kk),), anchor="mm")
    else:
        k = ease(clamp((t - a1 - 0.2) / 0.8))
        bl = clamp((t - a1 - 1.2) / 1.8)
        lid = math.sin(math.pi * clamp(bl * 1.0)) if bl < 1 else 0
        ex, ey = 540, 700
        e = spr(T2.eye)
        e = e.resize((e.size[0], max(4, int(e.size[1] * (1 - 0.94 * lid)))), Image.BILINEAR)
        paste(img, e, ex, ey, 1.6, k)
        d = ImageDraw.Draw(img, "RGBA")
        x0 = 140
        d.rounded_rectangle([x0, 980, x0 + 140 * k, 1040], radius=12, fill=YEL + (255,))
        spaced(d, x0 + 260, 1010, "AIRBAG", f(F_SER, 36), (255, 255, 255, int(255 * k)), 4)
        kb = ease(clamp((t - a1 - 1.0) / 1.2))
        d.rounded_rectangle([x0, 1090, x0 + 800 * kb, 1150], radius=12, fill=(140, 200, 255, 255))
        spaced(d, x0 + 160, 1180 + 10, "PARPADEO", f(F_SER, 36), (255, 255, 255, int(255 * kb)), 4)
    if t < a1:
        big(t, 0.3, "30 MILISEGUNDOS", 300, 84, YEL, pop=False)
    else:
        big(t, a1 + 0.2, "VARIAS VECES MÁS", 300, 80, (140, 200, 255), pop=False)
    vignette(img, 200)


def bag_back(img, t):
    sky(img, (26, 28, 36), (8, 8, 10), 1.0)
    paste(img, spr(airbag, 1.0, 0.0), 540, 860, 2.2)
    d = ImageDraw.Draw(img, "RGBA")
    for hx, hy in ((380, 1000), (700, 1000)):
        d.ellipse([hx - 40, hy - 26, hx + 40, hy + 26], fill=(60, 62, 70, 255), outline=(200, 204, 214, 255), width=5)
    T2.smoke(img, t, [(380, 1040, 0.9), (700, 1040, 0.9)], col=(235, 240, 250), alpha=70, spread=(60, 20), grow=90, speed=0.9)
    callout(img, t, 0.6, 700, 1000, 860, 1300, "AGUJEROS", YEL, 38)


def sh_vents(img, t, T, L):
    a1 = L[1][0]

    def B(im):
        q = clamp((t - a1 - 0.2) / 2.6)
        cabin(im, t, 0.2 + 0.5 * ease(q), 1.0, ease(q), False)
        T2.smoke(im, t, [(OX + BAG_C[0] - 60, OY + BAG_C[1] + 140, 0.7)], col=(235, 240, 250), alpha=60, spread=(50, 20), grow=70, speed=0.9)
    xf(img, t, a1, lambda im: bag_back(im, t), B, 0.7)
    if t < a1:
        big(t, 0.3, "NO ES UN COJÍN DURO", 290, 70, WHITE, pop=False)
    else:
        big(t, a1 + 0.3, "TE FRENA POCO A POCO", 290, 66, YEL, pop=False)
    vignette(img, 200)


def sh_belt(img, t, T, L):
    a1 = L[1][0]

    def A(im):
        cabin(im, t, 0.25, 1.0, 0.3, True)
        k = ease(clamp((t - 1.0) / 0.4))
        d = ImageDraw.Draw(im, "RGBA")
        x, y = 900, 1060
        d.ellipse([x - 70, y - 70, x + 70, y + 70], fill=(40, 170, 90, int(255 * k)), outline=(255, 255, 255, int(255 * k)), width=5)
        d.line([(x - 32, y), (x - 8, y + 26), (x + 36, y - 26)], fill=(255, 255, 255, int(255 * k)), width=14, joint="curve")

    def B(im):
        highway_night(im, t, 1.0, 820)
        paste(im, car_rear(RED, 0.0), 540, lerp(1180, 1080, ease(clamp((t - a1) / (T - a1)))), lerp(1.0, 0.7, ease(clamp((t - a1) / (T - a1)))))
    xf(img, t, a1, A, B, 0.8)
    if t < a1:
        top_shade(img)
        big(t, 0.3, "AIRBAG + CINTURÓN", 280, 76, YEL, pop=False)
    else:
        top_shade(img)
        title2(t, a1 + 0.3, "30 MILÉSIMAS", "QUE SALVAN VIDAS", 260, 60, 84, hold=max(2.0, T - a1 - 0.8), c1=YEL, c2=WHITE)
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "tension"), ("sensor", "exp"), ("chem", "creative"), ("timing", "tension"), ("vents", "doc"), ("belt", "epic")],
    "gains": {"exp": 0.7},
    "duck": [("open+1.2", "open+2.2", 0.5)],
    "amb": {"hum": ["sensor", "signal"], "road": ["belt"], "wind": ["chem"]},
    "sfx": [("open+0.1", "whoosh", 0.15), ("open+1.3", "boom", 0.45), ("open+1.3", "impact", 0.4), ("open+1.8", "whoosh_up", 0.2),
            ("sensor+0.4", "pop", 0.15), ("sensor+1.6", "whoosh", 0.12), ("sensor@L1", "beep", 0.05), ("sensor@L2+0.6", "riser", 0.1),
            ("sensor@L2+1.9", "impact", 0.25), ("sensor@L2+1.9", "beep", 0.08),
            ("signal+0.4", "zap", 0.12), ("signal+1.6", "click", 0.3), ("signal@L1+0.5", "crackle", 0.2), ("signal@L1+0.6", "boom", 0.25),
            ("chem+0.6", "whoosh_up", 0.15), ("chem@L1+0.2", "swell", 0.12), ("chem@L2+0.6", "whoosh_up", 0.14),
            ("timing+0.4", "tick", 0.2), ("timing+0.9", "tick", 0.2), ("timing+1.4", "tick", 0.2), ("timing+1.9", "pop", 0.2),
            ("timing@L1+1.4", "blip_down", 0.1),
            ("vents+0.6", "whoosh", 0.12), ("vents@L1+0.4", "thud", 0.25), ("vents@L1+0.8", "whoosh", 0.1),
            ("belt+0.6", "click", 0.3), ("belt+1.0", "ding", 0.08), ("belt@L1+0.3", "swell", 0.14)],
    "bed": [("sensor", "signal")],
    "bpm": 104,
}
