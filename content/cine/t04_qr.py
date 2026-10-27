"""T04 · ¿Qué esconde un código QR? (estilo Titanic, ilustración detallada)."""
from gadgets import *
import t02_microondas as T2
import t03_tactil as T3

xf, callout, glow_line, top_shade, sepia = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T2.sepia

TITLE = "Que_esconde_un_codigo_QR"
LINES = [
    "Un código QR parece ruido… pero tu móvil lo lee en *menos de un segundo*.",
    "¿Qué esconden esos cuadraditos?",
    "Se inventó en Japón en 1994, en la empresa *Denso Wave*.",
    "Querían seguir *las piezas de los coches* en las fábricas.",
    "Lo primero que busca la cámara son estos *tres cuadrados*.",
    "Le dicen dónde está el código… y si está *girado o torcido*.",
    "Y un cuadrado más pequeño ayuda a *corregir la perspectiva*.",
    "Luego divide el código en una rejilla y lee cada casilla: negra es *1*, blanca es *0*.",
    "Son *bits*, como los de un ordenador.",
    "Juntando bits salen *números, letras*… o una *dirección web*.",
    "En un solo QR caben hasta *7.089 números*.",
    "Y lo mejor: guarda la información *repetida* de forma inteligente.",
    "Aunque se rompa o se tape hasta *un 30 %*, se puede leer igual.",
    "Por eso hay QR con *logotipos* en medio.",
    "Su diseño se inspiró en un juego: las fichas blancas y negras del *Go*.",
    "Y Denso Wave decidió *no cobrar* por usar su patente.",
    "Por eso hoy está *en todas partes*.",
    "A veces, lo que parece *ruido*… es *puro orden*.",
]
SHOTS = [("open", 0, 1, 0.3), ("factory", 2, 3, 0.3), ("finders", 4, 6, 0.3), ("bits", 7, 10, 0.3), ("damage", 11, 13, 0.3),
         ("go", 14, 14, 0.3), ("free", 15, 17, 1.8)]
FOCUS = {"open": (420, 760, 1.32), "factory": (540, 900, 1.1), "go": (540, 880, 1.12)}
NOTIF = ("finders", 1.0)
HYPE = {"line": 1, "text": ['¿QUÉ ESCONDEN', 'ESOS CUADRADITOS?'], "delay": [0, 0.7]}
KW_OVERRIDE = {0: [], 14: ["FICHAS BLANCAS Y NEGRAS"], 17: []}
NARRATOR = {"open": ("wave", "left"), "factory": ("point", "left"), "finders": ("point", "left"), "bits": ("think", "left"),
            "damage": ("surprise", "left"), "go": ("point", "left"), "free": ("smirk", "left")}
NARRATOR_SCALE = 0.62   # los QR y el tablero bajan mucho: mascota algo más pequeña para no taparlos
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

N, Q, PX = 25, 2, 20
QS = (N + 2 * Q) * PX
GREEN = (90, 230, 130)


# ------------------------------------------------------------------ utilidades
def homog(src, dst):
    A, B = [], []
    for (x, y), (X, Y) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -X * x, -X * y])
        B.append(X)
        A.append([0, 0, 0, x, y, 1, -Y * x, -Y * y])
        B.append(Y)
    return np.linalg.solve(np.array(A, float), np.array(B, float))


def hmap(c, x, y):
    w_ = c[6] * x + c[7] * y + 1
    return ((c[0] * x + c[1] * y + c[2]) / w_, (c[3] * x + c[4] * y + c[5]) / w_)


def warp_paste(img, im, quad, alpha=1.0):
    w, h = im.size
    xs, ys = [p[0] for p in quad], [p[1] for p in quad]
    x0, y0 = int(math.floor(min(xs))), int(math.floor(min(ys)))
    x1, y1 = int(math.ceil(max(xs))), int(math.ceil(max(ys)))
    dst = [(x - x0, y - y0) for x, y in quad]
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    coef = homog(dst, src)
    out = im.transform((x1 - x0, y1 - y0), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC)
    if alpha < 1:
        out = with_alpha(out, alpha)
    AC(img, out, (x0, y0)) if x0 >= 0 and y0 >= 0 else img.paste(out, (x0, y0), out)
    return homog(src, quad)


