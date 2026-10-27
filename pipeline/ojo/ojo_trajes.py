"""Ojo (stickman con el ojo del logo 21) con algo más de personalidad: 4 trajes + fotos de perfil en primer plano. 21/10."""
import math, random
from PIL import Image, ImageDraw, ImageFont
import ojo_viejo as OV
from ojo_viejo import N, K, R, WH, BGP, IX, IB, OUT

SS = N.SS
GRAY = (236, 236, 238)


def coat(p, col=WH):
    p.poly([(440, 445), (560, 445), (650, 810), (350, 810)], col + (255,))
    p.stroke([(440, 445), (560, 445), (650, 810), (350, 810), (440, 445)], 9)
    p.stroke([(452, 450), (500, 575), (548, 450)], 8)
    p.stroke([(548, 640), (612, 640), (620, 700), (556, 700), (548, 640)], 7)
    p.stroke([(585, 600), (590, 655)], 8, R)


def bow(p):
    p.poly([(500, 462), (450, 432), (450, 492)], R + (255,))
    p.poly([(500, 462), (550, 432), (550, 492)], R + (255,))
    p.dot(500, 462, 14, R)


def hair(p, seed=3):
    rr = random.Random(seed)
    pts = []
    n = 26
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        r = (230 if i % 2 else 150) + rr.uniform(-15, 25)
        pts.append((500 + math.cos(a) * r * 1.05, 285 + math.sin(a) * r * 0.75))
    p.poly(pts, GRAY + (255,))
    p.stroke(pts + [pts[0]], 9)


def goggles(p):
    p.stroke([(330, 205), (670, 205)], 16)
    for x in (438, 562):
        p.dot(x, 200, 54, K)
        p.dot(x, 200, 40, (170, 220, 245))
        p.d.ellipse([(x - 26) * SS, (184) * SS, (x - 8) * SS, (202) * SS], fill=WH)


def flask(p, x, y):
    p.poly([(x - 14, y - 70), (x + 14, y - 70), (x + 14, y - 20), (x + 60, y + 60), (x - 60, y + 60), (x - 14, y - 20)], WH + (255,))
    p.poly([(x - 34, y + 15), (x + 34, y + 15), (x + 60, y + 60), (x - 60, y + 60)], R + (255,))
    p.stroke([(x - 14, y - 70), (x - 14, y - 20), (x - 60, y + 60), (x + 60, y + 60), (x + 14, y - 20), (x + 14, y - 70)], 8)
    p.stroke([(x - 24, y - 72), (x + 24, y - 72)], 10)
    for bx, by, r in ((x + 5, y - 100, 12), (x - 14, y - 135, 9), (x + 12, y - 165, 7)):
        p.d.ellipse([(bx - r) * SS, (by - r) * SS, (bx + r) * SS, (by + r) * SS], outline=K, width=int(6 * SS))


def cap(p):
    p.poly([(500, 150), (690, 205), (500, 260), (310, 205)], K + (255,))
    p.poly([(410, 215), (590, 215), (590, 262), (410, 262)], K + (255,))
    p.stroke([(670, 205), (690, 320)], 7, R)
    p.dot(690, 322, 14, R)


def pointer(p, x, y):
    p.stroke([(x, y), (x + 120, y - 60)], 10, (120, 78, 46))
    p.dot(x + 120, y - 60, 10, R)


def helmet(p):
    p.d.chord([340 * SS, 120 * SS, 660 * SS, 360 * SS], 180, 360, fill=(222, 196, 140), outline=K, width=int(9 * SS))
    p.stroke([(300, 240), (700, 240)], 22, (200, 170, 110))
    p.stroke([(300, 240), (700, 240)], 6)
    p.stroke([(380, 222), (620, 222)], 12, R)


def magnifier(p, x, y):
    p.stroke([(x, y), (x - 50, y + 70)], 18, (120, 78, 46))
    p.d.ellipse([(x - 10) * SS, (y - 110) * SS, (x + 110) * SS, (y + 10) * SS], fill=(210, 235, 250), outline=K, width=int(12 * SS))


def make(kind, pose):
    p = N.Pen()
    if kind in ("cient", "loco", "prof"):
        coat(p, WH if kind != "prof" else (60, 64, 80))
    if kind == "loco":
        hair(p)
    N._pose(p, pose, 0.0, (0.06, 0.0), 0.0)
    if kind == "cient":
        bow(p)
        flask(p, 330, 640)
        goggles(p)
    elif kind == "loco":
        goggles(p)
        bow(p)
    elif kind == "prof":
        bow(p)
        cap(p)
        pointer(p, 880, 400)
    elif kind == "expl":
        helmet(p)
        magnifier(p, 330, 720)
    return p.im.resize((N.W0 // 2, N.H0 // 2), Image.LANCZOS)


TRAJES = [("Científico", "cient", "wave"), ("Científico despeinado", "loco", "wave"), ("Profesor", "prof", "point"), ("Explorador", "expl", "wave")]


def profile(kind, pose, bg):
    f = make(kind, pose)
    im = Image.new("RGB", (600, 600), bg)
    big = f.resize((820, 984), Image.LANCZOS)
    im.paste(big, (-110, -40), big)
    return im


if __name__ == "__main__":
    sheet = Image.new("RGB", (4 * 330 + 50, 2 * 470 + 40), (16, 16, 20))
    dd = ImageDraw.Draw(sheet)
    for i, (nm, kind, pose) in enumerate(TRAJES):
        f = make(kind, pose)
        im = Image.new("RGB", (500, 600), BGP)
        im.paste(f, (0, 0), f)
        im.save(OUT + f"ojo_traje_{kind}.png")
        x = 10 + i * 340
        dd.text((x + 4, 30), f"{chr(65 + i)} · {nm}", font=ImageFont.truetype(IB, 26), fill=(255, 255, 255), anchor="lm")
        sheet.paste(im.resize((330, 396), Image.LANCZOS), (x, 56))
        pf = profile(kind, pose, R)
        pf.save(OUT + f"ojo_perfil_{kind}.png")
        m = Image.new("L", (330, 330), 0)
        ImageDraw.Draw(m).ellipse([0, 0, 329, 329], fill=255)
        sheet.paste(pf.resize((330, 330), Image.LANCZOS), (x, 520), m)
    dd.text((14, 492), "Fotos de perfil (primer plano, sin texto: en el móvil se ven más grandes)", font=ImageFont.truetype(IB, 24), fill=(255, 210, 60), anchor="lm")
    sheet.save(OUT + "ojo_trajes.jpg", quality=92)
    print("ok")
