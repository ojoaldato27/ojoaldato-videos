"""Piezas planas para el estilo 7 «minimal blanco» (líneas negras, acento rojo): barco, iceberg, llave, prismáticos,
campana, bolsillo, mazo de subasta, Marte, Fobos, nave, rover, cápsula con paracaídas, Australia… (21/10/2026)."""
import math
from PIL import Image, ImageDraw
import flat3 as FL
from flat3 import W, H, F
from render import ease, clamp, lerp

INK, RED, SOFT = (28, 28, 32), (230, 40, 40), (160, 160, 168)
PALE = (232, 232, 236)
WATER = (224, 236, 248)
ICE = (238, 246, 252)
BUFF = (236, 190, 110)
MARS, MARS_D = (222, 110, 70), (176, 74, 48)
PHOB, PHOB_D = (150, 140, 132), (104, 96, 90)


def D(img):
    return ImageDraw.Draw(img, "RGBA")


def txt(img, xy, s, size, col=INK, anchor="mm", font=None):
    D(img).text(xy, s, font=F(font or FL.INTER_X, size), fill=col, anchor=anchor)


def _tf(pts, cx, cy, s, a=0.0, flip=1):
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        x *= flip
        out.append((cx + (x * ca - y * sa) * s, cy + (x * sa + y * ca) * s))
    return out


# ------------------------------------------------------------------ mar
def water(img, y, t=0.0, x0=0, x1=W, y1=1150, waves=3):
    d = D(img)
    d.rectangle([x0, y, x1, y1], fill=WATER)
    for k in range(waves):
        yy = y + 30 + k * 70
        pts = [(x, yy + 8 * math.sin(x / 60 + t * 2 + k)) for x in range(int(x0), int(x1) + 20, 20)]
        d.line(pts, fill=(190, 206, 224), width=4)
    d.line([(x0, y), (x1, y)], fill=INK, width=5)


def ship(img, cx, cy, s=1.0, a=0.0, flip=1, lights=False):
    """Titanic de lado (proa a la derecha si flip=1), con la línea de flotación en (cx, cy)."""
    d = D(img)
    T = lambda p: _tf(p, cx, cy, s, a, flip)
    lw = max(3, int(5 * s))
    for mx, top in ((-250, -270), (255, -262)):
        d.line(T([(mx, -76), (mx - 10, top)]), fill=INK, width=max(2, int(4 * s)))
    nest = T([(244, -205), (266, -205), (264, -190), (246, -190)])
    d.polygon(nest, fill=INK)
    d.line(T([(-260, -262), (-150, -150)]) , fill=SOFT, width=max(1, int(2 * s)))
    d.line(T([(250, -255), (150, -150)]), fill=SOFT, width=max(1, int(2 * s)))
    for fx in (-140, -62, 16, 94):
        d.polygon(T([(fx - 18, -134), (fx + 18, -134), (fx + 5, -222), (fx - 31, -222)]), fill=BUFF, outline=INK, width=lw - 1)
        d.polygon(T([(fx - 29, -208), (fx + 7, -208), (fx + 5, -222), (fx - 31, -222)]), fill=INK)
    d.polygon(T([(-190, -136), (170, -136), (170, -110), (-190, -110)]), fill=(255, 255, 255), outline=INK, width=lw - 1)
    d.polygon(T([(-232, -112), (214, -112), (214, -76), (-232, -76)]), fill=(255, 255, 255), outline=INK, width=lw - 1)
    for k in range(-210, 200, 26):
        d.polygon(T([(k, -100), (k + 12, -100), (k + 12, -90), (k, -90)]), fill=(250, 214, 110) if lights else INK)
    d.polygon(T([(-305, -78), (338, -84), (302, 6), (-282, 6)]), fill=INK)
    d.polygon(T([(-288, -6), (306, -6), (302, 6), (-282, 6)]), fill=RED)
    for k in range(-250, 280, 34):
        p = T([(k, -44)])[0]
        r = 3.5 * s
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=(250, 214, 110) if lights else (255, 255, 255))


