"""T10 · ¿Por qué explotan las palomitas? (estilo Titanic, ilustración detallada en corte)."""
from gadgets import *
import t02_microondas as T2
import t04_qr as T4
import t06_nevera as T6

xf, callout, glow_line, top_shade, check, heat_arrows = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T4.check, T6.heat_arrows

TITLE = "Por_que_explotan_las_palomitas"
LINES = [
    "Cada palomita es una pequeña *bomba de vapor*.",
    "¿Qué pasa dentro del grano… y de dónde sale el *¡pop!*?",
    "Un grano de maíz tiene una cáscara muy dura… y dentro, *almidón y un poco de agua*.",
    "Al calentarlo, esa agua se convierte en *vapor*.",
    "Pero la cáscara no le deja salir… y *la presión sube y sube*.",
    "Cerca de los *180 grados*, dentro hay unas *10 atmósferas* de presión.",
    "*Diez veces* la presión del aire que te rodea.",
    "Hasta que la cáscara *revienta*.",
    "El almidón, blando por el calor, se hincha de golpe… y se enfría convertido en *espuma*.",
    "Eso blanco que te comes es *almidón inflado*.",
    "¿Y el ruido? En 2015, unos científicos lo grabaron a *3.000 imágenes por segundo*.",
    "Y descubrieron que el pop *no es la cáscara* rompiéndose…",
    "…es el *vapor* escapando de golpe.",
    "Y el grano salta porque le sale una especie de *pata* que empuja contra la sartén.",
    "Con una aceleración de unas *20 veces la gravedad*.",
    "Así que cada palomita es una explosión… *que te comes*.",
]
SHOTS = [("open", 0, 1, 0.3), ("kernel", 2, 3, 0.3), ("pressure", 4, 6, 0.3), ("burst", 7, 9, 0.3), ("camera", 10, 12, 0.3),
         ("jump", 13, 14, 0.3), ("final", 15, 15, 1.8)]
