"""Tres variantes más de pixel art (21/10, Iker: «el de pixel me gusta pero genera 3 más diferentes»):
A · Game Boy (4 tonos verdes, 8 bits), B · Arcade de carreras (vista trasera, carretera en perspectiva, atardecer),
C · Isométrico (diorama de ciudad con el coche en la calle). Todo dibujado a baja resolución y ampliado sin suavizar."""
import math, random
from PIL import Image, ImageDraw
import styles4 as S4

W, H = 1080, 1920


def _up(im, px):
    return im.resize((im.width * px, im.height * px), Image.NEAREST).crop((0, 0, W, H))


# ------------------------------------------------------------------ A · Game Boy
def gameboy():
    px = 8
    w, h = W // px + 1, H // px + 1               # 136 × 241
    G = [(15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)]
    im = Image.new("RGB", (w, h), G[3])
    d = ImageDraw.Draw(im)
    rng = random.Random(5)
    for _ in range(18):
        x, y = rng.randrange(w), rng.randrange(10, 80)
        d.rectangle([x, y, x + rng.randint(6, 14), y + 2], fill=G[2])
    d.ellipse([88, 22, 116, 50], fill=G[2])
    d.polygon([(0, 128), (24, 104), (46, 120), (72, 98), (100, 122), (136, 102), (136, 140), (0, 140)], fill=G[1])
    for k in range(10):
        x0 = k * 14
        hh = rng.randint(8, 22)
        d.rectangle([x0, 140 - hh, x0 + 11, 140], fill=G[0])
        for wy in range(140 - hh + 3, 139, 4):
            d.point((x0 + 3, wy), fill=G[2])
            d.point((x0 + 7, wy), fill=G[2] if rng.random() < 0.5 else G[0])
    d.rectangle([0, 140, w, h], fill=G[1])
    d.rectangle([0, 140, w, 141], fill=G[0])
    for x in range(0, w, 12):
        d.rectangle([x, 160, x + 6, 161], fill=G[3])
    s, ox, oy = 0.13, 3, 120
    prof = [(round(x), round(y)) for x, y in S4._prof(s, ox, oy, 3)]
    d.polygon(prof, fill=G[0])
    d.polygon([(round(x), round(y)) for x, y in S4._wind(s, ox, oy)], fill=G[2])
    d.line([(ox + 30 * s, oy + 190 * s), (ox + 900 * s, oy + 166 * s)], fill=G[1])
    for cx, cy, r in S4.WH:
        X, Y, R = ox + cx * s, oy + cy * s, r * s
        d.ellipse([X - R, Y - R, X + R, Y + R], fill=G[0])
        d.ellipse([X - R * 0.5, Y - R * 0.5, X + R * 0.5, Y + R * 0.5], fill=G[2])
    # marco de consola alrededor de la pantalla
    big = _up(im, px)
    fr = Image.new("RGB", (W, H), (196, 192, 186))
    fd = ImageDraw.Draw(fr)
    fd.rounded_rectangle([60, 260, 1020, 1500], radius=40, fill=(80, 82, 96))
    fr.paste(big.crop((0, 240, 860, 1340)).resize((860, 1100), Image.NEAREST), (110, 330))
    fd.text((540, 1580), "Nintendo-ish", fill=(60, 60, 140)) if False else None
    for cx, cy in ((260, 1700), (820, 1660), (920, 1760)):
        fd.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=(150, 30, 80))
    fd.rectangle([200, 1690, 320, 1710], fill=(40, 40, 46))
    fd.rectangle([250, 1640, 270, 1760], fill=(40, 40, 46))
    return fr


