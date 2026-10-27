"""Mascota de «No lo sabías»: un stickman con el ojo del logo como cabeza. 8 versiones (poses y estilos)."""
import sys, os, math
sys.path.insert(0, "/home/claude/shorts-ingenieria/pipeline")
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import cine
from cine import glow, F_SER, F_CAP

SS = 3
INK = (243, 240, 232)      # blanco roto del logo
BG = (14, 15, 18)          # casi negro del logo
YEL = (255, 210, 63)
OUT = "/home/claude/shorts-ingenieria/content/avatar/png"
os.makedirs(OUT, exist_ok=True)


class Pen:
    """Dibujo supermuestreado con trazos redondeados del grosor del logo."""

    def __init__(self, w=1000, h=1200):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def stroke(self, pts, w=26, col=INK):
        P_ = self.P(pts)
        ww = int(w * SS)
        self.d.line(P_, fill=col, width=ww, joint="curve")
        for x, y in (P_[0], P_[-1]):
            self.d.ellipse([x - ww / 2, y - ww / 2, x + ww / 2, y + ww / 2], fill=col)

    def curve(self, p0, p1, p2, w=26, col=INK, n=24):
        pts = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
                (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in [i / n for i in range(n + 1)]]
        self.stroke(pts, w, col)

    def dot(self, x, y, r, col=INK):
        self.d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=col)

    def poly(self, pts, col):
        self.d.polygon(self.P(pts), fill=col)

    def text(self, x, y, txt, size, col, font=F_CAP):
        self.d.text((x * SS, y * SS), txt, font=ImageFont.truetype(font, int(size * SS)), fill=col, anchor="mm")

    def paste(self, layer):
        self.im.alpha_composite(layer)
        self.d = ImageDraw.Draw(self.im)

    def done(self):
        return self.im.resize((self.w, self.h), Image.LANCZOS)


def almond(cx, cy, s, open_k=1.0, n=48):
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        x = cx - s / 2 + s * u
        dy = s * 0.21 * 4 * u * (1 - u) * open_k
        top.append((x, cy - dy))
        bot.append((x, cy + dy))
    return top, bot


def eye_head(p, cx, cy, s, look=(0, 0), open_k=1.0, lid=0.0, brow=None, filled=False, iris_r=0.19):
    """Cabeza = ojo del logo. look: desplazamiento del iris (en fracción de s); lid: párpado (0-1); brow: (inclinación, altura)."""
    top, bot = almond(cx, cy, s, open_k)
    W_, H_ = p.im.size
    mask = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(mask).polygon(p.P(top + bot[::-1]), fill=255)
    lay = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.polygon(p.P(top + bot[::-1]), fill=(236, 233, 224, 255) if filled else BG + (255,))
    if filled:
        sh = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([(cx - s * 0.5) * SS, (cy + s * 0.05) * SS, (cx + s * 0.5) * SS, (cy + s * 0.45) * SS], fill=(150, 150, 160, 120))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12 * SS)))
        ld = ImageDraw.Draw(lay)
    ix, iy, r = cx + look[0] * s, cy + look[1] * s, s * iris_r
    ld.ellipse([(ix - r) * SS, (iy - r) * SS, (ix + r) * SS, (iy + r) * SS], fill=YEL + (255,))
    fnt = ImageFont.truetype(F_CAP, int(r * 1.55 * SS))
    ld.text((ix * SS, (iy + r * 0.04) * SS), "?", font=fnt, fill=BG + (255,), anchor="mm")
    if filled:
        ld.ellipse([(ix + r * 0.35 - r * 0.16) * SS, (iy - r * 0.5 - r * 0.16) * SS, (ix + r * 0.35 + r * 0.16) * SS, (iy - r * 0.5 + r * 0.16) * SS],
                   fill=(255, 255, 255, 230))
    if lid > 0:
        y_l = cy - s * 0.21 * open_k + lid * s * 0.42 * open_k
        ld.rectangle([0, 0, W_, y_l * SS], fill=BG + (255,))
    clip = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    clip.paste(lay, (0, 0), mask)
    p.paste(clip)
    w = s * 0.045
    p.stroke(top, w)
    p.stroke(bot, w)
    if lid > 0:
        y_l = cy - s * 0.21 * open_k + lid * s * 0.42 * open_k
        xs = [x for x, y in top if y <= y_l + 1]
        if xs:
            p.curve((min(xs) + 6, y_l + 2), (cx, y_l + 10), (max(xs) - 6, y_l + 2), w * 0.9)
    if brow:
        tilt, hgt = brow
        y0 = cy - s * 0.21 * open_k - hgt
        p.curve((cx - s * 0.30, y0 + tilt), (cx, y0 - 24), (cx + s * 0.30, y0 - tilt), w * 1.1)


