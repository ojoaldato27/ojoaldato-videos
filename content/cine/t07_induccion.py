"""T07 · ¿Por qué la inducción no calienta el cristal? (estilo Titanic, ilustración detallada)."""
from gadgets import *
import t02_microondas as T2
import t04_qr as T4
import t03_tactil as T3
import t06_nevera as T6

xf, callout, glow_line, top_shade, wavy, check = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T2.wavy, T4.check
heat_arrows = T6.heat_arrows

TITLE = "Por_que_la_induccion_no_calienta_el_cristal"
LINES = [
    "La placa de inducción calienta la olla… pero *no el cristal*.",
    "¿Cómo puede ser… y por qué con algunas sartenes *no funciona*?",
    "Debajo del cristal hay una *bobina de cobre*.",
    "Por ella pasa una corriente que cambia de sentido *decenas de miles de veces por segundo*.",
    "Eso crea un *campo magnético* que sube y baja sin parar.",
    "El *cristal no reacciona* a ese campo… pero *el metal de la olla, sí*.",
    "El campo crea dentro del metal unas *corrientes en remolino*.",
    "Y esas corrientes calientan la olla *desde su propio fondo*.",
    "El cristal solo se calienta porque *la olla caliente* está encima.",
    "Por eso, al quitarla, deja de calentar *al momento*.",
    "¿Y las *sartenes* que no funcionan?",
    "Necesitan *hierro* en el fondo: el campo solo agarra bien en metales magnéticos.",
    "Truco: si un *imán* se pega al fondo, sirve.",
    "Además, aprovecha alrededor del *75 %* de la energía.",
    "El gas, solo un *40 %*: el resto se escapa calentando la cocina.",
    "En la inducción, *la olla es el fuego*.",
]
SHOTS = [("open", 0, 1, 0.3), ("coil", 2, 3, 0.3), ("field", 4, 5, 0.3), ("eddy", 6, 7, 0.3), ("glass", 8, 9, 0.3),
         ("pans", 10, 12, 0.3), ("eff", 13, 14, 0.3), ("final", 15, 15, 1.8)]
FOCUS = {"open": (540, 1000, 1.12), "final": (540, 980, 1.1)}
NOTIF = ("coil", 1.0)
HYPE = {"line": 1, "text": ['¿CÓMO PUEDE SER?', '¿Y SI LA SARTÉN NO VA?'], "delay": [0, 1.1]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

COPPER = (230, 140, 70)
FIELD = (120, 200, 255)
ORANGE = (255, 150, 60)
HOT = (255, 90, 50)


# ------------------------------------------------------------------ objetos
def pot(kind="steel", water=True):
    w, h = 600, 520
    c = Cv(w, h)
    cx = w / 2
    rx, ry, top, bot = 220, 42, 150, 440
    c.shadow((cx - 250, bot - 10, cx + 250, bot + 60), 170, 12)
    if kind == "steel":
        g1, g2 = ((120, 124, 132), (246, 248, 252)), ((246, 248, 252), (90, 94, 102))
    else:
        g1, g2 = ((170, 174, 180), (226, 228, 232)), ((226, 228, 232), (150, 154, 160))
    c.rect((cx - rx - 46, top + 40, cx - rx + 4, top + 64), fill=(40, 40, 44), r=10)
    c.rect((cx + rx - 4, top + 40, cx + rx + 46, top + 64), fill=(40, 40, 44), r=10)
    c.ellipse((cx - rx, bot - ry, cx + rx, bot + ry), fill=g2[1])
    c.rect((cx - rx, top, cx, bot), grad=g1, horizontal=True)
    c.rect((cx, top, cx + rx, bot), grad=g2, horizontal=True)
    c.ellipse((cx - rx, top - ry, cx + rx, top + ry), fill=(70, 72, 80))
    c.ellipse((cx - rx + 14, top - ry + 8, cx + rx - 14, top + ry - 8), fill=(30, 32, 36))
    if water:
        c.ellipse((cx - rx + 20, top - ry + 18, cx + rx - 20, top + ry - 6), radial=((120, 150, 170), (50, 70, 90)))
    c.rect((cx - rx * 0.62, top + 12, cx - rx * 0.5, bot - 10), fill=(255, 255, 255, 60))
    return c.done()


def _cooktop():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((54, 46, 42), (26, 22, 20)))
    for y in range(120, 760, 64):
        off = 60 if (y // 64) % 2 else 0
        for x in range(-120, W + 120, 120):
            c.rect((x + off + 3, y + 3, x + off + 117, y + 61), grad=((140, 132, 124), (110, 102, 96)), r=4)
    c.rect((0, 760, W, H), grad=((120, 110, 100), (60, 54, 50)))
    glass = [(170, 820), (910, 820), (1060, 1300), (20, 1300)]
    c.poly([(150, 812), (930, 812), (1080, 1316), (0, 1316)], fill=(60, 60, 64))
    c.poly(glass, grad=((30, 30, 36), (8, 8, 10)))
    c.poly([(260, 820), (420, 820), (240, 1300), (60, 1300)], fill=(255, 255, 255, 14))
    for cx, cy, rx, ry in ((540, 1010, 270, 80), (300, 900, 120, 34), (790, 900, 120, 34)):
        c.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=None)
        c.arc((cx - rx, cy - ry, cx + rx, cy + ry), 0, 360, (150, 150, 160, 120), 3)
    for i in range(5):
        x = 380 + i * 80
        c.text((x, 1250), "+−"[i % 2], 30, (200, 60, 50))
    return c.done().convert("RGBA")


