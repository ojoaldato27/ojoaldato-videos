"""Móvil, dedos, guantes y otros objetos ilustrados (estilo Titanic con volumen)."""
from kitchen import *

PH_W, PH_H = 480, 980
SCR = (26, 26, 454, 954)  # pantalla dentro del sprite del móvil

APP_COLS = [(255, 94, 87), (255, 179, 64), (90, 200, 120), (64, 156, 255), (170, 110, 255), (255, 120, 180), (40, 200, 210),
            (250, 220, 70), (120, 130, 150), (255, 140, 60), (80, 110, 250), (60, 190, 160)]


def phone_body():
    c = Cv(PH_W, PH_H)
    c.shadow((30, 930, 450, 990), 150, 14)
    c.rect((0, 0, PH_W, PH_H - 10), grad=((150, 156, 168), (60, 64, 74)), horizontal=True, r=70)
    c.rect((6, 6, PH_W - 6, PH_H - 16), fill=(12, 12, 14), r=64)
    c.rect((-4, 210, 4, 290), fill=(110, 114, 124), r=3)
    c.rect((PH_W - 4, 250, PH_W + 4, 360), fill=(110, 114, 124), r=3)
    im = c.done()
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(SCR, radius=52, fill=255)
    im.putalpha(ImageChops.subtract(im.getchannel("A"), m))
    return im


def phone_screen(mode="home", lit=1.0):
    w, h = SCR[2] - SCR[0], SCR[3] - SCR[1]
    c = Cv(w, h)
    if mode == "off":
        c.rect((0, 0, w, h), grad=((20, 22, 28), (6, 6, 8)))
    else:
        c.rect((0, 0, w, h), grad=((40, 60, 140), (200, 90, 140)))
        c.ellipse((-200, h * 0.45, w + 200, h * 1.3), radial=((255, 170, 120, 255), (200, 90, 140, 0)), power=1.0)
        c.ellipse((w * 0.3, -100, w * 1.4, h * 0.4), radial=((120, 200, 255, 180), (40, 60, 140, 0)))
        c.text((44, 44), "9:41", 26, (255, 255, 255), anchor="lm")
        if mode == "home":
            rr = random.Random(1)
            for j in range(5):
                for i in range(4):
                    x, y = 34 + i * 96, 130 + j * 120
                    col = APP_COLS[(i + j * 4) % len(APP_COLS)]
                    c.rect((x, y, x + 74, y + 74), grad=(shade(col, 1.25), shade(col, 0.8)), r=18)
                    k = rr.randint(0, 3)
                    cx_, cy_ = x + 37, y + 37
                    if k == 0:
                        c.ellipse((cx_ - 18, cy_ - 18, cx_ + 18, cy_ + 18), fill=(255, 255, 255, 230))
                    elif k == 1:
                        c.rect((cx_ - 18, cy_ - 14, cx_ + 18, cy_ + 14), fill=(255, 255, 255, 230), r=5)
                    elif k == 2:
                        c.poly([(cx_ - 16, cy_ + 16), (cx_, cy_ - 18), (cx_ + 16, cy_ + 16)], fill=(255, 255, 255, 230))
                    else:
                        c.rect((cx_ - 6, cy_ - 20, cx_ + 6, cy_ + 20), fill=(255, 255, 255, 230), r=4)
                        c.rect((cx_ - 20, cy_ - 6, cx_ + 20, cy_ + 6), fill=(255, 255, 255, 230), r=4)
                    c.rect((x + 14, y + 84, x + 60, y + 92), fill=(255, 255, 255, 120), r=4)
            c.rect((24, h - 130, w - 24, h - 26), fill=(255, 255, 255, 50), r=34)
            for i in range(4):
                x = 46 + i * 92
                col = APP_COLS[(i * 3 + 2) % len(APP_COLS)]
                c.rect((x, h - 114, x + 72, h - 42), grad=(shade(col, 1.25), shade(col, 0.8)), r=18)
        elif mode == "lock":
            c.text((w / 2, 230), "9:41", 120, (255, 255, 255))
            c.text((w / 2, 320), "martes, 13", 30, (255, 255, 255, 220))
            c.rect((w / 2 - 70, h - 40, w / 2 + 70, h - 32), fill=(255, 255, 255, 200), r=4)
    c.rect((w / 2 - 70, 20, w / 2 + 70, 62), fill=(0, 0, 0), r=21)
    if lit < 1:
        c.rect((0, 0, w, h), fill=(0, 0, 0, int(255 * (1 - lit))))
    return c.done()


