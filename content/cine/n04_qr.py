"""N04 · ¿Qué esconde un código QR? (estilo neón explicativo)."""
from neon import *

TITLE = "Que_esconde_un_codigo_QR"
LINES = [
    "Un código QR parece ruido… pero tu móvil lo lee en *menos de un segundo*.",
    "¿Qué esconden esos cuadraditos?",
    "Se inventó en Japón en 1994, en la empresa *Denso Wave*.",
    "Querían seguir las piezas de los coches en las fábricas.",
    "Lo primero que busca la cámara son estos *tres cuadrados*.",
    "Le dicen dónde está el código… y si está *girado o torcido*.",
    "Y un cuadrado más pequeño ayuda a corregir la perspectiva.",
    "Luego divide el código en una rejilla y lee cada casilla: negra es *1*, blanca es *0*.",
    "Son *bits*, como los de un ordenador.",
    "Juntando bits salen números, letras… o una dirección web.",
    "En un solo QR caben hasta *7.089 números*.",
    "Y lo mejor: guarda la información *repetida* de forma inteligente.",
    "Aunque se rompa o se tape hasta *un 30 %*, se puede leer igual.",
    "Por eso hay QR con *logotipos* en medio.",
    "Su diseño se inspiró en un juego: las fichas blancas y negras del *Go*.",
    "Y Denso Wave decidió *no cobrar* por usar su patente.",
    "Por eso hoy está en todas partes.",
    "La próxima vez que escanees uno… ya sabes *lo que está leyendo tu móvil*.",
]
SHOTS = [("open", 0, 1, 0.3), ("factory", 2, 3, 0.3), ("finders", 4, 6, 0.3), ("bits", 7, 10, 0.3), ("damage", 11, 13, 0.3),
         ("go", 14, 14, 0.3), ("free", 15, 17, 1.8)]
FOCUS = {"open": (540, 960, 1.12), "factory": (540, 1000, 1.12), "finders": (540, 960, 1.15), "bits": (540, 960, 1.12),
         "damage": (540, 960, 1.12), "go": (540, 960, 1.12), "free": (540, 960, 1.12)}
NOTIF = ("finders", 1.0)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon

N = 25


def qr_matrix(seed=7):
    rr = random.Random(seed)
    m = [[rr.random() < 0.48 for _ in range(N)] for _ in range(N)]
    reserved = [[False] * N for _ in range(N)]

    def finder(r0, c0):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr_, cc = r0 + r, c0 + c
                if 0 <= rr_ < N and 0 <= cc < N:
                    on = (0 <= r <= 6 and 0 <= c <= 6) and (r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4))
                    m[rr_][cc] = on
                    reserved[rr_][cc] = True
    finder(0, 0), finder(0, N - 7), finder(N - 7, 0)
    for i in range(8, N - 8):
        m[6][i] = m[i][6] = (i % 2 == 0)
        reserved[6][i] = reserved[i][6] = True
    for r in range(-2, 3):
        for c in range(-2, 3):
            m[18 + r][18 + c] = (max(abs(r), abs(c)) != 1)
            reserved[18 + r][18 + c] = True
    return m, reserved


QR, RES = qr_matrix()


def draw_qr(d, cx, cy, cell, k=1.0, col=WH, ang=0.0, hide=None, persp=0.0, highlight=None, t=0.0):
    tot = N * cell
    ca, sa = math.cos(ang), math.sin(ang)
    order = [(r, c) for r in range(N) for c in range(N)]
    nshow = int(len(order) * k)
    for idx, (r, c) in enumerate(order[:nshow]):
        if not QR[r][c]:
            continue
        if hide and hide(r, c):
            continue
        x = (c - N / 2 + 0.5) * cell
        y = (r - N / 2 + 0.5) * cell
        sc_ = 1 + persp * (y / tot)
        x *= sc_
        X, Y = cx + x * ca - y * sa, cy + x * sa + y * ca
        h = cell * 0.42
        cc = col
        if highlight and highlight(r, c):
            cc = highlight(r, c)
        pts = [(X + (dx * ca - dy * sa), Y + (dx * sa + dy * ca)) for dx, dy in ((-h, -h), (h, -h), (h, h), (-h, h))]
        d.polygon(pts, fill=tuple(int(v * 0.25) for v in cc), outline=cc)


def is_finder(r, c):
    return (r < 7 and c < 7) or (r < 7 and c >= N - 7) or (r >= N - 7 and c < 7)


def is_align(r, c):
    return 16 <= r <= 20 and 16 <= c <= 20


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    draw_qr(d, 540, 960, 26, ease(clamp(t / 1.6)), WH)
    y = 960 - 340 + ((t * 0.5) % 1.0) * 680
    d.line([(180, y), (900, y)], fill=RD, width=6)
    for k_ in range(1, 6):
        d.line([(180, y - k_ * 6), (900, y - k_ * 6)], fill=tuple(int(c * (1 - k_ / 6) * 0.4) for c in RD), width=4)
    for cx_, cy_ in ((170, 590), (910, 590), (170, 1330), (910, 1330)):
        sx = 1 if cx_ < 540 else -1
        sy = 1 if cy_ < 960 else -1
        d.line([(cx_, cy_), (cx_ + sx * 70, cy_)], fill=GR, width=8)
        d.line([(cx_, cy_), (cx_, cy_ + sy * 70)], fill=GR, width=8)
    finish(img, lay)
    gtitle2(t, 0.2, "¿QUÉ ESCONDE", "UN CÓDIGO QR?", 250, 60, 104, WH, CY, hold=max(1.6, L[1][0] + 1.2))
    vignette(img, 150)


