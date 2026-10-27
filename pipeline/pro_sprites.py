"""Sprites ilustrados con suavizado (se dibujan a 3x y se reducen) para el vídeo profesional del Titanic."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SS = 3


def canvas(w, h):
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def done(im, w, h):
    return im.resize((w, h), Image.LANCZOS)


def P(pts):
    return [(x * SS, y * SS) for x, y in pts]


def B(box):
    return [v * SS for v in box]


def vgrad(w, h, top, bot, power=1.0):
    ys = (np.linspace(0, 1, h) ** power)[:, None, None]
    arr = np.array(top, float) + (np.array(bot, float) - np.array(top, float)) * ys
    arr = np.broadcast_to(arr, (h, w, 3)).astype(np.uint8)
    return Image.fromarray(arr.copy(), "RGB")


def glow(r, col, strength=1.0):
    """Mancha de luz circular con caída suave."""
    s = int(r * 2)
    yy, xx = np.mgrid[0:s, 0:s]
    d = np.sqrt((xx - r) ** 2 + (yy - r) ** 2) / r
    a = np.clip(1 - d, 0, 1) ** 2.2 * 255 * strength
    im = Image.new("RGBA", (s, s), col + (0,))
    im.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return im


# ------------------------------------------------------------------ TITANIC (vista lateral, proa a la derecha)
def ship(night=False, lit=True, w=1000, h=480):
    im, d = canvas(w, h)
    hull = (16, 16, 20)
    wl = 380  # línea de flotación
    deck_s, deck_b = 250, 222  # cubierta en popa / proa (arrufo)

    def deck_y(x):
        return deck_s + (deck_b - deck_s) * (x - 40) / 920

    # obra viva (roja) y casco
    d.polygon(P([(70, wl), (955, wl), (948, 430), (110, 430)]), fill=(140, 32, 30))
    pts = [(40, deck_y(40))]
    pts += [(x, deck_y(x)) for x in range(60, 961, 20)]
    pts += [(962, deck_b - 4), (956, wl), (75, wl)]
    pts += [(52, wl - 30), (40, deck_y(40) + 40)]
    d.polygon(P(pts), fill=hull)
    # franja dorada
    d.line(P([(x, deck_y(x) + 12) for x in range(50, 955, 15)]), fill=(200, 160, 70), width=SS * 2)
    # superestructura blanca
    white = (238, 236, 228) if not night else (150, 152, 160)
    sup = [(160, deck_y(160) + 2), (830, deck_y(830) + 2), (830, deck_y(830) - 52), (160, deck_y(160) - 52)]
    d.polygon(P(sup), fill=white)
    boat = [(230, deck_y(230) - 52), (790, deck_y(790) - 52), (790, deck_y(790) - 70), (230, deck_y(230) - 70)]
    d.polygon(P(boat), fill=white)
    d.polygon(P([(760, deck_y(760) - 70), (835, deck_y(835) - 70), (835, deck_y(835) - 88), (760, deck_y(760) - 88)]), fill=white)
    # botes salvavidas
    for x in range(250, 780, 44):
        y = deck_y(x) - 76
        d.rounded_rectangle(B([x, y, x + 30, y + 8]), radius=SS * 4, fill=(225, 225, 220) if not night else (120, 122, 130))
    # chimeneas inclinadas hacia popa
    rake = 0.18
    for i, fx in enumerate((300, 425, 550, 675)):
        base = deck_y(fx) - 70
        top = base - 150
        x0, x1 = fx - 24, fx + 24
        poly = [(x0, base), (x1, base), (x1 - rake * 150, top), (x0 - rake * 150, top)]
        d.polygon(P(poly), fill=(214, 150, 64) if not night else (110, 78, 40))
        d.polygon(P([(x0 - rake * 120, top + 30), (x1 - rake * 120, top + 30), (x1 - rake * 150, top), (x0 - rake * 150, top)]),
                  fill=(16, 16, 18))
        d.line(P([(x0 + 6, base), (x0 + 6 - rake * 120, top + 30)]), fill=(240, 190, 110) if not night else (140, 100, 60), width=SS * 3)
    # mástiles y jarcia
    for mx, top in ((870, 20), (130, 50)):
        d.line(P([(mx, deck_y(mx)), (mx - 18, top)]), fill=(40, 34, 30), width=SS * 4)
    d.line(P([(852, 20), (112, 50)]), fill=(60, 60, 64), width=SS)
    d.line(P([(852, 20), (962, deck_b - 2)]), fill=(60, 60, 64), width=SS)
    d.line(P([(112, 50), (40, deck_y(40))]), fill=(60, 60, 64), width=SS)
    d.ellipse(B([845, 76, 864, 92]), fill=(30, 26, 24))  # cofa
    # ojos de buey y ventanas
    lit_col = (255, 214, 140)
    dark_col = (60, 62, 70) if not night else (30, 32, 40)
    winc = lit_col if (night and lit) else dark_col
    rng = random.Random(3)
    for x in range(110, 940, 17):
        for row in (22, 44):
            y = deck_y(x) + row
            if y < wl - 8:
                c = winc if (not night or rng.random() > 0.15) else dark_col
                d.ellipse(B([x, y, x + 5, y + 5]), fill=c)
    for x in range(175, 820, 14):
        for row in (12, 30):
            y = deck_y(x) - 52 + row
            c = winc if (not night or rng.random() > 0.2) else dark_col
            d.rectangle(B([x, y, x + 6, y + 7]), fill=c)
    out = done(im, w, h)
    if night and lit:
        g = out.copy()
        a = np.array(g)[:, :, :3].astype(int)
        mask = ((a[:, :, 0] > 200) & (a[:, :, 1] > 160)).astype(np.uint8) * 255
        gl = Image.new("RGBA", out.size, (255, 200, 120, 0))
        gl.putalpha(Image.fromarray(mask, "L").filter(ImageFilter.GaussianBlur(6)))
        base = Image.new("RGBA", out.size, (0, 0, 0, 0))
        base.alpha_composite(gl)
        base.alpha_composite(gl)
        base.alpha_composite(out)
        out = base
    return out


def iceberg(w=700, h=620):
    im, d = canvas(w, h)
    pts = [(20, 600), (90, 420), (150, 360), (210, 250), (260, 280), (330, 120), (380, 60), (430, 170), (480, 140),
           (560, 300), (620, 380), (690, 600)]
    d.polygon(P(pts), fill=(200, 222, 240))
    d.polygon(P([(330, 120), (380, 60), (430, 170), (400, 600), (300, 600)]), fill=(235, 245, 252))
    d.polygon(P([(430, 170), (480, 140), (560, 300), (620, 380), (690, 600), (400, 600)]), fill=(150, 180, 212))
    d.polygon(P([(20, 600), (90, 420), (150, 360), (210, 250), (260, 280), (300, 600)]), fill=(185, 210, 232))
    for _ in range(14):
        x = random.uniform(120, 600)
        y = random.uniform(260, 560)
        d.line(P([(x, y), (x + random.uniform(-30, 30), y + random.uniform(20, 60))]), fill=(130, 165, 200), width=SS * 2)
    return done(im, w, h)


def key(w=520, h=220, shine=0.0):
    im, d = canvas(w, h)
    brass_d, brass, brass_l = (150, 104, 36), (212, 162, 64), (250, 214, 130)
    cx, cy, r = 110, 110, 86
    d.ellipse(B([cx - r, cy - r, cx + r, cy + r]), fill=brass_d)
    d.ellipse(B([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8]), fill=brass)
    for k in range(3):
        a = k / 3 * 2 * math.pi + 0.5
        ox, oy = cx + 38 * math.cos(a), cy + 38 * math.sin(a)
        d.ellipse(B([ox - 22, oy - 22, ox + 22, oy + 22]), fill=(0, 0, 0, 0))
    d.ellipse(B([cx - 20, cy - 20, cx + 20, cy + 20]), fill=brass_d)
    d.rounded_rectangle(B([cx + 70, cy - 16, 470, cy + 16]), radius=SS * 10, fill=brass)
    d.rectangle(B([cx + 70, cy - 16, 470, cy - 6]), fill=brass_l)
    for x0, hh in ((390, 52), (430, 38), (455, 60)):
        d.rectangle(B([x0, cy + 10, x0 + 24, cy + 10 + hh]), fill=brass)
        d.rectangle(B([x0, cy + 10, x0 + 6, cy + 10 + hh]), fill=brass_l)
    d.arc(B([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10]), 200, 290, fill=brass_l, width=SS * 7)
    out = done(im, w, h)
    return out


def crows_nest(w=520, h=900, people=True):
    im, d = canvas(w, h)
    wood, wood_d = (70, 52, 40), (42, 32, 26)
    d.polygon(P([(236, 900), (284, 900), (270, 0), (250, 0)]), fill=wood_d)
    d.line(P([(250, 0), (20, 900)]), fill=(40, 40, 44), width=SS * 2)
    d.line(P([(270, 0), (500, 900)]), fill=(40, 40, 44), width=SS * 2)
    # cofa (barril)
    d.rounded_rectangle(B([130, 330, 390, 470]), radius=SS * 20, fill=wood)
    for x in range(140, 390, 26):
        d.line(P([(x, 334), (x, 466)]), fill=wood_d, width=SS * 2)
    d.rounded_rectangle(B([120, 320, 400, 344]), radius=SS * 10, fill=(96, 72, 54))
    if people:
        for px in (200, 320):
            d.ellipse(B([px - 30, 230, px + 30, 290]), fill=(18, 20, 26))
            d.rectangle(B([px - 36, 222, px + 36, 236]), fill=(18, 20, 26))
            d.rounded_rectangle(B([px - 42, 280, px + 42, 340]), radius=SS * 18, fill=(18, 20, 26))
    # campana
    d.line(P([(400, 380), (440, 380)]), fill=wood_d, width=SS * 4)
    d.polygon(P([(430, 384), (470, 384), (480, 430), (420, 430)]), fill=(200, 160, 70))
    d.ellipse(B([418, 424, 482, 438]), fill=(170, 130, 50))
    return done(im, w, h)


def officer(w=260, h=520, phase=0.0):
    im, d = canvas(w, h)
    c = (14, 16, 24)
    sw = math.sin(phase) * 26
    d.polygon(P([(110, 330), (150, 330), (150 + sw, 510), (128 + sw, 510)]), fill=c)
    d.polygon(P([(110, 330), (150, 330), (132 - sw, 510), (110 - sw, 510)]), fill=c)
    d.rounded_rectangle(B([80, 150, 180, 350]), radius=SS * 24, fill=c)
    d.ellipse(B([98, 70, 162, 140]), fill=c)
    d.rounded_rectangle(B([88, 60, 172, 84]), radius=SS * 8, fill=c)
    d.rectangle(B([94, 80, 166, 90]), fill=c)
    d.line(P([(90, 170), (60 - sw * 0.5, 320)]), fill=c, width=SS * 18)
    d.line(P([(170, 170), (196 + sw * 0.5, 300)]), fill=c, width=SS * 18)
    return done(im, w, h)


def binoculars(w=420, h=300):
    im, d = canvas(w, h)
    body, bl = (30, 30, 34), (70, 70, 78)
    for cx in (110, 310):
        d.rounded_rectangle(B([cx - 80, 40, cx + 80, 250]), radius=SS * 40, fill=body)
        d.rounded_rectangle(B([cx - 80, 40, cx - 50, 250]), radius=SS * 20, fill=bl)
        d.ellipse(B([cx - 70, 200, cx + 70, 290]), fill=(20, 20, 24))
        d.ellipse(B([cx - 52, 214, cx + 52, 280]), fill=(110, 170, 220))
        d.ellipse(B([cx - 30, 222, cx - 4, 240]), fill=(220, 240, 255))
    d.rounded_rectangle(B([180, 100, 240, 170]), radius=SS * 14, fill=bl)
    return done(im, w, h)


def box(w=700, h=520, lid=0.0):
    """Caja de madera; lid=0 cerrada, 1 abierta."""
    im, d = canvas(w, h)
    wood, wd, wl = (120, 76, 44), (82, 50, 28), (160, 108, 66)
    d.rectangle(B([80, 260, 620, 500]), fill=wood)
    for y in (300, 360, 420, 480):
        d.line(P([(80, y), (620, y)]), fill=wd, width=SS * 2)
    d.rectangle(B([80, 260, 620, 276]), fill=wl)
    d.rounded_rectangle(B([320, 300, 380, 360]), radius=SS * 6, fill=(200, 160, 70))
    d.ellipse(B([342, 318, 358, 334]), fill=(40, 30, 20))
    ang = lid * 1.9
    hx, hy = 80, 260
    L = 540
    pts = [(hx, hy), (hx + L * math.cos(-ang), hy + L * math.sin(-ang)),
           (hx + L * math.cos(-ang) + 40 * math.sin(ang), hy + L * math.sin(-ang) - 40 * math.cos(ang)),
           (hx + 40 * math.sin(ang), hy - 40 * math.cos(ang))]
    d.polygon(P(pts), fill=wl if lid > 0.5 else wood)
    return done(im, w, h)


def gavel(w=460, h=300, ang=0.0):
    im, d = canvas(w, h)
    pivot = (140, 230)
    def R_(x, y):
        dx, dy = x - pivot[0], y - pivot[1]
        return (pivot[0] + dx * math.cos(ang) - dy * math.sin(ang), pivot[1] + dx * math.sin(ang) + dy * math.cos(ang))
    d.polygon(P([R_(130, 225), R_(420, 210), R_(420, 230), R_(130, 240)]), fill=(110, 66, 36))
    d.polygon(P([R_(60, 150), R_(200, 150), R_(200, 260), R_(60, 260)]), fill=(132, 80, 44))
    d.polygon(P([R_(60, 150), R_(200, 150), R_(200, 168), R_(60, 168)]), fill=(200, 160, 70))
    d.polygon(P([R_(60, 242), R_(200, 242), R_(200, 260), R_(60, 260)]), fill=(200, 160, 70))
    return done(im, w, h)


def cushion(w=620, h=260):
    im, d = canvas(w, h)
    d.rounded_rectangle(B([20, 60, 600, 240]), radius=SS * 60, fill=(120, 20, 40))
    d.rounded_rectangle(B([40, 70, 580, 140]), radius=SS * 40, fill=(160, 40, 60))
    for x in (60, 560):
        d.ellipse(B([x - 18, 200, x + 18, 250]), fill=(212, 162, 64))
    return done(im, w, h)


def bell(w=260, h=280):
    im, d = canvas(w, h)
    d.polygon(P([(90, 40), (170, 40), (210, 210), (50, 210)]), fill=(212, 166, 70))
    d.polygon(P([(90, 40), (115, 40), (85, 210), (50, 210)]), fill=(245, 205, 120))
    d.ellipse(B([30, 196, 230, 236]), fill=(176, 130, 50))
    d.ellipse(B([110, 222, 150, 262]), fill=(140, 100, 40))
    d.rounded_rectangle(B([110, 10, 150, 46]), radius=SS * 8, fill=(150, 110, 44))
    return done(im, w, h)


def crane(w=360, h=700):
    im, d = canvas(w, h)
    c = (40, 44, 58)
    d.polygon(P([(140, 700), (220, 700), (200, 120), (160, 120)]), fill=c)
    for y in range(140, 700, 40):
        d.line(P([(160, y), (210, y + 40)]), fill=(70, 74, 90), width=SS * 2)
    d.polygon(P([(0, 140), (360, 110), (360, 130), (0, 160)]), fill=c)
    d.line(P([(300, 125), (300, 400)]), fill=c, width=SS * 2)
    return done(im, w, h)
