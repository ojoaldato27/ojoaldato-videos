"""T02 · ¿Cómo funciona un microondas? (estilo Titanic, ilustración detallada con vista de rayos X)."""
from kitchen import *

TITLE = "Como_funciona_un_microondas"
LINES = [
    "Un microondas calienta la comida *sin fuego* y sin resistencias al rojo.",
    "¿Cómo lo hace… y para qué sirve *la rejilla* de la puerta?",
    "Todo empieza aquí dentro: en el *magnetrón*.",
    "Unos *electrones* giran atrapados por un imán…",
    "…y al pasar por estas cavidades, generan *microondas*.",
    "Son ondas de radio, como las del wifi, que oscilan *2.450 millones de veces por segundo*.",
    "Una *guía* las conduce hasta la comida.",
    "Y la comida está llena de *agua*.",
    "Cada molécula de agua tiene un lado *negativo*… y otro *positivo*.",
    "Las microondas tiran de ellas *a un lado y a otro*, sin parar.",
    "Giran, chocan entre sí… y ese roce se convierte en *calor*.",
    "Por eso el hielo cuesta tanto: sus moléculas están atrapadas y casi *no pueden girar*.",
    "Y no calienta de dentro hacia fuera: las ondas solo entran *un par de centímetros*.",
    "Dentro hay zonas frías y calientes… por eso el plato *gira*.",
    "¿Y la *rejilla*?",
    "Sus agujeros miden alrededor de *un milímetro*.",
    "Pero las microondas miden *12 centímetros*: no caben.",
    "La *luz* es mucho más pequeña: *pasa*, y puedes ver tu comida.",
    "Se inventó en los años 40, cuando a Percy Spencer se le *derritió una chocolatina* junto a un magnetrón.",
    "Un invento nacido de *un accidente*.",
]
SHOTS = [("open", 0, 1, 0.3), ("magnetron", 2, 4, 0.3), ("wave", 5, 6, 0.3), ("water", 7, 8, 0.3), ("spin", 9, 10, 0.3),
         ("ice", 11, 11, 0.3), ("depth", 12, 12, 0.3), ("hotspots", 13, 13, 0.3), ("mesh", 14, 17, 0.3), ("spencer", 18, 19, 1.8)]
FOCUS = {"wave": (540, 860, 1.12), "water": (540, 880, 1.12), "spin": (540, 900, 1.1), "ice": (540, 900, 1.14),
         "depth": (540, 900, 1.12), "hotspots": (540, 880, 1.12), "spencer": (560, 820, 1.15)}