def phone(img, x, y, s=1.0, mode="home", rot=0.0, lit=1.0, extra=None):
    """Móvil completo centrado en (x, y). extra(img_scr) dibuja encima de la pantalla (coords de pantalla)."""
    scr = spr(phone_screen, mode, round(lit, 2)).copy()
    if extra:
        extra(scr)
    body = spr(phone_body)
    full = Image.new("RGBA", body.size, (0, 0, 0, 0))
    full.alpha_composite(scr, (SCR[0], SCR[1]))
    m = Image.new("L", full.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(SCR, radius=52, fill=255)
    full.putalpha(ImageChops.multiply(full.getchannel("A"), m))
    full.alpha_composite(body)
    g = Image.new("RGBA", full.size, (0, 0, 0, 0))
    ImageDraw.Draw(g).polygon([(60, 0), (230, 0), (40, 600), (-120, 600)], fill=(255, 255, 255, 20))
    g.putalpha(ImageChops.multiply(g.getchannel("A"), m))
    full.alpha_composite(g)
    paste(img, full, x, y, s, 1.0, rot)


def finger(kind="skin", length=640, width=120):
    """Dedo índice apuntando hacia arriba (la yema arriba). kind: skin | glove | tglove | sausage."""
    w, h = width + 80, length + 40
    c = Cv(w, h)
    cx = w / 2
    if kind == "sausage":
        c.rect((cx - width / 2, 30, cx + width / 2, h - 10), grad=((214, 120, 90), (150, 70, 50)), horizontal=True, r=width / 2)
        c.rect((cx - width / 2 + 14, 60, cx - width / 2 + 30, h - 40), fill=(255, 220, 200, 90), r=8)
        for y in range(90, h - 40, 70):
            c.arc((cx - width / 2, y, cx + width / 2, y + 30), 20, 160, (120, 50, 34, 120), 3)
        c.line([(cx, 30), (cx - 6, 6)], (190, 110, 80), 10)
        return c.done()
    if kind == "skin":
        g = ((246, 196, 160), (196, 132, 100))
    else:
        g = ((70, 74, 96), (36, 38, 52))
    c.rect((cx - width / 2, 30, cx + width / 2, h), grad=g, horizontal=True, r=width / 2)
    c.rect((cx - width / 2 + 16, 70, cx - width / 2 + 34, h - 30), fill=(255, 255, 255, 50), r=9)
    if kind == "skin":
        c.rect((cx - width * 0.32, 44, cx + width * 0.32, 150), grad=((255, 236, 226), (236, 196, 180)), r=width * 0.3)
        c.arc((cx - width * 0.32, 46, cx + width * 0.32, 160), 200, 340, (255, 255, 255, 140), 3)
        for y in (260, 290, 520, 545):
            c.arc((cx - width / 2 + 10, y, cx + width / 2 - 10, y + 30), 20, 160, (170, 110, 84), 3)
    else:
        rr = random.Random(3)
        for y in range(50, h, 22):
            for x in range(int(cx - width / 2 + 10), int(cx + width / 2 - 6), 18):
                c.line([(x, y), (x + 9, y + 12), (x + 18, y)], (100, 104, 130, 150), 3)
        c.rect((cx - width / 2, h - 120, cx + width / 2, h), grad=((90, 40, 50), (60, 24, 30)), horizontal=True)
        for x in range(int(cx - width / 2), int(cx + width / 2), 14):
            c.line([(x, h - 120), (x, h)], (120, 60, 70), 4)
        if kind == "tglove":
            c.rect((cx - width / 2, 30, cx + width / 2, 170), grad=((230, 232, 240), (130, 134, 146)), horizontal=True, r=width / 2)
            for y in range(60, 170, 16):
                c.line([(cx - width / 2 + 10, y), (cx + width / 2 - 10, y + 6)], (255, 255, 255, 160), 2)
    return c.done()


def hand_xray():
    c = Cv(700, 900)
    col = (60, 140, 220, 120)
    c.rect((170, 400, 560, 860), fill=col, r=120)
    for x, top, wd in ((190, 160, 84), (290, 60, 88), (390, 40, 88), (490, 110, 84)):
        c.rect((x - wd / 2 + 30, top, x + wd / 2 + 30, 520), fill=col, r=wd / 2)
    c.poly([(170, 560), (40, 360), (90, 320), (240, 500)], fill=col)
    c.ellipse((20, 310, 110, 400), fill=col)
    bone = (210, 236, 255, 200)
    for x, top in ((220, 190), (320, 90), (420, 70), (520, 140)):
        for k in range(3):
            y0 = top + k * 110
            c.rect((x - 14, y0, x + 14, y0 + 92), fill=bone, r=12)
        c.rect((x - 16, 520, x + 16, 700), fill=bone, r=14)
    c.line([(80, 360), (140, 450), (220, 560)], bone, 26)
    return c.done()


def radar_dish():
    c = Cv(560, 600)
    c.poly([(230, 590), (330, 590), (300, 330), (260, 330)], grad=((150, 150, 146), (70, 70, 68)), horizontal=True)
    c.poly([(150, 590), (410, 590), (380, 560), (180, 560)], fill=(80, 80, 78))
    c.line([(280, 330), (200, 250)], (90, 90, 88), 14)
    c.ellipse((40, 40, 400, 420), radial=((236, 236, 230), (120, 120, 116)), power=1.4, center=(0.62, 0.55))
    c.ellipse((60, 60, 380, 400), radial=((150, 150, 146), (226, 226, 220)), power=1.2, center=(0.6, 0.55))
    for k in range(5):
        a = k / 5 * math.pi * 2
        c.line([(220 + math.cos(a) * 150, 230 + math.sin(a) * 160), (300, 200)], (110, 110, 106), 4)
    c.line([(220, 230), (300, 200)], (90, 90, 88), 8)
    c.ellipse((288, 186, 316, 214), fill=(70, 70, 68))
    return c.done()


# ------------------------------------------------------------------ código QR (patrón ilustrativo, no codifica nada)
def qr_matrix(n=25, seed=7):
    rr = random.Random(seed)
    M_ = [[rr.random() < 0.5 for _ in range(n)] for _ in range(n)]
    fixed = [[False] * n for _ in range(n)]

    def finder(r0, c0):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr_, cc = r0 + r, c0 + c
                if 0 <= rr_ < n and 0 <= cc < n:
                    on = (0 <= r <= 6 and 0 <= c <= 6) and (r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4))
                    M_[rr_][cc] = on
                    fixed[rr_][cc] = True
    finder(0, 0)
    finder(0, n - 7)
    finder(n - 7, 0)
    for i in range(8, n - 8):
        M_[6][i] = M_[i][6] = (i % 2 == 0)
        fixed[6][i] = fixed[i][6] = True
    a = n - 7
    for r in range(-2, 3):
        for c in range(-2, 3):
            M_[a + r][a + c] = max(abs(r), abs(c)) != 1
            fixed[a + r][a + c] = True
    return M_, fixed