def iceberg(img, cx, cy, s=1.0, k=1.0, under=True):
    if k <= 0:
        return
    d = D(img)
    a = int(255 * clamp(k))
    top = [(-160, 0), (-120, -90), (-70, -120), (-30, -210), (20, -180), (60, -240), (110, -140), (150, -80), (175, 0)]
    pts = [(cx + x * s, cy + y * s) for x, y in top]
    d.polygon(pts, fill=ICE + (a,), outline=INK + (a,), width=max(3, int(5 * s)))
    d.line([(cx - 30 * s, cy - 210 * s), (cx - 10 * s, cy - 60 * s)], fill=(200, 214, 230, a), width=max(2, int(4 * s)))
    if under:
        bot = [(-160, 0), (-230, 90), (-150, 220), (60, 260), (230, 150), (175, 0)]
        d.polygon([(cx + x * s, cy + y * s) for x, y in bot], fill=(210, 226, 244, int(a * 0.8)))


# ------------------------------------------------------------------ objetos
def key(img, cx, cy, s=1.0, a=0.0, col=INK, tag=True):
    lay = Image.new("RGBA", (int(520 * s) + 4, int(260 * s) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    o = lambda x, y: (x * s + 2, y * s + 2)
    r = 70
    d.ellipse([*o(10, 130 - r), *o(10 + 2 * r, 130 + r)], outline=col, width=int(26 * s))
    d.ellipse([*o(48, 130 - 32), *o(48 + 64, 130 + 32)], outline=col, width=int(8 * s))
    d.rectangle([*o(140, 118), *o(470, 142)], fill=col)
    for x0, h in ((400, 60), (440, 40), (360, 46)):
        d.rectangle([*o(x0, 142), *o(x0 + 26, 142 + h)], fill=col)
    if tag:
        d.line([o(40, 70), o(20, 20)], fill=col, width=int(5 * s))
        d.rounded_rectangle([*o(0, -10 + 12), *o(70, 30)], radius=int(8 * s), fill=RED)
    lay = lay.rotate(math.degrees(-a), expand=True, resample=Image.BICUBIC)
    img.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)), lay)


def binoculars(img, cx, cy, s=1.0, col=INK, view=None):
    d = D(img)
    for sx in (-1, 1):
        x = cx + sx * 80 * s
        d.rounded_rectangle([x - 62 * s, cy - 130 * s, x + 62 * s, cy + 60 * s], radius=int(30 * s), fill=col)
        d.ellipse([x - 70 * s, cy + 20 * s, x + 70 * s, cy + 150 * s], fill=col)
        d.ellipse([x - 50 * s, cy + 40 * s, x + 50 * s, cy + 130 * s], fill=view or (120, 150, 190))
    d.rectangle([cx - 30 * s, cy - 60 * s, cx + 30 * s, cy - 10 * s], fill=col)


def bell(img, cx, cy, s=1.0, ang=0.0):
    """Campana colgada de (cx, cy), que se balancea ang grados."""
    S = int(640 * s)
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    px, py = S / 2, 40 * s
    o = lambda x, y: (px + x * s, py + y * s)
    G = (214, 170, 70)
    d.rectangle([*o(-12, -40), *o(12, 30)], fill=INK)
    d.pieslice([*o(-95, 20), *o(95, 200)], 180, 360, fill=G, outline=INK, width=int(6 * s))
    d.polygon([o(-95, 110), o(95, 110), o(140, 290), o(-140, 290)], fill=G)
    d.line([o(-95, 110), o(-140, 290)], fill=INK, width=int(6 * s))
    d.line([o(95, 110), o(140, 290)], fill=INK, width=int(6 * s))
    d.rectangle([*o(-150, 282), *o(150, 306)], fill=INK)
    d.ellipse([*o(-22, 300), *o(22, 348)], fill=INK)
    lay = lay.rotate(ang, center=(px, py), resample=Image.BICUBIC)
    img.paste(lay, (int(cx - px), int(cy - py)), lay)


def pocket(img, cx, cy, s=1.0):
    d = D(img)
    w, h = 300 * s, 340 * s
    d.rounded_rectangle([cx - w / 2 - 60 * s, cy - h / 2 - 80 * s, cx + w / 2 + 60 * s, cy + h / 2 + 40 * s], radius=int(30 * s), fill=(70, 86, 120))
    d.chord([cx - w / 2, cy - h / 2 - h * 0.25, cx + w / 2, cy + h / 2], 0, 180, fill=(54, 68, 98), outline=INK, width=int(6 * s))
    d.line([(cx - w / 2, cy - h * 0.17), (cx + w / 2, cy - h * 0.17)], fill=INK, width=int(8 * s))
    for k in range(12):
        x = cx - w / 2 + 14 + k * (w - 28) / 11
        d.line([(x, cy - h * 0.17 - 18 * s), (x + 8, cy - h * 0.17 - 18 * s)], fill=(230, 200, 120), width=int(3 * s))