def qr(seed=7, logo=False, n=N, px=PX):
    return spr(qr_sprite, px, seed, n, (16, 16, 20), (250, 248, 242), Q, logo)


def cup():
    c = Cv(300, 260)
    c.shadow((10, 200, 290, 256), 140, 8)
    c.ellipse((10, 190, 290, 246), radial=((250, 248, 244), (190, 186, 180)), power=1.0)
    c.arc((196, 70, 286, 170), 280, 80, (230, 228, 222), 18)
    c.poly([(50, 50), (250, 50), (230, 200), (70, 200)], grad=((252, 250, 246), (180, 176, 170)), horizontal=True)
    c.ellipse((50, 36, 250, 70), fill=(240, 238, 232))
    c.ellipse((60, 42, 240, 66), radial=((150, 96, 60), (70, 40, 22)))
    c.ellipse((100, 46, 150, 54), fill=(255, 230, 200, 60))
    return c.done()


def table_card():
    c = Cv(400, 560)
    c.shadow((20, 520, 380, 560), 150, 10)
    c.poly([(30, 30), (370, 30), (370, 530), (30, 530)], grad=((252, 250, 244), (220, 214, 202)))
    c.rect((30, 30, 370, 110), grad=((60, 40, 30), (40, 26, 20)))
    c.text((200, 70), "MENÚ", 40, (255, 230, 190))
    q = qr()
    qq = q.resize((300, 300), Image.LANCZOS)
    c.im.alpha_composite(qq.resize((900, 900), Image.BILINEAR), (150, 400))
    c.text((200, 500), "ESCANEA LA CARTA", 22, (60, 50, 40))
    return c.done()


def _cafe():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, 1000), grad=((60, 40, 30), (34, 22, 18)))
    rr = random.Random(5)
    for i in range(40):
        x, y, r = rr.uniform(0, W), rr.uniform(0, 900), rr.uniform(30, 90)
        c.ellipse((x - r, y - r, x + r, y + r), fill=rr.choice([(255, 190, 110), (255, 150, 80), (255, 220, 160)]) + (rr.randint(20, 60),))
    for k in range(9):
        y0 = 1000 + k * 110
        c.rect((0, y0, W, y0 + 110), grad=((150, 100, 60), (110, 70, 40)))
        c.line([(0, y0), (W, y0)], (80, 50, 30), 3)
    im = c.done().convert("RGBA").filter(ImageFilter.GaussianBlur(2))
    return im


def _factory():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((160, 170, 176), (70, 76, 80)))
    for x in range(0, W, 270):
        c.rect((x + 20, 120, x + 230, 460), grad=((220, 232, 240), (170, 186, 196)))
        c.line([(x + 125, 120), (x + 125, 460)], (90, 96, 100), 6)
        c.line([(x + 20, 290), (x + 230, 290)], (90, 96, 100), 6)
    c.rect((0, 520, W, 560), fill=(90, 96, 100))
    for x in range(0, W, 120):
        c.line([(x, 520), (x + 60, 560)], (70, 74, 78), 6)
    for x in (200, 540, 880):
        c.line([(x, 560), (x, 640)], (40, 40, 40), 4)
        c.poly([(x - 60, 680), (x + 60, 680), (x + 30, 640), (x - 30, 640)], fill=(60, 64, 68))
        c.glow(x, 700, 120, (255, 236, 190), 0.7)
    c.rect((0, 1100, W, H), grad=((110, 112, 112), (60, 60, 60)))
    c.rect((0, 1000, W, 1080), grad=((40, 40, 44), (20, 20, 22)))
    for x in range(20, W, 70):
        c.ellipse((x, 1062, x + 40, 1102), radial=((180, 184, 190), (80, 84, 90)))
    c.rect((0, 996, W, 1004), fill=(120, 124, 130))
    c.rect((440, 640, 640, 720), grad=((230, 200, 60), (180, 150, 30)), r=10)
    c.rect((520, 720, 560, 760), fill=(40, 40, 44))
    return c.done().convert("RGBA")


