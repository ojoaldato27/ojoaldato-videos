"""8 versiones de Ojo científico (1–8), 21/10."""
import math, random
from PIL import Image, ImageDraw, ImageFont
import ojo_trajes as T
from ojo_trajes import N, K, R, WH, BGP, IB, OUT, SS, coat, bow, hair, goggles, flask

YEL, GRN, BLU, BRN, DG = (255, 204, 48), (60, 190, 90), (120, 190, 240), (110, 70, 40), (40, 70, 55)
FB = ImageFont.truetype("/home/claude/shorts-ingenieria/fonts/permanent-marker.ttf", 40 * SS)


def glasses_round(p):
    """Un solo cristal redondo grande alrededor del ojo (es un cíclope) con las patillas a los lados."""
    p.d.ellipse([285 * SS, 115 * SS, 715 * SS, 545 * SS], outline=K, width=int(12 * SS))
    p.stroke([(285, 320), (220, 300)], 10)
    p.stroke([(715, 320), (780, 300)], 10)
    p.d.arc([320 * SS, 150 * SS, 680 * SS, 510 * SS], 200, 245, fill=(150, 200, 235), width=int(10 * SS))


def strap(p):
    p.stroke([(250, 330), (750, 330)], 26)


def big_goggles(p):
    p.d.ellipse([290 * SS, 210 * SS, 710 * SS, 450 * SS], outline=K, width=int(22 * SS))
    p.d.ellipse([304 * SS, 224 * SS, 696 * SS, 436 * SS], outline=(140, 200, 240), width=int(8 * SS))
    p.d.arc([330 * SS, 240 * SS, 520 * SS, 400 * SS], 200, 250, fill=WH, width=int(12 * SS))


def tube(p, x, y, col=GRN):
    p.d.rounded_rectangle([(x - 22) * SS, (y - 140) * SS, (x + 22) * SS, (y + 20) * SS], radius=22 * SS, fill=WH, outline=K, width=int(7 * SS))
    p.d.rounded_rectangle([(x - 16) * SS, (y - 60) * SS, (x + 16) * SS, (y + 14) * SS], radius=16 * SS, fill=col)
    for k in range(3):
        p.curve((x - 10 + k * 8, y - 160 - k * 30), (x + 20 - k * 4, y - 190 - k * 30), (x - 6 + k * 6, y - 220 - k * 30), 6)


def atom(p, x, y, r=90):
    for k in range(3):
        a0 = k * math.pi / 3
        pts = []
        for i in range(61):
            t = i * 2 * math.pi / 60
            ex, ey = math.cos(t) * r, math.sin(t) * r * 0.36
            pts.append((x + ex * math.cos(a0) - ey * math.sin(a0), y + ex * math.sin(a0) + ey * math.cos(a0)))
        p.stroke(pts, 7)
    p.dot(x, y, 20, R)


def microscope(p, x, y):
    p.d.rectangle([(x - 90) * SS, (y - 20) * SS, (x + 90) * SS, (y + 10) * SS], fill=K)
    p.stroke([(x + 40, y - 20), (x + 40, y - 200), (x - 10, y - 260)], 26)
    p.d.rounded_rectangle([(x - 60) * SS, (y - 330) * SS, (x + 10) * SS, (y - 200) * SS], radius=20 * SS, fill=WH, outline=K, width=int(8 * SS))
    p.stroke([(x - 60, y - 120), (x + 40, y - 120)], 14)


def telescope(p, x, y):
    for dx in (-70, 0, 70):
        p.stroke([(x, y - 200), (x + dx, y)], 10)
    tip = (x + 170, y - 420)
    p.stroke([(x - 70, y - 160), tip], 46)
    p.stroke([(x - 70, y - 160), tip], 30, WH)
    p.stroke([(tip[0] - 20, tip[1] + 10), (tip[0] + 20, tip[1] - 14)], 52, R)
    for (sx, sy, r) in ((x + 260, y - 520, 20), (x + 120, y - 560, 14)):
        N.sparkle(p, sx, sy, r, YEL)


def wrench(p, x, y):
    p.stroke([(x, y), (x - 90, y + 110)], 22, (150, 154, 166))
    p.d.ellipse([(x - 30) * SS, (y - 40) * SS, (x + 30) * SS, (y + 20) * SS], fill=(150, 154, 166), outline=K, width=int(6 * SS))
    p.d.rectangle([(x - 10) * SS, (y - 46) * SS, (x + 10) * SS, (y - 10) * SS], fill=BGP)