FOCUS = {"open": (540, 900, 1.12), "final": (540, 900, 1.1)}
NOTIF = ("pressure", 0.8)
HYPE = {"line": 1, "text": ['¿QUÉ PASA DENTRO?', '¿DE DÓNDE SALE EL «POP»?'], "delay": [0, 1.8]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

HULL = (226, 150, 40)
STARCH = (250, 236, 200)
STEAM = (235, 242, 255)
ORANGE = (255, 150, 60)


# ------------------------------------------------------------------ piezas
def popcorn(seed=1, s=1.0):
    c = Cv(260, 240)
    rr = random.Random(seed)
    blobs = []
    for _ in range(15):
        a, dd = rr.uniform(0, 6.28), rr.uniform(0, 1) ** 0.7 * 78
        blobs.append((130 + math.cos(a) * dd, 120 + math.sin(a) * dd * 0.85, rr.uniform(24, 46)))
    for x, y, r in blobs:
        c.ellipse((x - r, y - r + 4, x + r, y + r + 4), fill=(200, 180, 140))
    for x, y, r in blobs:
        c.ellipse((x - r, y - r, x + r, y + r), radial=((255, 252, 240), (226, 210, 170)), power=1.3, center=(0.36, 0.32))
    c.poly([(110, 170), (150, 160), (140, 196), (116, 192)], fill=HULL)
    return c.done()


def kernel_whole():
    c = Cv(300, 360)
    c.shadow((50, 320, 250, 356), 140, 8)
    c.poly([(150, 20), (240, 80), (270, 200), (220, 320), (150, 340), (80, 320), (30, 200), (60, 80)], grad=((250, 196, 80), (190, 110, 20)))
    c.ellipse((70, 60, 150, 240), fill=(255, 240, 200, 70))
    c.poly([(130, 300), (170, 300), (160, 340), (140, 340)], fill=(240, 220, 170))
    return c.done()


KS = (540, 860)
KPOLY = []
for _i in range(48):
    _a = _i / 48 * 2 * math.pi
    _w = 330 * (1.0 - 0.38 * max(0.0, math.cos(_a)) ** 1.6)
    KPOLY.append((math.sin(_a) * _w * (1 + 0.08 * math.sin(3 * _a)), -math.cos(_a) * 400))


def kernel_cut(img, t, water=1.0, vapor=0.0, press=0.0, heat=0.0, crack=0.0):
    cx, cy = KS
    pts = [(cx + x, cy + y) for x, y in KPOLY]
    inner = [(cx + x * 0.86, cy + y * 0.86) for x, y in KPOLY]
    c = Cv(W, H, 1)
    c.poly(pts, grad=(shade(HULL, 1.15), shade(HULL, 0.7)))
    c.poly(inner, grad=((252, 240, 206), (226, 206, 160)))
    c.poly([(cx - 120, cy + 200), (cx + 60, cy + 210), (cx + 30, cy + 330), (cx - 90, cy + 320)], grad=((240, 214, 140), (210, 170, 90)))
    rr = random.Random(5)
    for i in range(70):
        x, y = cx + rr.uniform(-280, 280), cy + rr.uniform(-300, 300)
        r = rr.uniform(8, 18)
        c.ellipse((x - r, y - r, x + r, y + r), fill=(236, 222, 186, 160))
    im = c.done()
    mo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mo).polygon(pts, fill=255)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mo))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(inner, fill=255)
    if heat > 0:
        paste(img, glow(700, (255, 120, 40), 0.5), cx, cy + 300, 1.0, heat)
    AC(img, im)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(cx - 60, cy - 330), (cx + 40, cy - 340), (cx - 80, cy - 240)], fill=(255, 255, 255, 50))
    rr = random.Random(9)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i in range(36):
        x0, y0 = cx + rr.uniform(-260, 260), cy + rr.uniform(-280, 280)
        if water > 0:
            r = 12 * water
            ld.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=(80, 150, 255, int(230 * water)))
        if vapor > 0:
            sp = 40 + 160 * press
            x = x0 + math.sin(t * (3 + press * 9) + i) * sp * 0.4
            y = y0 + math.cos(t * (2.6 + press * 8) + i * 1.3) * sp * 0.4
            r = 10 + 8 * vapor
            ld.ellipse([x - r, y - r, x + r, y + r], fill=STEAM + (int(200 * vapor),))
    lay.putalpha(ImageChops.multiply(lay.getchannel("A"), m))
    AC(img, lay)
    if crack > 0:
        d = ImageDraw.Draw(img, "RGBA")
        n = int(10 * crack)
        p = [(cx - 40, cy - 395)]
        rr = random.Random(2)
        for i in range(n):
            p.append((p[-1][0] + rr.uniform(-30, 30), p[-1][1] + 40))
        d.line(p, fill=(60, 30, 10, 255), width=6)
        q = [(cx + 300, cy - 240)]
        for i in range(n):
            q.append((q[-1][0] - 32, q[-1][1] + rr.uniform(-20, 30)))
        d.line(q, fill=(60, 30, 10, 255), width=6)


def gauge(img, v, cx, cy, r, label, vmax=12):
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], fill=(70, 72, 80, 255))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(246, 242, 230, 255))
    for k in range(vmax + 1):
        a = math.radians(140 + k / vmax * 260)
        d.line([(cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78), (cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92)], fill=(40, 40, 44), width=4)
    a = math.radians(140 + clamp(v / vmax) * 260)
    d.line([(cx, cy), (cx + math.cos(a) * r * 0.75, cy + math.sin(a) * r * 0.75)], fill=(200, 30, 30), width=7)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(40, 40, 44))
    d.text((cx, cy + r * 0.45), label, font=f(F_MONO, int(r * 0.26)), fill=(40, 40, 44), anchor="mm")


def thermo(img, v, x, y, h=300):
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([x - 24, y - h, x + 24, y + 20], radius=24, fill=(250, 250, 250, 255), outline=(80, 80, 90, 255), width=4)
    d.rounded_rectangle([x - 9, y - h * v + 10, x + 9, y + 10], radius=9, fill=(220, 40, 40, 255))
    d.ellipse([x - 36, y, x + 36, y + 72], fill=(220, 40, 40, 255))