def body(p, neck, hip, arms, legs, w=26):
    """neck/hip: puntos; arms/legs: listas de polilíneas desde el hombro/cadera."""
    p.stroke([neck, hip], w)
    for a in arms:
        p.stroke(a, w)
        p.dot(*a[-1], w * 0.95)
    for l in legs:
        p.stroke(l, w)
        x, y = l[-1]
        dirx = 1 if x >= hip[0] else -1
        p.stroke([(x, y), (x + 34 * dirx, y)], w)


def sparkle(p, x, y, r, col=YEL):
    p.poly([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y), (x + r * 0.28, y + r * 0.28), (x, y + r), (x - r * 0.28, y + r * 0.28),
            (x - r, y), (x - r * 0.28, y - r * 0.28)], col + (255,))


# ------------------------------------------------------------------ las 8 versiones
def v1_original():
    p = Pen()
    cx, hy = 500, 330
    eye_head(p, cx, hy, 380)
    neck, hip = (cx, hy + 100), (cx, 760)
    body(p, neck, hip,
         [[(cx, 520), (680, 460), (790, 330)], [(cx, 520), (380, 610), (330, 720)]],
         [[hip, (430, 920), (410, 1060)], [hip, (570, 920), (600, 1060)]])
    p.curve((770, 270), (815, 245), (850, 275), 10, YEL)
    p.curve((780, 230), (840, 190), (890, 240), 10, YEL)
    return p.done()


def v2_smirk():
    p = Pen()
    cx, hy = 500, 330
    eye_head(p, cx, hy, 380, look=(0.05, 0.03), lid=0.36, brow=(38, 30))
    neck, hip = (cx, hy + 100), (cx, 760)
    body(p, neck, hip,
         [[(cx, 520), (400, 600), (470, 700)], [(cx, 520), (610, 600), (530, 700)]],
         [[hip, (440, 920), (400, 1060)], [hip, (560, 920), (600, 1060)]])
    return p.done()


def v3_surprise():
    p = Pen()
    cx, hy = 500, 340
    eye_head(p, cx, hy, 380, open_k=1.32, iris_r=0.17)
    neck, hip = (cx, hy + 130), (cx, 780)
    body(p, neck, hip,
         [[(cx, 540), (360, 440), (300, 300)], [(cx, 540), (640, 440), (700, 300)]],
         [[hip, (420, 930), (380, 1070)], [hip, (580, 930), (620, 1070)]])
    for x, y, r in ((230, 230, 34), (790, 210, 40), (180, 380, 22), (850, 380, 24), (500, 90, 26)):
        sparkle(p, x, y, r)
    return p.done()


def v4_think():
    p = Pen()
    cx, hy = 470, 380
    eye_head(p, cx, hy, 360, look=(0.07, -0.05))
    neck, hip = (cx, hy + 95), (cx, 800)
    body(p, neck, hip,
         [[(cx, 570), (600, 640), (540, 520)], [(cx, 570), (360, 650), (330, 760)]],
         [[hip, (420, 950), (400, 1080)], [hip, (520, 950), (560, 1080)]])
    for x, y, r in ((660, 250, 16), (710, 190, 24)):
        p.dot(x, y, r, INK)
    p.d.ellipse([700 * SS, 40 * SS, 940 * SS, 190 * SS], outline=INK, width=int(10 * SS))
    p.text(820, 116, "?", 96, YEL)
    return p.done()


def v5_teacher():
    p = Pen()
    cx, hy = 360, 360
    eye_head(p, cx, hy, 340, look=(0.08, 0.02))
    neck, hip = (cx, hy + 90), (cx, 790)
    p.d.rounded_rectangle([600 * SS, 160 * SS, 960 * SS, 520 * SS], radius=24 * SS, fill=(30, 34, 40, 255), outline=INK, width=int(10 * SS))
    pts = [(640, 470), (720, 420), (790, 440), (860, 330), (930, 250)]
    p.stroke(pts, 12, YEL)
    p.poly([(930, 228), (948, 268), (906, 262)], YEL + (255,))
    body(p, neck, hip,
         [[(cx, 560), (480, 500), (560, 430)], [(cx, 560), (250, 640), (240, 760)]],
         [[hip, (300, 940), (280, 1070)], [hip, (420, 940), (460, 1070)]])
    p.stroke([(560, 430), (700, 330)], 12, (200, 160, 110))
    return p.done()