def box(seed):
    c = Cv(260, 220)
    c.shadow((10, 196, 250, 220), 140, 6)
    c.rect((10, 30, 250, 210), grad=((206, 160, 104), (160, 116, 68)), r=4)
    c.poly([(10, 30), (250, 30), (230, 6), (30, 6)], fill=(226, 184, 128))
    c.rect((10, 100, 250, 116), fill=(190, 150, 96))
    c.rect((150, 120, 236, 200), fill=(250, 248, 240))
    q = qr(seed).resize((72, 72), Image.LANCZOS)
    c.im.alpha_composite(q.resize((216, 216), Image.BILINEAR), (157 * 3, 124 * 3))
    c.text((80, 160), "PIEZA", 22, (90, 60, 30))
    return c.done()


def go_board():
    c = Cv(820, 820)
    c.shadow((20, 780, 800, 820), 160, 12)
    c.rect((10, 10, 810, 790), grad=((232, 186, 116), (196, 146, 80)), r=10)
    rr = random.Random(9)
    for k in range(18):
        y = 20 + k * 44
        c.line([(10, y), (810, y + rr.uniform(-6, 6))], (210, 160, 96, 120), 3)
    n = 13
    step = 720 / (n - 1)
    for i in range(n):
        p = 50 + i * step
        c.line([(50, p), (770, p)], (60, 40, 20), 3)
        c.line([(p, 50), (p, 770)], (60, 40, 20), 3)
    M_, _ = qr_matrix(n, 3)
    for r in range(n):
        for col in range(n):
            if rr.random() < 0.55:
                x, y = 50 + col * step, 50 + r * step
                if M_[r][col]:
                    c.ellipse((x - 26, y - 26, x + 26, y + 26), radial=((90, 90, 96), (10, 10, 12)), center=(0.36, 0.3))
                else:
                    c.ellipse((x - 26, y - 26, x + 26, y + 26), radial=((255, 255, 255), (196, 196, 190)), center=(0.36, 0.3))
    return c.done()


def check(img, x, y, k, r=70):
    if k <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    A = int(255 * k)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(40, 170, 90, A), outline=(255, 255, 255, A), width=5)
    p = [(x - r * 0.45, y), (x - r * 0.1, y + r * 0.35), (x + r * 0.5, y - r * 0.35)]
    n = max(2, int(3 * k))
    d.line(p[:n], fill=(255, 255, 255, A), width=int(r * 0.18), joint="curve")


def desk_bg(img):
    sky(img, (40, 44, 56), (12, 12, 16), 1.0)
    paste(img, glow(700, (120, 140, 200), 0.25), 540, 860)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    AC(img, cached("cafe", _cafe))
    paste(img, spr(cup), 840, 1000, 1.0)
    T2.smoke(img, t, [(840, 880, 0.5)], col=(255, 244, 230), alpha=40, spread=(60, 20), grow=50, speed=0.5)
    paste(img, spr(table_card), 420, 760, 1.0)
    k = ease(clamp((t - 0.3) / 0.8))
    scan = clamp((t - 1.3) / 0.8)

    def extra(scr):
        dd = ImageDraw.Draw(scr, "RGBA")
        dd.rectangle([0, 0, scr.size[0], scr.size[1]], fill=(50, 34, 26, 255))
        qq = qr().resize((300, 300), Image.LANCZOS)
        scr.alpha_composite(qq, (64, 290))
        x0, y0, x1, y1 = 50, 276, 378, 604
        col = YEL if scan < 1 else GREEN
        for (cx_, cy_, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x1, y1, -1, -1), (x0, y1, 1, -1)):
            dd.line([(cx_, cy_ + sy * 50), (cx_, cy_), (cx_ + sx * 50, cy_)], fill=col + (255,), width=8)
        if 0 < scan < 1:
            y = lerp(y0, y1, scan)
            dd.line([(x0, y), (x1, y)], fill=YEL + (200,), width=4)
        if scan >= 1:
            dd.rounded_rectangle([40, 660, 388, 740], radius=24, fill=(250, 250, 252, 240))
            dd.text((214, 700), "Abrir enlace", font=f(F_CAP, 30), fill=(30, 100, 220), anchor="mm")
    phone(img, lerp(1200, 790, k), 1160, 0.75, "home", -10, 1.0, extra)
    top_shade(img)
    title2(t, 0.3, "UN QR SE LEE EN", "< 1 SEGUNDO", 250, 56, 96, hold=max(1.8, L[1][0] - 0.3))
    vignette(img, 190)


