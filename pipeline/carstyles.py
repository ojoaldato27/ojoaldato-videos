"""Cuatro estilos de coche muy distintos para que Iker elija (21/10): realista de estudio, dibujo animado, neón de líneas y
plano minimalista. Cada función devuelve un fotograma 1080×1920 de muestra con su fondo."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import car_pro as CP

W, H = 1080, 1920
OUT = CP._spline([(24, 238), (40, 214), (120, 196), (250, 184), (370, 168), (432, 150), (500, 110), (560, 96), (640, 96),
                  (720, 116), (812, 150), (900, 170), (958, 186), (980, 214), (974, 248), (930, 260), (60, 262)], 8)
GLASS = CP._spline([(452, 150), (506, 114), (562, 104), (636, 104), (708, 122), (760, 146), (700, 158), (470, 160)], 6)
WHEELS = ((208, 262, 58), (790, 262, 60))


def _tr(pts, s, ox, oy, sy=1.0, cy=262):
    return [(ox + x * s, oy + (cy + (y - cy) * sy) * s) for x, y in pts]


# ------------------------------------------------------------------ A · realista de estudio
def realista():
    img = Image.new("RGB", (W, H), (8, 8, 10))
    ys = np.linspace(0, 1, H)[:, None]
    g = (np.clip(1 - np.abs(ys - 0.52) * 2.2, 0, 1) ** 1.6 * 58 + 10) * np.ones((1, W))
    img = Image.fromarray(np.stack([g, g, g * 1.04], -1).clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    # foco cenital
    cone = Image.new("L", (W, H), 0)
    ImageDraw.Draw(cone).polygon([(470, 0), (610, 0), (1020, 1240), (60, 1240)], fill=60)
    img.paste((255, 250, 240), (0, 0), cone.filter(ImageFilter.GaussianBlur(60)))
    car = CP.roadster(rim_cols=None, glow=False)
    s = 1.0
    cw, ch = int(car.width * s), int(car.height * s)
    car = car.resize((cw, ch), Image.LANCZOS)
    x0, y0 = (W - cw) // 2, 820
    # reflejo en el suelo pulido
    ref = car.transpose(Image.FLIP_TOP_BOTTOM)
    fade = np.linspace(0.42, 0, ch)[:, None] * np.ones((1, cw))
    a = np.array(ref.getchannel("A"), np.float32) * fade
    ref.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.paste(ref.filter(ImageFilter.GaussianBlur(3)), (x0, y0 + ch - 40), ref.filter(ImageFilter.GaussianBlur(3)))
    img.paste(car, (x0, y0), car)
    return img


# ------------------------------------------------------------------ B · dibujo animado
def cartoon():
    img = Image.new("RGB", (W, H))
    ys = np.linspace(0, 1, H)[:, None, None]
    top, bot = np.array((90, 200, 255), float), np.array((255, 240, 160), float)
    img = Image.fromarray((top * (1 - ys) + bot * ys).repeat(W, 1).astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    # rayos de velocidad
    cx, cy = 540, 1000
    for k in range(28):
        a0 = k * 2 * math.pi / 28
        d.polygon([(cx, cy), (cx + math.cos(a0) * 1600, cy + math.sin(a0) * 1600),
                   (cx + math.cos(a0 + 0.09) * 1600, cy + math.sin(a0 + 0.09) * 1600)], fill=(255, 255, 255, 55))
    d.rectangle([0, 1160, W, H], fill=(110, 200, 90))
    d.rectangle([0, 1160, W, 1176], fill=(70, 150, 60))
    s, ox, oy = 1.0, 40, 820
    body = _tr(OUT, s, ox, oy, 1.35)
    glass = _tr(GLASS, s, ox, oy, 1.35)
    # sombra
    d.ellipse([ox + 40, oy + 300, ox + 980, oy + 360], fill=(0, 0, 0, 70))
    d.polygon(body, fill=(255, 50, 60), outline=(20, 10, 20))
    # banda de sombra (cel shading)
    low = Image.new("L", (W, H), 0)
    ImageDraw.Draw(low).polygon(body, fill=255)
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).rectangle([0, oy + 230, W, oy + 300], fill=255)
    img.paste((200, 20, 40), (0, 0), ImageChops.multiply(low, band))
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon(glass, fill=(150, 225, 255))
    d.polygon([(ox + 520, oy + 92), (ox + 570, oy + 88), (ox + 520, oy + 140), (ox + 486, oy + 140)], fill=(255, 255, 255, 200))
    d.line(body + [body[0]], fill=(20, 10, 20), width=12, joint="curve")
    d.line(glass + [glass[0]], fill=(20, 10, 20), width=10, joint="curve")
    d.rounded_rectangle([ox + 160, oy + 150, ox + 420, oy + 172], radius=11, fill=(255, 255, 255, 200))
    for wx, wy, r in WHEELS:
        r2 = int(r * 1.35)
        X, Y = ox + wx, oy + wy + 18
        d.ellipse([X - r2, Y - r2, X + r2, Y + r2], fill=(40, 36, 48), outline=(20, 10, 20), width=10)
        d.ellipse([X - r2 * 0.5, Y - r2 * 0.5, X + r2 * 0.5, Y + r2 * 0.5], fill=(255, 210, 60), outline=(20, 10, 20), width=7)
        d.ellipse([X - 10, Y - 10, X + 10, Y + 10], fill=(20, 10, 20))
    # líneas de movimiento
    for k, yy in enumerate((oy + 140, oy + 200, oy + 260)):
        d.line([(ox + 1000 + k * 10, yy), (W, yy)], fill=(255, 255, 255, 220), width=10)
    return img


# ------------------------------------------------------------------ C · neón de líneas (synthwave)
def neon():
    img = Image.new("RGB", (W, H), (6, 2, 18))
    d = ImageDraw.Draw(img, "RGBA")
    # sol a rayas
    sun = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    for yy in range(700):
        u = yy / 700
        col = (int(255), int(60 + 160 * (1 - u)), int(160 * u + 40))
        sd.line([(0, yy), (700, yy)], fill=col + (255,))
    m = Image.new("L", (700, 700), 0)
    md = ImageDraw.Draw(m)
    md.ellipse([0, 0, 700, 700], fill=255)
    for k in range(8):
        y0 = 380 + k * 40
        md.rectangle([0, y0, 700, y0 + 6 + k * 2], fill=0)
    img.paste(sun, (190, 300), m)
    hz = 1000
    d.rectangle([0, hz, W, H], fill=(10, 0, 26))
    for k in range(1, 22):
        yy = hz + (H - hz) * (k / 22) ** 2
        d.line([(0, yy), (W, yy)], fill=(255, 40, 200, 170), width=2)
    for i in range(-14, 15):
        d.line([(540 + i * 12, hz), (540 + i * 150, H)], fill=(255, 40, 200, 150), width=2)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    s, ox, oy = 1.0, 40, 760
    body = _tr(OUT, s, ox, oy)
    glass = _tr(GLASS, s, ox, oy)
    ld.polygon(body, fill=(4, 2, 14, 255))
    ld.line(body + [body[0]], fill=(0, 240, 255, 255), width=6, joint="curve")
    ld.line(glass + [glass[0]], fill=(255, 60, 220, 255), width=5, joint="curve")
    ld.line(CP._open_spline([(ox + 70, oy + 214), (ox + 470, oy + 182), (ox + 930, oy + 192)]), fill=(0, 240, 255, 200), width=3)
    for wx, wy, r in WHEELS:
        X, Y = ox + wx, oy + wy
        ld.ellipse([X - r, Y - r, X + r, Y + r], fill=(4, 2, 14, 255), outline=(0, 240, 255, 255), width=6)
        ld.ellipse([X - r * 0.55, Y - r * 0.55, X + r * 0.55, Y + r * 0.55], outline=(255, 60, 220, 255), width=4)
    glow = lay.filter(ImageFilter.GaussianBlur(14))
    img.paste(glow, (0, 0), glow)
    img.paste(glow, (0, 0), glow)
    img.paste(lay, (0, 0), lay)
    return img


# ------------------------------------------------------------------ D · plano minimalista
def plano():
    img = Image.new("RGB", (W, H), (38, 70, 83))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([620, 330, 980, 690], fill=(244, 162, 97))
    for k, (yy, col) in enumerate(((1060, (42, 157, 143)), (1180, (38, 120, 120)), (1300, (30, 90, 100)))):
        d.polygon([(0, yy), (W * 0.4, yy - 120 + k * 30), (W, yy - 40), (W, H), (0, H)], fill=col)
    s, ox, oy = 1.0, 40, 820
    body = _tr(OUT, s, ox, oy)
    glass = _tr(GLASS, s, ox, oy)
    # sombra larga
    d.polygon([(ox + 60, oy + 262), (ox + 980, oy + 262), (ox + 1150, oy + 330), (ox + 230, oy + 330)], fill=(0, 0, 0, 50))
    d.polygon(body, fill=(231, 111, 81))
    d.polygon([(p[0], p[1]) for p in body if p[1] > oy + 205] or body, fill=(200, 85, 62))
    d.polygon(glass, fill=(233, 196, 106))
    for wx, wy, r in WHEELS:
        X, Y = ox + wx, oy + wy
        d.ellipse([X - r, Y - r, X + r, Y + r], fill=(38, 50, 56))
        d.ellipse([X - r * 0.42, Y - r * 0.42, X + r * 0.42, Y + r * 0.42], fill=(233, 196, 106))
    d.rectangle([ox + 30, oy + 226, ox + 110, oy + 236], fill=(250, 240, 220))
    return img


def sheet(path):
    fns = [("A · Realista de estudio", realista), ("B · Dibujo animado", cartoon), ("C · Neón de líneas", neon), ("D · Plano minimalista", plano)]
    tiles = []
    from docu import caps_font
    for name, fn in fns:
        im = fn().resize((432, 768), Image.LANCZOS)
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle([16, 16, 416, 76], radius=14, fill=(0, 0, 0, 170))
        d.text((216, 46), name, font=caps_font(26, "ExtraBold"), fill=(255, 255, 255), anchor="mm")
        tiles.append(im)
    out = Image.new("RGB", (432 * 2 + 12, 768 * 2 + 12), (255, 255, 255))
    for k, t in enumerate(tiles):
        out.paste(t, ((k % 2) * 444, (k // 2) * 780))
    out.save(path, quality=90)
