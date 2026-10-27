"""T03 · ¿Cómo sabe tu móvil dónde tocas? (estilo Titanic, ilustración detallada)."""
from gadgets import *
import t02_microondas as T2

xf, callout, glow_line, top_shade = T2.xf, T2.callout, T2.glow_line, T2.top_shade

TITLE = "Como_sabe_tu_movil_donde_tocas"
LINES = [
    "Tu móvil sabe exactamente *dónde pones el dedo*… pero ¿cómo?",
    "¿Y por qué con guantes *no funciona*?",
    "Bajo el cristal hay una rejilla invisible de *pistas finísimas*.",
    "Unas van en *horizontal*… y otras en *vertical*, sin tocarse.",
    "Cada cruce funciona como un pequeño *condensador*: guarda un poquito de carga.",
    "La pantalla manda *pulsos eléctricos* por cada línea, una tras otra, sin parar.",
    "Y tu cuerpo *conduce la electricidad*.",
    "Al acercar el dedo, *robas un poco de carga* en los cruces de debajo.",
    "El móvil ve qué cruces han cambiado… y calcula *el punto exacto*.",
    "Como cada cruce se lee por separado, puede seguir *varios dedos a la vez*.",
    "¿Y los guantes? La tela *no conduce*: el dedo ya no roba carga y la pantalla no te nota.",
    "Por eso los guantes táctiles llevan *hilo conductor* en las yemas.",
    "Y por eso funciona hasta con cosas raras… como *una salchicha*.",
    "Este tipo de pantalla se describió por primera vez en *1965*, en un centro de radares británico.",
    "Hoy la tocamos *miles de veces al día*…",
    "…sin preguntarnos nunca *cómo nos nota*.",
]
SHOTS = [("open", 0, 1, 0.3), ("grid", 2, 3, 0.3), ("cap", 4, 5, 0.3), ("finger", 6, 8, 0.3), ("multi", 9, 9, 0.3),
         ("gloves", 10, 11, 0.3), ("sausage", 12, 12, 0.3), ("history", 13, 15, 1.8)]
