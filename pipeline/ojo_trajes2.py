"""8 personajes más para Ojo (E–L), 21/10: astronauta, detective, reportero, piloto de F1, mago, callejero, ingeniero de obra, romano."""
import math
from PIL import Image, ImageDraw, ImageFont
import ojo_trajes as T
from ojo_trajes import N, K, R, WH, BGP, IB, OUT, SS, coat, bow, magnifier

YEL, ORA, BLU, PUR, BRN, GRN = (255, 204, 48), (255, 130, 30), (60, 120, 220), (120, 70, 200), (150, 100, 60), (70, 150, 70)


def astronauta_pre(p):
    p.poly([(410, 470), (590, 470), (600, 720), (400, 720)], (150, 154, 166, 255))
    p.d.rounded_rectangle([370 * SS, 450 * SS, 630 * SS, 800 * SS], radius=60 * SS, fill=WH, outline=K, width=int(9 * SS))
    p.d.rectangle([450 * SS, 520 * SS, 550 * SS, 590 * SS], fill=BLU, outline=K, width=int(6 * SS))


def astronauta_post(p):
    p.d.ellipse([255 * SS, 85 * SS, 745 * SS, 575 * SS], outline=K, width=int(12 * SS))
    p.d.arc([300 * SS, 130 * SS, 700 * SS, 530 * SS], 200, 250, fill=WH, width=int(16 * SS))
    p.stroke([(640, 130), (690, 50)], 8)
    p.dot(690, 46, 16, R)


def detective_post(p):
    p.poly([(300, 235), (700, 235), (690, 255), (310, 255)], (110, 80, 50, 255))
    p.poly([(370, 240), (630, 240), (600, 140), (400, 140)], (130, 95, 60, 255))
    p.stroke([(370, 240), (400, 140), (600, 140), (630, 240)], 8)
    p.stroke([(372, 215), (628, 215)], 14, K)
    T.magnifier(p, 880, 400)


def reportero_post(p):
    p.poly([(300, 235), (700, 235), (690, 255), (310, 255)], K + (255,))
    p.poly([(370, 240), (630, 240), (600, 150), (400, 150)], (60, 64, 80, 255))
    p.d.rectangle([560 * SS, 165 * SS, 640 * SS, 215 * SS], fill=WH, outline=K, width=int(5 * SS))
    p.d.text((600 * SS, 190 * SS), "PRENSA", font=ImageFont.truetype(IB, int(16 * SS)), fill=K, anchor="mm")
    x, y = 790, 330
    p.stroke([(x, y), (x + 10, y - 90)], 20)
    p.dot(x + 12, y - 120, 42, (170, 174, 186))
    p.stroke([(x - 18, y - 92), (x + 38, y - 88)], 14, R)


def piloto_pre(p):
    p.d.rounded_rectangle([290 * SS, 150 * SS, 710 * SS, 470 * SS], radius=150 * SS, fill=R, outline=K, width=int(10 * SS))
    p.stroke([(500, 152), (500, 240)], 26, WH)
    coat(p, R)
    p.stroke([(470, 460), (440, 805)], 12, WH)
    p.stroke([(530, 460), (560, 805)], 12, WH)


def mago_pre(p):
    coat(p, PUR)


def mago_post(p):
    p.poly([(330, 250), (670, 250), (520, 0), (500, -10)], PUR + (255,))
    p.stroke([(330, 250), (505, -10), (670, 250)], 9)
    p.stroke([(320, 252), (680, 252)], 22, PUR)
    p.stroke([(320, 252), (680, 252)], 6)
    for (x, y, r) in ((470, 130, 18), (540, 70, 14), (560, 190, 16)):
        T.N.sparkle(p, x, y, r, YEL)
    x, y = 790, 330
    p.stroke([(x, y), (x + 60, y - 120)], 12, (90, 60, 40))
    T.N.sparkle(p, x + 66, y - 132, 34, YEL)


def calle_pre(p):
    coat(p, (90, 94, 110))
    p.d.chord([360 * SS, 380 * SS, 640 * SS, 560 * SS], 0, 180, fill=(70, 74, 90), outline=K, width=int(8 * SS))