NOTIF = ("wave", 1.0)
HYPE = {"line": 1, "text": ['¿CÓMO LO HACE…', '¿Y LA REJILLA?'], "delay": [0, 1.1]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

MY = COUNTER_Y - 245
BLUE_ = (120, 190, 255)
ORANGE = (255, 150, 60)


# ------------------------------------------------------------------ utilidades
def top_shade(img, a=170, h=600):
    def mk():
        g = np.linspace(1, 0, h) ** 1.4 * a
        arr = np.zeros((h, W, 4), np.uint8)
        arr[..., 3] = g[:, None].astype(np.uint8)
        return Image.fromarray(arr, "RGBA")
    AC(img, cached(("topshade", a, h), mk))


def xf(img, t, a, A, B, d=0.6):
    """Fundido interno entre dos dibujos dentro del mismo plano."""
    if t < a - d / 2:
        A(img)
        return
    if t > a + d / 2:
        B(img)
        return
    k = ease((t - (a - d / 2)) / d)
    im2 = img.copy()
    A(img)
    B(im2)
    img.paste(Image.blend(img, im2, k))


def callout(img, t, t0, px, py, tx, ty, txt, col=YEL, size=40):
    k = ease(clamp((t - t0) / 0.5))
    if k <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    A = int(255 * k)
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=col + (A,), outline=(0, 0, 0, A // 2), width=2)
    ex, ey = lerp(px, tx, k), lerp(py, ty, k)
    d.line([(px, py), (ex, ey)], fill=col + (int(230 * k),), width=4)
    if k > 0.5:
        kk = clamp((k - 0.5) / 0.5)
        w = spaced(d, tx, ty - 58, txt, f(F_SER, size), (255, 255, 255, int(255 * kk)), 4)
        d.line([(tx - w / 2, ty - 6), (tx + w / 2, ty - 6)], fill=col + (int(230 * kk),), width=3)


def glow_line(img, pts, col, w=6, blur=10, alpha=220):
    if len(pts) < 2:
        return
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, y0 = int(max(0, min(xs) - 40)), int(max(0, min(ys) - 40))
    x1, y1 = int(min(W, max(xs) + 40)), int(min(H, max(ys) + 40))
    if x1 <= x0 or y1 <= y0:
        return
    im = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P_ = [(x - x0, y - y0) for x, y in pts]
    d.line(P_, fill=col + (int(alpha * 0.6),), width=w * 3, joint="curve")
    im = im.filter(ImageFilter.GaussianBlur(blur))
    d = ImageDraw.Draw(im)
    d.line(P_, fill=col + (alpha,), width=w, joint="curve")
    d.line(P_, fill=(255, 255, 240, alpha), width=max(1, w // 3), joint="curve")
    AC(img, im, (x0, y0))


def wavy(pts, prog, amp, wl, phase):
    """Polilínea que sigue un camino con una onda sinusoidal superpuesta, recortada a la fracción prog."""
    segs = []
    tot = 0
    for p, q in zip(pts, pts[1:]):
        L_ = math.hypot(q[0] - p[0], q[1] - p[1])
        segs.append((p, q, L_))
        tot += L_
    lim = tot * clamp(prog)
    out, acc = [], 0
    for p, q, L_ in segs:
        nx, ny = (q[0] - p[0]) / L_, (q[1] - p[1]) / L_
        px_, py_ = -ny, nx
        n = max(2, int(L_ / 6))
        for i in range(n + 1):
            s_ = acc + L_ * i / n
            if s_ > lim:
                return out
            u = i / n
            off = math.sin(s_ / wl * 2 * math.pi - phase) * amp
            out.append((p[0] + nx * L_ * u + px_ * off, p[1] + ny * L_ * u + py_ * off))
        acc += L_
    return out


# ------------------------------------------------------------------ sprites del vídeo
def magnetron_xsec():
    c = Cv(800, 800)
    cx = cy = 400
    c.ellipse((6, 6, 794, 794), radial=((124, 128, 138), (40, 42, 50)), power=0.8, center=(0.42, 0.36))
    c.arc((20, 20, 780, 780), 200, 290, (255, 255, 255, 70), 6)
    c.ellipse((70, 70, 730, 730), fill=(10, 12, 18))
    c.ellipse((94, 94, 706, 706), radial=((250, 184, 120), (140, 74, 32)), power=1.0, center=(0.4, 0.34))
    c.arc((104, 104, 696, 696), 200, 280, (255, 230, 200, 110), 5)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        nx, ny = math.cos(a), math.sin(a)
        hx, hy = cx + nx * 228, cy + ny * 228
        c.ellipse((hx - 44, hy - 44, hx + 44, hy + 44), radial=((40, 26, 20), (8, 6, 6)), power=0.8)
        px_, py_ = -ny, nx
        r0, r1, wd = 140, 200, 15
        c.poly([(cx + nx * r0 + px_ * wd, cy + ny * r0 + py_ * wd), (cx + nx * r1 + px_ * wd, cy + ny * r1 + py_ * wd),
                (cx + nx * r1 - px_ * wd, cy + ny * r1 - py_ * wd), (cx + nx * r0 - px_ * wd, cy + ny * r0 - py_ * wd)], fill=(14, 10, 10))
        c.arc((hx - 44, hy - 44, hx + 44, hy + 44), 30, 120, (255, 220, 180, 90), 3)
    c.ellipse((250, 250, 550, 550), radial=((24, 30, 48), (8, 10, 16)), power=1.2)
    c.ellipse((354, 354, 446, 446), radial=((255, 240, 190), (200, 90, 28)), center=(0.42, 0.36))
    c.glow(400, 400, 100, (255, 170, 80), 0.7)
    return c.done()


def router():
    c = Cv(440, 300)
    c.shadow((20, 250, 420, 296), 150, 8)
    for x, a in ((90, -12), (220, 0), (350, 12)):
        tx = x + math.sin(math.radians(a)) * 170
        c.line([(x, 170), (tx, 10)], (30, 30, 34), 22)
        c.line([(x - 4, 170), (tx - 4, 14)], (90, 92, 100), 4)
    c.poly([(30, 170), (410, 170), (430, 210), (10, 210)], grad=((70, 72, 80), (40, 42, 48)))
    c.rect((10, 208, 430, 270), grad=((36, 38, 44), (12, 12, 14)), r=10)
    c.rect((14, 210, 426, 218), fill=(255, 255, 255, 40), r=4)
    for i in range(6):
        x = 90 + i * 52
        col = (80, 220, 255) if i < 5 else (90, 255, 140)
        c.ellipse((x - 6, 234, x + 6, 246), fill=col)
        c.glow(x, 240, 18, col, 0.8)
    return c.done()


def eye():
    c = Cv(300, 200)
    c.poly([(10, 100), (60, 50), (150, 26), (240, 50), (290, 100), (240, 150), (150, 172), (60, 150)], grad=((250, 246, 240), (200, 190, 184)))
    c.ellipse((92, 40, 212, 160), radial=((110, 180, 120), (30, 70, 50)), power=0.9)
    c.ellipse((126, 74, 178, 126), fill=(8, 8, 10))
    c.ellipse((140, 76, 162, 96), fill=(255, 255, 255, 220))
    c.line([(10, 100), (60, 48), (150, 22), (240, 48), (290, 100)], (40, 28, 24), 8)
    for k in range(9):
        x = 50 + k * 25
        y = 100 - 76 * math.sin(math.pi * (x - 10) / 280)
        c.line([(x, y), (x - 6 + k * 1.5, y - 20)], (40, 28, 24), 3)
    return c.done()


def lasagna():
    w, h = 760, 400
    c = Cv(w, h)
    layers = [((244, 210, 130), (214, 170, 90), 48), ((196, 56, 34), (140, 30, 20), 50), ((246, 236, 210), (220, 206, 176), 36),
              ((240, 206, 124), (206, 164, 86), 44), ((190, 52, 30), (130, 28, 18), 52), ((246, 236, 210), (220, 206, 176), 34),
              ((242, 206, 124), (206, 166, 90), 44), ((250, 196, 80), (214, 140, 40), 60)]
    y = h
    rr = random.Random(5)
    for top, bot, th in layers:
        y0 = y - th
        pts = [(0, y)] + [(x, y0 + math.sin(x / 70 + rr.uniform(0, 6)) * 5) for x in range(0, w + 1, 40)] + [(w, y)]
        c.poly(pts, grad=(top, bot))
        y = y0
    for i in range(40):
        x, yy = rr.uniform(20, w - 20), rr.uniform(10, 60)
        c.ellipse((x - 14, yy - 6, x + 14, yy + 6), fill=(170, 96, 30, 160))
    for i in range(30):
        x, yy = rr.uniform(20, w - 20), rr.uniform(90, h - 20)
        c.ellipse((x - 5, yy - 4, x + 5, yy + 4), fill=(100, 30, 18, 120))
    return c.done()


def heat_map(w=760, h=400, depth=46):
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    dist = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    band = np.exp(-dist / depth)
    hot = np.zeros((h, w, 4), np.uint8)
    hot[..., 0], hot[..., 1], hot[..., 2] = 255, (90 + 120 * band).astype(np.uint8), 40
    hot[..., 3] = (210 * band).astype(np.uint8)
    cold = np.zeros((h, w, 4), np.uint8)
    cold[..., 0], cold[..., 1], cold[..., 2] = 70, 150, 255
    cold[..., 3] = (120 * np.clip(1 - band * 1.6, 0, 1)).astype(np.uint8)
    return Image.fromarray(hot, "RGBA"), Image.fromarray(cold, "RGBA")


HOT = [(-258, -172), (-86, -172), (86, -172), (258, -172), (-172, 0), (0, 0), (172, 0), (-258, 172), (-86, 172), (86, 172), (258, 172),
       (-172, -344), (172, -344), (-172, 344), (172, 344)]


def thermal(size=860):
    yy, xx = np.mgrid[0:size, 0:size].astype(float) - size / 2
    v = np.zeros_like(xx)
    for hx, hy in HOT:
        v += np.exp(-((xx - hx) ** 2 + (yy - hy) ** 2) / (2 * 52 ** 2))
    v = np.clip(v, 0, 1)
    cols = np.array([(40, 70, 220), (60, 200, 230), (250, 230, 70), (250, 90, 40), (230, 30, 30)], float)
    idx = v * (len(cols) - 1)
    i0 = np.floor(idx).astype(int).clip(0, len(cols) - 2)
    fr = (idx - i0)[..., None]
    rgb = cols[i0] * (1 - fr) + cols[i0 + 1] * fr
    arr = np.zeros((size, size, 4), np.uint8)
    arr[..., :3] = rgb.astype(np.uint8)
    arr[..., 3] = (110 + 60 * v).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def chocolate():
    w, h = 520, 200
    c = Cv(w, h)
    c.shadow((10, 170, 510, 205), 140, 8)
    c.rect((0, 0, w, h - 10), grad=((120, 70, 40), (66, 34, 18)), r=12)
    for i in range(8):
        for j in range(3):
            x, y = 10 + i * 63, 10 + j * 60
            c.rect((x, y, x + 56, y + 52), grad=((118, 68, 38), (78, 42, 22)), r=6)
            c.rect((x + 4, y + 3, x + 52, y + 9), fill=(255, 220, 190, 40), r=3)
    # zonas derretidas donde caen los puntos calientes con el plato parado
    for hx, hy in HOT:
        bx, by = hx + w / 2, hy + h / 2 - 10
        if 20 < bx < w - 20 and 10 < by < h - 20:
            c.ellipse((bx - 42, by - 30, bx + 42, by + 30), radial=((150, 90, 50), (90, 50, 26)), power=1.4)
            c.ellipse((bx - 22, by - 16, bx + 4, by - 6), fill=(255, 230, 200, 120))
    return c.done()


def _cavity_big():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), fill=(12, 10, 10))
    bw = ((240, 206, 140), (196, 146, 76))
    sw = ((206, 160, 92), (130, 88, 40))
    c.poly([(60, 420), (1020, 420), (850, 600), (230, 600)], grad=((150, 110, 60), (214, 168, 100)))
    c.poly([(60, 1300), (1020, 1300), (850, 1060), (230, 1060)], grad=((190, 140, 74), (120, 80, 36)))
    c.poly([(60, 420), (230, 600), (230, 1060), (60, 1300)], grad=sw, horizontal=True)
    c.poly([(1020, 420), (850, 600), (850, 1060), (1020, 1300)], grad=sw[::-1], horizontal=True)
    c.rect((230, 600, 850, 1060), grad=bw)
    for i in range(6):
        for j in range(5):
            x, y = 110 + i * 18, 700 + j * 26 + i * 6
            c.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(80, 56, 30))
    c.poly([(902, 560), (984, 498), (984, 640), (902, 690)], grad=((140, 112, 84), (96, 72, 50)))
    for x, y in ((914, 572), (972, 520), (972, 622), (914, 672)):
        c.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(220, 220, 226))
    c.glow(300, 640, 220, (255, 240, 200), 0.8)
    c.ellipse((240, 1150, 840, 1290), fill=(255, 255, 255, 40))
    c.arc((240, 1150, 840, 1290), 0, 180, (255, 255, 255, 110), 4)
    for k in range(3):
        a = k * 2 * math.pi / 3
        c.ellipse((540 + math.cos(a) * 230 - 14, 1220 + math.sin(a) * 50 - 8, 540 + math.cos(a) * 230 + 14, 1220 + math.sin(a) * 50 + 8), fill=(60, 50, 40, 160))
    return c.done().convert("RGBA")