FOCUS = {"grid": (540, 900, 1.1), "multi": (540, 900, 1.1), "sausage": (540, 860, 1.12), "history": (540, 860, 1.12)}
NOTIF = ("grid", 1.0)
HYPE = {"line": 1, "text": ['¿POR QUÉ CON GUANTES', 'NO FUNCIONA?'], "delay": [0, 1.4]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

CY_ = (90, 200, 255)
TEAL = (60, 230, 200)
ORANGE = (255, 150, 60)


# ------------------------------------------------------------------ fondos y piezas
def _bokeh(seed=4, top=(8, 10, 22), bot=(20, 14, 26)):
    im = vgrad(("bokeh", seed), top, bot, 1.0).copy()
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rr = random.Random(seed)
    for i in range(70):
        x, y = rr.uniform(-50, W + 50), rr.uniform(0, H)
        r = rr.uniform(20, 90)
        col = rr.choice([(255, 190, 110), (255, 120, 90), (120, 170, 255), (255, 230, 170)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (rr.randint(30, 90),))
    lay = lay.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(lay)
    return im


def bokeh(img, seed=4):
    AC(img, cached(("bokeh_bg", seed), lambda: _bokeh(seed)))


def place_finger(img, kind, tx, ty, s=1.0, ang=0.0, alpha=1.0, hover=0.0):
    fs = spr(finger, kind)
    r = (fs.size[1] / 2 - 30) * s
    th = math.radians(ang)
    cx, cy = tx + r * math.sin(th), ty + r * math.cos(th)
    if hover > 0:
        paste(img, glow(160, (0, 0, 0), 0.9), tx + 40 * hover, ty + 60 * hover, 1.0, 0.5 * alpha)
    paste(img, fs, cx + 0 * hover, cy, s * (1 + 0.06 * hover), alpha, ang)


def ripple(img, x, y, t, t0, col=(255, 255, 255), n=3):
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(n):
        u = (t - t0 - i * 0.18)
        if 0 < u < 0.9:
            r = 20 + u * 160
            d.ellipse([x - r, y - r, x + r, y + r], outline=col + (int(220 * (1 - u / 0.9)),), width=6)


# grid 2D vista desde arriba
ROWS = [560 + i * 104 for i in range(8)]
COLS = [170 + j * 185 for j in range(5)]


def glass_bg(img, tint=(8, 12, 22)):
    sky(img, (26, 36, 60), tint, 1.0)
    paste(img, glow(640, (40, 80, 160), 0.25), 540, 900)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([60, 440, W - 60, 1380], radius=50, outline=(255, 255, 255, 40), width=4)
    d.polygon([(120, 440), (360, 440), (120, 1100)], fill=(255, 255, 255, 10))


def grid2d(img, t, robbed=None, kh=1.0, kv=1.0, pulse_row=None, node_k=1.0):
    """robbed(x, y) -> 0..1 cuánta carga ha perdido cada cruce."""
    d = ImageDraw.Draw(img, "RGBA")
    for y in ROWS:
        d.line([(100, y), (W - 100, y)], fill=CY_ + (int(150 * kh),), width=6)
    for x in COLS:
        d.line([(x, 480), (x, 1340)], fill=TEAL + (int(130 * kv),), width=6)
    if pulse_row is not None:
        i, u = pulse_row
        y = ROWS[i]
        x = lerp(100, W - 100, u)
        glow_line(img, [(max(100, x - 220), y), (x, y)], (200, 240, 255), 6, 10, 230)
        paste(img, glow(80, (220, 245, 255), 1.0), x, y)
    for y in ROWS:
        for x in COLS:
            q = robbed(x, y) if robbed else 0.0
            col = (int(lerp(140, 255, q)), int(lerp(220, 140, q)), int(lerp(255, 60, q)))
            paste(img, glow(int(70 - 30 * q), col, 0.9), x, y, 1.0, node_k * (1 - 0.5 * q))
            d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col + (int(240 * node_k),))


def near(tx, ty, rad=170):
    return lambda x, y: clamp(1 - math.hypot(x - tx, y - ty) / rad) ** 0.7


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    bokeh(img)
    px, py = 540, 830
    tx, ty = 646, 676
    if t < a1:
        k = ease(clamp((t - 0.6) / 0.6))
        tip = (lerp(980, tx, k), lerp(1500, ty, k))
        phone(img, px, py, 0.95, "home")
        if t > 1.2:
            ripple(img, tx, ty, t, 1.2)
            ripple(img, tx, ty, t, 2.4)
        place_finger(img, "skin", tip[0], tip[1], 1.0, 24, 1.0, 1 - k)
    else:
        k = ease(clamp((t - a1 - 0.2) / 0.6))
        tip = (lerp(1000, tx, k), lerp(1500, ty, k))
        phone(img, px, py, 0.95, "home")
        particles(img, t, 60, 8, (255, 255, 255), 60, (2, 4), 170, 30)
        place_finger(img, "glove", tip[0], tip[1], 1.12, 24, 1.0, 1 - k)
        if t > a1 + 0.9:
            kk = ease(clamp((t - a1 - 0.9) / 0.3))
            d = ImageDraw.Draw(img, "RGBA")
            d.ellipse([tx - 60, ty - 60, tx + 60, ty + 60], outline=(255, 80, 80, int(230 * kk)), width=8)
            d.line([(tx - 34, ty - 34), (tx + 34, ty + 34)], fill=(255, 80, 80, int(230 * kk)), width=8)
    top_shade(img)
    title2(t, 0.3, "¿CÓMO SABE TU MÓVIL", "DÓNDE TOCAS?", 250, 56, 92, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def iso(u, v, z, C=(540, 900), A=(420, 150), B=(-230, 300)):
    return (C[0] + (u - 0.5) * A[0] + (v - 0.5) * B[0], C[1] + (u - 0.5) * A[1] + (v - 0.5) * B[1] + z)


def plane(img, z, fill, edge=(255, 255, 255, 120), thick=0, side=(40, 60, 80, 200)):
    d = ImageDraw.Draw(img, "RGBA")
    pts = [iso(0, 0, z), iso(1, 0, z), iso(1, 1, z), iso(0, 1, z)]
    if thick:
        d.polygon([iso(0, 1, z), iso(1, 1, z), iso(1, 1, z + thick), iso(0, 1, z + thick)], fill=side)
        d.polygon([iso(1, 0, z), iso(1, 1, z), iso(1, 1, z + thick), iso(1, 0, z + thick)], fill=shade(side[:3], 0.7) + (side[3],))
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=edge, width=3)
    return pts


def sh_grid(img, t, T, L):
    a1 = L[1][0]
    sky(img, (14, 18, 34), (4, 6, 12), 1.0)
    paste(img, glow(700, (60, 100, 200), 0.3), 540, 900)
    sep = ease(clamp(t / 1.4))
    split = ease(clamp((t - a1 - 1.6) / 0.8))
    zd, zg = 250 * sep, -250 * sep
    # pantalla (abajo)
    plane(img, zd, (30, 40, 90, 255), (120, 140, 200, 160), 16, (20, 20, 30, 255))
    d = ImageDraw.Draw(img, "RGBA")
    for j in range(5):
        for i in range(4):
            u0, v0 = 0.1 + i * 0.21, 0.1 + j * 0.16
            q = [iso(u0, v0, zd), iso(u0 + 0.14, v0, zd), iso(u0 + 0.14, v0 + 0.1, zd), iso(u0, v0 + 0.1, zd)]
            d.polygon(q, fill=APP_COLS[(i + j * 4) % len(APP_COLS)] + (230,))
    # rejilla
    kh = 1.0 if t < a1 else 0.4 + 0.6 * (0.5 + 0.5 * math.sin((t - a1) * 8)) if t < a1 + 1.4 else 1.0
    kv = 1.0 if t < a1 + 1.0 else 0.4 + 0.6 * (0.5 + 0.5 * math.sin((t - a1) * 8)) if t < a1 + 2.4 else 1.0
    zh, zv = -30 * split, 30 * split
    plane(img, zv, (120, 200, 255, 22), (140, 210, 255, 90))
    for k in range(1, 6):
        u = k / 6
        glow_line(img, [iso(u, 0, zv), iso(u, 1, zv)], TEAL, 3, 6, int(200 * kv * sep))
    for k in range(1, 10):
        v = k / 10
        glow_line(img, [iso(0, v, zh), iso(1, v, zh)], CY_, 3, 6, int(210 * kh * sep))
    # cristal (arriba)
    pts = plane(img, zg, (220, 240, 255, 40), (255, 255, 255, 200), 14, (200, 230, 255, 70))
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([iso(0.08, 0, zg), iso(0.28, 0, zg), iso(0.08, 0.7, zg), iso(-0.0, 0.7, zg)], fill=(255, 255, 255, 30))
    if sep > 0.9:
        x, y = iso(1, 0.15, zg)
        callout(img, t, 1.4, x, y, 900, y - 80, "CRISTAL", (230, 240, 255), 34)
        x, y = iso(0, 0.6, 0)
        callout(img, t, 1.9, x, y, 200, y - 90, "REJILLA", CY_, 36)
        x, y = iso(1, 0.8, zd)
        callout(img, t, 2.4, x, y, 880, y + 150, "PANTALLA", (200, 200, 230), 34)
    if t < a1:
        big(t, 0.3, "PISTAS FINÍSIMAS", 300, 84, CY_, pop=False)
    else:
        big(t, a1 + 0.1, "HORIZONTALES", 270, 70, CY_, hold=1.2, pop=False)
        big(t, a1 + 1.5, "Y VERTICALES", 270, 70, TEAL, pop=False)
    vignette(img, 200)


def cap_close(img, t, t0):
    sky(img, (12, 16, 30), (4, 6, 12), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([470, 420, 610, 1340], radius=16, fill=(40, 180, 160, 150), outline=(140, 255, 230, 200), width=4)
    paste(img, glow(260, (90, 200, 255), 0.4), 540, 860)
    for i in range(7):
        x = 486 + i * 18
        y0, y1 = 806, 914
        al = int(160 * (0.5 + 0.5 * math.sin(t * 6 + i)))
        d = ImageDraw.Draw(img, "RGBA")
        d.line([(x, y0), (x, y1)], fill=(255, 240, 160, al), width=3)
    AC(img, Image.new("RGBA", (W, 130), (60, 150, 230, 160)), (0, 730))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 730, W, 736], fill=(200, 240, 255, 200))
    d.rectangle([0, 854, W, 860], fill=(20, 60, 120, 200))
    k = ease(clamp((t - t0 - 0.6) / 0.8))
    for i in range(5):
        x = 500 + i * 20
        d.text((x, 800), "+", font=f(F_CAP, 34), fill=(255, 255, 255, int(255 * k)), anchor="mm")
        d.text((x, 940), "−", font=f(F_CAP, 34), fill=(255, 255, 255, int(255 * k)), anchor="mm")
    callout(img, t, t0 + 1.2, 610, 860, 860, 1080, "CONDENSADOR", YEL, 40)
    spaced(d, 260, 700, "LÍNEA HORIZONTAL", f(F_SER, 30), (220, 240, 255, 220), 4)
    spaced(d, 690, 1300, "LÍNEA VERTICAL", f(F_SER, 30), (200, 255, 240, 220), 4)