def gavel(img, cx, cy, s=1.0, ang=0.0):
    lay = Image.new("RGBA", (int(420 * s), int(420 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    o = lambda x, y: (x * s, y * s)
    d.rounded_rectangle([*o(195, 120), *o(225, 400)], radius=int(10 * s), fill=(150, 96, 50), outline=INK, width=int(5 * s))
    d.rounded_rectangle([*o(110, 50), *o(310, 140)], radius=int(16 * s), fill=(150, 96, 50), outline=INK, width=int(6 * s))
    d.rectangle([*o(110, 80), *o(310, 96)], fill=(214, 170, 70))
    lay = lay.rotate(ang, center=(210 * s, 400 * s), resample=Image.BICUBIC)
    img.paste(lay, (int(cx - 210 * s), int(cy - 400 * s)), lay)


def stick(img, x, y, s=1.0, col=INK, arm=0.0):
    d = D(img)
    lw = max(3, int(7 * s))
    d.ellipse([x - 18 * s, y - 120 * s, x + 18 * s, y - 84 * s], fill=col)
    d.line([(x, y - 84 * s), (x, y - 36 * s)], fill=col, width=lw)
    d.line([(x, y - 36 * s), (x - 16 * s, y)], fill=col, width=lw)
    d.line([(x, y - 36 * s), (x + 16 * s, y)], fill=col, width=lw)
    d.line([(x, y - 72 * s), (x - 22 * s, y - 46 * s)], fill=col, width=lw)
    d.line([(x, y - 72 * s), (x + 24 * s, y - 72 * s - 26 * s * arm)], fill=col, width=lw)


def moon_x(img, cx, cy, r, k):
    if k <= 0:
        return
    d = D(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=8)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 1.4, cy + r * 0.9], fill=FL.TH["bg"])
    q = ease(clamp(k))
    d.line([(cx - r * 1.1, cy + r * 1.1), (cx - r * 1.1 + 2.2 * r * q, cy + r * 1.1 - 2.2 * r * q)], fill=RED, width=14)


def snow(img, cx, cy, r, col=(120, 160, 210)):
    d = D(img)
    for k in range(3):
        a = k * math.pi / 3
        d.line([(cx - math.cos(a) * r, cy - math.sin(a) * r), (cx + math.cos(a) * r, cy + math.sin(a) * r)], fill=col, width=10)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=col)


def crack(img, x, y, k, s=1.0, seed=2):
    if k <= 0:
        return
    d = D(img)
    rnd = [(0.6, 0.2), (0.9, -0.4), (0.4, -0.9), (-0.5, -0.8), (-0.9, 0.1), (-0.3, 0.7), (0.5, 0.8)]
    for i, (dx, dy) in enumerate(rnd):
        L = (70 + 30 * ((i * seed) % 3)) * s * ease(clamp(k))
        mx, my = x + dx * L * 0.5 + 10 * (-1) ** i, y + dy * L * 0.5
        d.line([(x, y), (mx, my), (x + dx * L, y + dy * L)], fill=RED, width=max(4, int(8 * s)))


# ------------------------------------------------------------------ espacio
def stars(img, seed=4, n=40, y0=380, y1=1150, col=(200, 200, 206)):
    d = D(img)
    import random
    R = random.Random(seed)
    for _ in range(n):
        x, y = R.uniform(20, W - 20), R.uniform(y0, y1)
        r = R.choice((3, 4, 5))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def mars(img, cx, cy, r, rot=0.0):
    d = D(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MARS, outline=INK, width=max(4, int(r / 22)))
    for dx, dy, rr in ((-0.35, -0.2, 0.16), (0.3, 0.25, 0.12), (0.05, -0.5, 0.09), (-0.15, 0.45, 0.1), (0.5, -0.2, 0.08)):
        x = cx + ((dx + rot) % 1.6 - 0.8) * r
        if abs(x - cx) > r * 0.8:
            continue
        d.ellipse([x - rr * r, cy + dy * r - rr * r * 0.7, x + rr * r, cy + dy * r + rr * r * 0.7], fill=MARS_D)
    d.chord([cx - r * 0.42, cy - r * 0.97, cx + r * 0.42, cy - r * 0.62], 180, 360, fill=(250, 246, 240))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=max(4, int(r / 22)))