def _cinema():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((20, 12, 14), (6, 4, 4)))
    c.rect((60, 120, 1020, 640), grad=((150, 170, 200), (90, 110, 150)))
    c.rect((40, 100, 1040, 120), fill=(90, 20, 26))
    for x in range(0, W, 60):
        c.rect((x, 0, x + 40, 110), grad=((130, 20, 30), (70, 10, 16)))
    for row in range(3):
        y = 900 + row * 160
        for k in range(8):
            x = 70 + k * 135 + (row % 2) * 60
            c.rect((x, y, x + 110, y + 140), grad=((120, 20, 30), (60, 10, 14)), r=26)
    return c.done().convert("RGBA")


def bucket():
    c = Cv(520, 640)
    c.shadow((60, 600, 460, 640), 160, 12)
    c.poly([(40, 120), (480, 120), (420, 620), (100, 620)], fill=(250, 250, 250))
    for k in range(6):
        x0 = 40 + k * 88
        x1 = x0 + 44
        c.poly([(x0, 120), (x1, 120), (100 + (x1 - 40) * 320 / 440, 620), (100 + (x0 - 40) * 320 / 440, 620)], fill=(210, 30, 40))
    c.rect((30, 100, 490, 140), grad=((250, 250, 250), (210, 210, 214)), r=10)
    rr = random.Random(3)
    for i in range(18):
        x, y = rr.uniform(60, 460), rr.uniform(10, 120)
        p = spr(popcorn, i % 6 + 1).resize((110, 100), Image.LANCZOS)
        c.im.alpha_composite(p.resize((330, 300), Image.BILINEAR), (int((x - 55) * 3), int((y - 50) * 3)))
    return c.done()