def sh_factory(img, t, T, L):
    a1 = L[1][0]
    AC(img, cached("factory", _factory))
    for i in range(5):
        x = ((t * 140 + i * 300) % 1500) - 200
        paste(img, spr(box, i + 3), x, 900, 1.0)
        if abs(x - 540) < 60:
            d = ImageDraw.Draw(img, "RGBA")
            d.polygon([(540, 760), (440, 980), (640, 980)], fill=(255, 40, 40, 50))
            d.line([(440, 930), (640, 930)], fill=(255, 60, 60, 220), width=4)
            paste(img, glow(120, (90, 255, 140), 0.8), 540, 700, 1.0, 1 - abs(x - 540) / 60)
    sepia(img, 0.3)
    top_shade(img, 210, 640)
    date_stamp(t, 0.4, "1994 · JAPÓN", 260, hold=max(1.8, a1 - 0.8))
    if t > a1:
        lower_third(img, t, a1 + 0.1, "DENSO WAVE", "PARA SEGUIR PIEZAS DE COCHE", 260, T - a1 - 0.5)
    vignette(img, 190)


def finder_boxes(c):
    return [((0, 0), (7, 7)), ((0, N - 7), (7, N)), ((N - 7, 0), (N, 7))]


def sh_finders(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    desk_bg(img)
    cx, cy, s = 540, 860, 1.25
    hw = QS * s / 2
    flat = [(cx - hw, cy - hw), (cx + hw, cy - hw), (cx + hw, cy + hw), (cx - hw, cy + hw)]
    tilt = [(cx - hw * 0.62, cy - hw * 0.95), (cx + hw * 0.98, cy - hw * 0.55), (cx + hw * 0.74, cy + hw * 0.96), (cx - hw * 0.92, cy + hw * 0.62)]
    if t < a1:
        quad = flat
    elif t < a2:
        k = ease(clamp((t - a1) / 1.0))
        quad = [(lerp(a[0], b[0], k), lerp(a[1], b[1], k)) for a, b in zip(flat, tilt)]
    else:
        k = ease(clamp((t - a2 - 0.8) / 1.2))
        quad = [(lerp(b[0], a[0], k), lerp(b[1], a[1], k)) for a, b in zip(flat, tilt)]
    paste(img, glow(600, (0, 0, 0), 0.8), cx + 20, cy + 40, 1.0, 0.6)
    H_ = warp_paste(img, qr(), quad)
    d = ImageDraw.Draw(img, "RGBA")
    centers = []
    for i, ((r0, c0), (r1, c1)) in enumerate(finder_boxes(None)):
        pts = [hmap(H_, (c0 + Q) * PX - 6, (r0 + Q) * PX - 6), hmap(H_, (c1 + Q) * PX + 6, (r0 + Q) * PX - 6),
               hmap(H_, (c1 + Q) * PX + 6, (r1 + Q) * PX + 6), hmap(H_, (c0 + Q) * PX - 6, (r1 + Q) * PX + 6)]
        centers.append(hmap(H_, (c0 + 3.5 + Q) * PX, (r0 + 3.5 + Q) * PX))
        k = ease(clamp((t - 0.6 - i * 0.45) / 0.4))
        if k > 0:
            d.polygon(pts, fill=YEL + (int(60 * k),))
            d.line(pts + [pts[0]], fill=YEL + (int(255 * k),), width=7)
    if t > a1 + 0.6:
        k = ease(clamp((t - a1 - 0.6) / 0.6)) * (1 - ease(clamp((t - a2) / 0.5)))
        if k > 0:
            d.line(centers + [centers[0]], fill=(255, 255, 255, int(220 * k)), width=5)
            for x, y in centers:
                d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(255, 255, 255, int(255 * k)))
    if t > a2:
        a = N - 7
        k = ease(clamp((t - a2 - 0.2) / 0.4))
        pts = [hmap(H_, (a - 2.5 + Q) * PX, (a - 2.5 + Q) * PX), hmap(H_, (a + 2.5 + Q) * PX, (a - 2.5 + Q) * PX),
               hmap(H_, (a + 2.5 + Q) * PX, (a + 2.5 + Q) * PX), hmap(H_, (a - 2.5 + Q) * PX, (a + 2.5 + Q) * PX)]
        d.polygon(pts, fill=(90, 200, 255, int(70 * k)))
        d.line(pts + [pts[0]], fill=(90, 200, 255, int(255 * k)), width=6)
        g = ease(clamp((t - a2 - 0.8) / 1.2))
        for i in range(0, N + 1, 5):
            p0, p1 = hmap(H_, (i + Q) * PX, Q * PX), hmap(H_, (i + Q) * PX, (N + Q) * PX)
            d.line([p0, p1], fill=(90, 200, 255, int(90 * g)), width=2)
            p0, p1 = hmap(H_, Q * PX, (i + Q) * PX), hmap(H_, (N + Q) * PX, (i + Q) * PX)
            d.line([p0, p1], fill=(90, 200, 255, int(90 * g)), width=2)
    if t < a1:
        big(t, 0.4, "3 CUADRADOS GUÍA", 290, 84, YEL, pop=False)
    elif t < a2:
        big(t, a1 + 0.3, "¿GIRADO? ¿TORCIDO?", 290, 80, WHITE, pop=False)
    else:
        big(t, a2 + 0.3, "CORRIGE LA PERSPECTIVA", 290, 62, (140, 210, 255), pop=False)
    vignette(img, 200)