def rocket(img, x, yb, s=1.0, flame=0.0, t=0.0):
    """Cohete sencillo tipo H3 (blanco, con dos aceleradores) con la base en yb."""
    d = D(img)
    w, h = 90 * s, 520 * s
    if flame > 0:
        fl = (150 + 30 * math.sin(t * 30)) * s * flame
        d.polygon([(x - w * 0.4, yb), (x + w * 0.4, yb), (x, yb + fl)], fill=(255, 150, 60))
        d.polygon([(x - w * 0.2, yb), (x + w * 0.2, yb), (x, yb + fl * 0.6)], fill=(255, 230, 120))
    for sx in (-1, 1):
        bx = x + sx * (w / 2 + 18 * s)
        d.rounded_rectangle([bx - 18 * s, yb - h * 0.38, bx + 18 * s, yb], radius=int(14 * s), fill=(236, 236, 240), outline=INK, width=max(3, int(4 * s)))
    d.rectangle([x - w / 2, yb - h, x + w / 2, yb], fill=(250, 250, 252), outline=INK, width=max(3, int(5 * s)))
    d.polygon([(x - w / 2, yb - h), (x, yb - h - 120 * s), (x + w / 2, yb - h)], fill=(250, 250, 252), outline=INK)
    d.rectangle([x - w / 2, yb - h * 0.55, x + w / 2, yb - h * 0.48], fill=RED)
    txt(img, (x, yb - h * 0.25), "H3", int(34 * s), INK)


PHOBOS_PTS = [(-1.0, -0.05), (-0.86, -0.42), (-0.5, -0.66), (-0.05, -0.72), (0.42, -0.6), (0.8, -0.36), (1.0, 0.0),
              (0.86, 0.38), (0.5, 0.62), (0.0, 0.7), (-0.5, 0.6), (-0.86, 0.36)]


def phobos(img, cx, cy, r, ang=0.0):
    d = D(img)
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(cx + (x * ca - y * sa) * r, cy + (x * sa + y * ca) * r * 0.8) for x, y in PHOBOS_PTS]
    d.polygon(pts, fill=PHOB, outline=INK, width=max(3, int(r / 18)))
    for dx, dy, rr in ((-0.4, -0.1, 0.22), (0.35, 0.15, 0.14), (0.1, -0.38, 0.1), (-0.05, 0.3, 0.08)):
        x, y = cx + (dx * ca - dy * sa) * r, cy + (dx * sa + dy * ca) * r * 0.8
        d.ellipse([x - rr * r, y - rr * r * 0.8, x + rr * r, y + rr * r * 0.8], fill=PHOB_D, outline=INK, width=max(2, int(r / 40)))


def probe(img, cx, cy, s=1.0, ang=0.0, flame=0.0):
    """Nave MMX: cuerpo dorado con dos paneles solares y antena."""
    lay = Image.new("RGBA", (int(520 * s), int(260 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    o = lambda x, y: (x * s, y * s)
    for x0 in (10, 340):
        d.rectangle([*o(x0, 90), *o(x0 + 170, 170)], fill=(52, 78, 140), outline=INK, width=int(5 * s))
        for k in range(1, 4):
            d.line([o(x0 + k * 42, 90), o(x0 + k * 42, 170)], fill=(120, 150, 210), width=int(3 * s))
    d.rectangle([*o(180, 122), *o(340, 138)], fill=INK)
    d.rectangle([*o(205, 70), *o(315, 190)], fill=(222, 182, 80), outline=INK, width=int(6 * s))
    d.pieslice([*o(225, 20), *o(295, 80)], 180, 360, fill=(255, 255, 255), outline=INK, width=int(5 * s))
    if flame > 0:
        d.polygon([o(240, 190), o(280, 190), o(260, 190 + 60 * flame)], fill=(255, 150, 60))
    lay = lay.rotate(math.degrees(-ang), expand=True, resample=Image.BICUBIC)
    img.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)), lay)


def rover(img, cx, cy, s=1.0, t=0.0):
    d = D(img)
    d.rectangle([cx - 90 * s, cy - 70 * s, cx + 90 * s, cy - 20 * s], fill=(236, 236, 240), outline=INK, width=int(5 * s))
    d.rectangle([cx - 110 * s, cy - 100 * s, cx + 110 * s, cy - 78 * s], fill=(52, 78, 140), outline=INK, width=int(4 * s))
    d.line([(cx + 60 * s, cy - 100 * s), (cx + 70 * s, cy - 140 * s)], fill=INK, width=int(5 * s))
    d.ellipse([cx + 58 * s, cy - 156 * s, cx + 86 * s, cy - 128 * s], fill=RED)
    for wx in (-70, 0, 70):
        x = cx + wx * s
        d.ellipse([x - 24 * s, cy - 30 * s, x + 24 * s, cy + 18 * s], fill=INK)
        a = t * 6
        d.line([(x, cy - 6 * s), (x + math.cos(a) * 18 * s, cy - 6 * s + math.sin(a) * 18 * s)], fill=(200, 200, 206), width=int(4 * s))