def _mesh_macro():
    w, h = W, H
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    sp, rh = 96.0, 30.0
    row = np.round((yy - 860) / (sp * 0.866))
    gx = xx - 540 - (row % 2) * sp / 2
    dx = gx - np.round(gx / sp) * sp
    dy = (yy - 860) - row * sp * 0.866
    dist = np.sqrt(dx ** 2 + dy ** 2)
    base = 46 + 14 * np.sin(yy / 3.0) * 0.2 + 18 * (1 - yy / h)
    rgb = np.stack([base, base + 2, base + 8], -1)
    ring = np.clip(1 - np.abs(dist - rh - 3) / 6, 0, 1)
    rgb += (ring * np.clip(dy / rh, 0, 1) * 60)[..., None]
    rgb -= (ring * np.clip(-dy / rh, 0, 1) * 30)[..., None]
    a = np.where(dist < rh, 0, 255)
    edge = np.clip((dist - rh) / 1.5, 0, 1)
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    arr[..., 3] = (a * edge).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def _lab():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((112, 92, 70), (52, 40, 30)))
    for y in range(0, 1180, 64):
        off = 60 if (y // 64) % 2 else 0
        for x in range(-120, W + 120, 120):
            c.rect((x + off + 3, y + 3, x + off + 117, y + 61), grad=((122, 98, 76), (100, 80, 60)), r=3)
    c.rect((80, 120, 520, 700), fill=(40, 34, 28), r=6)
    c.rect((96, 136, 504, 684), grad=((240, 226, 190), (190, 170, 130)))
    for x in (232, 368):
        c.rect((x - 6, 136, x + 6, 684), fill=(40, 34, 28))
    for y in (318, 500):
        c.rect((96, y - 6, 504, y + 6), fill=(40, 34, 28))
    # armario de equipos
    c.rect((700, 330, 1040, 1180), grad=((96, 98, 96), (50, 52, 50)), horizontal=True, r=6)
    for i, y in enumerate((400, 560)):
        for j, x in enumerate((780, 960)):
            c.ellipse((x - 58, y - 58, x + 58, y + 58), radial=((240, 232, 210), (170, 160, 140)), center=(0.4, 0.35))
            c.arc((x - 62, y - 62, x + 62, y + 62), 0, 360, (40, 40, 40), 5)
            c.line([(x, y), (x + math.cos(-2.2 + i + j) * 46, y + math.sin(-2.2 + i + j) * 46)], (160, 30, 30), 4)
    for k in range(5):
        x = 740 + k * 62
        c.rect((x, 690, x + 34, 740), grad=((60, 60, 60), (24, 24, 24)), r=6)
        c.ellipse((x + 6, 700, x + 28, 722), fill=(255, 190, 90))
    for k in range(4):
        x = 760 + k * 74
        c.rect((x, 800, x + 40, 900), fill=(200, 196, 180, 60), r=18)
        c.ellipse((x + 8, 830, x + 32, 870), fill=(255, 150, 60, 200))
    # mesa de trabajo y magnetrón sobre soporte
    c.rect((0, 1180, W, 1230), grad=((120, 84, 52), (70, 46, 28)))
    c.rect((0, 1230, W, H), grad=((50, 36, 26), (20, 14, 10)))
    for y in range(980, 1120, 12):
        c.rect((520, y, 660, y + 6), grad=((220, 210, 190), (130, 120, 104)), horizontal=True, r=2)
    c.rect((560, 960, 620, 1150), grad=((240, 168, 104), (132, 72, 34)), horizontal=True, r=6)
    c.rect((540, 1150, 640, 1180), fill=(50, 46, 40))
    c.line([(620, 1060), (700, 1100), (720, 1180)], (30, 30, 30), 6)
    return c.done().convert("RGBA")


def melt_inset(t, k):
    r = 170
    c = Cv(2 * r + 20, 2 * r + 20, 2)
    cx = cy = r + 10
    c.ellipse((cx - r, cy - r, cx + r, cy + r), radial=((90, 76, 60), (40, 32, 24)))
    c.poly([(cx - 150, cy - 20), (cx + 150, cy - 70), (cx + 160, cy + 10), (cx - 140, cy + 60)], grad=((200, 40, 40), (130, 20, 20)))
    c.text((cx + 10, cy - 8), "CHOCOLATE", 26, (255, 236, 200))
    c.poly([(cx - 150, cy + 60), (cx + 160, cy + 10), (cx + 160, cy + 70), (cx - 150, cy + 120)], grad=((120, 70, 40), (70, 36, 18)))
    for i in range(5):
        x = cx - 110 + i * 60
        y = cy + 108 - i * 10
        ln = 20 + 90 * k * (0.6 + 0.4 * math.sin(i * 1.7))
        c.line([(x, y), (x, y + ln)], (90, 50, 24), 16)
        c.ellipse((x - 11, y + ln - 10, x + 11, y + ln + 12), fill=(96, 54, 26))
        c.ellipse((x - 5, y + 6, x, y + ln * 0.6), fill=(255, 220, 190, 70))
    m = Image.new("L", c.im.size, 0)
    ImageDraw.Draw(m).ellipse([(cx - r) * 2, (cy - r) * 2, (cx + r) * 2, (cy + r) * 2], fill=255)
    c.im.putalpha(ImageChops.multiply(c.im.getchannel("A"), m))
    c.d = ImageDraw.Draw(c.im)
    c.arc((cx - r, cy - r, cx + r, cy + r), 0, 360, (240, 220, 180), 8)
    return c.done()


def sepia(img, k=0.55):
    g = img.convert("L")
    sep = Image.merge("RGB", (g.point(lambda v: min(255, int(v * 1.08 + 18))), g.point(lambda v: int(v * 0.92 + 8)), g.point(lambda v: int(v * 0.72))))
    img.paste(Image.blend(img.convert("RGB"), sep, k))


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    kitchen(img)
    q = ease(clamp((t - a1) / 2.6))
    s = lerp(1.0, 1.22, q)
    ox, oy = lerp(540, 600, q), lerp(MY, MY + 40, q)
    microwave(img, ox, oy, s, t, True, display=f"0:{max(0, 30 - int(t)):02d}")
    if t > a1 + 0.8:
        p = clamp((t - a1 - 0.8) / 1.4)
        x0, y0 = mw_pos(ox, oy, s, WIN[0], WIN[1])
        x1, y1 = mw_pos(ox, oy, s, WIN[2], WIN[3])
        band = Image.new("RGBA", (int(x1 - x0), int(y1 - y0)), (0, 0, 0, 0))
        dd = ImageDraw.Draw(band)
        bx = lerp(-300, band.size[0] + 300, p)
        dd.polygon([(bx, 0), (bx + 120, 0), (bx - 80, band.size[1]), (bx - 200, band.size[1])], fill=(255, 255, 255, 60))
        AC(img, band.filter(ImageFilter.GaussianBlur(10)), (x0, y0))
    top_shade(img)
    title2(t, 0.3, "¿CÓMO FUNCIONA", "UN MICROONDAS?", 250, 58, 92, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def mag_cut(img, t, T, L):
    kitchen(img)
    overlay(img, (6, 10, 20), 0.6)
    q = ease(clamp(t / 1.8))
    s = lerp(1.22, 1.75, q)
    ox, oy = lerp(600, 540 - 293 * 1.75, q), lerp(MY + 40, 820, q)
    g = ease(clamp((t - 0.7) / 0.9))
    microwave(img, ox, oy, s, t, True, guts=g, display="")
    if 0.5 < t < 1.9:
        px0, _ = mw_pos(ox, oy, s, 610, 0)
        px1, _ = mw_pos(ox, oy, s, 796, 0)
        x = lerp(px0, px1, clamp((t - 0.5) / 1.4))
        _, y0 = mw_pos(ox, oy, s, 0, 30)
        _, y1 = mw_pos(ox, oy, s, 0, 458)
        glow_line(img, [(x, y0), (x, y1)], (120, 230, 255), 4, 12, 200)
    if g > 0.8:
        mx, my = mw_pos(ox, oy, s, 700, 170)
        callout(img, t, 1.7, mx + 60, my, 900, my - 160, "MAGNETRÓN", YEL, 44)
        wx, wy = mw_pos(ox, oy, s, 560, 60)
        callout(img, t, 2.3, wx, wy, 260, wy - 110, "GUÍA DE ONDAS", (140, 220, 255), 36)
        tx, ty = mw_pos(ox, oy, s, 732, 370)
        callout(img, t, 2.8, tx + 50, ty, 900, ty + 200, "TRANSFORMADOR", (220, 220, 230), 34)


def mag_xsec(img, t, T, L):
    a2 = L[2][0]
    sky(img, (10, 14, 26), (4, 6, 10), 1.0)
    cx, cy, s = 540, 880, 0.9
    if t > a2:
        k = ease(clamp((t - a2) / 0.6))
        for i in range(5):
            rr = ((t - a2) * 300 + i * 130) % 650
            al = int(200 * k * (1 - rr / 650))
            if al > 4:
                d = ImageDraw.Draw(img, "RGBA")
                d.arc([cx - rr - 360, cy - 360 - rr - 30, cx + rr + 360, cy - 360 + rr + 30], 200, 340, fill=YEL + (al,), width=8)
    paste(img, spr(magnetron_xsec), cx, cy, s)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        hx, hy = cx + math.cos(a) * 228 * s, cy + math.sin(a) * 228 * s
        if t > a2:
            pul = 0.5 + 0.5 * math.sin(t * 9 + k * math.pi)
            paste(img, glow(120, (255, 200, 120), 0.8), hx, hy, 1.0, ease(clamp((t - a2) / 0.5)) * (0.4 + 0.6 * pul))
    w = 1.7
    for k in range(4):
        for j in range(17):
            r = 46 + j * 5.8
            ang = w * t + k * math.pi / 2 + (r - 46) / 98 * 1.1
            x, y = cx + math.cos(ang) * r * s, cy + math.sin(ang) * r * s
            paste(img, glow(22 + j, BLUE_, 1.0), x, y, 1.0, 0.95)
    rr_ = random.Random(4)
    for i in range(36):
        r = rr_.uniform(48, 140)
        ang = rr_.uniform(0, 6.28) + t * rr_.uniform(1.5, 3.0)
        paste(img, glow(14, (200, 230, 255), 1.0), cx + math.cos(ang) * r * s, cy + math.sin(ang) * r * s, 1.0, 0.7)
    callout(img, t, 0.6, cx, cy, 250, cy + 470, "CÁTODO", (255, 190, 120), 34)
    callout(img, t, 1.1, cx + 330 * s * 0.75, cy - 330 * s * 0.75, 900, 560, "IMÁN", (220, 220, 230), 36)
    if t > a2:
        a = math.pi / 8
        callout(img, t, a2 + 0.5, cx + math.cos(a) * 228 * s, cy + math.sin(a) * 228 * s, 860, cy + 470, "CAVIDADES", YEL, 34)


def sh_magnetron(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    xf(img, t, a1, lambda im: mag_cut(im, t, T, L), lambda im: mag_xsec(im, t - a1 + 0.3, T, [(l0 - a1 + 0.3, l1 - a1 + 0.3) for l0, l1 in L]), 0.7)
    if t < a1:
        pass
    elif t < a2:
        big(t, a1 + 0.3, "ELECTRONES", 290, 96, BLUE_, sub="ATRAPADOS POR UN IMÁN")
    else:
        big(t, a2 + 0.4, "MICROONDAS", 300, 110, YEL)
    vignette(img, 200)


def wave_a(img, t, T, L):
    sky(img, (12, 16, 30), (30, 26, 40), 1.1)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 8), width=1)
    d.rectangle([0, 1130, 620, 1170], fill=(110, 76, 48))
    d.rectangle([0, 1170, 620, 1180], fill=(60, 40, 26))
    paste(img, spr(router), 300, 990, 1.0)
    for i in range(3):
        ph = (t * 1.2 - i * 0.25) % 1.0
        al = int(200 * math.sin(math.pi * ph))
        r = 70 + i * 55
        d = ImageDraw.Draw(img, "RGBA")
        d.arc([300 - r, 830 - r, 300 + r, 830 + r], 225, 315, fill=(140, 220, 255, al), width=10)
    ph = t * 7
    pts = [(x, 640 + math.sin(x / 360 * 2 * math.pi - ph) * 120) for x in range(-20, W + 30, 8)]
    glow_line(img, pts, YEL, 7, 14, 230)
    spaced(ImageDraw.Draw(img, "RGBA"), 300, 1210, "WIFI · 2,4 GHZ", f(F_SER, 36), (200, 230, 255, 220), 5)


def wave_b(img, t, T, L, t0):
    AC(img, cached("cavity_big", _cavity_big))
    paste(img, spr(bowl, int(t * 3) % 12), 540, 1170, 1.6)
    paths = [[(944, 570), (150, 840), (540, 1150)], [(944, 570), (600, 440), (300, 1250), (520, 1160)], [(944, 570), (860, 1240), (580, 1150)]]
    for i, P_ in enumerate(paths):
        prog = clamp((t - t0 - 0.2 - i * 0.35) / 1.6)
        if prog > 0:
            glow_line(img, wavy(P_, prog, 18, 90, t * 14), YEL, 5, 10, 220)
    hit = clamp((t - t0 - 1.6) / 1.0)
    if hit > 0:
        paste(img, glow(260, (255, 170, 80), 0.6), 540, 1130, 1.0, hit * (0.7 + 0.3 * math.sin(t * 8)))
    callout(img, t, t0 + 0.6, 944, 570, 820, 380, "GUÍA DE ONDAS", (140, 220, 255), 38)
    smoke(img, t, [(540, 1100, 0.6)], col=(255, 240, 220), alpha=50, spread=(80, 20), grow=60, speed=0.6)


def sh_wave(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: wave_a(im, t, T, L), lambda im: wave_b(im, t, T, L, a1), 0.7)
    if t < a1:
        big(t, 0.3, "ONDAS DE RADIO", 300, 80, WHITE, hold=1.6, pop=False)
        if t > 2.4:
            n = counter(t, 2.5, a1 - 0.4, 0, 2450000000)
            big(t, 2.4, n, 320, 96, YEL, sub="VECES POR SEGUNDO", pop=False)
    vignette(img, 200)


def mol_field(img, t, n=14, seed=3, area=(0, 0, W, H), s=0.32, speed=40, rot=True, alpha=1.0):
    rr = random.Random(seed)
    m = spr(water_mol)
    for i in range(n):
        x = area[0] + (rr.uniform(0, 1) * (area[2] - area[0]) + t * rr.uniform(-1, 1) * speed) % (area[2] - area[0])
        y = area[1] + (rr.uniform(0, 1) * (area[3] - area[1]) + t * rr.uniform(-1, 1) * speed) % (area[3] - area[1])
        ang = rr.uniform(0, 360) + (t * rr.uniform(-60, 60) if rot else 0)
        paste(img, m, x, y, s * rr.uniform(0.8, 1.2), alpha, ang)


def water_a(img, t, T, L):
    kb = cached("kitchen_blur", lambda: Image.alpha_composite(cached(("kitchen", True), lambda: _kitchen(True)),
                                                               Image.new("RGBA", (W, H), (0, 0, 0, 140))).filter(ImageFilter.GaussianBlur(22)))
    AC(img, kb)
    paste(img, glow(600, (255, 170, 90), 0.35), 540, 1000)
    paste(img, spr(bowl, int(t * 2) % 12), 540, 1080, 2.8)
    smoke(img, t, [(440, 900, 0.8), (640, 900, 0.8)], col=(255, 244, 230), alpha=50, spread=(120, 30), grow=90, speed=0.5)
    k = ease(clamp((t - 0.4) / 1.0))
    cx, cy = lerp(1300, 560, k), lerp(600, 800, k)
    r = 230
    lens = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    lens.paste(vgrad("lensw", (40, 100, 170), (16, 50, 110), 1.0, 2 * r, 2 * r), (0, 0))
    tmp = Image.new("RGB", (2 * r, 2 * r))
    tmp.paste(lens.convert("RGB"))
    mol_field(tmp, t, 11, 5, (0, 0, 2 * r, 2 * r), 0.36, 30)
    m = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 2 * r, 2 * r], fill=255)
    lens = tmp.convert("RGBA")
    lens.putalpha(m)
    AC(img, lens, (cx - r, cy - r))
    paste(img, spr(magnifier, r), cx, cy + 100, 1.0)