# ------------------------------------------------------------------ B · arcade de carreras (vista trasera)
def arcade():
    px = 5
    w, h = W // px, H // px                       # 216 × 384
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    sky = [(40, 10, 70), (90, 20, 100), (160, 40, 120), (230, 80, 110), (255, 140, 90), (255, 200, 110)]
    hz = 170
    bh = hz // len(sky)
    for i, c in enumerate(sky):
        d.rectangle([0, i * bh, w, (i + 1) * bh], fill=c)
    d.ellipse([70, 80, 146, 156], fill=(255, 230, 120))
    for k in range(5):
        y0 = 120 + k * 8
        d.rectangle([60, y0, 156, y0 + 2 + k], fill=sky[4])
    d.polygon([(0, hz), (30, 150), (60, hz - 6), (100, 146), (140, hz - 4), (190, 152), (216, hz), ], fill=(70, 30, 90))
    d.rectangle([0, hz, w, h], fill=(50, 120, 60))
    # carretera en perspectiva con franjas alternas
    vx = w // 2
    for y in range(hz, h):
        z = (y - hz) / (h - hz)
        half = 6 + z * 150
        stripe = int((1 / (z + 0.08)) * 6) % 2
        d.line([(0, y), (w, y)], fill=(60, 140, 70) if stripe else (46, 112, 56))
        d.line([(vx - half, y), (vx + half, y)], fill=(90, 90, 100) if stripe else (80, 80, 90))
        d.line([(vx - half - 4 - z * 10, y), (vx - half, y)], fill=(230, 230, 230) if stripe else (220, 40, 40))
        d.line([(vx + half, y), (vx + half + 4 + z * 10, y)], fill=(230, 230, 230) if stripe else (220, 40, 40))
        if stripe and z > 0.05:
            d.line([(vx - 1 - z * 3, y), (vx + 1 + z * 3, y)], fill=(240, 240, 240))
    # palmeras
    for side, x0 in ((-1, 26), (1, 190)):
        for k, (yy, s) in enumerate(((230, 1.0), (200, 0.6))):
            xx = x0 + side * k * -10
            d.line([(xx, yy), (xx + side * 4 * s, yy - 50 * s)], fill=(90, 60, 40), width=max(1, int(3 * s)))
            for a in range(6):
                ang = a * math.pi / 5 + math.pi
                d.line([(xx + side * 4 * s, yy - 50 * s), (xx + side * 4 * s + math.cos(ang) * 22 * s, yy - 50 * s + math.sin(ang) * 10 * s + 6 * s)],
                       fill=(40, 120, 60), width=max(1, int(3 * s)))
    # Roadster visto desde atrás
    cx, by = w // 2, 330
    d.ellipse([cx - 66, by + 8, cx + 66, by + 20], fill=(30, 60, 36))
    d.polygon([(cx - 62, by), (cx - 58, by - 30), (cx - 40, by - 42), (cx + 40, by - 42), (cx + 58, by - 30), (cx + 62, by)], fill=(196, 14, 30))
    d.polygon([(cx - 34, by - 42), (cx - 22, by - 62), (cx + 22, by - 62), (cx + 34, by - 42)], fill=(160, 10, 24))
    d.polygon([(cx - 28, by - 44), (cx - 19, by - 59), (cx + 19, by - 59), (cx + 28, by - 44)], fill=(30, 40, 66))
    d.line([(cx - 52, by - 30), (cx + 52, by - 30)], fill=(255, 40, 60), width=2)
    d.line([(cx - 52, by - 29), (cx + 52, by - 29)], fill=(255, 150, 150))
    d.rectangle([cx - 46, by - 18, cx + 46, by - 10], fill=(110, 6, 16))
    d.rectangle([cx - 10, by - 16, cx + 10, by - 12], fill=(230, 230, 230))
    for sx in (-1, 1):
        d.rectangle([cx + sx * 50 - 9, by - 8, cx + sx * 50 + 9, by + 12], fill=(20, 20, 24))
        d.line([(cx + sx * 50 - 7, by - 4), (cx + sx * 50 + 7, by - 4)], fill=(70, 70, 80))
    return _up(im, px)