def v6_engineer():
    p = Pen()
    cx, hy = 500, 380
    eye_head(p, cx, hy, 360, look=(-0.02, 0.02))
    # casco de obra blanco
    o = 52
    p.d.chord([(cx - 150) * SS, (hy - 260 + o) * SS, (cx + 150) * SS, (hy - 20 + o) * SS], 180, 360, fill=(246, 246, 240, 255))
    p.d.rounded_rectangle([(cx - 200) * SS, (hy - 150 + o) * SS, (cx + 200) * SS, (hy - 120 + o) * SS], radius=14 * SS, fill=(220, 220, 214, 255))
    p.d.rectangle([(cx - 14) * SS, (hy - 255 + o) * SS, (cx + 14) * SS, (hy - 150 + o) * SS], fill=(205, 205, 198, 255))
    neck, hip = (cx, hy + 95), (cx, 800)
    body(p, neck, hip,
         [[(cx, 570), (620, 640), (700, 700)], [(cx, 570), (380, 650), (350, 770)]],
         [[hip, (440, 950), (420, 1080)], [hip, (560, 950), (600, 1080)]])
    p.d.rounded_rectangle([640 * SS, 610 * SS, 900 * SS, 680 * SS], radius=30 * SS, fill=(70, 140, 230, 255))
    p.d.ellipse([870 * SS, 610 * SS, 930 * SS, 680 * SS], fill=(110, 170, 250, 255))
    return p.done()


def v7_racer():
    p = Pen()
    cx, hy = 470, 360
    eye_head(p, cx, hy, 350, look=(0.06, 0.0), brow=(10, 40))
    neck, hip = (cx + 10, hy + 92), (cx + 40, 770)
    body(p, neck, hip,
         [[(cx + 18, 550), (620, 470), (700, 330)], [(cx + 18, 550), (360, 620), (300, 560)]],
         [[hip, (620, 900), (700, 1030)], [hip, (420, 900), (330, 1000)]])
    p.stroke([(700, 330), (720, 60)], 12, (200, 200, 205))
    for i in range(4):
        for j in range(3):
            col = (250, 250, 250, 255) if (i + j) % 2 else (20, 20, 24, 255)
            x0, y0 = 722 + i * 52, 60 + j * 52 + math.sin(i * 0.9) * 8
            p.poly([(x0, y0), (x0 + 52, y0 + math.sin((i + 1) * 0.9) * 8 - math.sin(i * 0.9) * 8), (x0 + 52, y0 + 52), (x0, y0 + 52)], col)
    for y in (880, 940, 1000):
        p.stroke([(130, y), (250, y)], 8, (243, 240, 232, 120))
    return p.done()


def v8_filled():
    p = Pen()
    cx, hy = 500, 330
    eye_head(p, cx, hy, 400, look=(0.03, 0.0), filled=True)
    neck, hip = (cx, hy + 105), (cx, 760)
    body(p, neck, hip,
         [[(cx, 520), (680, 480), (800, 360)], [(cx, 520), (380, 600), (340, 710)]],
         [[hip, (430, 920), (410, 1060)], [hip, (570, 920), (600, 1060)]], w=34)
    return p.done()


VERS = [("v1_original", v1_original), ("v2_a_que_no_lo_sabias", v2_smirk), ("v3_sorprendido", v3_surprise), ("v4_pensando", v4_think),
        ("v5_el_profe", v5_teacher), ("v6_ingeniero", v6_engineer), ("v7_piloto", v7_racer), ("v8_relleno", v8_filled)]


def card(fig):
    """Tarjeta de presentación: fondo de la marca, brillo amarillo y sombra en el suelo."""
    c = Image.new("RGBA", (1080, 1350), BG + (255,))
    g = cine.glow(560, YEL, 0.22)
    c.alpha_composite(g, (540 - g.size[0] // 2, 560 - g.size[1] // 2))
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([300, 1150, 780, 1210], fill=(0, 0, 0, 170))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    c.alpha_composite(fig, (40, 60))
    return c.convert("RGB")


if __name__ == "__main__":
    sheet = Image.new("RGB", (270 * 4, 337 * 2), BG)
    for i, (name, fn) in enumerate(VERS):
        fig = fn()
        fig.save(os.path.join(OUT, name + "_transparente.png"))
        cd = card(fig)
        cd.save(os.path.join(OUT, name + ".png"))
        sheet.paste(cd.resize((270, 337)), ((i % 4) * 270, (i // 4) * 337))
    sheet.save("/tmp/claude-0/-home-claude/13f796bb-3765-545c-b200-821b21939a08/scratchpad/avatares.jpg", quality=88)
    print("ok")