def pulses(img, t, t0):
    glass_bg(img)
    i = int((t - t0) * 5) % len(ROWS)
    u = ((t - t0) * 5) % 1.0
    grid2d(img, t, None, 0.7, 0.7, (i, u))


def sh_cap(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: cap_close(im, t, 0), lambda im: pulses(im, t, a1), 0.7)
    if t < a1:
        big(t, 0.4, "CADA CRUCE", 290, 90, YEL, sub="GUARDA UN POCO DE CARGA")
    else:
        big(t, a1 + 0.2, "PULSOS SIN PARAR", 300, 84, (200, 240, 255), pop=False)
    vignette(img, 200)


def body_scene(img, t):
    sky(img, (10, 20, 50), (2, 4, 12), 1.0)
    paste(img, glow(600, (60, 120, 255), 0.35), 540, 820)
    paste(img, spr(hand_xray), 540, 900, 1.0)
    rr = random.Random(3)
    paths = [[(380, 1340), (340, 1080), (270, 640)], [(470, 1340), (450, 1000), (420, 540)], [(560, 1340), (560, 980), (560, 520)],
             [(650, 1340), (660, 1000), (680, 600)], [(330, 1300), (200, 1000), (130, 820)]]
    for P_ in paths:
        for k in range(6):
            u = ((t * 0.7 + k / 6 + rr.random()) % 1.0)
            if u < 0.5:
                x, y = lerp(P_[0][0], P_[1][0], u * 2), lerp(P_[0][1], P_[1][1], u * 2)
            else:
                x, y = lerp(P_[1][0], P_[2][0], u * 2 - 1), lerp(P_[1][1], P_[2][1], u * 2 - 1)
            paste(img, glow(30, (180, 230, 255), 1.0), x, y)