def water_b(img, t, T, L, t0):
    sky(img, (10, 30, 70), (4, 10, 26), 1.0)
    mol_field(img, t, 16, 9, (0, 300, W, 1500), 0.3, 25, True, 0.25)
    cx, cy = 540, 860 + math.sin(t * 1.4) * 10
    k1 = ease(clamp((t - t0 - 0.6) / 0.6))
    k2 = ease(clamp((t - t0 - 2.0) / 0.6))
    paste(img, glow(420, (90, 140, 255), 0.55), cx, cy - 70, 1.0, k1)
    paste(img, glow(260, (255, 90, 90), 0.5), cx - 184, cy + 150, 1.0, k2)
    paste(img, glow(260, (255, 90, 90), 0.5), cx + 184, cy + 150, 1.0, k2)
    paste(img, spr(water_mol), cx, cy, 2.0)
    d = ImageDraw.Draw(img, "RGBA")

    def badge(x, y, sym, col, k):
        if k <= 0:
            return
        rad = 54 * (0.6 + 0.4 * k)
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=col + (int(235 * k),), outline=(255, 255, 255, int(255 * k)), width=5)
        d.text((x, y - 4), sym, font=f(F_CAP, int(76 * (0.6 + 0.4 * k))), fill=(255, 255, 255, int(255 * k)), anchor="mm")
    badge(cx, cy - 330, "−", (40, 90, 220), k1)
    badge(cx - 300, cy + 300, "+", (220, 50, 50), k2)
    badge(cx + 300, cy + 300, "+", (220, 50, 50), k2)
    spaced(d, cx, cy - 470, "OXÍGENO", f(F_SER, 40), (200, 220, 255, int(230 * k1)), 6)
    spaced(d, cx, cy + 400, "HIDRÓGENO", f(F_SER, 40), (255, 210, 210, int(230 * k2)), 6)


