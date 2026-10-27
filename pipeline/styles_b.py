"""Otros cuatro estilos muy distintos (21/10, Iker: «a parte del estilo pixel créame otros 3 o 4 totalmente diferentes»):
low-poly 3D, plastilina, boceto a lápiz y acuarela. Mismo Tesla Roadster de perfil (styles4.PROFILE)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import styles4 as S4

W, H = 1080, 1920


def _mask(pts):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def _emask(box):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse(box, fill=255)
    return m


def _car_geo(s=1.0, ox=40, oy=820):
    prof = S4._prof(s, ox, oy)
    wind = S4._wind(s, ox, oy)
    wh = [(ox + cx * s, oy + cy * s, r * s) for cx, cy, r in S4.WH]
    return prof, wind, wh


# ------------------------------------------------------------------ 1 · low-poly 3D
def _facets(img, mask, base, light=(-0.5, -0.8), seed=1, step=46, contrast=0.32):
    rng = np.random.default_rng(seed)
    bb = mask.getbbox()
    if not bb:
        return
    x0, y0, x1, y1 = bb
    xs = np.arange(x0 - step, x1 + step * 2, step)
    ys = np.arange(y0 - step, y1 + step * 2, step)
    pts = {(i, j): (x + rng.uniform(-step * 0.35, step * 0.35), y + rng.uniform(-step * 0.35, step * 0.35)) for i, x in enumerate(xs) for j, y in enumerate(ys)}
    lay = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(lay)
    lx, ly = light
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            a, b, c, e = pts[(i, j)], pts[(i + 1, j)], pts[(i + 1, j + 1)], pts[(i, j + 1)]
            for tri in ((a, b, c), (a, c, e)):
                cy_ = sum(p[1] for p in tri) / 3
                v = (cy_ - y0) / max(1, (y1 - y0))
                k = 1.0 + contrast * (0.5 - v) + rng.uniform(-0.12, 0.12)
                d.polygon(tri, fill=tuple(int(max(0, min(255, cch * k))) for cch in base))
    img.paste(lay, (0, 0), mask)


def lowpoly():
    img = Image.new("RGB", (W, H))
    sky = _mask([(0, 0), (W, 0), (W, 1100), (0, 1100)])
    _facets(img, sky, (60, 120, 200), seed=2, step=120, contrast=0.6)
    for k, (pts, col) in enumerate((([(0, 1000), (180, 720), (380, 900), (560, 660), (800, 880), (1080, 700), (1080, 1150), (0, 1150)], (90, 110, 150)),
                                    ([(0, 1080), (260, 900), (520, 1040), (760, 920), (1080, 1020), (1080, 1200), (0, 1200)], (60, 140, 90)))):
        _facets(img, _mask(pts), col, seed=3 + k, step=80, contrast=0.5)
    _facets(img, _mask([(0, 1150), (W, 1150), (W, H), (0, H)]), (70, 72, 84), seed=9, step=90, contrast=0.2)
    prof, wind, wh = _car_geo(oy=840)
    _facets(img, _mask(prof), (200, 20, 34), seed=5, step=38, contrast=0.9)
    _facets(img, _mask(wind), (40, 60, 100), seed=6, step=30, contrast=1.0)
    d = ImageDraw.Draw(img)
    for X, Y, r in wh:
        oct_ = [(X + math.cos(a) * r, Y + math.sin(a) * r) for a in np.linspace(0, 2 * math.pi, 9)[:-1]]
        d.polygon(oct_, fill=(28, 28, 34))
        hexi = [(X + math.cos(a + 0.3) * r * 0.55, Y + math.sin(a + 0.3) * r * 0.55) for a in np.linspace(0, 2 * math.pi, 7)[:-1]]
        d.polygon(hexi, fill=(180, 186, 196))
        d.polygon(hexi[:3] + [(X, Y)], fill=(210, 214, 224))
    return img


# ------------------------------------------------------------------ 2 · plastilina
def _clay(img, mask, col, seed=1, bevel=14):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, 6, (H, W))
    base = np.array(col, np.float32)[None, None, :] + noise[..., None]
    tex = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    soft = mask.filter(ImageFilter.GaussianBlur(bevel))
    hi = ImageChops.subtract(soft, ImageChops.offset(soft, 9, 12))
    lo = ImageChops.subtract(soft, ImageChops.offset(soft, -9, -12))
    sh = mask.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.5))
    img.paste((40, 30, 30), (10, 16), sh)
    img.paste(tex, (0, 0), mask)
    img.paste((255, 255, 255), (0, 0), ImageChops.multiply(hi.point(lambda v: min(255, v * 3)), mask).point(lambda v: int(v * 0.55)))
    img.paste((0, 0, 0), (0, 0), ImageChops.multiply(lo.point(lambda v: min(255, v * 3)), mask).point(lambda v: int(v * 0.45)))


def clay():
    img = Image.new("RGB", (W, H), (250, 214, 160))
    _clay(img, _emask([660, 300, 960, 600]), (255, 200, 60), 1)
    _clay(img, _mask([(0, 1050), (200, 860), (420, 980), (640, 820), (900, 960), (1080, 880), (1080, 1300), (0, 1300)]), (110, 190, 110), 2)
    _clay(img, _mask([(0, 1160), (W, 1160), (W, H), (0, H)]), (150, 140, 130), 3)
    prof, wind, wh = _car_geo(oy=860)
    _clay(img, _mask(prof), (220, 40, 50), 4, 18)
    _clay(img, _mask(wind), (90, 150, 210), 5, 8)
    for i, (X, Y, r) in enumerate(wh):
        _clay(img, _emask([X - r, Y - r, X + r, Y + r]), (50, 46, 52), 6 + i, 10)
        _clay(img, _emask([X - r * 0.5, Y - r * 0.5, X + r * 0.5, Y + r * 0.5]), (220, 220, 210), 8 + i, 6)
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(3)
    for _ in range(40):              # huellas
        x, y = rng.uniform(80, 1000), rng.uniform(870, 1110)
        d.arc([x - 14, y - 10, x + 14, y + 10], 200, 340, fill=(120, 10, 20, 60), width=2)
    return img


# ------------------------------------------------------------------ 3 · boceto a lápiz
def _jline(d, pts, col, w, rng, j=2.5, passes=3):
    for _ in range(passes):
        q = [(x + rng.uniform(-j, j), y + rng.uniform(-j, j)) for x, y in pts]
        d.line(q, fill=col, width=w, joint="curve")


def sketch():
    img = Image.new("RGB", (W, H), (250, 246, 232))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(140, H, 54):
        d.line([(0, y), (W, y)], fill=(150, 180, 220, 110), width=2)
    d.line([(110, 0), (110, H)], fill=(230, 120, 120, 140), width=3)
    rng = random.Random(7)
    prof, wind, wh = _car_geo(oy=800)
    # relleno con lápiz rojo a trazos
    m = _mask(prof)
    hat = Image.new("L", (W, H), 0)
    hd = ImageDraw.Draw(hat)
    for k in range(-400, 1400, 9):
        hd.line([(k, 1100), (k + 300, 760)], fill=150 + rng.randint(0, 80), width=3)
    img.paste((205, 40, 50), (0, 0), ImageChops.multiply(m, hat))
    cross = Image.new("L", (W, H), 0)
    cd = ImageDraw.Draw(cross)
    for k in range(-400, 1400, 12):
        cd.line([(k, 760), (k + 300, 1100)], fill=170, width=2)
    low = _mask([(0, 1010), (W, 1000), (W, 1100), (0, 1100)])
    img.paste((70, 60, 70), (0, 0), ImageChops.multiply(ImageChops.multiply(m, cross), low))
    d = ImageDraw.Draw(img, "RGBA")
    _jline(d, prof + [prof[0]], (40, 40, 50, 200), 3, rng)
    _jline(d, wind + [wind[0]], (40, 40, 50, 200), 3, rng)
    for X, Y, r in wh:
        circ = [(X + math.cos(a) * r, Y + math.sin(a) * r) for a in np.linspace(0, 2 * math.pi, 40)]
        _jline(d, circ, (30, 30, 40, 220), 4, rng, 2.0)
        circ2 = [(X + math.cos(a) * r * 0.55, Y + math.sin(a) * r * 0.55) for a in np.linspace(0, 2 * math.pi, 30)]
        _jline(d, circ2, (60, 60, 70, 200), 3, rng, 1.5)
    _jline(d, [(60, 1080), (1020, 1074)], (60, 60, 70, 160), 3, rng, 3)
    # notas a mano
    from docu import font, F_TITLE
    fo = font(F_TITLE, 64, "SemiBold Italic")
    d.text((160, 560), "Tesla Roadster", font=fo, fill=(40, 40, 60, 230))
    _jline(d, [(160, 650), (640, 646)], (205, 40, 50, 200), 4, rng, 2)
    d.text((620, 1170), "← 0 a 97 km/h en 0,81 s", font=font(F_TITLE, 44, "SemiBold Italic"), fill=(40, 40, 60, 220), anchor="mm")
    return img


# ------------------------------------------------------------------ 4 · acuarela
def _wash(img, mask, col, seed=1, alpha=0.85, edge=0.55):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (H // 8, W // 8))
    n = np.array(Image.fromarray(((n - n.min()) / (np.ptp(n) + 1e-9) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(10)), np.float32) / 255
    m = np.array(mask.filter(ImageFilter.GaussianBlur(3)), np.float32) / 255
    mm = np.clip(m * (0.75 + 0.5 * n) - 0.1, 0, 1)
    soft = np.array(mask.filter(ImageFilter.GaussianBlur(10)), np.float32) / 255
    rim = np.clip((m - soft) * 4, 0, 1) * edge                      # borde más oscuro, como el agua al secar
    a = np.clip(mm * alpha + rim, 0, 1)
    gran = rng.normal(0, 0.06, (H, W))
    out = np.array(img, np.float32)
    c = np.array(col, np.float32)[None, None, :] * (1 - rim[..., None] * 0.45 + gran[..., None])
    out = out * (1 - a[..., None] * 0.9) + c * a[..., None] * 0.9
    img.paste(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)))


def watercolor():
    rng = np.random.default_rng(1)
    paper = np.full((H, W, 3), (246, 241, 228), np.float32) + rng.normal(0, 4, (H, W, 1))
    img = Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8))
    _wash(img, _mask([(0, 0), (W, 0), (W, 1000), (0, 1000)]), (120, 170, 220), 2, 0.55)
    _wash(img, _emask([650, 320, 950, 620]), (255, 190, 90), 3, 0.8)
    _wash(img, _mask([(0, 1020), (200, 840), (420, 960), (660, 800), (900, 940), (1080, 860), (1080, 1250), (0, 1250)]), (110, 170, 120), 4, 0.7)
    _wash(img, _mask([(0, 1150), (W, 1150), (W, H), (0, H)]), (130, 128, 136), 5, 0.6)
    prof, wind, wh = _car_geo(oy=850)
    _wash(img, _mask(prof), (200, 30, 44), 6, 0.95, 0.8)
    _wash(img, _mask(wind), (60, 80, 120), 7, 0.9)
    for i, (X, Y, r) in enumerate(wh):
        _wash(img, _emask([X - r, Y - r, X + r, Y + r]), (40, 40, 50), 8 + i, 0.95)
        _wash(img, _emask([X - r * 0.5, Y - r * 0.5, X + r * 0.5, Y + r * 0.5]), (200, 200, 205), 10 + i, 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(110, 1036), (470, 1012)], fill=(255, 255, 255, 170), width=8)
    return img


def sheet(path):
    from docu import caps_font
    fns = [("1 · Low-poly 3D", lowpoly), ("2 · Plastilina", clay), ("3 · Boceto a lápiz", sketch), ("4 · Acuarela", watercolor)]
    tiles = []
    for name, fn in fns:
        im = fn().resize((432, 768), Image.LANCZOS)
        dd = ImageDraw.Draw(im, "RGBA")
        dd.rounded_rectangle([16, 16, 416, 76], radius=14, fill=(0, 0, 0, 170))
        dd.text((216, 46), name, font=caps_font(28, "ExtraBold"), fill=(255, 255, 255), anchor="mm")
        tiles.append(im)
    out = Image.new("RGB", (432 * 2 + 12, 768 * 2 + 12), (255, 255, 255))
    for k, t in enumerate(tiles):
        out.paste(t, ((k % 2) * 444, (k // 2) * 780))
    out.save(path, quality=90)
