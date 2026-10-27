"""Cuatro formatos visuales para que Iker elija (21/10, «dame opciones de formatos rollo pixel… que se parezca lo máximo a lo
real en colores y forma»): pixel art, plano técnico, cómic y recortes de papel. El coche es el Tesla Roadster (2.ª generación)
de perfil con sus proporciones reales: muy bajo, morro redondo sin parrilla, parabrisas muy inclinado, techo corto hacia atrás,
zaga en caída con pequeño alerón y llantas grandes."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import car_pro as CP

W, H = 1080, 1920
RED = (196, 14, 30)
# perfil en un lienzo de 1000×300 (y hacia abajo); ruedas en (205,240) r62 y (792,240) r64
PROFILE = [(18, 228), (10, 204), (40, 186), (130, 176), (250, 168), (370, 154), (430, 136), (480, 108), (540, 94), (600, 90),
           (660, 94), (730, 114), (820, 142), (910, 158), (962, 164), (984, 180), (986, 212), (972, 236), (920, 246), (70, 248)]
WIND = [(452, 140), (496, 110), (552, 98), (606, 96), (664, 100), (722, 120), (680, 138), (470, 144)]
WH = ((205, 240, 62), (792, 240, 64))


def _prof(s=1.0, ox=0, oy=0, n=8):
    return [(ox + x * s, oy + y * s) for x, y in CP._spline(PROFILE, n)]


def _wind(s=1.0, ox=0, oy=0):
    return [(ox + x * s, oy + y * s) for x, y in CP._spline(WIND, 6)]


# ------------------------------------------------------------------ 1 · pixel art (16 bits)
def pixel():
    px = 6
    w, h = W // px, H // px                     # 180 × 320
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    sky = [(28, 18, 66), (52, 28, 98), (98, 44, 120), (170, 70, 120), (240, 120, 110), (255, 180, 110)]
    band = 150 // len(sky)
    for i, c in enumerate(sky):
        d.rectangle([0, 10 + i * band, w, 10 + (i + 1) * band], fill=c)
        if i:                                     # tramado entre bandas
            for x in range(0, w, 2):
                d.point((x + (i % 2), 10 + i * band), fill=sky[i - 1])
    d.rectangle([0, 0, w, 10], fill=sky[0])
    rng = random.Random(3)
    for _ in range(40):
        d.point((rng.randrange(w), rng.randrange(0, 70)), fill=(255, 255, 230))
    d.ellipse([110, 70, 160, 120], fill=(255, 214, 120))
    # montañas y ciudad
    d.polygon([(0, 160), (30, 130), (60, 150), (95, 118), (130, 148), (180, 126), (180, 170), (0, 170)], fill=(60, 30, 80))
    for k in range(14):
        x0 = k * 13
        hh = rng.randint(10, 34)
        d.rectangle([x0, 170 - hh, x0 + 10, 172], fill=(34, 20, 52))
        for wy in range(170 - hh + 3, 170, 4):
            if rng.random() < 0.5:
                d.point((x0 + 3, wy), fill=(255, 210, 120))
    d.rectangle([0, 172, w, h], fill=(36, 36, 44))
    for x in range(0, w, 16):
        d.rectangle([x, 196, x + 8, 197], fill=(230, 220, 120))
    d.rectangle([0, 172, w, 174], fill=(90, 90, 100))
    # coche en baja resolución, sin suavizado y con paleta corta
    s, ox, oy = 0.17, 5, 144
    prof = [(round(x), round(y)) for x, y in _prof(s, ox, oy, 4)]
    d.polygon(prof, fill=RED)
    d.polygon([(x, y) for x, y in prof if y > oy + 205 * s] or prof, fill=(140, 8, 20))
    d.line(prof + [prof[0]], fill=(30, 6, 12), width=1)
    d.line([(ox + 30 * s, oy + 192 * s), (ox + 900 * s, oy + 168 * s)], fill=(255, 110, 110), width=1)
    d.polygon([(round(x), round(y)) for x, y in _wind(s, ox, oy)], fill=(40, 52, 80))
    d.line([(ox + 520 * s, oy + 100 * s), (ox + 470 * s, oy + 140 * s)], fill=(140, 170, 220))
    d.point((round(ox + 18 * s), round(oy + 200 * s)), fill=(255, 255, 220))
    d.line([(ox + 950 * s, oy + 170 * s), (ox + 982 * s, oy + 178 * s)], fill=(255, 40, 60))
    for cx, cy, r in WH:
        X, Y, R = ox + cx * s, oy + cy * s, r * s
        d.ellipse([X - R, Y - R, X + R, Y + R], fill=(20, 20, 24))
        d.ellipse([X - R * 0.6, Y - R * 0.6, X + R * 0.6, Y + R * 0.6], fill=(170, 176, 186))
        d.point((round(X), round(Y)), fill=(60, 60, 70))
    return im.resize((W, H), Image.NEAREST)


# ------------------------------------------------------------------ 2 · plano técnico (blueprint)
def blueprint():
    im = Image.new("RGB", (W, H), (14, 64, 128))
    d = ImageDraw.Draw(im, "RGBA")
    for x in range(0, W, 30):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 40 if x % 150 else 80), width=1)
    for y in range(0, H, 30):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 40 if y % 150 else 80), width=1)
    s, ox, oy = 1.0, 40, 820
    prof = _prof(s, ox, oy)
    d.line(prof + [prof[0]], fill=(255, 255, 255, 255), width=5, joint="curve")
    d.line(_wind(s, ox, oy) + [_wind(s, ox, oy)[0]], fill=(255, 255, 255, 230), width=4, joint="curve")
    d.line([(ox + 462, oy + 150), (ox + 456, oy + 236)], fill=(255, 255, 255, 160), width=3)
    d.line([(ox + 40, oy + 194), (ox + 940, oy + 166)], fill=(255, 255, 255, 120), width=2)
    for cx, cy, r in WH:
        X, Y = ox + cx, oy + cy
        d.ellipse([X - r, Y - r, X + r, Y + r], outline=(255, 255, 255, 255), width=5)
        d.ellipse([X - r * 0.62, Y - r * 0.62, X + r * 0.62, Y + r * 0.62], outline=(255, 255, 255, 200), width=3)
        d.line([(X - r - 14, Y), (X + r + 14, Y)], fill=(255, 255, 255, 120), width=1)
        d.line([(X, Y - r - 14), (X, Y + r + 14)], fill=(255, 255, 255, 120), width=1)
    # cotas
    from docu import font, F_UI_B
    fo = font(F_UI_B, 30)
    yb = oy + 340

    def arrow(x0, x1, y, txt):
        d.line([(x0, y), (x1, y)], fill=(255, 255, 255, 220), width=2)
        for x, sgn in ((x0, 1), (x1, -1)):
            d.polygon([(x, y), (x + 18 * sgn, y - 8), (x + 18 * sgn, y + 8)], fill=(255, 255, 255, 230))
            d.line([(x, y - 30), (x, y + 10)], fill=(255, 255, 255, 140), width=1)
        d.text(((x0 + x1) / 2, y - 22), txt, font=fo, fill=(255, 255, 255), anchor="mm")

    arrow(ox + 10, ox + 986, yb, "≈ 4,0 m")
    arrow(ox + 205, ox + 792, yb + 90, "BATALLA")
    d.line([(ox + 1000, oy + 90), (ox + 1000, oy + 248)], fill=(255, 255, 255, 200), width=2)
    d.text((ox + 980, oy + 70), "≈ 1,1 m", font=font(F_UI_B, 26), fill=(255, 255, 255), anchor="rm")
    d.rectangle([600, 1640, 1040, 1860], outline=(255, 255, 255, 220), width=3)
    d.text((620, 1680), "TESLA ROADSTER", font=font(F_UI_B, 34), fill=(255, 255, 255), anchor="lm")
    d.text((620, 1730), "VISTA LATERAL · ESC. 1:20", font=font(F_UI_B, 24), fill=(200, 220, 255), anchor="lm")
    d.text((620, 1780), "PROPULSORES: 10 TOBERAS", font=font(F_UI_B, 24), fill=(200, 220, 255), anchor="lm")
    return im


# ------------------------------------------------------------------ 3 · cómic con tramas
def comic():
    im = Image.new("RGB", (W, H), (255, 214, 0))
    d = ImageDraw.Draw(im, "RGBA")
    cx, cy = 540, 960
    for k in range(36):
        a = k * 2 * math.pi / 36
        if k % 2:
            d.polygon([(cx, cy), (cx + math.cos(a) * 1800, cy + math.sin(a) * 1800),
                       (cx + math.cos(a + 2 * math.pi / 36) * 1800, cy + math.sin(a + 2 * math.pi / 36) * 1800)], fill=(255, 170, 0))
    # trama de puntos
    dots = Image.new("L", (W, H), 0)
    dd = ImageDraw.Draw(dots)
    for y in range(0, H, 22):
        for x in range((y // 22) % 2 * 11, W, 22):
            r = 2 + 5 * (1 - min(1, math.hypot(x - cx, y - cy) / 1100))
            dd.ellipse([x - r, y - r, x + r, y + r], fill=255)
    im.paste((230, 120, 0), (0, 0), dots)
    d = ImageDraw.Draw(im, "RGBA")
    s, ox, oy = 1.0, 40, 840
    prof = _prof(s, ox, oy)
    d.polygon([(x + 14, y + 16) for x, y in prof], fill=(0, 0, 0))
    d.polygon(prof, fill=(225, 25, 40))
    # sombreado en trama sobre la parte baja del coche
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(prof, fill=255)
    low = Image.new("L", (W, H), 0)
    ImageDraw.Draw(low).rectangle([0, oy + 205, W, oy + 260], fill=255)
    hd = Image.new("L", (W, H), 0)
    hdd = ImageDraw.Draw(hd)
    for y in range(oy + 200, oy + 260, 10):
        for x in range(0, W, 10):
            hdd.ellipse([x - 3, y - 3, x + 3, y + 3], fill=255)
    im.paste((120, 0, 10), (0, 0), ImageChops.multiply(ImageChops.multiply(m, low), hd))
    d = ImageDraw.Draw(im, "RGBA")
    d.polygon(_wind(s, ox, oy), fill=(120, 200, 255))
    d.polygon([(ox + 520, oy + 100), (ox + 560, oy + 98), (ox + 500, oy + 140), (ox + 474, oy + 140)], fill=(255, 255, 255))
    d.line(prof + [prof[0]], fill=(0, 0, 0), width=12, joint="curve")
    d.line(_wind(s, ox, oy) + [_wind(s, ox, oy)[0]], fill=(0, 0, 0), width=9, joint="curve")
    d.line([(ox + 60, oy + 196), (ox + 420, oy + 172)], fill=(255, 255, 255), width=10)
    for cx2, cy2, r in WH:
        X, Y = ox + cx2, oy + cy2
        d.ellipse([X - r, Y - r, X + r, Y + r], fill=(30, 30, 30), outline=(0, 0, 0), width=10)
        d.ellipse([X - r * 0.55, Y - r * 0.55, X + r * 0.55, Y + r * 0.55], fill=(230, 230, 235), outline=(0, 0, 0), width=6)
    # onomatopeya
    from docu import caps_font
    bx, by = 290, 520
    burst = [(bx + math.cos(a) * (230 if i % 2 else 150), by + math.sin(a) * (170 if i % 2 else 110))
             for i, a in enumerate(np.linspace(0, 2 * math.pi, 24, endpoint=False))]
    d.polygon(burst, fill=(255, 255, 255), outline=(0, 0, 0))
    d.line(burst + [burst[0]], fill=(0, 0, 0), width=8)
    d.text((bx, by), "¡ZAS!", font=caps_font(104, "Black"), fill=(225, 25, 40), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
    for k, yy in enumerate((oy + 120, oy + 180, oy + 240)):
        d.line([(ox + 1010 + k * 8, yy), (W, yy)], fill=(0, 0, 0), width=8)
    return im


# ------------------------------------------------------------------ 4 · recortes de papel
def _paper(lay, col, shadow=10, seed=1):
    """Pinta la máscara 'lay' como papel: color con textura y sombra suave debajo."""
    rng = np.random.default_rng(seed)
    noise = (rng.normal(0, 7, (H, W))).astype(np.int16)
    base = np.array(col, np.int16)[None, None, :] + noise[..., None]
    tex = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")
    sh = lay.filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: int(v * 0.55))
    return tex, sh


def paper():
    im = Image.new("RGB", (W, H), (190, 228, 240))
    layers = []

    def poly_mask(pts):
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon(pts, fill=255)
        return m

    def ell_mask(box):
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).ellipse(box, fill=255)
        return m

    layers.append((ell_mask([640, 300, 960, 620]), (255, 196, 70)))
    layers.append((poly_mask([(0, 980), (200, 820), (420, 940), (650, 780), (900, 920), (1080, 840), (1080, 1300), (0, 1300)]), (120, 190, 150)))
    layers.append((poly_mask([(0, 1080), (300, 980), (620, 1060), (1080, 990), (1080, 1400), (0, 1400)]), (80, 160, 120)))
    layers.append((poly_mask([(0, 1120), (1080, 1120), (1080, H), (0, H)]), (70, 70, 80)))
    s, ox, oy = 1.0, 40, 860
    layers.append((poly_mask(_prof(s, ox, oy)), RED))
    layers.append((poly_mask(_wind(s, ox, oy)), (40, 56, 86)))
    for cx, cy, r in WH:
        layers.append((ell_mask([ox + cx - r, oy + cy - r, ox + cx + r, oy + cy + r]), (34, 34, 40)))
        layers.append((ell_mask([ox + cx - r * 0.58, oy + cy - r * 0.58, ox + cx + r * 0.58, oy + cy + r * 0.58]), (200, 204, 212)))
    for i, (m, col) in enumerate(layers):
        tex, sh = _paper(m, col, 12, i)
        im.paste((20, 30, 40), (8, 12), sh)
        im.paste(tex, (0, 0), m)
    d = ImageDraw.Draw(im, "RGBA")
    for k in range(0, W, 120):
        d.rectangle([k, 1340, k + 60, 1352], fill=(240, 240, 230, 230))
    return im


def sheet(path):
    fns = [("1 · Pixel art", pixel), ("2 · Plano técnico", blueprint), ("3 · Cómic", comic), ("4 · Recortes de papel", paper)]
    from docu import caps_font
    tiles = []
    for name, fn in fns:
        im = fn().resize((432, 768), Image.LANCZOS)
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle([16, 16, 416, 76], radius=14, fill=(0, 0, 0, 170))
        d.text((216, 46), name, font=caps_font(28, "ExtraBold"), fill=(255, 255, 255), anchor="mm")
        tiles.append(im)
    out = Image.new("RGB", (432 * 2 + 12, 768 * 2 + 12), (255, 255, 255))
    for k, t in enumerate(tiles):
        out.paste(t, ((k % 2) * 444, (k // 2) * 780))
    out.save(path, quality=90)