def sh_water(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: water_a(im, t, T, L), lambda im: water_b(im, t, T, L, a1), 0.7)
    if t < a1:
        big(t, 0.9, "AGUA", 300, 130, BLUE_)
    vignette(img, 200)


def sh_spin(img, t, T, L):
    a1 = L[1][0]
    heat = ease(clamp((t - a1 - 0.3) / 2.4))
    sky(img, (14, 18, 34), (6, 8, 14), 1.0)
    overlay(img, (255, 110, 40), 0.32 * heat)
    E = math.sin(2 * math.pi * 0.85 * t)
    d = ImageDraw.Draw(img, "RGBA")
    for yb, sgn in ((520, 1), (1240, -1)):
        pol = sgn * E
        col = (lerp(60, 230, (pol + 1) / 2), 60, lerp(230, 60, (pol + 1) / 2))
        col = tuple(int(v) for v in col)
        d.rounded_rectangle([60, yb - 22, W - 60, yb + 22], radius=14, fill=col + (240,))
        d.rounded_rectangle([64, yb - 18, W - 64, yb - 10], radius=6, fill=(255, 255, 255, 50))
        sym = "+" if pol > 0 else "−"
        for x in range(160, W - 100, 190):
            d.text((x, yb - 3), sym, font=f(F_CAP, 40), fill=(255, 255, 255, 230), anchor="mm")
    for x in range(110, W, 216):
        for y0 in (580, 900):
            al = int(70 * abs(E))
            if E > 0:
                d.line([(x, y0), (x, y0 + 260)], fill=(255, 255, 255, al), width=3)
                d.polygon([(x - 10, y0 + 240), (x + 10, y0 + 240), (x, y0 + 262)], fill=(255, 255, 255, al))
            else:
                d.line([(x, y0 + 262), (x, y0)], fill=(255, 255, 255, al), width=3)
                d.polygon([(x - 10, y0 + 22), (x + 10, y0 + 22), (x, y0)], fill=(255, 255, 255, al))
    m = spr(water_mol)
    rr = random.Random(7)
    jit = 4 + 26 * heat
    for i, x in enumerate((210, 437, 663, 890)):
        for j, y in enumerate((660, 820, 980, 1140)):
            lag = rr.uniform(0, 0.25)
            e = math.sin(2 * math.pi * 0.85 * (t - lag))
            ang = 90 * (1 - math.tanh(2.6 * e) / math.tanh(2.6)) + rr.uniform(-12, 12) + math.sin(t * 13 + i * 3 + j) * jit * 0.8
            dx = math.sin(t * 11 + i * 1.7 + j * 2.3) * jit
            dy = math.cos(t * 9.4 + i * 2.1 + j * 1.3) * jit
            paste(img, m, x + dx, y + dy, 0.52, 1.0, ang)
    if heat > 0.05:
        for i in range(6):
            ph = (t * 2.2 + i * 0.37) % 1.0
            if ph < 0.25:
                x = 320 + (i * 157) % 460
                y = 740 + (i * 211) % 320
                paste(img, glow(90, (255, 230, 160), 1.0), x, y, 1.0, heat * math.sin(math.pi * ph / 0.25))
    if t < a1:
        big(t, 0.3, "A UN LADO… Y A OTRO", 300, 74, WHITE, pop=False)
    else:
        big(t, a1 + 1.4, "ROCE = CALOR", 300, 104, ORANGE)
    vignette(img, 200)