def loupe(p):
    p.d.ellipse([560 * SS, 270 * SS, 680 * SS, 390 * SS], fill=(210, 235, 250, ), outline=K, width=int(14 * SS))
    p.stroke([(670, 300), (720, 280)], 22)


def lightning_hair(p):
    hair(p, 7)
    for (x, y) in ((330, 150), (680, 140)):
        p.poly([(x, y), (x + 30, y - 60), (x + 10, y - 60), (x + 40, y - 120), (x - 10, y - 50), (x + 10, y - 50)], YEL + (255,))


def burn(p):
    rr = random.Random(2)
    for _ in range(7):
        x, y = rr.uniform(400, 600), rr.uniform(520, 780)
        p.dot(x, y, rr.uniform(8, 16), (70, 70, 70))


def board(p):
    p.d.rectangle([600 * SS, 60 * SS, 980 * SS, 330 * SS], fill=DG, outline=BRN, width=int(14 * SS))
    for i, s in enumerate(("F = m · a", "c ≈ 300.000 km/s", "H₂O")):
        p.d.text((620 * SS, (90 + i * 75) * SS), s, font=FB, fill=WH)


def ponytail(p):
    p.d.chord([320 * SS, 160 * SS, 680 * SS, 380 * SS], 180, 360, fill=BRN, outline=K, width=int(8 * SS))
    p.d.ellipse([640 * SS, 200 * SS, 760 * SS, 420 * SS], fill=BRN, outline=K, width=int(8 * SS))
    p.dot(650, 250, 18, R)


V = [
    ("Clásico", "wave", lambda p: coat(p), lambda p: (bow(p), glasses_round(p), flask(p, 330, 640))),
    ("Químico", "wave", lambda p: (strap(p), coat(p)), lambda p: (big_goggles(p), tube(p, 330, 720))),
    ("Físico", "wave", lambda p: coat(p), lambda p: (bow(p), atom(p, 800, 210))),
    ("Biólogo", "point", lambda p: coat(p), lambda p: (glasses_round(p), microscope(p, 840, 1060))),
    ("Astrónomo", "think", lambda p: coat(p, (40, 50, 90)), lambda p: telescope(p, 780, 1060)),
    ("Inventor", "wave", lambda p: coat(p), lambda p: (loupe(p), burn(p), wrench(p, 330, 720))),
    ("Científico loco", "surprise", lambda p: (coat(p), None), lambda p: (lightning_hair(p), burn(p))),
    ("Profe de ciencias", "point", lambda p: (board(p), coat(p)), lambda p: (glasses_round(p), bow(p))),
]

if __name__ == "__main__":
    sheet = Image.new("RGB", (4 * 330 + 50, 4 * 430 + 60), (16, 16, 20))
    dd = ImageDraw.Draw(sheet)
    for i, (nm, pose, pre, post) in enumerate(V):
        p = N.Pen()
        if nm == "Científico loco":
            hair(p, 7)
        pre(p)
        N._pose(p, pose, 0.0, (0.06, 0.0), 0.0)
        post(p)
        f = p.im.resize((N.W0 // 2, N.H0 // 2), Image.LANCZOS)
        im = Image.new("RGB", (500, 600), BGP)
        im.paste(f, (0, 0), f)
        im.save(OUT + f"ojo_cient_{i + 1}.png")
        col, row = i % 4, (i // 4) * 2
        x, y = 10 + col * 340, 10 + row * 440
        dd.text((x + 4, y + 22), f"{i + 1} · {nm}", font=ImageFont.truetype(IB, 26), fill=(255, 255, 255), anchor="lm")
        sheet.paste(im.resize((300, 360), Image.LANCZOS), (x + 15, y + 44))
        pf = Image.new("RGB", (600, 600), R)
        big = f.resize((820, 984), Image.LANCZOS)
        pf.paste(big, (-110, -20), big)
        pf.save(OUT + f"ojo_cient_perfil_{i + 1}.png")
        m = Image.new("L", (300, 300), 0)
        ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=255)
        sheet.paste(pf.resize((300, 300), Image.LANCZOS), (x + 15, y + 460), m)
    sheet.save(OUT + "ojo_cientificos.jpg", quality=92)
    print("ok")