def touch_scene(img, t, t0, mode):
    glass_bg(img)
    tx, ty = 545, 870
    k = ease(clamp((t - t0 - 0.2) / 1.0))
    q = clamp((t - t0 - 0.9) / 0.6)
    rob = near(tx, ty)
    grid2d(img, t, (lambda x, y: rob(x, y) * q) if mode != "none" else None)
    if mode == "touch" and q > 0:
        for y in ROWS:
            for x in COLS:
                w_ = rob(x, y)
                if w_ > 0.05:
                    for j in range(3):
                        u = ((t * 1.4 + j / 3 + x * 0.01) % 1.0)
                        paste(img, glow(22, (255, 200, 120), 1.0), lerp(x, tx, u), lerp(y, ty, u), 1.0, w_ * q)
    if mode == "calc":
        kk = ease(clamp((t - t0 - 0.2) / 0.6))
        d = ImageDraw.Draw(img, "RGBA")
        for y in ROWS:
            for x in COLS:
                w_ = rob(x, y)
                if w_ > 0.05:
                    d.rectangle([x - 60, y - 40, x + 60, y + 40], fill=(255, int(160 - 100 * w_), 60, int(140 * w_ * kk)))
        g = ease(clamp((t - t0 - 0.7) / 0.8))
        r = lerp(300, 30, g)
        A = int(255 * kk)
        d.ellipse([tx - r, ty - r, tx + r, ty + r], outline=YEL + (A,), width=5)
        d.line([(tx - r - 40, ty), (tx + r + 40, ty)], fill=YEL + (A,), width=3)
        d.line([(tx, ty - r - 40), (tx, ty + r + 40)], fill=YEL + (A,), width=3)
        if g > 0.9:
            spaced(d, tx, ty + 110, "X 412 · Y 788", f(F_MONO, 36), (255, 255, 255, A), 2, shadow=True)
        place_finger(img, "skin", tx + 160 * g, ty + 300 * g, 1.0, 0, 0.35 + 0.65 * (1 - g), 0.6 * g)
    else:
        place_finger(img, "skin", lerp(700, tx, k), lerp(1500, ty, k), 1.0, 0, 1.0 - 0.5 * q, 1 - k)
        if mode == "touch" and q > 0:
            paste(img, glow(220, (255, 170, 80), 0.6), tx, ty, 1.0, q * (0.7 + 0.3 * math.sin(t * 6)))