def sh_ice(img, t, T, L):
    sky(img, (150, 200, 240), (30, 70, 130), 1.1)
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(2)
    for i in range(16):
        x, y = rr.uniform(0, W), rr.uniform(300, 1500)
        r = rr.uniform(120, 300)
        pts = [(x + math.cos(a) * r, y + math.sin(a) * r * 0.8) for a in [rr.uniform(0, 6.28) for _ in range(5)]]
        pts.sort(key=lambda p: math.atan2(p[1] - y, p[0] - x))
        d.polygon(pts, fill=(255, 255, 255, rr.randint(8, 22)))
    pos = []
    for r_ in range(7):
        for c_ in range(6):
            pos.append((150 + c_ * 160 + (r_ % 2) * 80, 560 + r_ * 128))
    for i, (x, y) in enumerate(pos):
        for x2, y2 in pos[i + 1:]:
            if math.hypot(x2 - x, y2 - y) < 170:
                n = 8
                for k in range(n):
                    if k % 2 == 0:
                        d.line([(lerp(x, x2, k / n), lerp(y, y2, k / n)), (lerp(x, x2, (k + 1) / n), lerp(y, y2, (k + 1) / n))],
                               fill=(255, 255, 255, 150), width=4)
    m = spr(water_mol)
    for i, (x, y) in enumerate(pos):
        base = (i * 67) % 360
        ang = base + math.sin(t * 9 + i) * 5
        paste(img, m, x, y, 0.38, 1.0, ang)
    overlay(img, (180, 220, 255), 0.12)
    particles(img, t, 40, 6, (255, 255, 255), 30, (1.5, 3.0), 160, 20)
    big(t, 0.3, "HIELO", 270, 110, WHITE, sub="CASI NO PUEDEN GIRAR", subcol=(230, 240, 255))
    vignette(img, 170)