def cooktop(img, t, pot_kind="steel", boil=1.0, lift=0.0, on=True, display="9"):
    AC(img, cached("cooktop", _cooktop))
    d = ImageDraw.Draw(img, "RGBA")
    if on:
        d.text((700, 1250), display, font=f(F_MONO, 44), fill=(255, 60, 40, 230), anchor="mm")
        paste(img, glow(40, (255, 60, 40), 0.6), 700, 1250)
    if pot_kind:
        paste(img, glow(300, (0, 0, 0), 0.9), 540, 1020, 1.0, 0.6 * (1 - lift))
        y = 1010 - 180 - lift * 260
        paste(img, spr(pot, pot_kind), 540, y, 1.0)
        if boil > 0 and pot_kind == "steel":
            T2.smoke(img, t, [(480, y - 120, 0.9), (600, y - 120, 0.9)], col=(240, 244, 250), alpha=int(70 * boil), spread=(100, 20), grow=120, speed=0.6)


def coil_top(img, t, cx=540, cy=880, flip=None):
    pts = []
    for i in range(500):
        a = i / 500 * 2 * math.pi * 8
        r = 70 + i / 500 * 300
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    glow_line(img, pts, (90, 50, 20), 18, 4, 255)
    glow_line(img, pts, COPPER, 11, 6, 255)
    d = ImageDraw.Draw(img, "RGBA")
    d.line(pts, fill=(255, 210, 160, 140), width=3)
    if flip is not None:
        sgn = 1 if math.sin(t * 2 * math.pi * 3) > 0 else -1
        for k in range(24):
            u = (k / 24 + sgn * t * 0.25) % 1.0
            i = int(u * 499)
            x, y = pts[i]
            paste(img, glow(34, (255, 240, 160), 1.0), x, y)