def bits_zoom(img, t, t0):
    desk_bg(img)
    M_, _ = qr_matrix(N, 7)
    r0, c0, n = 9, 9, 7
    cs = 120
    x0, y0 = 540 - n * cs / 2, 860 - n * cs / 2
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([x0 - 20, y0 - 20, x0 + n * cs + 20, y0 + n * cs + 20], fill=(250, 248, 242, 255))
    order = 0
    for r in range(n):
        for c in range(n):
            on = M_[r0 + r][c0 + c]
            x, y = x0 + c * cs, y0 + r * cs
            if on:
                d.rectangle([x, y, x + cs, y + cs], fill=(16, 16, 20, 255))
            kk = clamp((t - t0 - 0.4 - order * 0.045) / 0.2)
            if kk > 0:
                d.text((x + cs / 2, y + cs / 2), "1" if on else "0", font=f(F_MONO, 54),
                       fill=((255, 210, 63) if on else (60, 60, 70)) + (int(255 * kk),), anchor="mm")
            order += 1
    for i in range(n + 1):
        d.line([(x0 + i * cs, y0), (x0 + i * cs, y0 + n * cs)], fill=(90, 200, 255, 160), width=2)
        d.line([(x0, y0 + i * cs), (x0 + n * cs, y0 + i * cs)], fill=(90, 200, 255, 160), width=2)
    sc = (t - t0 - 0.4) / 0.045
    if 0 <= sc < n * n:
        r, c = int(sc) // n, int(sc) % n
        d.rectangle([x0 + c * cs, y0 + r * cs, x0 + (c + 1) * cs, y0 + (r + 1) * cs], outline=YEL + (255,), width=6)