def sh_factory(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    y = 1200
    d.line([(0, y), (W, y)], fill=DIM, width=6)
    for k in range(12):
        x = (k * 100 - t * 160) % (W + 100) - 50
        circle(d, x, y + 30, 20, DIM, 4)
    for k in range(4):
        x = (k * 320 + t * 160) % (W + 320) - 160
        rect(d, x - 110, y - 200, x + 110, y - 6, OR, 6)
        rr = random.Random(k)
        for r in range(5):
            for c in range(5):
                if rr.random() < 0.5 or (r in (0, 4) and c in (0, 4)):
                    d.rectangle([x - 50 + c * 20, y - 150 + r * 20, x - 50 + c * 20 + 16, y - 150 + r * 20 + 16], outline=WH, width=2)
    car(d, 540, 820, 1.0, CY, ease(clamp((t - L[1][0]) / 1.2)), -t * 3)
    finish(img, lay)
    chip(t, 0.3, "JAPÓN · 1994", 540, 330, YE, 50)
    gtitle(t, 0.9, "DENSO WAVE", 400, 84, WH, pop=False)
    vignette(img, 150)


def sh_finders(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    ang = 0.0
    persp = 0.0
    if t > a1:
        ang = math.radians(18) * math.sin((t - a1) * 1.4)
        persp = 0.25 * clamp((t - a2) / 1.0) if t > a2 else 0.0
    pulse = 0.6 + 0.4 * math.sin(t * 6) ** 2
    hi = lambda r, c: (tuple(int(v * pulse) for v in GR) if is_finder(r, c) else (YE if (t > a2 and is_align(r, c)) else None))
    draw_qr(d, 540, 960, 26, 1.0, tuple(int(v * 0.45) for v in WH), ang, None, persp, hi)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "3 CUADRADOS GUÍA", 300, 84, GR)
    elif t < a2:
        chip(t, a1 + 0.2, "POSICIÓN · GIRO", 540, 330, GR, 44)
    else:
        chip(t, a2 + 0.2, "PERSPECTIVA", 540, 330, YE, 44)
    vignette(img, 150)


def sh_bits(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2, a3 = L[1][0], L[2][0], L[3][0]
    if t < a2:
        cell = 26
        x0, y0 = 540 - N * cell / 2, 960 - N * cell / 2
        for i in range(N + 1):
            d.line([(x0 + i * cell, y0), (x0 + i * cell, y0 + N * cell)], fill=(30, 50, 90), width=1)
            d.line([(x0, y0 + i * cell), (x0 + N * cell, y0 + i * cell)], fill=(30, 50, 90), width=1)
        q = clamp((t - 0.6) / 2.4)
        nrev = int(N * N * q)
        for idx in range(N * N):
            r, c = divmod(idx, N)
            x, y = x0 + c * cell + cell / 2, y0 + r * cell + cell / 2
            if idx < nrev:
                label(d, x, y, "1" if QR[r][c] else "0", 20, YE if QR[r][c] else DIM, F_MONO)
            elif QR[r][c]:
                d.rectangle([x - cell * 0.4, y - cell * 0.4, x + cell * 0.4, y + cell * 0.4], outline=WH, width=2)
        if t > a1:
            chip(t, a1 + 0.1, "BITS", 540, 330, YE, 60)
    else:
        rr = random.Random(int(t * 8))
        for row in range(6):
            bits = "".join(rr.choice("01") for _ in range(16))
            label(d, 540, 640 + row * 70, bits, 46, tuple(int(c * 0.6) for c in YE), F_MONO)
        msg = "HOLA · 1234 · nolosabias"
        n = int(len(msg) * clamp((t - a2) / 1.6))
        label(d, 540, 1150, msg[:n] + ("▌" if int(t * 3) % 2 else ""), 54, CY, F_MONO)
        if t > a3:
            gtitle(t, a3 + 0.2, "7.089 NÚMEROS", 300, 92, YE)
    finish(img, lay)
    vignette(img, 150)


def sh_damage(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    if t < a1:
        draw_qr(d, 540, 960, 26, 1.0, WH)
        for k in range(8):
            u = (t * 0.7 + k / 8) % 1.0
            rr = random.Random(k)
            r, c = rr.randrange(N), rr.randrange(N)
            x, y = 540 + (c - N / 2 + 0.5) * 26, 960 + (r - N / 2 + 0.5) * 26
            line(d, [(x, y), (540 + (rr.randrange(N) - N / 2) * 26, 960 + (rr.randrange(N) - N / 2) * 26)], tuple(int(v * (1 - u)) for v in CY), 3)
        gtitle(t, 0.3, "DATOS REPETIDOS", 300, 84, CY, pop=False)
    else:
        cut = clamp((t - a1 - 0.2) / 0.8) * 0.30
        if t < a2:
            hide = lambda r, c: (r / N + c / N) / 2 > 1 - cut and not is_finder(r, c)
            draw_qr(d, 540, 960, 26, 1.0, WH, hide=hide)
            for k in range(14):
                x = 540 + 200 + k * 10
                d.line([(x, 1040 - k * 30), (x + 60, 1330 - k * 30)], fill=RD, width=3)
            if cut >= 0.29:
                line(d, [(420, 970), (500, 1050), (680, 860)], GR, 14, ease(clamp((t - a1 - 1.2) / 0.5)))
            gtitle(t, a1 + 0.2, "HASTA UN 30 %", 300, 96, GR)
        else:
            hide = lambda r, c: abs(r - 12) <= 3 and abs(c - 12) <= 3
            draw_qr(d, 540, 960, 26, 1.0, WH, hide=hide)
            rrect(d, 540 - 95, 960 - 95, 540 + 95, 960 + 95, 20, YE, 5)
            finish(img, lay)
            R.eye_icon(ImageDraw.Draw(img), 540, 960, 150, (255, 255, 255), YE, (14, 15, 18))
            gtitle(t, a2 + 0.2, "CON LOGO", 300, 100, YE)
            vignette(img, 150)
            return
    finish(img, lay)
    vignette(img, 150)


def sh_go(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    n, cell = 9, 90
    x0, y0 = 540 - (n - 1) * cell / 2, 960 - (n - 1) * cell / 2
    for i in range(n):
        d.line([(x0 + i * cell, y0), (x0 + i * cell, y0 + (n - 1) * cell)], fill=OR, width=3)
        d.line([(x0, y0 + i * cell), (x0 + (n - 1) * cell, y0 + i * cell)], fill=OR, width=3)
    rr = random.Random(5)
    stones = [(rr.randrange(n), rr.randrange(n), rr.random() < 0.5) for _ in range(26)]
    for i, (a, b, wht) in enumerate(stones[: int(len(stones) * clamp((t - 0.3) / 2.0))]):
        x, y = x0 + a * cell, y0 + b * cell
        circle(d, x, y, 36, WH if wht else DIM, 6)
        if wht:
            dot(d, x, y, 26, (60, 64, 80))
    finish(img, lay)
    gtitle(t, 0.3, "INSPIRADO EN EL GO", 300, 84, OR, pop=False)
    vignette(img, 150)


def sh_free(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    if t < a1:
        rect(d, 300, 600, 780, 1240, WH, 5)
        for j in range(9):
            d.line([(350, 700 + j * 52), (730 - (j % 3) * 60, 700 + j * 52)], fill=DIM, width=4)
        label(d, 540, 650, "PATENTE", 40, WH, F_POP)
        k = ease(clamp((t - 0.8) / 0.4))
        if k > 0:
            rrect(d, 330, 1060, 750, 1180, 16, GR, 8)
            label(d, 540, 1120, "GRATIS", 60, GR, F_POP)
    else:
        rr = random.Random(9)
        spots = [(300, 640), (780, 640), (540, 900), (300, 1160), (780, 1160), (540, 1400)]
        for k, (x, y) in enumerate(spots):
            s_ = 9
            kk = ease(clamp((t - a1 - k * 0.08) / 0.4))
            if kk > 0:
                draw_qr(d, x, y, s_, 1.0, CY if k % 2 else MG)
        if t > a2:
            overlay(img, (0, 0, 0), 0.0)
    finish(img, lay)
    if t < a1:
        gtitle(t, 0.3, "SIN COBRAR", 300, 100, GR)
    elif t < a2:
        gtitle(t, a1 + 0.2, "EN TODAS PARTES", 300, 90, CY, pop=False)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "exp"), ("factory", "creative"), ("bits", "exp"), ("go", "space"), ("free", "creative")],
    "gains": {"exp": 0.7},
    "amb": {"hum": ["open", "finders", "bits", "damage"]},
    "sfx": [("open+0.2", "draw", 0.2), ("open+1.0", "beep", 0.1), ("factory+0.3", "blip", 0.15),
            ("finders+0.3", "pop", 0.2), ("finders@L1+0.2", "whoosh", 0.12), ("finders@L2+0.2", "blip", 0.15),
            ("bits+0.6", "glitch", 0.12), ("bits@L1+0.1", "blip", 0.12), ("bits@L2", "type", 0.12), ("bits@L3+0.2", "impact", 0.2),
            ("damage+0.3", "draw", 0.15), ("damage@L1+0.2", "glitch", 0.15), ("damage@L1+1.2", "ding", 0.1),
            ("damage@L2+0.2", "pop", 0.2), ("go+0.3", "click", 0.3), ("go+0.9", "click", 0.3), ("go+1.5", "click", 0.3),
            ("free+0.8", "thud", 0.3), ("free@L1", "pop", 0.15), ("free@L1+0.3", "pop", 0.15)],
    "bed": [("factory", "go")],
    "bpm": 112,
}