def side_cross(img, t, field=0.0, pot_on=True, glow_base=0.0, eddy=0.0, lift=0.0, glass_hot=0.0, kind="steel"):
    sky(img, (24, 26, 34), (8, 8, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    gy = 900
    if field > 0:
        pul = 0.55 + 0.45 * math.sin(t * 14)
        for cxx in (370, 710):
            for k in range(5):
                rx, ry = 70 + k * 46, 120 + k * 70
                d.ellipse([cxx - rx, gy + 60 - ry, cxx + rx, gy + 60 + ry], outline=FIELD + (int(150 * field * pul * (1 - k * 0.12)),), width=4)
    d.rectangle([60, gy, 1020, gy + 36], fill=(30, 34, 44, 230))
    d.rectangle([60, gy, 1020, gy + 6], fill=(255, 255, 255, 50))
    if glass_hot > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rectangle([300, gy, 780, gy + 36], fill=(255, 120, 40, int(200 * glass_hot)))
        AC(img, lay.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img, "RGBA")
    for i, x in enumerate(range(250, 840, 44)):
        if 470 < x < 610:
            continue
        sgn = (x < 540) ^ (math.sin(t * 2 * math.pi * 3) > 0)
        d.ellipse([x - 18, gy + 50, x + 18, gy + 86], fill=COPPER + (255,), outline=(120, 60, 20, 255), width=3)
        if field > 0:
            if sgn:
                d.ellipse([x - 5, gy + 63, x + 5, gy + 73], fill=(40, 20, 10, 255))
            else:
                d.line([(x - 7, gy + 61), (x + 7, gy + 75)], fill=(40, 20, 10, 255), width=3)
                d.line([(x + 7, gy + 61), (x - 7, gy + 75)], fill=(40, 20, 10, 255), width=3)
    for x in range(260, 840, 120):
        d.rectangle([x, gy + 100, x + 80, gy + 124], fill=(60, 60, 66, 255))
    if pot_on:
        oy = -lift * 240
        bc = (int(lerp(150, 255, glow_base)), int(lerp(154, 90, glow_base)), int(lerp(160, 40, glow_base)))
        wall = (170, 174, 182) if kind == "steel" else (206, 208, 212)
        d.rectangle([250, gy - 360 + oy, 270, gy - 4 + oy], fill=wall + (255,))
        d.rectangle([810, gy - 360 + oy, 830, gy - 4 + oy], fill=wall + (255,))
        d.rectangle([270, gy - 300 + oy, 810, gy - 34 + oy], fill=(70, 110, 160, 220))
        d.rectangle([250, gy - 34 + oy, 830, gy - 4 + oy], fill=bc + (255,))
        if glow_base > 0:
            paste(img, glow(300, (255, 120, 40), 0.6), 540, gy - 20 + oy, 1.0, glow_base)
        if eddy > 0:
            d = ImageDraw.Draw(img, "RGBA")
            for x in range(300, 800, 90):
                ph = (t * 6 + x * 0.05) % (2 * math.pi)
                d.arc([x - 30, gy - 34 + oy, x + 30, gy - 4 + oy], math.degrees(ph), math.degrees(ph) + 270, fill=(255, 230, 120, int(255 * eddy)), width=4)
        rr = random.Random(4)
        bub = glow_base * (1 - lift)
        for i in range(int(30 * bub)):
            x = rr.uniform(290, 790)
            ph = (t * rr.uniform(0.6, 1.2) + rr.random()) % 1.0
            y = gy - 40 + oy - ph * 250
            r = 4 + 8 * ph
            d.ellipse([x - r, y - r, x + r, y + r], outline=(230, 240, 255, int(200 * (1 - ph))), width=2)


def magnet():
    c = Cv(300, 300)
    c.arc((40, 20, 260, 240), 180, 360, (200, 30, 30), 60)
    c.line([(70, 130), (70, 270)], (200, 30, 30), 60)
    c.line([(230, 130), (230, 270)], (200, 30, 30), 60)
    c.rect((40, 230, 100, 290), grad=((240, 240, 246), (150, 154, 160)), horizontal=True)
    c.rect((200, 230, 260, 290), grad=((240, 240, 246), (150, 154, 160)), horizontal=True)
    c.arc((50, 30, 250, 230), 200, 260, (255, 140, 140), 8)
    return c.done()


def flame_ring(img, t, cx, cy, s=1.0):
    rr = random.Random(2)
    for k in range(14):
        a = k / 14 * 2 * math.pi
        x, y = cx + math.cos(a) * 150 * s, cy + math.sin(a) * 34 * s
        hgt = (60 + 20 * math.sin(t * 14 + k)) * s
        d = ImageDraw.Draw(img, "RGBA")
        d.polygon([(x - 14 * s, y), (x + 14 * s, y), (x, y - hgt)], fill=(80, 150, 255, 200))
        d.polygon([(x - 7 * s, y), (x + 7 * s, y), (x, y - hgt * 0.55)], fill=(200, 230, 255, 230))
    paste(img, glow(int(200 * s), (90, 150, 255), 0.5), cx, cy - 30 * s)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        cooktop(img, t, "steel", 1.0)
        k = ease(clamp((t - 0.8) / 0.8))
        hx, hy = lerp(1200, 880, k), lerp(1300, 1130, k)
        T3.place_finger(img, "skin", hx, hy, 0.9, 40, 1.0, 0.0)
        check(img, 880, 1000, ease(clamp((t - 1.8) / 0.4)), 50)
    else:
        cooktop(img, t, "alu", 0.0, 0.0, True, "U" if int(t * 3) % 2 else "")
        k = ease(clamp((t - a1 - 0.6) / 0.3))
        d = ImageDraw.Draw(img, "RGBA")
        x, y = 820, 640
        d.ellipse([x - 60, y - 60, x + 60, y + 60], outline=(255, 80, 80, int(230 * k)), width=10)
        d.line([(x - 36, y - 36), (x + 36, y + 36)], fill=(255, 80, 80, int(230 * k)), width=10)
        d.line([(x + 36, y - 36), (x - 36, y + 36)], fill=(255, 80, 80, int(230 * k)), width=10)
    top_shade(img)
    title2(t, 0.3, "CALIENTA LA OLLA", "PERO NO EL CRISTAL", 250, 60, 80, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def sh_coil(img, t, T, L):
    a1 = L[1][0]
    sky(img, (20, 18, 16), (6, 6, 6), 1.0)
    paste(img, glow(600, (255, 140, 60), 0.2), 540, 880)
    coil_top(img, t, flip=(t > a1) or None)
    if t > a1:
        sgn = 1 if math.sin(t * 2 * math.pi * 3) > 0 else -1
        d = ImageDraw.Draw(img, "RGBA")
        for x in (150, 930):
            y0, y1 = (760, 1000) if sgn > 0 else (1000, 760)
            d.line([(x, y0), (x, y1)], fill=(255, 240, 160, 230), width=8)
            d.polygon([(x - 20, y1 - sgn * 30), (x + 20, y1 - sgn * 30), (x, y1)], fill=(255, 240, 160, 230))
    if t < a1:
        big(t, 0.3, "BOBINA DE COBRE", 290, 88, COPPER, pop=False)
    else:
        big(t, a1 + 0.3, "DECENAS DE MILES", 280, 80, YEL, sub="DE VECES POR SEGUNDO", pop=False)
    vignette(img, 200)


def sh_field(img, t, T, L):
    a1 = L[1][0]
    fk = ease(clamp((t - 0.3) / 0.8))
    side_cross(img, t, fk, True, 0.0)
    if t > a1:
        callout(img, t, a1 + 0.2, 950, 918, 900, 1180, "CRISTAL: NADA", (200, 210, 230), 32)
        callout(img, t, a1 + 1.4, 540, 880, 540, 470, "METAL: ¡SÍ!", YEL, 36)
        k = ease(clamp((t - a1 - 1.4) / 0.6))
        paste(img, glow(320, (255, 200, 120), 0.5), 540, 880, 1.0, k * (0.6 + 0.4 * math.sin(t * 14)))
    if t < a1:
        big(t, 0.3, "CAMPO MAGNÉTICO", 290, 84, FIELD, pop=False)
    vignette(img, 200)


def base_top(img, t, k):
    sky(img, (24, 24, 28), (8, 8, 10), 1.0)
    cx, cy, r = 540, 860, 380
    col = (int(lerp(170, 255, k)), int(lerp(174, 120, k)), int(lerp(182, 60, k)))
    paste(img, glow(520, (255, 120, 40), 0.5), cx, cy, 1.0, k)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,), outline=(90, 94, 100, 255), width=10)
    for rr_ in (120, 220, 310):
        ph = t * 160 * (1 if rr_ % 200 else -1)
        for k2 in range(3):
            a0 = ph + k2 * 120
            d.arc([cx - rr_, cy - rr_, cx + rr_, cy + rr_], a0, a0 + 80, fill=(255, 240, 160, 230), width=8)
            a = math.radians(a0 + 80)
            hx, hy = cx + math.cos(a) * rr_, cy + math.sin(a) * rr_
            tx, ty = -math.sin(a), math.cos(a)
            d.polygon([(hx + tx * 24, hy + ty * 24), (hx - ty * 14, hy + tx * 14), (hx + ty * 14, hy - tx * 14)], fill=(255, 240, 160, 230))


def sh_eddy(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: base_top(im, t, ease(clamp((t - 0.5) / 2.0)) * 0.6),
       lambda im: side_cross(im, t, 0.7, True, ease(clamp((t - a1) / 1.0)), 1.0), 0.7)
    if t < a1:
        big(t, 0.3, "CORRIENTES EN REMOLINO", 290, 64, YEL, pop=False)
    else:
        big(t, a1 + 0.2, "CALIENTA DESDE EL FONDO", 290, 62, ORANGE, pop=False)
    vignette(img, 200)


def sh_glass(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        side_cross(img, t, 0.5, True, 1.0, 0.6, 0.0, ease(clamp((t - 0.4) / 1.2)))
        k = ease(clamp((t - 1.0) / 0.6))
        for x in (380, 540, 700):
            heat_arrows(img, t, [[(x, 860), (x, 960)]], ORANGE, k)
        callout(img, t, 1.2, 760, 918, 860, 1200, "SOLO POR CONTACTO", ORANGE, 32)
    else:
        q = ease(clamp((t - a1 - 0.2) / 0.8))
        side_cross(img, t, 0.5 * (1 - q), True, 1.0 - q, 0.0, q, 0.4 * (1 - q))
    if t < a1:
        big(t, 0.3, "EL CRISTAL", 280, 90, WHITE, sub="LO CALIENTA LA OLLA")
    else:
        big(t, a1 + 0.3, "SE APAGA AL MOMENTO", 290, 66, YEL, pop=False)
    vignette(img, 200)


def pan_layers(img, t, t0):
    sky(img, (24, 26, 34), (8, 8, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y = 140, 940, 900
    d.rectangle([x0, y - 160, x1, y - 120], fill=(200, 204, 212, 255))
    d.rectangle([x0, y - 120, x1, y - 60], fill=(226, 228, 232, 255))
    d.rectangle([x0, y - 60, x1, y], fill=(90, 92, 98, 255))
    k = ease(clamp((t - t0 - 0.6) / 0.6))
    for cxx in (360, 720):
        for kk in range(4):
            rx, ry = 70 + kk * 46, 80 + kk * 50
            d.arc([cxx - rx, y + 40 - ry, cxx + rx, y + 40 + ry], 180, 360, fill=FIELD + (int(170 * k),), width=4)
    paste(img, glow(260, (255, 150, 60), 0.5), 540, y - 30, 1.0, k * (0.6 + 0.4 * math.sin(t * 12)))
    callout(img, t, t0 + 0.3, 900, y - 30, 820, y + 330, "HIERRO", (230, 230, 240), 38)
    callout(img, t, t0 + 0.7, 260, y - 90, 260, y + 330, "ALUMINIO", (210, 214, 220), 32)


def pan_magnet(img, t, t0):
    sky(img, (34, 30, 30), (10, 8, 8), 1.0)
    paste(img, spr(pot, "steel", False), 540, 700, 1.1)
    k = ease(clamp((t - t0 - 0.3) / 0.8))
    my = lerp(1450, 1080, k)
    paste(img, spr(magnet), 540, my, 0.9, 1.0, 180)
    check(img, 860, 1000, ease(clamp((t - t0 - 1.2) / 0.4)), 60)


def sh_pans(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a1 - 0.4:
        cooktop(img, t, "alu", 0.0, 0.0, True, "U" if int(t * 3) % 2 else "")
    elif t < a2 - 0.4:
        xf(img, t, a1, lambda im: cooktop(im, t, "alu", 0.0, 0.0, True, ""), lambda im: pan_layers(im, t, a1), 0.6)
    else:
        xf(img, t, a2, lambda im: pan_layers(im, t, a1), lambda im: pan_magnet(im, t, a2), 0.6)
    if t < a1:
        top_shade(img)
        big(t, 0.2, "¿NO FUNCIONA?", 280, 96, (255, 120, 100))
    elif t < a2:
        big(t, a1 + 0.2, "NECESITA HIERRO", 290, 88, WHITE, pop=False)
    else:
        big(t, a2 + 0.2, "TRUCO: EL IMÁN", 290, 92, YEL)
    vignette(img, 200)


def sh_eff(img, t, T, L):
    a1 = L[1][0]
    sky(img, (28, 26, 30), (8, 8, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    for x in (290, 790):
        d.rectangle([x - 200, 1000, x + 200, 1020], fill=(40, 40, 46, 255))
    paste(img, spr(pot, "steel"), 290, 830, 0.62)
    T2.smoke(img, t, [(290, 720, 0.6)], col=(240, 244, 250), alpha=60, spread=(60, 14), grow=60, speed=0.6)
    k2 = ease(clamp((t - a1) / 0.6))
    if k2 > 0:
        flame_ring(img, t, 790, 980, 0.9)
        paste(img, spr(pot, "steel"), 790, 830, 0.62, k2)
        heat_arrows(img, t, [[(640, 960), (520, 860)], [(940, 960), (1060, 860)], [(660, 900), (560, 760)], [(920, 900), (1030, 760)]], ORANGE, k2)
    d = ImageDraw.Draw(img, "RGBA")
    k1 = ease(clamp((t - 0.4) / 1.0))
    d.rounded_rectangle([190, 1080, 190 + 200 * k1, 1140], radius=14, fill=(90, 230, 130, 255))
    spaced(d, 290, 1180, f"{int(75 * k1)} %", f(F_SER, 56), (255, 255, 255, int(255 * k1)), 4)
    spaced(d, 290, 1250, "INDUCCIÓN", f(F_SER, 34), (220, 220, 230, int(255 * k1)), 5)
    if k2 > 0:
        d.rounded_rectangle([690, 1080, 690 + 200 * 0.53 * k2, 1140], radius=14, fill=(255, 120, 80, 255))
        spaced(d, 790, 1180, f"{int(40 * k2)} %", f(F_SER, 56), (255, 255, 255, int(255 * k2)), 4)
        spaced(d, 790, 1250, "GAS", f(F_SER, 34), (220, 220, 230, int(255 * k2)), 5)
    if t < a1:
        big(t, 0.3, "APROVECHA MÁS", 290, 88, (90, 230, 130), pop=False)
    else:
        big(t, a1 + 0.3, "EL RESTO SE ESCAPA", 290, 72, ORANGE, pop=False)
    vignette(img, 200)


def sh_final(img, t, T, L):
    cooktop(img, t, "steel", 1.0)
    paste(img, glow(320, (255, 130, 50), 0.4), 540, 990, 1.0, 0.6 + 0.4 * math.sin(t * 3))
    top_shade(img)
    title2(t, 0.3, "EN LA INDUCCIÓN", "LA OLLA ES EL FUEGO", 250, 58, 80, hold=max(2.0, T - 1.2))
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "warm"), ("coil", "exp"), ("eddy", "creative"), ("glass", "doc"), ("pans", "playful"), ("eff", "doc"),
              ("final", "premium")],
    "gains": {"exp": 0.7},
    "amb": {"hum": ["coil", "field", "eddy"], "room": ["open", "pans", "final"], "fire": ["eff"]},
    "sfx": [("open+0.3", "beep", 0.06), ("open+1.8", "ding", 0.08), ("open@L1+0.2", "beep", 0.06), ("open@L1+0.6", "blip_down", 0.12),
            ("coil+0.3", "whoosh", 0.12), ("coil@L1", "hum_on", 0.2), ("coil@L1+0.4", "zap", 0.08),
            ("field+0.3", "swell", 0.12), ("field@L1+1.4", "pop", 0.15),
            ("eddy+0.4", "whoosh_up", 0.12), ("eddy@L1+0.3", "crackle", 0.1),
            ("glass@L1+0.2", "whoosh", 0.12), ("glass@L1+0.6", "blip_down", 0.12),
            ("pans+0.2", "beep", 0.06), ("pans@L1+0.3", "pop", 0.14), ("pans@L2+1.0", "clack", 0.3), ("pans@L2+1.2", "ding", 0.08),
            ("eff+0.4", "riser", 0.08), ("eff@L1+0.3", "whoosh", 0.12), ("final+0.3", "swell", 0.14)],
    "bed": [("coil", "eddy")],
    "bpm": 98,
}