def capsule(img, cx, cy, s=1.0, chute=1.0):
    d = D(img)
    if chute > 0:
        r = 170 * s * ease(clamp(chute))
        d.pieslice([cx - r, cy - 300 * s - r * 0.7, cx + r, cy - 300 * s + r * 0.7], 180, 360, fill=RED, outline=INK, width=int(6 * s))
        for k in (-1, -0.33, 0.33, 1):
            d.line([(cx + k * r, cy - 300 * s), (cx, cy - 40 * s)], fill=INK, width=int(3 * s))
    d.polygon([(cx - 60 * s, cy + 30 * s), (cx + 60 * s, cy + 30 * s), (cx + 30 * s, cy - 40 * s), (cx - 30 * s, cy - 40 * s)],
              fill=(236, 236, 240), outline=INK)
    d.line([(cx - 60 * s, cy + 30 * s), (cx + 60 * s, cy + 30 * s)], fill=INK, width=int(8 * s))


AUS = [(0.0, -0.62), (0.18, -0.8), (0.3, -0.55), (0.45, -0.7), (0.62, -0.5), (0.8, -0.1), (0.95, 0.2), (0.78, 0.55),
       (0.5, 0.72), (0.38, 0.6), (0.18, 0.66), (-0.1, 0.48), (-0.45, 0.55), (-0.85, 0.42), (-0.95, 0.05), (-0.8, -0.3),
       (-0.5, -0.45), (-0.25, -0.5)]


def australia(img, cx, cy, r, k=1.0):
    if k <= 0:
        return
    d = D(img)
    a = int(255 * clamp(k))
    d.polygon([(cx + x * r, cy + y * r) for x, y in AUS], fill=(236, 200, 150, a), outline=INK + (a,), width=6)


def japan_flag(img, cx, cy, w, k=1.0):
    if k <= 0:
        return
    d = D(img)
    s = FL.pop(k)
    ww, hh = w * s, w * 0.66 * s
    d.rectangle([cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2], fill=(255, 255, 255), outline=INK, width=5)
    r = hh * 0.3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 20, 40))


def orbit(img, cx, cy, rx, ry, col=SOFT, w=4, dash=True):
    d = D(img)
    n = 72
    for i in range(n):
        if dash and i % 2:
            continue
        a0, a1 = i * 2 * math.pi / n, (i + 1) * 2 * math.pi / n
        d.line([(cx + math.cos(a0) * rx, cy + math.sin(a0) * ry), (cx + math.cos(a1) * rx, cy + math.sin(a1) * ry)], fill=col, width=w)