def sh_finger(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a2 - 0.4:
        xf(img, t, a1, lambda im: body_scene(im, t), lambda im: touch_scene(im, t, a1, "touch"), 0.7)
    else:
        xf(img, t, a2, lambda im: touch_scene(im, t, a1, "touch"), lambda im: touch_scene(im, t, a2, "calc"), 0.7)
    if t < a1:
        big(t, 0.3, "TU CUERPO CONDUCE", 300, 80, CY_, pop=False)
    elif t < a2:
        big(t, a1 + 1.0, "ROBAS CARGA", 300, 100, ORANGE)
    else:
        big(t, a2 + 1.2, "EL PUNTO EXACTO", 300, 88, YEL)
    vignette(img, 200)


def sh_multi(img, t, T, L):
    glass_bg(img)
    sp = ease(clamp((t - 0.6) / 1.6))
    tips = [(lerp(470, 280, sp), lerp(900, 700, sp)), (lerp(620, 800, sp), lerp(820, 1080, sp)), (380, 1220)]
    fns = [near(x, y, 150) for x, y in tips]
    grid2d(img, t, lambda x, y: min(1, sum(fn(x, y) for fn in fns)))
    angs = (-20, 25, -10)
    for i, ((x, y), a) in enumerate(zip(tips, angs)):
        if i < 2 or t > 1.4:
            place_finger(img, "skin", x, y, 0.85, a, 1.0 if i < 2 else ease(clamp((t - 1.4) / 0.4)), 0.0)
    d = ImageDraw.Draw(img, "RGBA")
    for i, (x, y) in enumerate(tips):
        if i < 2 or t > 1.6:
            d.ellipse([x - 34, y - 130, x + 34, y - 62], fill=YEL + (230,))
            d.text((x, y - 97), str(i + 1), font=f(F_CAP, 40), fill=(20, 20, 20), anchor="mm")
    big(t, 0.4, "VARIOS DEDOS", 300, 96, YEL, sub="A LA VEZ")
    vignette(img, 200)


def glove_scene(img, t, t0, kind):
    glass_bg(img)
    tx, ty = 545, 870
    k = ease(clamp((t - t0 - 0.2) / 1.0))
    q = clamp((t - t0 - 0.9) / 0.6)
    rob = near(tx, ty)
    works = kind == "tglove"
    grid2d(img, t, (lambda x, y: rob(x, y) * q) if works else None)
    place_finger(img, kind, lerp(700, tx, k), lerp(1500, ty, k), 1.15, 0, 1.0 - 0.45 * q, 1 - k)
    if not works and q > 0:
        d = ImageDraw.Draw(img, "RGBA")
        kk = ease(clamp(q / 0.5))
        d.ellipse([tx - 120, ty - 260, tx + 120, ty - 20], outline=(255, 80, 80, int(230 * kk)), width=10)
        d.line([(tx - 70, ty - 210), (tx + 70, ty - 70)], fill=(255, 80, 80, int(230 * kk)), width=10)
    if works:
        callout(img, t, t0 + 1.4, tx + 60, ty + 60, 860, ty + 330, "HILO CONDUCTOR", (230, 236, 250), 34)


def sh_gloves(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: glove_scene(im, t, 0, "glove"), lambda im: glove_scene(im, t, a1, "tglove"), 0.7)
    if t < a1:
        big(t, 1.6, "LA TELA NO CONDUCE", 300, 74, (255, 120, 100), pop=False)
    else:
        big(t, a1 + 0.3, "GUANTES TÁCTILES", 300, 80, YEL, pop=False)
    vignette(img, 200)


def sh_sausage(img, t, T, L):
    sky(img, (40, 30, 26), (14, 10, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1180, W, H], fill=(96, 66, 44))
    for x in range(0, W, 90):
        d.line([(x, 1180), (x - 40, H)], fill=(80, 54, 36), width=4)
    unlocked = t > 2.0
    mode = "home" if unlocked else "lock"
    tx, ty = 560, 1080 if not unlocked else 700
    phone(img, 540, 760, 0.9, mode, -4)
    k = ease(clamp((t - 0.4) / 1.0))
    sw = clamp((t - 1.3) / 0.6)
    stx, sty = lerp(620, 560, k), lerp(1500, 1180 - 260 * ease(sw), k)
    place_finger(img, "sausage", stx, sty, 1.2, -18, 1.0, 1 - k)
    if unlocked:
        ripple(img, 540, 700, t, 2.0, (255, 255, 255))
    big(t, 0.3, "¿UNA SALCHICHA?", 260, 84, WHITE, hold=1.6, pop=False)
    if unlocked:
        big(t, 2.1, "SÍ, FUNCIONA", 260, 96, YEL)
    vignette(img, 200)


def _countryside():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, 1000), grad=((190, 200, 210), (236, 230, 214)))
    c.poly([(0, 900), (200, 820), (460, 860), (700, 780), (1080, 840), (1080, 1100), (0, 1100)], grad=((120, 130, 110), (90, 100, 84)))
    c.poly([(0, 1000), (300, 940), (620, 980), (1080, 920), (1080, H), (0, H)], grad=((110, 120, 96), (50, 56, 44)))
    c.rect((560, 860, 860, 980), grad=((200, 196, 186), (150, 146, 136)))
    for x in range(580, 850, 40):
        c.rect((x, 890, x + 22, 930), fill=(60, 66, 70))
    c.poly([(550, 862), (870, 862), (840, 830), (580, 830)], fill=(120, 110, 100))
    return c.done().convert("RGBA")