def bytes_scene(img, t, t0, t1, t2):
    desk_bg(img)
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(2)
    for i in range(30):
        x = (rr.uniform(0, W) + t * 160) % (W + 200) - 100
        y = rr.uniform(450, 1300)
        d.text((x, y), rr.choice("01"), font=f(F_MONO, int(rr.uniform(30, 60))), fill=(90, 200, 255, rr.randint(40, 110)), anchor="mm")
    if t < t1:
        k = ease(clamp((t - t0 - 0.2) / 0.8))
        bits = "01001000"
        for i, b in enumerate(bits):
            x = 540 + (i - 3.5) * 100
            y = lerp(1300, 860, ease(clamp(k * 1.4 - i * 0.05)))
            d.rounded_rectangle([x - 42, y - 56, x + 42, y + 56], radius=12, fill=(20, 24, 34, 230), outline=(90, 200, 255, 220), width=3)
            d.text((x, y), b, font=f(F_MONO, 64), fill=YEL + (255,), anchor="mm")
        spaced(d, 540, 1010, "8 BITS = 1 BYTE", f(F_SER, 44), (255, 255, 255, int(255 * k)), 6)
    elif t < t2:
        k = ease(clamp((t - t1 - 0.2) / 0.6))
        spaced(d, 540, 640, "01001000  →  H", f(F_MONO, 54), (255, 255, 255, int(255 * k)), 2)
        k2 = ease(clamp((t - t1 - 1.0) / 0.6))
        for i, ch in enumerate("HOLA"):
            x = 540 + (i - 1.5) * 150
            d.rounded_rectangle([x - 60, 780, x + 60, 920], radius=16, fill=(250, 248, 242, int(240 * k2)))
            d.text((x, 850), ch, font=f(F_CAP, 84), fill=(20, 20, 24, int(255 * k2)), anchor="mm")
        k3 = ease(clamp((t - t1 - 2.0) / 0.6))
        d.rounded_rectangle([200, 1000, 880, 1100], radius=50, fill=(250, 250, 252, int(240 * k3)))
        d.text((540, 1050), "https://…", font=f(F_CAP, 50), fill=(30, 100, 220, int(255 * k3)), anchor="mm")
    else:
        k = ease(clamp((t - t2) / 0.8))
        big_qr = spr(qr_sprite, 4, 11, 177, (16, 16, 20), (250, 248, 242), 2, False)
        paste(img, big_qr, 540, 900, lerp(0.6, 1.0, k), k)


def sh_bits(img, t, T, L):
    a1, a2, a3 = L[1][0], L[2][0], L[3][0]
    xf(img, t, a1, lambda im: bits_zoom(im, t, 0), lambda im: bytes_scene(im, t, a1, a2, a3), 0.6)
    if t < a1:
        big(t, 0.3, "NEGRA = 1 · BLANCA = 0", 290, 66, WHITE, pop=False)
    elif t < a2:
        big(t, a1 + 0.2, "BITS", 290, 120, YEL)
    elif t < a3:
        big(t, a2 + 0.2, "NÚMEROS, LETRAS, WEBS", 290, 62, WHITE, pop=False)
    else:
        big(t, a3 + 0.3, "7.089 NÚMEROS", 290, 92, YEL, sub="EN UN SOLO QR")
    vignette(img, 200)