def scale_10g(img, cx, cy, k=1.0, val="10 g"):
    d = D(img)
    d.rounded_rectangle([cx - 200, cy, cx + 200, cy + 150], radius=24, fill=(255, 255, 255), outline=INK, width=8)
    d.rounded_rectangle([cx - 120, cy + 40, cx + 120, cy + 120], radius=12, fill=(28, 34, 40))
    d.rectangle([cx - 160, cy - 26, cx + 160, cy], fill=INK)
    q = ease(clamp(k))
    if q > 0:
        for i in range(9):
            x = cx - 60 + (i % 5) * 30
            y = cy - 40 - (i // 5) * 26 - (1 - q) * 300
            d.ellipse([x - 18, y - 14, x + 18, y + 14], fill=PHOB_D, outline=INK, width=3)
    txt(img, (cx, cy + 80), val if q > 0.95 else "0 g", 54, (120, 255, 160))


# ------------------------------------------------------------------ motor (F1 actual) y Tierra por dentro
def f1m(img, cx, cy, s=1.0, rot=0.0, glow=0.0, flip=1):
    """F1 moderno de lado (morro a la derecha), con halo, alerones y discos que se ponen al rojo (glow 0-1)."""
    d = D(img)
    P = lambda x, y: (cx + x * s * flip, cy + y * s)
    body = (220, 40, 40)
    d.polygon([P(-420, -40), P(-420, -150), P(-330, -150), P(-330, -60)], fill=INK)            # alerón trasero
    d.polygon([P(-360, -40), P(-200, -110), P(-60, -112), P(60, -80), P(380, -40), P(470, -10), P(470, 18), P(-360, 18)],
              fill=body, outline=INK)
    d.polygon([P(-40, -112), P(40, -112), P(80, -84), P(-60, -84)], fill=INK)                   # cockpit
    d.line([P(-60, -120), P(20, -140), P(70, -100)], fill=INK, width=max(4, int(9 * s)))         # halo
    d.ellipse([*P(-20, -138), *P(20, -104)] if flip == 1 else [*P(20, -138), *P(-20, -104)], fill=(250, 210, 60))
    d.polygon([P(380, 10), P(500, 10), P(500, 30), P(380, 30)], fill=INK)                       # alerón delantero
    d.line([P(-200, -20), P(300, -20)], fill=(255, 255, 255), width=max(2, int(5 * s)))
    for wx, r in ((-250, 92), (300, 86)):
        x, y = P(wx, 30)
        rr = r * s
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=INK)
        if glow > 0:
            g = clamp(glow)
            col = (int(lerp(90, 255, g)), int(lerp(90, 120 * g + 30, g)), int(lerp(96, 40, g)))
            d.ellipse([x - rr * 0.55, y - rr * 0.55, x + rr * 0.55, y + rr * 0.55], fill=col)
        else:
            d.ellipse([x - rr * 0.55, y - rr * 0.55, x + rr * 0.55, y + rr * 0.55], fill=(90, 90, 96))
        for k in range(5):
            a = rot + k * 2 * math.pi / 5
            d.line([(x, y), (x + math.cos(a) * rr * 0.5, y + math.sin(a) * rr * 0.5)], fill=INK, width=max(2, int(5 * s)))


def disc(img, cx, cy, r, heat=0.0, warp=0.0):
    """Disco de freno de frente: agujeros de ventilación y color según la temperatura (0 = negro, 1 = al rojo)."""
    d = D(img)
    h = clamp(heat)
    col = (int(lerp(40, 255, h)), int(lerp(40, 110, h ** 1.5) + 40 * h ** 3), int(lerp(44, 30, h)))
    if h > 0.5:
        for k in range(3):
            rr = r * (1.15 + 0.12 * k)
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 120, 40, int(40 * (h - 0.5) * 2 / (k + 1))))
    pts = []
    for k in range(48):
        a = k * 2 * math.pi / 48
        rr = r * (1 + warp * 0.08 * math.sin(3 * a))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=col, outline=INK)
    for ring, n in ((0.82, 28), (0.68, 22)):
        for k in range(n):
            a = k * 2 * math.pi / n + ring
            x, y = cx + math.cos(a) * r * ring, cy + math.sin(a) * r * ring
            d.ellipse([x - r * 0.035, y - r * 0.035, x + r * 0.035, y + r * 0.035], fill=INK)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45], fill=(200, 200, 206), outline=INK, width=6)
    for k in range(6):
        a = k * math.pi / 3
        x, y = cx + math.cos(a) * r * 0.28, cy + math.sin(a) * r * 0.28
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=INK)


def weight(img, cx, cy, w, label, col=INK):
    d = D(img)
    d.polygon([(cx - w * 0.4, cy - w * 0.5), (cx + w * 0.4, cy - w * 0.5), (cx + w * 0.55, cy + w * 0.3), (cx - w * 0.55, cy + w * 0.3)], fill=col)
    d.ellipse([cx - w * 0.14, cy - w * 0.72, cx + w * 0.14, cy - w * 0.44], outline=col, width=max(6, int(w / 16)))
    txt(img, (cx, cy - w * 0.05), label, int(w * 0.24), (255, 255, 255))


def earth_cut(img, cx, cy, r, glow=0.0):
    """La Tierra cortada por la mitad: corteza, manto, núcleo externo e interno."""
    d = D(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 150, 230), outline=INK, width=8)
    for f, col in ((0.97, (150, 110, 80)), (0.9, (236, 140, 70)), (0.55, (246, 190, 70)), (0.19, (255, 236, 130))):
        rr = r * f
        if f < 0.6 and glow > 0:
            col = tuple(int(lerp(c, t, glow)) for c, t in zip(col, (255, 120, 60)))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col, outline=INK, width=3)
    for dx, dy, rr in ((-0.5, -0.75, 0.22), (0.35, -0.82, 0.18)):
        d.chord([cx + (dx - rr) * r, cy + (dy - rr * 0.5) * r, cx + (dx + rr) * r, cy + (dy + rr * 0.5) * r], 180, 360, fill=(110, 190, 110))