def history_scene(img, t):
    AC(img, cached("countryside", _countryside))
    paste(img, spr(radar_dish), 300, 760, 0.9, 1.0, math.sin(t * 0.6) * 4)
    clouds(img, t, 300, (255, 255, 255), 100, 8, 3, 1.0)
    T2.sepia(img, 0.75)


def today_scene(img, t, t0):
    bokeh(img, 6)
    def extra(scr):
        dd = ImageDraw.Draw(scr, "RGBA")
        rr = random.Random(int((t - t0) * 3))
        for i in range(3):
            x, y = rr.uniform(60, 370), rr.uniform(120, 860)
            u = ((t - t0) * 3) % 1.0
            r = 20 + u * 90
            dd.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, int(200 * (1 - u))), width=5)
    phone(img, 540, 840, 0.95, "home", 0, 1.0, extra)


def sh_history(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a2 - 0.4:
        xf(img, t, a1, lambda im: history_scene(im, t), lambda im: today_scene(im, t, a1), 0.8)
    else:
        today_scene(img, t, a1)
        k = ease(clamp((t - a2 - 0.2) / 1.2))
        d = ImageDraw.Draw(img, "RGBA")
        for y in range(420, 1260, 70):
            d.line([(340, y), (740, y)], fill=CY_ + (int(90 * k),), width=3)
        for x in range(340, 760, 80):
            d.line([(x, 400), (x, 1270)], fill=TEAL + (int(80 * k),), width=3)
    if t < a1:
        date_stamp(t, 0.4, "1965 · REINO UNIDO", 260, hold=max(1.8, a1 - 0.9))
    elif t < a2:
        big(t, a1 + 0.2, "MILES DE VECES AL DÍA", 290, 70, WHITE, pop=False)
    else:
        big(t, a2 + 0.3, "¿CÓMO NOS NOTA?", 290, 92, YEL, hold=max(1.6, T - a2 - 0.8))
    vignette(img, 200)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "creative"), ("grid", "exp"), ("finger", "mystery"), ("multi", "creative"), ("gloves", "playful"),
              ("history", "premium")],
    "gains": {"exp": 0.7, "mystery": 0.8},
    "amb": {"hum": ["grid", "cap", "finger", "multi"], "city": ["open"], "room": ["sausage"], "wind": ["history"]},
    "sfx": [("open+1.2", "click", 0.3), ("open+1.25", "blip", 0.12), ("open+2.4", "click", 0.3), ("open@L1+0.9", "knock", 0.2),
            ("grid+0.2", "whoosh_up", 0.14), ("grid+1.4", "pop", 0.15), ("grid+1.9", "pop", 0.14), ("grid+2.4", "pop", 0.14),
            ("grid@L1", "blip", 0.12), ("grid@L1+1.5", "blip_down", 0.12),
            ("cap+0.6", "zap", 0.08), ("cap@L1", "whoosh", 0.12), ("cap@L1+0.3", "tick", 0.12), ("cap@L1+0.5", "tick", 0.12),
            ("finger+0.3", "hum_on", 0.14), ("finger@L1+1.0", "zap", 0.1), ("finger@L2+0.8", "ding", 0.08),
            ("multi+0.6", "click", 0.3), ("multi+1.4", "click", 0.3),
            ("gloves+1.0", "knock", 0.22), ("gloves+1.2", "blip_down", 0.12), ("gloves@L1+1.0", "click", 0.3), ("gloves@L1+1.1", "blip", 0.14),
            ("sausage+1.6", "click", 0.3), ("sausage+2.0", "chime", 0.08),
            ("history+0.3", "paper", 0.15), ("history@L1", "whoosh", 0.14), ("history@L2+0.4", "swell", 0.14)],
    "bed": [("grid", "cap")],
    "bpm": 100,
}