def sh_damage(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    desk_bg(img)
    cx, cy, s = 540, 860, 1.25
    if t < a2:
        paste(img, qr(), cx, cy, s)
        d = ImageDraw.Draw(img, "RGBA")
        M_, fixed = qr_matrix(N, 7)
        x0, y0 = cx - QS * s / 2 + Q * PX * s, cy - QS * s / 2 + Q * PX * s
        cs = PX * s
        if t < a1:
            k = ease(clamp((t - 0.6) / 0.8))
            for r in range(N):
                for c in range(N):
                    if not fixed[r][c]:
                        col = (60, 140, 255) if c < 13 else (255, 150, 60)
                        d.rectangle([x0 + c * cs, y0 + r * cs, x0 + (c + 1) * cs, y0 + (r + 1) * cs], fill=col + (int(110 * k),))
            callout(img, t, 1.2, cx - 200, cy + 120, 260, 1330, "DATOS", (120, 180, 255), 36)
            callout(img, t, 1.8, cx + 200, cy + 120, 820, 1330, "COPIA DE SEGURIDAD", (255, 170, 90), 32)
        else:
            k = ease(clamp((t - a1 - 0.2) / 0.8))
            st = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sd = ImageDraw.Draw(st)
            rr = random.Random(4)
            pts = [(cx + 120 + math.cos(a) * rr.uniform(150, 210) * k, cy - 140 + math.sin(a) * rr.uniform(150, 210) * k) for a in np.linspace(0, 6.28, 18)]
            sd.polygon(pts, fill=(120, 74, 40, 200))
            AC(img, st.filter(ImageFilter.GaussianBlur(3)))
            d = ImageDraw.Draw(img, "RGBA")
            tear = [(cx - QS * s / 2 - 10, cy + QS * s / 2 - 260 * k), (cx - QS * s / 2 + 230 * k, cy + QS * s / 2 + 10),
                    (cx - QS * s / 2 - 10, cy + QS * s / 2 + 10)]
            d.polygon(tear, fill=(26, 28, 36, 255))
            check(img, cx + 300, cy - 330, ease(clamp((t - a1 - 1.4) / 0.4)))
            big(t, a1 + 0.3, "HASTA UN 30 %", 290, 92, YEL)
    else:
        k = ease(clamp((t - a2) / 0.6))
        paste(img, qr(7, True), cx, cy, lerp(1.1, 1.25, k), 1.0)
        check(img, cx + 300, cy - 330, ease(clamp((t - a2 - 0.9) / 0.4)))
        big(t, a2 + 0.2, "CON LOGOTIPO", 290, 92, WHITE)
    if t < a1:
        big(t, 0.3, "INFORMACIÓN REPETIDA", 290, 70, WHITE, pop=False)
    vignette(img, 200)


def sh_go(img, t, T, L):
    sky(img, (50, 40, 30), (16, 12, 10), 1.0)
    paste(img, glow(700, (255, 200, 140), 0.3), 540, 860)
    k = ease(clamp((t - 1.6) / 1.0))
    paste(img, spr(go_board), lerp(540, 330, k), 860, lerp(1.1, 0.62, k), 1.0, lerp(0, -6, k))
    if k > 0:
        paste(img, qr(), lerp(1100, 770, k), 860, 0.75, k, 6 * k)
    big(t, 0.3, "INSPIRADO EN EL GO", 290, 80, YEL, pop=False)
    vignette(img, 200)


def patent(img, t, t0):
    desk_bg(img)
    pp = spr(paper, 640, 860, "PATENTE", 0, (244, 238, 222), (40, 34, 28), 2,
             ("Código de barras", "bidimensional", "", "Titular: Denso Wave", "", "Uso del estándar:", "sin cobrar licencias"), "GRATIS")
    k = ease(clamp((t - t0 - 0.1) / 0.8))
    paste(img, pp, 540, lerp(1500, 860, k), 1.0, 1.0, -3)


def montage(img, t, t0):
    desk_bg(img)
    cards = [("MENÚ", (250, 244, 230), 300, 640, -6), ("ENTRADA", (230, 240, 255), 780, 620, 5),
             ("CARTEL", (255, 230, 220), 300, 1100, 4), ("PRODUCTO", (235, 250, 235), 780, 1110, -5)]
    for i, (name, col, x, y, rot) in enumerate(cards):
        k = ease(clamp((t - t0 - i * 0.25) / 0.6))
        if k <= 0:
            continue
        im = Image.new("RGBA", (380, 420), col + (255,))
        dd = ImageDraw.Draw(im)
        dd.text((190, 50), name, font=f(F_SER, 46), fill=(40, 34, 30), anchor="mm")
        q = qr(i + 20).resize((260, 260), Image.LANCZOS)
        im.alpha_composite(q, (60, 110))
        paste(img, glow(260, (0, 0, 0), 0.8), x + 10, y + 20, 1.0, 0.5 * k)
        paste(img, im, x, y, lerp(0.6, 1.0, k), k, rot)


def final_scan(img, t, t0):
    AC(img, cached("cafe", _cafe))
    paste(img, spr(table_card), 540, 760, 1.0)
    scan = clamp((t - t0 - 0.4) / 0.8)

    def extra(scr):
        dd = ImageDraw.Draw(scr, "RGBA")
        dd.rectangle([0, 0, scr.size[0], scr.size[1]], fill=(50, 34, 26, 255))
        qq = qr().resize((300, 300), Image.LANCZOS)
        scr.alpha_composite(qq, (64, 290))
        col = YEL if scan < 1 else GREEN
        for (cx_, cy_, sx, sy) in ((50, 276, 1, 1), (378, 276, -1, 1), (378, 604, -1, -1), (50, 604, 1, -1)):
            dd.line([(cx_, cy_ + sy * 50), (cx_, cy_), (cx_ + sx * 50, cy_)], fill=col + (255,), width=8)
    phone(img, 760, 1180, 0.72, "home", -10, 1.0, extra)


def sh_free(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a2 - 0.4:
        xf(img, t, a1, lambda im: patent(im, t, 0), lambda im: montage(im, t, a1), 0.6)
    else:
        xf(img, t, a2, lambda im: montage(im, t, a1), lambda im: final_scan(im, t, a2), 0.7)
    if t < a1:
        big(t, 0.4, "SIN COBRAR", 290, 100, YEL)
    elif t < a2:
        big(t, a1 + 0.2, "EN TODAS PARTES", 290, 84, WHITE, pop=False)
    else:
        top_shade(img)
        title2(t, a2 + 0.3, "LO QUE PARECE RUIDO…", "ES PURO ORDEN", 250, 56, 84, hold=max(1.6, T - a2 - 0.8), c1=WHITE, c2=YEL)
    vignette(img, 200)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "creative"), ("factory", "doc"), ("finders", "exp"), ("bits", "creative"), ("damage", "tension"),
              ("go", "warm"), ("free", "premium")],
    "gains": {"exp": 0.7},
    "amb": {"city": ["open"], "hum": ["factory", "bits"], "room": ["go"]},
    "sfx": [("open+1.3", "beep", 0.08), ("open+2.1", "ding", 0.08), ("open@L1", "whoosh", 0.14),
            ("factory+0.3", "paper", 0.14), ("factory+1.6", "beep", 0.06), ("factory+3.7", "beep", 0.06), ("factory@L1+0.1", "whoosh", 0.1),
            ("finders+0.6", "pop", 0.16), ("finders+1.05", "pop", 0.16), ("finders+1.5", "pop", 0.16),
            ("finders@L1", "whoosh", 0.12), ("finders@L2+0.2", "blip", 0.12), ("finders@L2+0.8", "whoosh_up", 0.1),
            ("bits+0.4", "type", 0.12), ("bits@L1", "whoosh", 0.12), ("bits@L2+0.3", "blip", 0.12), ("bits@L2+1.2", "blip", 0.12),
            ("bits@L3", "riser", 0.1), ("bits@L3+0.3", "impact", 0.2),
            ("damage+0.6", "swell", 0.12), ("damage@L1+0.3", "paper", 0.2), ("damage@L1+1.4", "ding", 0.1), ("damage@L2+0.9", "ding", 0.1),
            ("go+0.3", "knock", 0.14), ("go+0.7", "knock", 0.12), ("go+1.6", "whoosh", 0.12),
            ("free+0.1", "paper", 0.2), ("free+0.9", "thud", 0.2), ("free@L1", "pop", 0.14), ("free@L1+0.5", "pop", 0.14),
            ("free@L2+1.2", "beep", 0.08), ("free@L2+1.4", "swell", 0.14)],
    "bed": [("finders", "bits")],
    "bpm": 100,
}
