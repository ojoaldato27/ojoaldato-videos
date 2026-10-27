"""Muestras de los formatos virales que se pueden hacer aquí sin IA (21/10): tipo The Paint Explainer (monigotes estilo
Paint), pantalla partida con minijuego en pixel art y documental oscuro tipo fern. Tesla Roadster con su perfil real."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import styles4 as S4
from docu import font, caps_font, F_UI_B

W, H = 1080, 1920
ARIAL = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def _wobble(pts, rng, j=3.0):
    return [(x + rng.uniform(-j, j), y + rng.uniform(-j, j)) for x, y in pts]


# ------------------------------------------------------------------ 3 · tipo The Paint Explainer
def paint():
    rng = random.Random(4)
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    fo = font(ARIAL, 74) if True else None
    d.text((W / 2, 250), "ESTE COCHE", font=fo, fill=(0, 0, 0), anchor="mm")
    d.text((W / 2, 340), "VA BOCA ABAJO", font=fo, fill=(0, 0, 0), anchor="mm")
    # techo del túnel
    d.line([(40, 640), (1040, 640)], fill=(0, 0, 0), width=8)
    for k in range(60, 1040, 60):
        d.line([(k, 640), (k - 30, 610)], fill=(0, 0, 0), width=4)
    # coche boca abajo pegado al techo (relleno plano tipo bote de pintura, borde negro tembloroso)
    s, ox, oy = 0.9, 90, 0
    prof = [(ox + x * s, 640 + (262 - y) * s) for x, y in S4._prof(1, 0, 0, 5)]
    prof = _wobble(prof, rng, 2.5)
    d.polygon(prof, fill=(237, 28, 36))
    d.line(prof + [prof[0]], fill=(0, 0, 0), width=7)
    wind = [(ox + x * s, 640 + (262 - y) * s) for x, y in S4._wind(1, 0, 0)]
    d.polygon(_wobble(wind, rng, 2), fill=(153, 217, 234), outline=(0, 0, 0))
    for cx, cy, r in S4.WH:
        X, Y, R = ox + cx * s, 640 + (262 - cy) * s, r * s
        d.ellipse([X - R, Y - R, X + R, Y + R], fill=(0, 0, 0))
        d.ellipse([X - R * 0.4, Y - R * 0.4, X + R * 0.4, Y + R * 0.4], fill=(195, 195, 195))
    # flechas de succión
    for x in (300, 540, 780):
        d.line([(x, 1000), (x, 900)], fill=(0, 162, 232), width=9)
        d.polygon([(x - 26, 905), (x + 26, 905), (x, 862)], fill=(0, 162, 232))
    # monigote que flipa
    mx, my = 760, 1380
    d.ellipse([mx - 70, my - 70, mx + 70, my + 70], fill=(255, 255, 255), outline=(0, 0, 0), width=7)
    d.ellipse([mx - 34, my - 22, mx - 10, my + 2], fill=(0, 0, 0))
    d.ellipse([mx + 10, my - 22, mx + 34, my + 2], fill=(0, 0, 0))
    d.ellipse([mx - 18, my + 22, mx + 18, my + 52], fill=(0, 0, 0))
    d.line([(mx, my + 70), (mx, my + 260)], fill=(0, 0, 0), width=8)
    d.line([(mx, my + 120), (mx - 110, my + 40)], fill=(0, 0, 0), width=8)
    d.line([(mx, my + 120), (mx + 110, my + 40)], fill=(0, 0, 0), width=8)
    d.line([(mx, my + 260), (mx - 70, my + 380)], fill=(0, 0, 0), width=8)
    d.line([(mx, my + 260), (mx + 70, my + 380)], fill=(0, 0, 0), width=8)
    d.text((mx, my - 130), "¿¿QUÉ??", font=font(ARIAL, 70), fill=(0, 0, 0), anchor="mm")
    d.text((300, 1500), "ventiladores", font=font(ARIAL, 48), fill=(0, 162, 232), anchor="mm")
    d.line([(300, 1460), (330, 1020)], fill=(0, 162, 232), width=5)
    # subtítulo
    d.text((W / 2, 1090), "lo ", font=font(ARIAL, 64), fill=(0, 0, 0), anchor="rm")
    d.text((W / 2, 1090), "CHUPAN", font=font(ARIAL, 64), fill=(237, 28, 36), anchor="lm")
    return im


# ------------------------------------------------------------------ 4 · pantalla partida con minijuego
def split():
    top = Image.new("RGB", (W, H // 2), (14, 16, 30))
    d = ImageDraw.Draw(top, "RGBA")
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H // 2)], fill=(255, 255, 255, 14))
    car = S4.pixel().crop((0, 600, W, 1560)).resize((W, H // 2), Image.NEAREST)
    top = car
    d = ImageDraw.Draw(top, "RGBA")
    d.rounded_rectangle([60, 70, 1020, 200], radius=24, fill=(0, 0, 0, 170))
    d.text((W / 2, 135), "0 a 97 km/h en 0,81 s", font=caps_font(58, "Black"), fill=(255, 255, 255), anchor="mm")
    # abajo: plataformas pixel que corren solas
    px = 6
    w, h = W // px, (H // 2) // px
    g = Image.new("RGB", (w, h), (92, 148, 252))
    gd = ImageDraw.Draw(g)
    rng = random.Random(8)
    for k in range(6):
        x = rng.randrange(w)
        y = rng.randrange(10, 50)
        gd.ellipse([x, y, x + 24, y + 10], fill=(255, 255, 255))
    gd.rectangle([0, h - 26, w, h], fill=(200, 76, 12))
    for x in range(0, w, 8):
        gd.rectangle([x, h - 26, x + 7, h - 20], fill=(240, 150, 60))
    for bx, by, bw in ((30, 100, 24), (80, 80, 32), (130, 104, 20)):
        gd.rectangle([bx, by, bx + bw, by + 6], fill=(230, 120, 30))
        gd.rectangle([bx, by, bx + bw, by + 1], fill=(255, 200, 120))
    for cx in (40, 92, 140):
        gd.ellipse([cx, 70, cx + 6, 78], fill=(255, 214, 0))
    # personaje (el ojo de la mascota) saltando
    hx, hy = 64, 112
    gd.ellipse([hx - 7, hy - 14, hx + 7, hy - 4], fill=(255, 255, 255), outline=(0, 0, 0))
    gd.ellipse([hx - 2, hy - 11, hx + 2, hy - 7], fill=(255, 196, 0))
    gd.line([(hx, hy - 4), (hx, hy + 6)], fill=(255, 255, 255))
    gd.line([(hx, hy + 6), (hx - 4, hy + 12)], fill=(255, 255, 255))
    gd.line([(hx, hy + 6), (hx + 4, hy + 12)], fill=(255, 255, 255))
    gd.rectangle([170, h - 34, 178, h - 26], fill=(120, 60, 20))
    game = g.resize((w * px, h * px), Image.NEAREST)
    gd2 = ImageDraw.Draw(game)
    gd2.text((30, 30), "MONEDAS × 27", font=caps_font(36, "Black"), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(top, (0, 0))
    out.paste(game.crop((0, 0, W, H // 2)), (0, H // 2))
    od = ImageDraw.Draw(out)
    od.rectangle([0, H // 2 - 4, W, H // 2 + 4], fill=(255, 255, 255))
    od.text((W / 2, H // 2 - 90), "Y PUEDE IR", font=caps_font(80, "Black"), fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    od.text((W / 2, H // 2 + 6), "BOCA ABAJO", font=caps_font(80, "Black"), fill=(255, 214, 0), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    return out


# ------------------------------------------------------------------ 5 · documental oscuro tipo fern
def fern():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    # niebla y luz volumétrica desde arriba
    base = np.full((H, W, 3), (8, 10, 14), np.float32)
    beam = np.clip(1 - np.abs((xs - 540) - (ys - 300) * 0.18) / (180 + ys * 0.25), 0, 1) * np.clip((ys - 120) / 900, 0, 1) * (ys < 1300)
    base += beam[..., None] * np.array((120, 130, 140), np.float32) * 0.55
    fog = np.clip(1 - np.abs(ys - 1180) / 260, 0, 1)
    base += fog[..., None] * np.array((30, 34, 40), np.float32)
    rng = np.random.default_rng(2)
    base += rng.normal(0, 3, (H, W, 1))
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 1200, W, H], fill=(6, 7, 9, 255))
    # coche en silueta con reflejo de la luz en el contorno superior
    s, ox, oy = 1.0, 40, 940
    prof = S4._prof(s, ox, oy)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon(prof, fill=255)
    im.paste((12, 12, 14), (0, 0), m)
    edge = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(5)))
    top = Image.fromarray((np.clip((1250 - ys) / 300, 0, 1) * 255).astype(np.uint8))
    rim = ImageChops.multiply(edge, top).filter(ImageFilter.GaussianBlur(1.5))
    im.paste((200, 210, 220), (0, 0), rim)
    d = ImageDraw.Draw(im, "RGBA")
    for cx, cy, r in S4.WH:
        X, Y = ox + cx, oy + cy
        d.ellipse([X - r, Y - r, X + r, Y + r], fill=(10, 10, 12), outline=(60, 64, 70), width=2)
    d.line([(ox + 30, oy + 228), (ox + 120, oy + 212)], fill=(230, 236, 255), width=5)
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse([ox - 60, oy + 170, ox + 220, oy + 270], fill=160)
    im.paste((200, 210, 255), (0, 0), glow.filter(ImageFilter.GaussianBlur(30)))
    # bandas de cine y subtítulo sobrio
    d.rectangle([0, 0, W, 170], fill=(0, 0, 0))
    d.rectangle([0, H - 170, W, H], fill=(0, 0, 0))
    d.text((W / 2, 1500), "Nadie lo ha comprobado todavía.", font=font("/home/claude/shorts-ingenieria/fonts/PlayfairDisplay-Italic.ttf", 54, "Italic"),
           fill=(230, 230, 230), anchor="mm")
    return im


def sheet(path):
    fns = [("3 · Tipo Paint Explainer", paint), ("4 · Pantalla partida", split), ("5 · Documental tipo fern", fern)]
    tiles = []
    for name, fn in fns:
        im = fn().resize((432, 768), Image.LANCZOS)
        dd = ImageDraw.Draw(im, "RGBA")
        dd.rounded_rectangle([16, 16, 416, 76], radius=14, fill=(0, 0, 0, 190))
        dd.text((216, 46), name, font=caps_font(26, "ExtraBold"), fill=(255, 255, 255), anchor="mm")
        tiles.append(im)
    out = Image.new("RGB", (432 * 3 + 24, 768), (255, 255, 255))
    for k, t in enumerate(tiles):
        out.paste(t, (k * 444, 0))
    out.save(path, quality=90)