def faller(img, x, y, s=1.0, ang=0.0, col=RED):
    """Monigote cayendo con brazos arriba."""
    d = D(img)
    lw = max(3, int(7 * s))
    ca, sa = math.cos(ang), math.sin(ang)
    T = lambda px, py: (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)
    hx, hy = T(0, -48)
    d.ellipse([hx - 18 * s, hy - 18 * s, hx + 18 * s, hy + 18 * s], fill=col)
    d.line([T(0, -30), T(0, 20)], fill=col, width=lw)
    d.line([T(0, -20), T(-26, -56)], fill=col, width=lw)
    d.line([T(0, -20), T(26, -56)], fill=col, width=lw)
    d.line([T(0, 20), T(-18, 56)], fill=col, width=lw)
    d.line([T(0, 20), T(18, 56)], fill=col, width=lw)


# ------------------------------------------------------------------ mapas, globo y aviones (aviones en curva, Concorde)
CONT = {
    "na": [(-168, 66), (-140, 70), (-95, 72), (-80, 68), (-62, 60), (-55, 52), (-65, 45), (-75, 38), (-81, 30), (-80, 25),
           (-97, 26), (-105, 22), (-95, 16), (-83, 9), (-78, 8), (-90, 14), (-106, 23), (-117, 32), (-124, 40), (-125, 48),
           (-135, 58), (-150, 60), (-165, 60)],
    "sa": [(-78, 8), (-60, 10), (-50, 0), (-35, -6), (-40, -22), (-48, -28), (-58, -38), (-66, -55), (-72, -50), (-75, -40),
           (-71, -18), (-81, -5)],
    "gl": [(-73, 78), (-40, 83), (-20, 80), (-20, 70), (-43, 60), (-55, 65), (-60, 75)],
    "eu": [(-10, 36), (-9, 43), (-2, 48), (-5, 58), (10, 63), (20, 70), (40, 68), (60, 70), (80, 73), (105, 77), (140, 72),
           (170, 68), (180, 66), (160, 60), (142, 50), (135, 43), (122, 40), (120, 30), (110, 20), (105, 10), (100, 13), (98, 8),
           (92, 22), (80, 15), (77, 8), (72, 20), (60, 25), (50, 30), (48, 28), (56, 25), (52, 15), (43, 13), (35, 30), (35, 36),
           (28, 37), (23, 40), (15, 40), (10, 44), (3, 43), (-5, 36)],
    "af": [(-17, 21), (-10, 30), (-5, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 12), (40, -5), (40, -15),
           (35, -25), (28, -34), (18, -35), (12, -18), (9, -2), (9, 4), (-8, 5), (-15, 11)],
    "au": [(114, -22), (130, -12), (137, -12), (145, -15), (153, -28), (147, -38), (138, -35), (115, -34)],
}
LAND = (226, 214, 190)
SEA = (224, 236, 248)


def merc(lon, lat, box):
    """box = (x0, y0, x1, y1, lon0, lon1, lat_top, lat_bot) → píxeles en Mercator."""
    x0, y0, x1, y1, lo0, lo1, lt, lb = box
    m = lambda la: math.log(math.tan(math.pi / 4 + math.radians(max(-84, min(84, la))) / 2))
    x = x0 + (lon - lo0) / (lo1 - lo0) * (x1 - x0)
    y = y0 + (m(lt) - m(lat)) / (m(lt) - m(lb)) * (y1 - y0)
    return x, y


def world_map(img, box, hi=None, k=1.0, clip=None):
    """Mapa en Mercator recortado a su marco (clip = marco visible si el mapa está ampliado)."""
    x0, y0, x1, y1 = box[:4]
    cx0, cy0, cx1, cy1 = clip or (max(0, x0), max(0, y0), min(W, x1), min(H, y1))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    for key, pts in CONT.items():
        col = RED if hi and key in hi else LAND
        d.polygon([merc(lo, la, box) for lo, la in pts], fill=col, outline=INK)
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rectangle([cx0, cy0, cx1, cy1], fill=255)
    img.paste(lay, (0, 0), Image.composite(lay.split()[3], m, m).point(lambda v: v) if False else _and(lay.split()[3], m))
    D(img).rectangle([cx0, cy0, cx1, cy1], outline=INK, width=5)


def _and(a, b):
    from PIL import ImageChops
    return ImageChops.multiply(a, b)