def sh_depth(img, t, T, L):
    sky(img, (34, 26, 22), (10, 8, 8), 1.0)
    paste(img, glow(700, (255, 160, 80), 0.25), 540, 900)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([60, 1050, 1020, 1210], fill=(230, 228, 222, 255))
    d.ellipse([100, 1070, 980, 1180], fill=(244, 242, 238, 255))
    lx, ly = 540, 900
    paste(img, spr(lasagna), lx, ly, 1.0)
    hot, cold = cached("heatmap", heat_map)
    k = ease(clamp((t - 1.0) / 1.6))
    paste(img, hot, lx, ly, 1.0, k)
    paste(img, cold, lx, ly, 1.0, ease(clamp((t - 1.8) / 1.0)))
    x0, y0, x1, y1 = lx - 380, ly - 200, lx + 380, ly + 200
    pr = clamp((t - 0.3) / 1.2)
    for i in range(5):
        x = x0 + 80 + i * 150
        pts = wavy([(x, 380), (x, y0 + 46)], pr, 14, 70, t * 12)
        if pts:
            glow_line(img, pts, YEL, 4, 8, int(200 - 0 * i))
    for yy in (y0 + 90, y0 + 250):
        for xs, xe in ((60, x0 + 46), (W - 60, x1 - 46)):
            pts = wavy([(xs, yy), (xe, yy)], pr, 14, 70, t * 12)
            if pts:
                glow_line(img, pts, YEL, 4, 8, 200)
    if t > 2.0:
        kk = ease(clamp((t - 2.0) / 0.5))
        dd = ImageDraw.Draw(img, "RGBA")
        bx = x1 + 34
        dd.line([(bx, y0), (bx, y0 + 70)], fill=(255, 255, 255, int(255 * kk)), width=5)
        for yy in (y0, y0 + 70):
            dd.line([(bx - 14, yy), (bx + 14, yy)], fill=(255, 255, 255, int(255 * kk)), width=5)
        spaced(dd, bx - 50, y0 - 70, "≈ 2 CM", f(F_SER, 44), (255, 255, 255, int(255 * kk)), 4)
    big(t, 0.4, "UN PAR DE CM", 290, 100, YEL, sub="NO DE DENTRO A FUERA")
    vignette(img, 200)


def sh_hotspots(img, t, T, L):
    sky(img, (40, 40, 44), (14, 14, 16), 1.0)
    cx, cy = 540, 880
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([cx - 450, cy - 450, cx + 450, cy + 450], radius=20, fill=(70, 70, 76))
    d.rounded_rectangle([cx - 430, cy - 430, cx + 430, cy + 430], radius=14, fill=(110, 110, 116))
    t_rot = 1.9
    ang = 0 if t < t_rot else -(t - t_rot) ** 1.3 * 50
    d.ellipse([cx - 340, cy - 340, cx + 340, cy + 340], fill=(200, 220, 230, 90), outline=(255, 255, 255, 140), width=5)
    paste(img, spr(chocolate), cx, cy, 1.0, 1.0, ang)
    paste(img, cached("thermal", thermal), cx, cy, 1.0, 0.55)
    if t > t_rot:
        k = ease(clamp((t - t_rot) / 0.5))
        dd = ImageDraw.Draw(img, "RGBA")
        a0 = (t * 60) % 360
        for off in (0, 180):
            dd.arc([cx - 390, cy - 390, cx + 390, cy + 390], a0 + off, a0 + off + 110, fill=(255, 255, 255, int(230 * k)), width=10)
            aa = math.radians(a0 + off + 110)
            hx, hy = cx + math.cos(aa) * 390, cy + math.sin(aa) * 390
            tx, ty = -math.sin(aa), math.cos(aa)
            dd.polygon([(hx + tx * 30, hy + ty * 30), (hx - ty * 22, hy + tx * 22), (hx + ty * 22, hy - tx * 22)], fill=(255, 255, 255, int(230 * k)))
    if t < t_rot:
        big(t, 0.3, "ZONAS CALIENTES", 270, 84, (255, 120, 80), sub="Y ZONAS FRÍAS", subcol=(140, 200, 255), pop=False)
    else:
        big(t, t_rot + 0.1, "POR ESO GIRA", 290, 104, YEL)
    vignette(img, 190)


def mesh_zoom(img, t, a1):
    kitchen(img)
    q = ease(clamp(t / max(0.5, a1)))
    s = lerp(1.22, 3.4, q)
    ox, oy = 540 - (309 - 410) * s, 860 - (245 - 250) * s
    microwave(img, ox, oy, s, t, True, display="")
    top_shade(img)


def mesh_front(img, t, t0):
    AC(img, vgrad("meshbg", (255, 210, 140), (190, 120, 50), 1.0))
    paste(img, glow(700, (255, 240, 200), 0.6), 540, 860)
    paste(img, spr(bowl, 0), 560, 1050, 3.0, 0.6)
    s = lerp(1.0, 1.06, clamp((t - t0) / 3.0))
    mm = cached("mesh_macro", _mesh_macro)
    paste(img, mm, 540, 860, s)
    top_shade(img, 200, 640)
    k = ease(clamp((t - t0 - 0.6) / 0.5))
    if k > 0:
        dd = ImageDraw.Draw(img, "RGBA")
        hx, hy = 540, 860
        r = 30 * s
        dd.ellipse([hx - r - 6, hy - r - 6, hx + r + 6, hy + r + 6], outline=YEL + (int(255 * k),), width=5)
        dd.line([(hx - r, hy - 90), (hx + r, hy - 90)], fill=(255, 255, 255, int(255 * k)), width=5)
        for x in (hx - r, hx + r):
            dd.line([(x, hy - 106), (x, hy - 74)], fill=(255, 255, 255, int(255 * k)), width=5)