def calle_post(p):
    p.d.chord([350 * SS, 160 * SS, 650 * SS, 360 * SS], 180, 360, fill=R, outline=K, width=int(9 * SS))
    p.stroke([(600, 262), (690, 270)], 22, (170, 30, 40))
    p.stroke([(430, 470), (500, 610), (570, 470)], 8, YEL)
    p.dot(500, 618, 22, YEL)
    p.dot(500, 618, 10, R)
    for x in (380, 620):
        p.stroke([(x, 1060), (x + (40 if x > 500 else -40), 1060)], 34, R)


def obra_pre(p):
    p.poly([(440, 445), (560, 445), (630, 790), (370, 790)], ORA + (255,))
    p.stroke([(440, 445), (560, 445), (630, 790), (370, 790), (440, 445)], 9)
    for y in (600, 700):
        p.stroke([(395, y), (605, y)], 16, (230, 230, 230))


def obra_post(p):
    p.d.chord([330 * SS, 120 * SS, 670 * SS, 380 * SS], 180, 360, fill=YEL, outline=K, width=int(9 * SS))
    p.stroke([(310, 250), (690, 250)], 18, YEL)
    p.stroke([(310, 250), (690, 250)], 6)
    p.stroke([(500, 125), (500, 245)], 12, (230, 180, 30))
    x, y = 350, 730
    p.d.rounded_rectangle([(x - 120) * SS, (y - 22) * SS, (x + 20) * SS, (y + 22) * SS], radius=20 * SS, fill=BLU, outline=K, width=int(6 * SS))
    p.stroke([(x - 100, y - 20), (x - 100, y + 20)], 5, WH)


def romano_pre(p):
    p.poly([(440, 445), (560, 445), (640, 800), (360, 800)], WH + (255,))
    p.stroke([(440, 445), (560, 445), (640, 800), (360, 800), (440, 445)], 9)
    p.poly([(440, 450), (480, 450), (640, 760), (600, 790)], R + (255,))


def romano_post(p):
    for side in (-1, 1):
        for k in range(6):
            a = math.radians(200 + k * 14) if side < 0 else math.radians(340 - k * 14)
            x, y = 500 + math.cos(a) * 200, 330 + math.sin(a) * 120
            p.d.ellipse([(x - 26) * SS, (y - 12) * SS, (x + 26) * SS, (y + 12) * SS], fill=GRN, outline=K, width=int(4 * SS))


CHARS = [("Astronauta", astronauta_pre, astronauta_post, "wave"), ("Detective", lambda p: coat(p, (196, 160, 110)), detective_post, "point"),
         ("Reportero", lambda p: coat(p, (60, 64, 80)), reportero_post, "wave"), ("Piloto de F1", piloto_pre, None, "flag"),
         ("Mago", mago_pre, mago_post, "wave"), ("Callejero", calle_pre, calle_post, "wave"),
         ("Ingeniero de obra", obra_pre, obra_post, "point"), ("Romano", romano_pre, romano_post, "point")]


def make(pre, post, pose):
    p = N.Pen()
    if pre:
        pre(p)
    N._pose(p, pose, 0.0, (0.06, 0.0), 0.0)
    if post:
        post(p)
    return p.im.resize((N.W0 // 2, N.H0 // 2), Image.LANCZOS)


if __name__ == "__main__":
    sheet = Image.new("RGB", (4 * 330 + 50, 4 * 430 + 60), (16, 16, 20))
    dd = ImageDraw.Draw(sheet)
    for i, (nm, pre, post, pose) in enumerate(CHARS):
        f = make(pre, post, pose)
        im = Image.new("RGB", (500, 600), BGP)
        im.paste(f, (0, 0), f)
        col, row = i % 4, (i // 4) * 2
        x, y = 10 + col * 340, 10 + row * 440
        dd.text((x + 4, y + 22), f"{chr(69 + i)} · {nm}", font=ImageFont.truetype(IB, 26), fill=(255, 255, 255), anchor="lm")
        sheet.paste(im.resize((300, 360), Image.LANCZOS), (x + 15, y + 44))
        pf = Image.new("RGB", (600, 600), R)
        big = f.resize((820, 984), Image.LANCZOS)
        pf.paste(big, (-110, -20), big)
        pf.save(OUT + f"ojo_perfil2_{i}.png")
        m = Image.new("L", (300, 300), 0)
        ImageDraw.Draw(m).ellipse([0, 0, 299, 299], fill=255)
        sheet.paste(pf.resize((300, 300), Image.LANCZOS), (x + 15, y + 440 + 20), m)
    sheet.save(OUT + "ojo_trajes2.jpg", quality=92)
    print("ok")