def gc_points(a, b, n=60):
    """Puntos (lon, lat) del círculo máximo entre a y b (lat, lon)."""
    la1, lo1 = map(math.radians, a)
    la2, lo2 = map(math.radians, b)
    p1 = (math.cos(la1) * math.cos(lo1), math.cos(la1) * math.sin(lo1), math.sin(la1))
    p2 = (math.cos(la2) * math.cos(lo2), math.cos(la2) * math.sin(lo2), math.sin(la2))
    om = math.acos(max(-1, min(1, sum(u * v for u, v in zip(p1, p2)))))
    out = []
    for i in range(n + 1):
        f = i / n
        A, B = math.sin((1 - f) * om) / math.sin(om), math.sin(f * om) / math.sin(om)
        x = [A * u + B * v for u, v in zip(p1, p2)]
        out.append((math.degrees(math.atan2(x[1], x[0])), math.degrees(math.asin(x[2]))))
    return out


def plane_top(img, x, y, ang, s=1.0, col=INK):
    """Avión visto desde arriba, apuntando en la dirección ang (radianes, 0 = derecha)."""
    d = D(img)
    pts = [(30, 0), (8, -4), (2, -26), (-6, -26), (-4, -4), (-20, -3), (-26, -12), (-30, -12), (-26, 0), (-30, 12), (-26, 12),
           (-20, 3), (-4, 4), (-6, 26), (2, 26), (8, 4)]
    ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s) for px, py in pts], fill=col)


def globe(img, cx, cy, r, rot=0.0):
    d = D(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEA, outline=INK, width=8)
    for k in range(-2, 3):
        ry = r * math.cos(math.radians(k * 30))
        yy = cy - r * math.sin(math.radians(k * 30))
        d.line([(cx - ry, yy), (cx + ry, yy)], fill=(190, 206, 224), width=3)
    for k in range(6):
        a = (k * 30 + math.degrees(rot)) % 180
        w = r * abs(math.cos(math.radians(a)))
        d.ellipse([cx - w, cy - r, cx + w, cy + r], outline=(190, 206, 224), width=3)
    # dos «continentes» de bulto
    d.chord([cx - r * 0.7, cy - r * 0.7, cx + r * 0.1, cy + r * 0.1], 200, 340, fill=LAND, outline=INK)
    d.chord([cx - r * 0.1, cy - r * 0.6, cx + r * 0.8, cy + r * 0.4], 190, 330, fill=LAND, outline=INK)


def concorde(img, cx, cy, s=1.0, ang=0.0, stretch=1.0, nose=0.0, col=(250, 250, 252)):
    """Concorde de lado (morro a la derecha): fuselaje fino, ala en delta, morro que se baja (nose 0-1)."""
    lay = Image.new("RGBA", (int(1100 * s * stretch) + 40, int(360 * s) + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    L = 1000 * stretch
    o = lambda x, y: (20 + x * s, 20 + y * s)
    body = [(0, 150), (60, 120), (L - 160, 112), (L - 60, 118), (L, 140 + 30 * nose), (L - 60, 162), (L - 160, 170), (40, 172)]
    d.polygon([o(x, y) for x, y in body], fill=col, outline=INK)
    d.polygon([o(x, y) for x, y in [(L * 0.25, 168), (L * 0.78, 162), (L * 0.32, 230), (L * 0.18, 232)]], fill=(214, 216, 222), outline=INK)
    d.polygon([o(x, y) for x, y in [(30, 124), (120, 118), (60, 10), (20, 10)]], fill=col, outline=INK)
    for x in range(int(L * 0.3), int(L * 0.85), int(34 * stretch) + 1):
        d.ellipse([*o(x, 132), *o(x + 10, 142)], fill=(80, 110, 160))
    d.rectangle([*o(L * 0.22, 176), *o(L * 0.42, 196)], fill=(120, 124, 132), outline=INK)
    d.line([o(60, 150), o(L - 70, 150)], fill=RED, width=max(2, int(5 * s)))
    lay = lay.rotate(math.degrees(-ang), expand=True, resample=Image.BICUBIC)
    img.paste(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)), lay)


def ruler(img, x0, y, x1, k=1.0, col=INK, ticks=10):
    d = D(img)
    xe = x0 + (x1 - x0) * clamp(k)
    d.rectangle([x0, y - 22, xe, y + 22], fill=(255, 226, 120), outline=col, width=4)
    for i in range(ticks + 1):
        x = x0 + (x1 - x0) * i / ticks
        if x <= xe:
            d.line([(x, y - 22), (x, y - 6)], fill=col, width=3)