def qr_sprite(px=20, seed=7, n=25, ink=(16, 16, 20), paper=(250, 248, 242), quiet=2, logo=False):
    M_, fixed = qr_matrix(n, seed)
    S_ = (n + 2 * quiet) * px
    c = Cv(S_, S_, 2)
    c.rect((0, 0, S_, S_), fill=paper)
    for r in range(n):
        for col in range(n):
            if M_[r][col]:
                x, y = (col + quiet) * px, (r + quiet) * px
                c.rect((x, y, x + px + 0.6, y + px + 0.6), fill=ink)
    if logo:
        m = n * px * 0.26
        cx = cy = S_ / 2
        c.rect((cx - m, cy - m, cx + m, cy + m), fill=paper, r=m * 0.25)
        c.rect((cx - m * 0.8, cy - m * 0.8, cx + m * 0.8, cy + m * 0.8), grad=((255, 214, 80), (230, 160, 30)), r=m * 0.2)
        c.ellipse((cx - m * 0.55, cy - m * 0.32, cx + m * 0.55, cy + m * 0.32), fill=(20, 20, 24))
        c.ellipse((cx - m * 0.2, cy - m * 0.2, cx + m * 0.2, cy + m * 0.2), fill=(255, 214, 80))
    return c.done()


def qr_cell(n=25, quiet=2, px=20, r=0, col=0):
    """Centro (en coordenadas del sprite) de la casilla (r, col)."""
    return ((col + quiet + 0.5) * px, (r + quiet + 0.5) * px)
