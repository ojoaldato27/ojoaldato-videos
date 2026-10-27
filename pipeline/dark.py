"""Estilo «documental oscuro minimalista» (elegido por Iker el 21/10: «el oscuro me gusta, así estilo minimalista»).
Fondo casi negro con niebla y un haz de luz, coches en silueta con luz de borde, faros encendidos, bandas de cine y frases
sobrias en serif. Coches con su forma real: Tesla Cybertruck (cuña de acero) y Tesla Roadster (2.ª generación)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import car_pro as CP

W, H = 1080, 1920
SERIF = "/home/claude/shorts-ingenieria/fonts/PlayfairDisplay-Italic.ttf"

# ------------------------------------------------------------------ coches (lienzo 1000×300, morro a la izquierda, suelo y=300)
CYBER = dict(
    body=[(2, 176), (440, 44), (998, 134), (994, 238), (952, 252), (884, 252), (856, 150), (720, 150), (690, 252),
          (300, 252), (272, 150), (132, 150), (104, 252), (40, 252), (10, 236)],
    glass=[(258, 130), (436, 60), (640, 92), (640, 126), (258, 140)],
    lines=[[(260, 142), (258, 250)], [(645, 128), (650, 250)], [(20, 200), (990, 186)]],
    wheels=[(202, 222, 78), (788, 222, 78)],
    front=[(2, 172), (14, 182)], rear=[(990, 132), (998, 150)], smooth=False)
ROADSTER = dict(
    body=CP._spline([(18, 240), (6, 220), (22, 200), (110, 188), (250, 178), (372, 162), (446, 132), (520, 104), (600, 92),
                     (684, 98), (764, 122), (846, 140), (910, 146), (962, 140), (984, 150), (990, 178), (982, 214), (962, 240),
                     (884, 248), (120, 248)], 8),
    glass=CP._spline([(462, 140), (520, 110), (600, 100), (676, 106), (744, 128), (690, 142), (480, 146)], 6),
    lines=[CP._open_spline([(250, 196), (470, 184), (700, 178), (840, 168), (900, 162)]),
           CP._open_spline([(560, 230), (640, 196), (720, 184)])],
    wheels=[(200, 238, 64), (806, 236, 68)],
    front=[(10, 214), (90, 200)], rear=[(940, 144), (986, 152)], smooth=True)


def _car_layer(spec, s, ox, oy, rim_col=(210, 220, 235)):
    T = lambda pts: [(ox + x * s, oy + y * s) for x, y in pts]
    body = T(spec["body"])
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(body, fill=255)
    for cx, cy, r in spec["wheels"]:
        X, Y, R = ox + cx * s, oy + cy * s, r * s
        ImageDraw.Draw(m).ellipse([X - R, Y - R, X + R, Y + R], fill=255)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay.paste((10, 11, 13, 255), (0, 0), m)
    d = ImageDraw.Draw(lay, "RGBA")
    d.polygon(T(spec["glass"]), fill=(22, 26, 34, 255))
    for ln in spec["lines"]:
        d.line(T(ln), fill=(70, 76, 86, 160), width=2)
    for cx, cy, r in spec["wheels"]:
        X, Y, R = ox + cx * s, oy + cy * s, r * s
        d.ellipse([X - R, Y - R, X + R, Y + R], fill=(6, 6, 8, 255), outline=(48, 52, 58, 255), width=2)
        d.ellipse([X - R * 0.62, Y - R * 0.62, X + R * 0.62, Y + R * 0.62], outline=(70, 74, 82, 255), width=2)
        for k in range(6):
            a = k * math.pi / 3 + 0.3
            d.line([(X + math.cos(a) * R * 0.18, Y + math.sin(a) * R * 0.18), (X + math.cos(a) * R * 0.6, Y + math.sin(a) * R * 0.6)],
                   fill=(56, 60, 68, 255), width=3)
    # luz de borde (desde arriba) sobre la carrocería
    edge = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(5)))
    ys = np.linspace(0, 1, H)[:, None] * np.ones((1, W))
    top = Image.fromarray((np.clip((oy + 200 * s - ys * H) / (150 * s), 0, 1) * 255).astype(np.uint8))
    rim = ImageChops.multiply(edge, top).filter(ImageFilter.GaussianBlur(1.2))
    lay.paste(rim_col + (255,), (0, 0), rim)
    # faros y pilotos
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    f0, f1 = T(spec["front"])
    r0, r1 = T(spec["rear"])
    gd.line([f0, f1], fill=(235, 242, 255, 255), width=int(7 * s))
    gd.line([r0, r1], fill=(255, 30, 40, 255), width=int(6 * s))
    return lay, m, glow, (f0, r0)


def scene(spec, caption, s=1.0, ox=40, oy=900, sub=None):
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.full((H, W, 3), (7, 8, 11), np.float32)
    beam = np.clip(1 - np.abs((xs - 560) - (ys - 300) * 0.16) / (170 + ys * 0.26), 0, 1) * np.clip((ys - 140) / 850, 0, 1) * (ys < 1240)
    base += beam[..., None] * np.array((120, 128, 140), np.float32) * 0.5
    fog = np.clip(1 - np.abs(ys - (oy + 260 * s)) / 230, 0, 1)
    base += fog[..., None] * np.array((26, 30, 36), np.float32)
    rng = np.random.default_rng(2)
    base += rng.normal(0, 2.6, (H, W, 1))
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")
    gy = int(oy + 300 * s)
    d.rectangle([0, gy, W, H], fill=(5, 6, 8, 255))
    d.line([(0, gy), (W, gy)], fill=(40, 44, 52, 255), width=2)
    lay, m, glow, (fpt, rpt) = _car_layer(spec, s, ox, oy)
    # reflejo tenue en el suelo mojado
    ref = lay.transpose(Image.FLIP_TOP_BOTTOM).crop((0, H - gy - (gy - int(oy)), W, H - gy + 0))
    refl = lay.crop((0, int(oy), W, gy)).transpose(Image.FLIP_TOP_BOTTOM)
    a = refl.getchannel("A").point(lambda v: int(v * 0.16))
    refl.putalpha(a)
    im.paste(refl, (0, gy), refl)
    im.paste(lay, (0, 0), lay)
    # haces de los faros y resplandor
    hb = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(hb)
    hd.polygon([fpt, (fpt[0] - 900, fpt[1] - 160), (fpt[0] - 900, fpt[1] + 200)], fill=70)
    im.paste((210, 220, 255), (0, 0), hb.filter(ImageFilter.GaussianBlur(40)))
    g2 = glow.filter(ImageFilter.GaussianBlur(14))
    im.paste(g2, (0, 0), g2)
    im.paste(g2, (0, 0), g2)
    im.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 0, W, 170], fill=(0, 0, 0))
    d.rectangle([0, H - 170, W, H], fill=(0, 0, 0))
    from docu import font
    d.text((W / 2, 1520), caption, font=font(SERIF, 56, "Italic"), fill=(232, 232, 232), anchor="mm")
    if sub:
        d.text((W / 2, 1600), sub, font=font("/usr/share/fonts/opentype/inter/Inter-Medium.otf", 26), fill=(150, 156, 168), anchor="mm")
    return im


def sheet(path):
    from docu import caps_font
    a = scene(CYBER, "Parece un dibujo… pero existe.", 1.0, 40, 880, "TESLA CYBERTRUCK")
    b = scene(ROADSTER, "Nadie lo ha comprobado todavía.", 1.0, 40, 900, "TESLA ROADSTER")
    tiles = []
    for name, im in (("Cybertruck", a), ("Roadster rehecho", b)):
        t = im.resize((540, 960), Image.LANCZOS)
        dd = ImageDraw.Draw(t, "RGBA")
        dd.rounded_rectangle([20, 190, 520, 250], radius=14, fill=(255, 255, 255, 30))
        dd.text((270, 220), name, font=caps_font(30, "ExtraBold"), fill=(255, 255, 255), anchor="mm")
        tiles.append(t)
    out = Image.new("RGB", (1092, 960), (255, 255, 255))
    out.paste(tiles[0], (0, 0))
    out.paste(tiles[1], (552, 0))
    out.save(path, quality=90)