def side_view(img, t, wave_k, light_k, t_l):
    sky(img, (30, 22, 16), (12, 10, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 420, 640, 1300], fill=(70, 50, 30, 255))
    AC(img, vgrad("sv_in", (230, 180, 110), (150, 100, 50), 1.0, 880, 640), (0, 420))
    paste(img, glow(400, (255, 230, 180), 0.6), 280, 640)
    paste(img, spr(bowl, int(t * 3) % 12), 290, 1170, 1.4)
    dx = 640
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(420, 1300, 44):
        d.rectangle([dx, y + 10, dx + 26, y + 44], fill=(60, 62, 70, 255))
        d.rectangle([dx, y + 10, dx + 6, y + 44], fill=(140, 144, 154, 255))
    d.rectangle([dx + 44, 400, dx + 56, 1320], fill=(200, 230, 255, 70))
    d.rectangle([dx - 30, 380, dx + 80, 420], fill=(150, 154, 164, 255))
    d.rectangle([dx - 30, 1300, dx + 80, 1340], fill=(150, 154, 164, 255))
    if wave_k > 0:
        ph = t * 6
        pts = [(x, 840 + math.sin(x / 520 * 2 * math.pi - ph) * 150 * (0.5 + 0.5 * min(1, x / 300))) for x in range(20, dx - 4, 8)]
        glow_line(img, pts, YEL, 8, 14, int(230 * wave_k))
        dd = ImageDraw.Draw(img, "RGBA")
        A = int(255 * wave_k)
        dd.line([(60, 560), (580, 560)], fill=(255, 255, 255, A), width=4)
        for xx in (60, 580):
            dd.line([(xx, 544), (xx, 576)], fill=(255, 255, 255, A), width=4)
        spaced(dd, 320, 500, "12 CM", f(F_SER, 46), (255, 255, 255, A), 5)
        for i in range(3):
            y = 760 + i * 80
            dd.line([(dx - 20, y), (dx - 90, y - 40)], fill=(255, 120, 80, A), width=6)
            dd.polygon([(dx - 98, y - 46), (dx - 70, y - 44), (dx - 86, y - 22)], fill=(255, 120, 80, A))
    if light_k > 0:
        for i, y in enumerate(range(474, 1250, 88)):
            pr = clamp((t - t_l - i * 0.06) / 0.9)
            if pr <= 0:
                continue
            x_end = lerp(320, 930, pr)
            gy = y + 5
            pts = []
            for x in range(320, int(x_end), 4):
                if x < dx:
                    yy = lerp(1000, gy, (x - 320) / (dx - 320))
                else:
                    yy = lerp(gy, 860, (x - dx) / (930 - dx))
                pts.append((x, yy + math.sin(x / 14 - t * 30) * 3))
            if len(pts) > 2:
                glow_line(img, pts, (255, 250, 200), 3, 6, int(200 * light_k))
        paste(img, spr(eye), 940, 860, 0.8, light_k)


def sh_mesh(img, t, T, L):
    a1, a2, a3 = L[1][0], L[2][0], L[3][0]

    def A(im):
        if t < a1 + 0.35:
            mesh_zoom(im, t, a1)
        else:
            mesh_front(im, t, a1)

    def B(im):
        side_view(im, t, ease(clamp((t - a2 - 0.2) / 0.6)) * (1 - 0.6 * ease(clamp((t - a3) / 0.6))), ease(clamp((t - a3) / 0.4)), a3 + 0.2)

    if t < a2 - 0.4:
        xf(img, t, a1, lambda im: mesh_zoom(im, t, a1), lambda im: mesh_front(im, t, a1), 0.6)
    else:
        xf(img, t, a2, A, B, 0.7)
    if t < a1:
        big(t, 0.2, "¿Y LA REJILLA?", 300, 96, WHITE)
    elif t < a2:
        big(t, a1 + 0.7, "≈ 1 MM", 300, 120, YEL, sub="CADA AGUJERO")
    elif t < a3:
        big(t, a2 + 0.6, "NO CABEN", 290, 110, (255, 120, 80))
    else:
        big(t, a3 + 0.4, "LA LUZ SÍ PASA", 290, 96, (255, 240, 180))
    vignette(img, 200)


def sh_spencer(img, t, T, L):
    a1 = L[1][0]
    AC(img, cached("lab", _lab))
    rays(img, t, 300, 300, 10, (255, 230, 170), 26, 1500, 0.07, 0.02)
    pul = 0.6 + 0.4 * math.sin(t * 5)
    paste(img, glow(240, (255, 170, 90), 0.5), 590, 1050, 1.0, pul)
    paste(img, spr(person, 200, 520, (34, 28, 22), None, True, False, 0.9), 330, 1060, 1.5)
    px, py = 330 + 26 * 1.5, 1060 + (230 - 260) * 1.5
    k = ease(clamp((t - 2.2) / 0.6))
    melt = clamp((t - 2.6) / 4.0)
    if k > 0:
        ix, iy = 760, 560
        dd = ImageDraw.Draw(img, "RGBA")
        dd.line([(px, py), (ix - 120, iy + 120)], fill=(240, 220, 180, int(220 * k)), width=4)
        dd.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(240, 220, 180, int(255 * k)))
        paste(img, melt_inset(t, round(melt * 20) / 20), ix, iy, lerp(0.6, 1.0, k), k)
    sepia(img, 0.5)
    date_stamp(t, 0.4, "AÑOS 40 · EE. UU.", 250, hold=max(1.8, 2.0))
    lower_third(img, t, 2.8, "PERCY SPENCER", "INGENIERO DE RAYTHEON", 250, max(1.5, a1 - 3.2))
    if t > a1:
        big(t, a1 + 0.2, "UN ACCIDENTE", 290, 110, YEL, hold=max(1.6, T - a1 - 0.8))
    vignette(img, 220)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "warm"), ("magnetron", "mystery"), ("water", "creative"), ("ice", "space"), ("mesh", "playful"),
              ("spencer", "noir")],
    "gains": {"mystery": 0.8},
    "amb": {"hum": ["open", "magnetron", "wave", "spin", "hotspots"], "room": ["spencer"]},
    "sfx": [("open+0.2", "hum_on", 0.2), ("open@L1+0.8", "whoosh", 0.1), ("open@L1+1.2", "ding", 0.06),
            ("magnetron+0.5", "riser", 0.1), ("magnetron+0.8", "glitch", 0.08), ("magnetron+1.7", "pop", 0.18), ("magnetron+2.3", "pop", 0.14),
            ("magnetron@L1", "whoosh", 0.14), ("magnetron@L1+0.3", "zap", 0.1), ("magnetron@L2+0.3", "whoosh_up", 0.14), ("magnetron@L2+0.4", "hum_on", 0.12),
            ("wave+0.2", "whoosh", 0.12), ("wave+2.4", "riser", 0.1), ("wave@L1", "whoosh", 0.14), ("wave@L1+1.6", "swell", 0.12),
            ("water+0.4", "whoosh", 0.1), ("water+0.9", "pop", 0.2), ("water@L1+0.6", "blip_down", 0.14), ("water@L1+2.0", "blip", 0.14),
            ("spin+0.3", "click", 0.3), ("spin+0.9", "click", 0.3), ("spin+1.5", "click", 0.3), ("spin@L1+1.4", "swell", 0.18),
            ("ice+0.2", "chime", 0.06), ("ice+0.3", "glitch", 0.06), ("depth+0.3", "whoosh", 0.12), ("depth+2.0", "tick", 0.15),
            ("hotspots+0.3", "blip", 0.12), ("hotspots+1.9", "whoosh_up", 0.12),
            ("mesh+0.1", "whoosh_up", 0.15), ("mesh@L1+0.6", "tick", 0.2), ("mesh@L2+0.4", "thud", 0.25), ("mesh@L3+0.3", "chime", 0.06),
            ("spencer+0.3", "paper", 0.15), ("spencer+2.2", "pop", 0.14), ("spencer@L1+0.2", "ding", 0.1), ("spencer@L1+0.4", "swell", 0.12)],
    "bed": [("magnetron", "wave"), ("spin", "hotspots")],
    "bpm": 96,
}