def sh_open(img, t, T, L):
    a1 = L[1][0]
    AC(img, cached("cinema", _cinema))
    spotlight(img, t, 540, 0, 900, 30, 400, 26, dust=True)
    paste(img, spr(bucket), 540, 1080, 1.0)
    rr = random.Random(4)
    for i in range(12):
        st = rr.uniform(0, 2.4)
        u = (t - st) % 2.4
        if u < 1.2:
            x = 540 + rr.uniform(-200, 200) + rr.uniform(-1, 1) * u * 200
            y = 820 - u * 900 + 600 * u * u
            paste(img, spr(popcorn, i % 6 + 1), x, y, 0.5, 1.0, u * 300)
    top_shade(img)
    title2(t, 0.3, "CADA PALOMITA ES", "UNA BOMBA DE VAPOR", 250, 56, 84, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def sh_kernel(img, t, T, L):
    a1 = L[1][0]
    sky(img, (30, 22, 16), (8, 6, 4), 1.0)
    if t < 0.9:
        paste(img, spr(kernel_whole), KS[0], KS[1], lerp(1.6, 2.4, t / 0.9))
    else:
        k = clamp((t - a1) / 1.4) if t > a1 else 0.0
        kernel_cut(img, t, 1.0 - k, k, 0.1, k)
        if t < a1:
            callout(img, t, 1.2, KS[0] + 262, KS[1] - 100, 920, 470, "CÁSCARA", HULL, 34)
            callout(img, t, 1.8, KS[0] - 150, KS[1] - 60, 200, 470, "ALMIDÓN", (250, 240, 210), 34)
            callout(img, t, 2.4, KS[0] + 100, KS[1] + 120, 900, 1330, "AGUA", (120, 180, 255), 34)
    if t < a1:
        big(t, 0.3, "DENTRO DEL GRANO", 290, 84, WHITE, pop=False)
    else:
        big(t, a1 + 0.4, "AGUA → VAPOR", 290, 92, STEAM)
    vignette(img, 190)


def sh_pressure(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    sky(img, (34, 20, 14), (10, 6, 4), 1.0)
    p = ease(clamp(t / (a2 + 0.6)))
    if t < a2 - 0.3:
        kernel_cut(img, t, 0.0, 1.0, p, 1.0)
        gauge(img, 1 + 9 * p, 860, 1250, 120, f"{1 + 9 * p:.0f} ATM")
        thermo(img, 0.3 + 0.6 * p, 180, 1260, 260)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((180, 1360), f"{int(100 + 80 * p)} °C", font=f(F_MONO, 34), fill=(255, 255, 255), anchor="mm")
    else:
        sky(img, (110, 160, 220), (200, 225, 245), 1.0)
        clouds(img, t, 400, (255, 255, 255), 120, 10, 4, 1.0)
        k = ease(clamp((t - a2) / 1.4))
        d = ImageDraw.Draw(img, "RGBA")
        for i in range(10):
            kk = clamp(k * 10 - i)
            if kk <= 0:
                continue
            x, y = 220 + (i % 5) * 160, 760 + (i // 5) * 200
            d.ellipse([x - 60, y - 60, x + 60, y + 60], fill=(255, 255, 255, int(230 * kk)), outline=(60, 110, 230, int(255 * kk)), width=6)
            d.text((x, y), "1", font=f(F_SER, 60), fill=(60, 110, 230, int(255 * kk)), anchor="mm")
        d.text((540, 1200), "1 ATM = EL AIRE QUE TE RODEA", font=f(F_SER, 40), fill=(30, 50, 90), anchor="mm")
    if t < a1:
        big(t, 0.3, "LA PRESIÓN SUBE", 290, 88, ORANGE, pop=False)
    elif t < a2:
        big(t, a1 + 0.2, "180 °C · 10 ATM", 290, 88, YEL, pop=False)
    else:
        big(t, a2 + 0.2, "10 VECES MÁS", 290, 100, (30, 60, 140))
    vignette(img, 190)


def foam(img, t, k, cx=540, cy=860):
    rr = random.Random(7)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i in range(70):
        a = rr.uniform(0, 6.28)
        dist = rr.uniform(0, 1) ** 0.6 * 420 * k
        x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist * 0.9
        r = (40 + rr.uniform(0, 60)) * (0.3 + 0.7 * k)
        ld.ellipse([x - r, y - r + 8, x + r, y + r + 8], fill=(200, 180, 140, 255))
    for i in range(70):
        pass
    rr = random.Random(7)
    for i in range(70):
        a = rr.uniform(0, 6.28)
        dist = rr.uniform(0, 1) ** 0.6 * 420 * k
        x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist * 0.9
        r = (40 + rr.uniform(0, 60)) * (0.3 + 0.7 * k)
        ld.ellipse([x - r, y - r, x + r, y + r], fill=(252, 246, 228, 255))
        ld.ellipse([x - r * 0.6, y - r * 0.7, x - r * 0.1, y - r * 0.3], fill=(255, 255, 255, 140))
    AC(img, lay)
    if k > 0.2:
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(11)
        for i in range(40):
            x, y = cx + rr.uniform(-300, 300) * k, cy + rr.uniform(-300, 300) * k
            r = rr.uniform(4, 10)
            d.ellipse([x - r, y - r, x + r, y + r], outline=(210, 196, 160, 200), width=2)


def sh_burst(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    sky(img, (34, 20, 14), (10, 6, 4), 1.0)
    pop_t = 1.0
    if t < pop_t:
        kernel_cut(img, t, 0.0, 1.0, 1.0, 1.0, clamp(t / pop_t))
        sx, sy = shake(t, 0.0, 6, 0.1)
    elif t < a2 - 0.3:
        k = ease(clamp((t - pop_t) / 1.6))
        foam(img, t, max(0.15, k))
        if t - pop_t < 0.5:
            overlay(img, (255, 255, 255), 0.8 * (1 - (t - pop_t) / 0.5))
        rr = random.Random(2)
        for i in range(5):
            a = rr.uniform(0, 6.28)
            dd = 200 + 300 * k
            paste(img, spr(kernel_whole).resize((80, 96)), 540 + math.cos(a) * dd, 860 + math.sin(a) * dd, 1.0, 1.0, rr.uniform(0, 360))
    else:
        k = ease(clamp((t - a2) / 0.6))
        paste(img, glow(600, (255, 220, 160), 0.3), 540, 860)
        paste(img, spr(popcorn, 3), 540, 860, lerp(2.4, 3.2, k))
    if t < a1:
        big(t, 0.6, "¡REVIENTA!", 290, 110, ORANGE)
    elif t < a2:
        big(t, a1 + 0.2, "ESPUMA", 290, 120, STARCH)
    else:
        big(t, a2 + 0.2, "ALMIDÓN INFLADO", 290, 84, YEL, pop=False)
    vignette(img, 190)


def lab_cam(img, t, t0):
    sky(img, (24, 28, 34), (8, 8, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1100, W, H], fill=(60, 62, 70, 255))
    d.rounded_rectangle([560, 1000, 940, 1100], radius=12, fill=(40, 40, 46, 255))
    d.rectangle([580, 990, 920, 1004], fill=(255, 90, 40, 255))
    paste(img, glow(200, (255, 120, 40), 0.5), 750, 1000)
    paste(img, spr(kernel_whole), 750, 950, 0.3)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(260, 1100), (200, 1300)], fill=(30, 30, 34), width=10)
    d.line([(260, 1100), (320, 1300)], fill=(30, 30, 34), width=10)
    d.line([(260, 1100), (260, 1320)], fill=(30, 30, 34), width=10)
    d.rounded_rectangle([140, 880, 400, 1100], radius=20, fill=(34, 34, 40, 255), outline=(90, 90, 100, 255), width=4)
    d.rectangle([400, 940, 480, 1040], fill=(20, 20, 24, 255))
    d.ellipse([470, 930, 530, 1050], fill=(60, 90, 140, 255))
    d.ellipse([200, 910, 220, 930], fill=(255, 40, 40, 255) if int(t * 3) % 2 else (90, 20, 20, 255))
    d.rounded_rectangle([150, 760, 410, 850], radius=14, fill=(0, 0, 0, 200))
    d.text((280, 805), "3.000 FPS", font=f(F_MONO, 44), fill=(120, 255, 170), anchor="mm")


def film(img, t, t0, steam_k):
    sky(img, (14, 14, 18), (4, 4, 6), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 520, W, 1220], fill=(20, 20, 22, 255))
    for x in range(0, W, 60):
        d.rounded_rectangle([x + 10, 540, x + 40, 570], radius=6, fill=(220, 220, 220, 255))
        d.rounded_rectangle([x + 10, 1170, x + 40, 1200], radius=6, fill=(220, 220, 220, 255))
    off = ((t - t0) * 120) % 360
    for i in range(-1, 4):
        x = 60 + i * 360 - off
        d.rectangle([x, 600, x + 330, 1140], fill=(60, 50, 40, 255))
        paste(img, spr(kernel_whole), x + 165, 880, 0.7)
        if i >= 1:
            d = ImageDraw.Draw(img, "RGBA")
            d.line([(x + 140, 780), (x + 170, 860), (x + 150, 940)], fill=(60, 30, 10, 255), width=6)
        d = ImageDraw.Draw(img, "RGBA")
    if steam_k > 0:
        T2.smoke(img, t, [(560, 820, 1.4)], col=STEAM, alpha=int(140 * steam_k), spread=(80, 60), grow=200, speed=1.4)
        d = ImageDraw.Draw(img, "RGBA")
        for i in range(4):
            r = 120 + ((t * 300) + i * 90) % 360
            d.ellipse([560 - r, 820 - r, 560 + r, 820 + r], outline=(255, 210, 63, int(200 * steam_k * (1 - (r - 120) / 360))), width=6)


def sh_camera(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a1 - 0.3:
        lab_cam(img, t, 0)
    else:
        xf(img, t, a1, lambda im: lab_cam(im, t, 0), lambda im: film(im, t, a1, ease(clamp((t - a2) / 0.4)) if t > a2 else 0.0), 0.6)
    if t < a1:
        date_stamp(t, 0.3, "2015", 270, hold=max(1.6, a1 - 0.8))
    elif t < a2:
        big(t, a1 + 0.2, "NO ES LA CÁSCARA", 290, 84, WHITE, pop=False)
        if t > a1 + 1.0:
            T2.strike(t, a1 + 1.0, W / 2, 300, 740, (255, 80, 80), 8) if hasattr(T2, "strike") else None
    else:
        big(t, a2 + 0.2, "¡ES EL VAPOR!", 290, 100, YEL)
    vignette(img, 190)


def sh_jump(img, t, T, L):
    a1 = L[1][0]
    sky(img, (30, 24, 20), (10, 8, 6), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1200, W, 1260], fill=(60, 62, 70, 255))
    d.rectangle([0, 1196, W, 1206], fill=(255, 100, 40, 255))
    paste(img, glow(500, (255, 120, 40), 0.35), 540, 1200)
    u = clamp((t - 0.6) / 1.2)
    leg = ease(clamp((t - 0.3) / 0.5))
    if t < 0.6:
        y, rot = 1100, 0
    else:
        y = 1100 - 900 * u + 700 * u * u
        rot = -u * 260
    x = 540 + 160 * u
    if t < 0.9:
        d.rounded_rectangle([x - 24, y + 60, x + 24, y + 60 + 50 * leg], radius=20, fill=STARCH + (255,))
    paste(img, spr(kernel_whole), x, y, 0.55, 1.0, rot)
    if 0.6 < t < 1.4:
        for k in range(3):
            d.line([(x - 60 + k * 60, y + 140), (x - 70 + k * 60, y + 200)], fill=(255, 255, 255, 160), width=4)
    if t > a1:
        k = ease(clamp((t - a1 - 0.2) / 0.5))
        d.polygon([(160, 1100), (240, 960), (320, 1100)], fill=YEL + (int(255 * k),))
        d.rectangle([215, 1100, 265, 1300], fill=YEL + (int(255 * k),))
    if t < a1:
        big(t, 0.3, "LE SALE UNA «PATA»", 290, 76, STARCH, pop=False)
    else:
        big(t, a1 + 0.2, "≈ 20 G", 290, 130, YEL, sub="DE ACELERACIÓN")
    vignette(img, 190)


def sh_final(img, t, T, L):
    AC(img, cached("cinema", _cinema))
    spotlight(img, t, 540, 0, 900, 30, 400, 26, dust=True)
    paste(img, spr(bucket), 540, 1080, 1.0)
    top_shade(img)
    title2(t, 0.3, "UNA EXPLOSIÓN", "QUE TE COMES", 250, 60, 92, hold=max(2.0, T - 1.2))
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "playful"), ("kernel", "creative"), ("pressure", "tension"), ("burst", "epic"), ("camera", "doc"),
              ("jump", "playful"), ("final", "premium")],
    "duck": [("burst+0.8", "burst+1.6", 0.6)],
    "amb": {"crowd": ["open", "final"], "fire": ["kernel", "pressure", "jump"], "room": ["camera"]},
    "sfx": [("open+0.4", "pop", 0.25), ("open+0.9", "pop", 0.2), ("open+1.5", "pop", 0.22), ("open+2.1", "pop", 0.2),
            ("open@L1", "whoosh", 0.12), ("kernel+0.9", "shutter", 0.15), ("kernel+1.2", "pop", 0.12), ("kernel@L1+0.3", "crackle", 0.1),
            ("pressure+0.3", "riser_long", 0.1), ("pressure@L1+0.2", "tick", 0.15), ("pressure@L2+0.2", "whoosh", 0.12),
            ("burst+1.0", "boom", 0.4), ("burst+1.0", "pop", 0.4), ("burst@L1", "swell", 0.12), ("burst@L2+0.2", "ding", 0.08),
            ("camera+0.3", "shutter", 0.2), ("camera+0.6", "beep", 0.05), ("camera@L1", "whoosh", 0.12), ("camera@L2+0.2", "pop", 0.35),
            ("jump+0.6", "pop", 0.3), ("jump+0.7", "whoosh_up", 0.14), ("jump@L1+0.2", "impact", 0.2), ("final+0.3", "swell", 0.14)],
    "bed": [("kernel", "pressure")],
    "bpm": 104,
}