# ------------------------------------------------------------------ C · isométrico
def iso():
    px = 6
    w, h = W // px, H // px                       # 180 × 320
    im = Image.new("RGB", (w, h), (30, 34, 60))
    d = ImageDraw.Draw(im)

    def P(x, y, z=0):                             # mundo → pantalla (isométrico 2:1)
        return (90 + (x - y) * 2, 120 + (x + y) - z)

    # suelo y calle
    for gx in range(-20, 21):
        for gy in range(-20, 21):
            road = abs(gy) <= 3
            col = (78, 80, 92) if road else ((70, 150, 80) if (gx + gy) % 2 else (62, 138, 72))
            a, b, c, e = P(gx * 4, gy * 4), P(gx * 4 + 4, gy * 4), P(gx * 4 + 4, gy * 4 + 4), P(gx * 4, gy * 4 + 4)
            d.polygon([a, b, c, e], fill=col)
            if road and gy == 0 and gx % 2 == 0:
                d.line([P(gx * 4, 2), P(gx * 4 + 2, 2)], fill=(240, 220, 120))

    def box(x, y, z, sx, sy, sz, col):
        top = [P(x, y, z + sz), P(x + sx, y, z + sz), P(x + sx, y + sy, z + sz), P(x, y + sy, z + sz)]
        left = [P(x, y + sy, z), P(x + sx, y + sy, z), P(x + sx, y + sy, z + sz), P(x, y + sy, z + sz)]
        right = [P(x + sx, y, z), P(x + sx, y + sy, z), P(x + sx, y + sy, z + sz), P(x + sx, y, z + sz)]
        d.polygon(left, fill=tuple(int(v * 0.72) for v in col))
        d.polygon(right, fill=tuple(int(v * 0.88) for v in col))
        d.polygon(top, fill=col)

    rng = random.Random(4)
    blds = [(-40, -40), (-26, -42), (-10, -40), (6, -44), (22, -40), (-40, 18), (-24, 20), (-8, 18), (8, 22), (26, 18)]
    for bx, by in sorted(blds, key=lambda b: b[0] + b[1]):
        hh = rng.randint(20, 60)
        col = rng.choice([(200, 190, 170), (150, 170, 200), (220, 150, 120), (170, 150, 200)])
        box(bx, by, 0, 12, 12, hh, col)
        for k in range(4, hh - 2, 6):
            a = P(bx + 12, by + 3, k)
            d.point(a, fill=(255, 230, 150))
            d.point(P(bx + 12, by + 8, k), fill=(255, 230, 150))
    # el coche en la calle (cajas con las proporciones del Roadster)
    cx, cy = -4, -3
    for wx in (cx + 3, cx + 15):
        for wy in (cy, cy + 7):
            box(wx, wy, 0, 3, 1, 3, (24, 24, 28))
    box(cx, cy + 0.5, 1.5, 20, 7, 3, (196, 14, 30))
    box(cx + 7, cy + 1, 4.5, 8, 6, 2.2, (36, 48, 80))
    d.point(P(cx + 20, cy + 2, 3), fill=(255, 255, 220))
    d.point(P(cx + 20, cy + 6, 3), fill=(255, 255, 220))
    return _up(im, px)


def sheet(path):
    from docu import caps_font
    fns = [("A · Game Boy", gameboy), ("B · Arcade de carreras", arcade), ("C · Isométrico", iso)]
    tiles = []
    for name, fn in fns:
        im = fn().resize((432, 768), Image.LANCZOS)
        dd = ImageDraw.Draw(im, "RGBA")
        dd.rounded_rectangle([16, 16, 416, 76], radius=14, fill=(0, 0, 0, 170))
        dd.text((216, 46), name, font=caps_font(28, "ExtraBold"), fill=(255, 255, 255), anchor="mm")
        tiles.append(im)
    out = Image.new("RGB", (432 * 3 + 24, 768), (255, 255, 255))
    for k, t in enumerate(tiles):
        out.paste(t, (k * 444, 0))
    out.save(path, quality=90)
