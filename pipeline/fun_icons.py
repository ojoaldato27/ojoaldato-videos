"""Iconos planos con contorno grueso (estilo pegatina) + la mascota del canal (el ojo).
Todos se dibujan en vectorial con PIL: draw(name, d, cx, cy, s, t, **opt)."""
import math, random
from PIL import ImageFont
import render as R

INK = (34, 30, 52)
WHITE = (255, 255, 255)
YEL = (255, 210, 63)
GF = "/usr/share/fonts/truetype/google-fonts/"
_F = {}


def pf(size, bold=True):
    k = (size, bold)
    if k not in _F:
        _F[k] = ImageFont.truetype(GF + ("Poppins-Bold.ttf" if bold else "Poppins-Medium.ttf"), max(8, int(size)))
    return _F[k]


def lw(s):
    return max(3, int(s * 0.035))


def circ(d, cx, cy, r, fill, s, outline=True):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=INK if outline else None, width=lw(s) if outline else 0)


def poly(d, pts, fill, s, outline=True):
    d.polygon(pts, fill=fill, outline=INK if outline else None, width=lw(s) if outline else 0)


def rrect(d, box, r, fill, s, outline=True):
    w_ = lw(s) if outline else 0
    if box[2] - box[0] < 2 * w_ + 2 or box[3] - box[1] < 2 * w_ + 2:
        return
    r = min(r, (box[2] - box[0]) / 2 - 1, (box[3] - box[1]) / 2 - 1)
    d.rounded_rectangle(box, radius=r, fill=fill, outline=INK if outline else None, width=lw(s) if outline else 0)


def line(d, pts, s, col=INK, w=None):
    d.line(pts, fill=col, width=w or lw(s), joint="curve")


def text_c(d, cx, cy, txt, size, col=INK, bold=True):
    f = pf(size, bold)
    tw = d.textlength(txt, font=f)
    d.text((cx - tw / 2, cy - size * 0.62), txt, font=f, fill=col)


def cute_face(d, cx, cy, s, t, look=0.0):
    """Ojitos y sonrisa para personajes (bacterias, células…)."""
    blink = (t % 3.1) < 0.12
    for sx in (-1, 1):
        ex, ey = cx + sx * s * 0.14, cy - s * 0.04
        if blink:
            line(d, [(ex - s * 0.05, ey), (ex + s * 0.05, ey)], s)
        else:
            circ(d, ex, ey, s * 0.06, WHITE, s * 0.6)
            circ(d, ex + look * s * 0.02, ey, s * 0.03, INK, s, False)
    d.arc([cx - s * 0.1, cy, cx + s * 0.1, cy + s * 0.14], 20, 160, fill=INK, width=lw(s))


# ------------------------------------------------------------------ iconos
def ship(d, cx, cy, s, t, tilt=0.0, **o):
    w, h = s, s * 0.5
    sink = tilt
    def P(x, y):
        a = math.radians(sink)
        dx, dy = x - cx, y - cy
        return (cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a))
    hull = [P(cx - w * 0.5, cy), P(cx + w * 0.5, cy), P(cx + w * 0.42, cy + h * 0.38), P(cx - w * 0.44, cy + h * 0.38)]
    poly(d, hull, (40, 40, 52), s)
    poly(d, [P(cx - w * 0.47, cy + h * 0.24), P(cx + w * 0.46, cy + h * 0.24), P(cx + w * 0.42, cy + h * 0.38),
             P(cx - w * 0.44, cy + h * 0.38)], (200, 50, 50), s)
    poly(d, [P(cx - w * 0.36, cy - h * 0.2), P(cx + w * 0.36, cy - h * 0.2), P(cx + w * 0.36, cy), P(cx - w * 0.36, cy)], WHITE, s)
    for i in range(4):
        fx = cx - w * 0.24 + i * w * 0.16
        poly(d, [P(fx - w * 0.04, cy - h * 0.62), P(fx + w * 0.04, cy - h * 0.62), P(fx + w * 0.045, cy - h * 0.2),
                 P(fx - w * 0.045, cy - h * 0.2)], (240, 170, 40), s)
        poly(d, [P(fx - w * 0.04, cy - h * 0.62), P(fx + w * 0.04, cy - h * 0.62), P(fx + w * 0.042, cy - h * 0.52),
                 P(fx - w * 0.042, cy - h * 0.52)], INK, s, False)
    for i in range(9):
        x = cx - w * 0.32 + i * w * 0.08
        circ(d, *P(x, cy - h * 0.1), s * 0.012, INK, s, False)


def iceberg(d, cx, cy, s, t, **o):
    poly(d, [(cx - s * 0.5, cy + s * 0.1), (cx - s * 0.2, cy + s * 0.6), (cx + s * 0.35, cy + s * 0.55), (cx + s * 0.5, cy + s * 0.1)],
         (170, 215, 240), s)
    poly(d, [(cx - s * 0.32, cy + s * 0.1), (cx - s * 0.12, cy - s * 0.3), (cx + s * 0.02, cy - s * 0.12), (cx + s * 0.15, cy - s * 0.4),
             (cx + s * 0.34, cy + s * 0.1)], WHITE, s)
    line(d, [(cx - s * 0.55, cy + s * 0.1), (cx + s * 0.55, cy + s * 0.1)], s, (60, 120, 200), lw(s) * 2)


def key(d, cx, cy, s, t, **o):
    gold = (250, 195, 60)
    circ(d, cx - s * 0.28, cy, s * 0.2, gold, s)
    circ(d, cx - s * 0.28, cy, s * 0.08, o.get("hole", (255, 240, 200)), s)
    rrect(d, [cx - s * 0.1, cy - s * 0.05, cx + s * 0.45, cy + s * 0.05], s * 0.03, gold, s)
    for x in (0.25, 0.37):
        rrect(d, [cx + s * x, cy + s * 0.04, cx + s * (x + 0.07), cy + s * 0.17], s * 0.02, gold, s)


def binoculars(d, cx, cy, s, t, **o):
    for sx in (-1, 1):
        rrect(d, [cx + sx * s * 0.22 - s * 0.16, cy - s * 0.3, cx + sx * s * 0.22 + s * 0.16, cy + s * 0.3], s * 0.08, (60, 60, 76), s)
        circ(d, cx + sx * s * 0.22, cy + s * 0.3, s * 0.15, (120, 190, 240), s)
    rrect(d, [cx - s * 0.08, cy - s * 0.12, cx + s * 0.08, cy + s * 0.05], s * 0.03, (90, 90, 110), s)


def mast(d, cx, cy, s, t, **o):
    rrect(d, [cx - s * 0.04, cy - s * 0.5, cx + s * 0.04, cy + s * 0.5], s * 0.02, (150, 100, 60), s)
    rrect(d, [cx - s * 0.18, cy - s * 0.32, cx + s * 0.18, cy - s * 0.12], s * 0.03, (190, 130, 80), s)
    circ(d, cx - s * 0.06, cy - s * 0.38, s * 0.06, (255, 220, 190), s)
    circ(d, cx + s * 0.07, cy - s * 0.38, s * 0.06, (255, 220, 190), s)


def clock(d, cx, cy, s, t, speed=1.0, **o):
    circ(d, cx, cy, s * 0.45, WHITE, s)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        line(d, [(cx + s * 0.36 * math.cos(a), cy + s * 0.36 * math.sin(a)), (cx + s * 0.41 * math.cos(a), cy + s * 0.41 * math.sin(a))], s)
    a1 = t * speed * 2 - math.pi / 2
    a2 = t * speed * 0.2 - math.pi / 2
    line(d, [(cx, cy), (cx + s * 0.32 * math.cos(a1), cy + s * 0.32 * math.sin(a1))], s)
    line(d, [(cx, cy), (cx + s * 0.22 * math.cos(a2), cy + s * 0.22 * math.sin(a2))], s, INK, lw(s) * 2)
    circ(d, cx, cy, s * 0.04, INK, s, False)


def money(d, cx, cy, s, t, sym="£", **o):
    for i, off in enumerate((0.06, 0.0)):
        rrect(d, [cx - s * 0.45 + s * off, cy - s * 0.25 - s * off, cx + s * 0.45 + s * off, cy + s * 0.25 - s * off], s * 0.05,
              (130, 210, 140), s)
    circ(d, cx, cy, s * 0.15, (90, 180, 110), s)
    text_c(d, cx, cy, sym, s * 0.22, INK)


def moon(d, cx, cy, s, t, side="near", **o):
    r = s * 0.48
    circ(d, cx, cy, r, (225, 225, 232), s)
    rng = random.Random(1 if side == "near" else 2)
    if side == "near":
        for _ in range(5):
            x, y, rr = rng.uniform(-0.45, 0.3), rng.uniform(-0.4, 0.3), rng.uniform(0.12, 0.22)
            d.ellipse([cx + r * x - r * rr, cy + r * y - r * rr * 0.8, cx + r * x + r * rr, cy + r * y + r * rr * 0.8],
                      fill=(165, 165, 180))
    for _ in range(9 if side == "near" else 18):
        x, y, rr = rng.uniform(-0.6, 0.6), rng.uniform(-0.6, 0.6), rng.uniform(0.04, 0.1)
        if x * x + y * y < 0.55:
            d.ellipse([cx + r * x - r * rr, cy + r * y - r * rr, cx + r * x + r * rr, cy + r * y + r * rr],
                      outline=(150, 150, 165), width=max(2, lw(s) // 2))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=lw(s))
    if o.get("face"):
        cute_face(d, cx, cy + r * 0.1, s * 0.8, t)


def earth(d, cx, cy, s, t, **o):
    r = s * 0.48
    circ(d, cx, cy, r, (70, 150, 235), s)
    sh = (t * 30) % (2 * r)
    for bx, by, br in ((-0.3, -0.2, 0.28), (0.25, 0.15, 0.32), (-0.1, 0.45, 0.18)):
        x = cx + r * bx + sh * 0.2
        d.ellipse([x - r * br, cy + r * by - r * br * 0.8, x + r * br, cy + r * by + r * br * 0.8], fill=(110, 200, 120))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=lw(s))
    if o.get("face"):
        cute_face(d, cx, cy + r * 0.1, s * 0.8, t)


def sun(d, cx, cy, s, t, **o):
    for i in range(10):
        a = i / 10 * 2 * math.pi + t * 0.6
        x0, y0 = cx + s * 0.36 * math.cos(a), cy + s * 0.36 * math.sin(a)
        x1, y1 = cx + s * 0.5 * math.cos(a), cy + s * 0.5 * math.sin(a)
        line(d, [(x0, y0), (x1, y1)], s, (255, 170, 40), lw(s) * 2)
    circ(d, cx, cy, s * 0.3, (255, 205, 60), s)
    if o.get("face", True):
        cute_face(d, cx, cy + s * 0.04, s * 0.7, t)


def satellite(d, cx, cy, s, t, **o):
    for sx in (-1, 1):
        rrect(d, [cx + sx * s * 0.18 - (s * 0.3 if sx < 0 else 0), cy - s * 0.1, cx + sx * s * 0.18 + (s * 0.3 if sx > 0 else 0),
                  cy + s * 0.1], s * 0.02, (90, 140, 230), s)
    circ(d, cx, cy, s * 0.17, (210, 210, 220), s)
    line(d, [(cx, cy - s * 0.17), (cx + s * 0.1, cy - s * 0.4)], s)
    circ(d, cx + s * 0.1, cy - s * 0.42, s * 0.03, (255, 80, 80), s)


def camera(d, cx, cy, s, t, flash=False, **o):
    rrect(d, [cx - s * 0.45, cy - s * 0.25, cx + s * 0.45, cy + s * 0.3], s * 0.08, (70, 70, 90), s)
    rrect(d, [cx - s * 0.2, cy - s * 0.36, cx + s * 0.05, cy - s * 0.24], s * 0.03, (70, 70, 90), s)
    circ(d, cx, cy + s * 0.03, s * 0.18, (120, 190, 240), s)
    circ(d, cx, cy + s * 0.03, s * 0.08, INK, s, False)
    if flash:
        for i in range(8):
            a = i / 8 * 2 * math.pi
            line(d, [(cx + s * 0.55 * math.cos(a), cy + s * 0.55 * math.sin(a)), (cx + s * 0.7 * math.cos(a), cy + s * 0.7 * math.sin(a))],
                 s, (255, 230, 80), lw(s) * 2)


def flag(d, cx, cy, s, t, col=(220, 40, 40), **o):
    rrect(d, [cx - s * 0.3, cy - s * 0.5, cx - s * 0.25, cy + s * 0.5], s * 0.02, (150, 150, 160), s)
    wv = math.sin(t * 4) * s * 0.03
    poly(d, [(cx - s * 0.25, cy - s * 0.5), (cx + s * 0.35, cy - s * 0.48 + wv), (cx + s * 0.35, cy - s * 0.1 + wv), (cx - s * 0.25, cy - s * 0.12)],
         col, s)
    star(d, cx - s * 0.1, cy - s * 0.31, s * 0.09, (255, 220, 60))


def star(d, cx, cy, r, col):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col)


def tower(d, cx, cy, s, t, grow=0.0, **o):
    h = s * (1 + grow)
    top = cy - h * 0.5
    base = cy + s * 0.5
    col = (120, 85, 60)
    # patas
    for sx in (-1, 1):
        poly(d, [(cx + sx * s * 0.34, base), (cx + sx * s * 0.2, base), (cx + sx * s * 0.07, top + h * 0.45), (cx + sx * s * 0.12, top + h * 0.45)],
             col, s)
    d.arc([cx - s * 0.2, base - s * 0.22, cx + s * 0.2, base + s * 0.12], 180, 360, fill=INK, width=lw(s))
    rrect(d, [cx - s * 0.2, base - s * 0.24, cx + s * 0.2, base - s * 0.2], 2, col, s)
    poly(d, [(cx - s * 0.11, top + h * 0.47), (cx + s * 0.11, top + h * 0.47), (cx + s * 0.03, top + h * 0.12), (cx - s * 0.03, top + h * 0.12)],
         col, s)
    rrect(d, [cx - s * 0.13, top + h * 0.44, cx + s * 0.13, top + h * 0.48], 2, col, s)
    line(d, [(cx, top + h * 0.12), (cx, top)], s, INK, lw(s) * 2)
    for k in range(6):
        y = base - (base - top - h * 0.47) * k / 6 - s * 0.24
        if y > top + h * 0.47:
            line(d, [(cx - s * 0.25 + k * s * 0.02, y), (cx + s * 0.25 - k * s * 0.02, y - s * 0.06)], s, (90, 60, 40), max(2, lw(s) // 2))


def thermometer(d, cx, cy, s, t, level=0.5, hot=True, **o):
    rrect(d, [cx - s * 0.1, cy - s * 0.48, cx + s * 0.1, cy + s * 0.25], s * 0.1, WHITE, s)
    col = (240, 70, 60) if hot else (80, 160, 240)
    circ(d, cx, cy + s * 0.32, s * 0.17, col, s)
    yt = cy + s * 0.25 - (s * 0.68) * level
    rrect(d, [cx - s * 0.05, yt, cx + s * 0.05, cy + s * 0.3], s * 0.05, col, s, False)


def snowflake(d, cx, cy, s, t, **o):
    for i in range(6):
        a = i / 6 * math.pi + t * 0.3
        dx, dy = math.cos(a) * s * 0.45, math.sin(a) * s * 0.45
        line(d, [(cx - dx, cy - dy), (cx + dx, cy + dy)], s, (120, 190, 240), lw(s) * 2)


def island(d, cx, cy, s, t, **o):
    for i in range(3):
        y = cy + s * 0.3 + i * s * 0.07
        line(d, [(cx - s * 0.6 + x * s * 0.1, y + math.sin(t * 3 + x + i) * s * 0.015) for x in range(13)], s, (70, 150, 235), lw(s))
    poly(d, [(cx - s * 0.55, cy + s * 0.3), (cx - s * 0.3, cy - s * 0.15), (cx - s * 0.12, cy + s * 0.05), (cx + s * 0.05, cy - s * 0.35),
             (cx + s * 0.25, cy - s * 0.05), (cx + s * 0.38, cy - s * 0.2), (cx + s * 0.55, cy + s * 0.3)], (110, 190, 110), s)
    for x0, x1 in ((-0.12, -0.05), (0.25, 0.3)):
        line(d, [(cx + s * x0, cy + s * 0.05), (cx + s * (x0 + 0.06), cy + s * 0.28)], s, (70, 130, 70))
        line(d, [(cx + s * x1, cy - s * 0.05), (cx + s * (x1 - 0.03), cy + s * 0.28)], s, (70, 130, 70))


def person(d, cx, cy, s, t, whistle=False, col=(240, 120, 80), **o):
    rrect(d, [cx - s * 0.2, cy - s * 0.05, cx + s * 0.2, cy + s * 0.5], s * 0.12, col, s)
    circ(d, cx, cy - s * 0.22, s * 0.18, (255, 215, 180), s)
    poly(d, [(cx - s * 0.26, cy - s * 0.3), (cx + s * 0.26, cy - s * 0.3), (cx + s * 0.14, cy - s * 0.42), (cx - s * 0.14, cy - s * 0.42)],
         (120, 80, 50), s)
    if whistle:
        line(d, [(cx + s * 0.18, cy + s * 0.1), (cx + s * 0.05, cy - s * 0.15)], s, (255, 215, 180), lw(s) * 3)
        for k in range(3):
            r = s * (0.25 + k * 0.13) + (t * s * 0.2) % (s * 0.13)
            d.arc([cx + s * 0.1 - r, cy - s * 0.2 - r, cx + s * 0.1 + r, cy - s * 0.2 + r], -40, 40, fill=INK, width=lw(s))


def waves(d, cx, cy, s, t, **o):
    for k in range(4):
        r = s * 0.15 + ((t * 0.6 + k * 0.25) % 1.0) * s * 0.4
        a = 1 - ((t * 0.6 + k * 0.25) % 1.0)
        col = tuple(int(INK[i] * a + 255 * (1 - a)) for i in range(3))
        d.arc([cx - r, cy - r, cx + r, cy + r], -45, 45, fill=col, width=lw(s))


def medal(d, cx, cy, s, t, **o):
    poly(d, [(cx - s * 0.2, cy - s * 0.5), (cx - s * 0.05, cy - s * 0.5), (cx + s * 0.05, cy - s * 0.05), (cx - s * 0.1, cy - s * 0.05)], (90, 140, 230), s)
    poly(d, [(cx + s * 0.2, cy - s * 0.5), (cx + s * 0.05, cy - s * 0.5), (cx - s * 0.05, cy - s * 0.05), (cx + s * 0.1, cy - s * 0.05)], (230, 80, 90), s)
    circ(d, cx, cy + s * 0.15, s * 0.3, (250, 200, 60), s)
    star(d, cx, cy + s * 0.15, s * 0.16, WHITE)


def book(d, cx, cy, s, t, **o):
    rrect(d, [cx - s * 0.45, cy - s * 0.3, cx, cy + s * 0.3], s * 0.03, (90, 140, 230), s)
    rrect(d, [cx, cy - s * 0.3, cx + s * 0.45, cy + s * 0.3], s * 0.03, (90, 140, 230), s)
    rrect(d, [cx - s * 0.4, cy - s * 0.25, cx - s * 0.02, cy + s * 0.25], s * 0.02, WHITE, s)
    rrect(d, [cx + s * 0.02, cy - s * 0.25, cx + s * 0.4, cy + s * 0.25], s * 0.02, WHITE, s)
    for k in range(4):
        y = cy - s * 0.15 + k * s * 0.09
        line(d, [(cx - s * 0.33, y), (cx - s * 0.08, y)], s, (170, 170, 190), max(2, lw(s) // 2))
        line(d, [(cx + s * 0.08, y), (cx + s * 0.33, y)], s, (170, 170, 190), max(2, lw(s) // 2))


def cloud(d, cx, cy, s, t, rain=False, **o):
    if rain:
        for k in range(7):
            x = cx - s * 0.3 + k * s * 0.1
            y = cy + s * 0.2 + ((t * 1.5 + k * 0.37) % 1.0) * s * 0.4
            line(d, [(x, y), (x - s * 0.02, y + s * 0.07)], s, (70, 150, 235), lw(s) * 2)
    for bx, by, br in ((-0.25, 0.05, 0.2), (0.0, -0.08, 0.27), (0.25, 0.05, 0.2)):
        circ(d, cx + s * bx, cy + s * by, s * br, WHITE, s)
    d.rectangle([cx - s * 0.25, cy, cx + s * 0.25, cy + s * 0.24], fill=WHITE)
    line(d, [(cx - s * 0.32, cy + s * 0.24), (cx + s * 0.32, cy + s * 0.24)], s)


def rock(d, cx, cy, s, t, **o):
    poly(d, [(cx - s * 0.45, cy + s * 0.3), (cx - s * 0.35, cy - s * 0.1), (cx - s * 0.05, cy - s * 0.3), (cx + s * 0.3, cy - s * 0.2),
             (cx + s * 0.45, cy + s * 0.3)], (160, 150, 145), s)
    for k in range(5):
        x = cx - s * 0.2 + k * s * 0.1
        circ(d, x, cy + s * 0.05 + (k % 2) * s * 0.08, s * 0.025, (250, 250, 250), s, False)


def river(d, cx, cy, s, t, **o):
    pts_l = [(cx - s * 0.5 + i * s * 0.1, cy - s * 0.1 + math.sin(i * 0.8 + t * 2) * s * 0.06) for i in range(11)]
    pts_r = [(x, y + s * 0.2) for x, y in pts_l]
    poly(d, pts_l + pts_r[::-1], (110, 180, 245), s)


def ocean(d, cx, cy, s, t, **o):
    rrect(d, [cx - s * 0.55, cy - s * 0.25, cx + s * 0.55, cy + s * 0.3], s * 0.08, (60, 130, 220), s)
    for k in range(3):
        y = cy - s * 0.12 + k * s * 0.13
        line(d, [(cx - s * 0.45 + i * s * 0.1, y + math.sin(i * 1.3 + t * 3 + k) * s * 0.03) for i in range(10)], s, WHITE, lw(s))


def salt(d, cx, cy, s, t, **o):
    rrect(d, [cx - s * 0.2, cy - s * 0.25, cx + s * 0.2, cy + s * 0.45], s * 0.08, WHITE, s)
    rrect(d, [cx - s * 0.2, cy - s * 0.42, cx + s * 0.2, cy - s * 0.22], s * 0.08, (180, 180, 200), s)
    for x in (-0.08, 0, 0.08):
        circ(d, cx + s * x, cy - s * 0.32, s * 0.018, INK, s, False)
    text_c(d, cx, cy + s * 0.12, "SAL", s * 0.13)


def crystals(d, cx, cy, s, t, **o):
    rng = random.Random(4)
    for _ in range(9):
        x, y, r = cx + rng.uniform(-0.4, 0.4) * s, cy + rng.uniform(-0.3, 0.3) * s, s * rng.uniform(0.05, 0.1)
        rrect(d, [x - r, y - r, x + r, y + r], 2, WHITE, s)


def glass(d, cx, cy, s, t, salty=False, **o):
    poly(d, [(cx - s * 0.3, cy - s * 0.45), (cx + s * 0.3, cy - s * 0.45), (cx + s * 0.22, cy + s * 0.45), (cx - s * 0.22, cy + s * 0.45)],
         (235, 245, 255), s)
    poly(d, [(cx - s * 0.27, cy - s * 0.15), (cx + s * 0.27, cy - s * 0.15), (cx + s * 0.22, cy + s * 0.43), (cx - s * 0.22, cy + s * 0.43)],
         (110, 180, 245), s, False)
    if salty:
        crystals(d, cx, cy + s * 0.15, s * 0.4, t)


def plane(d, cx, cy, s, t, col=WHITE, stripe=(90, 140, 230), **o):
    poly(d, [(cx - s * 0.3, cy - s * 0.03), (cx - s * 0.48, cy - s * 0.32), (cx - s * 0.36, cy - s * 0.32), (cx - s * 0.18, cy - s * 0.05)],
         stripe, s)
    rrect(d, [cx - s * 0.5, cy - s * 0.1, cx + s * 0.5, cy + s * 0.1], s * 0.1, col, s)
    poly(d, [(cx - s * 0.05, cy + s * 0.02), (cx + s * 0.12, cy + s * 0.02), (cx - s * 0.1, cy + s * 0.3), (cx - s * 0.2, cy + s * 0.3)], col, s)
    for k in range(9):
        circ(d, cx - s * 0.25 + k * s * 0.07, cy - s * 0.02, s * 0.018, (90, 140, 230), s, False)
    poly(d, [(cx + s * 0.38, cy - s * 0.05), (cx + s * 0.46, cy - s * 0.05), (cx + s * 0.48, cy), (cx + s * 0.38, cy)], (90, 140, 230), s, False)


def paint(d, cx, cy, s, t, col=(240, 80, 120), **o):
    poly(d, [(cx - s * 0.3, cy - s * 0.25), (cx + s * 0.3, cy - s * 0.25), (cx + s * 0.24, cy + s * 0.4), (cx - s * 0.24, cy + s * 0.4)],
         (200, 200, 215), s)
    d.ellipse([cx - s * 0.3, cy - s * 0.33, cx + s * 0.3, cy - s * 0.17], fill=col, outline=INK, width=lw(s))
    drip = ((t * 0.7) % 1.0) * s * 0.3
    rrect(d, [cx + s * 0.12, cy - s * 0.25, cx + s * 0.2, cy - s * 0.15 + drip], s * 0.04, col, s)


def magnifier(d, cx, cy, s, t, crack=True, **o):
    line(d, [(cx + s * 0.2, cy + s * 0.2), (cx + s * 0.45, cy + s * 0.45)], s, (120, 80, 50), lw(s) * 4)
    circ(d, cx - s * 0.05, cy - s * 0.05, s * 0.32, (220, 240, 255), s)
    if crack:
        line(d, [(cx - s * 0.25, cy - s * 0.15), (cx - s * 0.1, cy - s * 0.05), (cx - s * 0.13, cy + s * 0.05),
                 (cx + s * 0.05, cy + s * 0.1), (cx + s * 0.15, cy + s * 0.02)], s, (220, 60, 60), lw(s))


def bird(d, cx, cy, s, t, **o):
    f = math.sin(t * 8) * s * 0.15
    line(d, [(cx - s * 0.4, cy - f), (cx - s * 0.1, cy), (cx, cy + s * 0.08), (cx + s * 0.1, cy), (cx + s * 0.4, cy - f)], s, INK, lw(s) * 2)


def weight(d, cx, cy, s, t, label="kg", **o):
    poly(d, [(cx - s * 0.3, cy - s * 0.2), (cx + s * 0.3, cy - s * 0.2), (cx + s * 0.42, cy + s * 0.35), (cx - s * 0.42, cy + s * 0.35)],
         (90, 90, 110), s)
    d.arc([cx - s * 0.12, cy - s * 0.42, cx + s * 0.12, cy - s * 0.12], 180, 360, fill=INK, width=lw(s) * 2)
    text_c(d, cx, cy + s * 0.1, label, s * 0.2, WHITE)


def window(d, cx, cy, s, t, shade=0.0, night=False, **o):
    rrect(d, [cx - s * 0.32, cy - s * 0.45, cx + s * 0.32, cy + s * 0.45], s * 0.3, (235, 235, 240), s)
    sky = (30, 40, 90) if night else (140, 200, 255)
    rrect(d, [cx - s * 0.22, cy - s * 0.33, cx + s * 0.22, cy + s * 0.33], s * 0.2, sky, s)
    if not night:
        cloud(d, cx, cy + s * 0.1, s * 0.25, t)
    if shade > 0:
        rrect(d, [cx - s * 0.22, cy - s * 0.33, cx + s * 0.22, cy - s * 0.33 + s * 0.66 * shade], s * 0.15, (200, 200, 210), s)


def bulb(d, cx, cy, s, t, on=1.0, **o):
    if on > 0.05:
        for i in range(8):
            a = i / 8 * 2 * math.pi
            col = (255, 220, 80)
            line(d, [(cx + s * 0.38 * math.cos(a), cy - s * 0.1 + s * 0.38 * math.sin(a)),
                     (cx + s * (0.38 + 0.12 * on) * math.cos(a), cy - s * 0.1 + s * (0.38 + 0.12 * on) * math.sin(a))], s, col, lw(s) * 2)
    glow = tuple(int(200 + 55 * on) if i < 2 else int(200 - 120 * on) for i in range(3))
    circ(d, cx, cy - s * 0.1, s * 0.28, glow, s)
    rrect(d, [cx - s * 0.13, cy + s * 0.15, cx + s * 0.13, cy + s * 0.35], s * 0.04, (160, 160, 175), s)


def exit_sign(d, cx, cy, s, t, **o):
    rrect(d, [cx - s * 0.5, cy - s * 0.2, cx + s * 0.5, cy + s * 0.2], s * 0.05, (40, 170, 90), s)
    text_c(d, cx, cy + s * 0.02, "SALIDA", s * 0.2, WHITE)


def fire(d, cx, cy, s, t, **o):
    f = math.sin(t * 10) * s * 0.04
    poly(d, [(cx - s * 0.3, cy + s * 0.35), (cx - s * 0.32, cy), (cx - s * 0.12, cy - s * 0.2), (cx - s * 0.05 + f, cy - s * 0.5),
             (cx + s * 0.12, cy - s * 0.15), (cx + s * 0.25, cy - s * 0.3 - f), (cx + s * 0.32, cy + s * 0.05), (cx + s * 0.3, cy + s * 0.35)],
         (255, 120, 40), s)
    poly(d, [(cx - s * 0.15, cy + s * 0.35), (cx - s * 0.12, cy + s * 0.08), (cx + f, cy - s * 0.15), (cx + s * 0.13, cy + s * 0.1),
             (cx + s * 0.15, cy + s * 0.35)], (255, 210, 60), s, False)


def bacteria(d, cx, cy, s, t, col=(120, 210, 120), **o):
    wob = math.sin(t * 3) * s * 0.02
    for k in range(3):
        y = cy + (k - 1) * s * 0.12
        line(d, [(cx + s * 0.38, y), (cx + s * 0.48, y + math.sin(t * 6 + k) * s * 0.05), (cx + s * 0.58, y)], s)
    rrect(d, [cx - s * 0.4, cy - s * 0.22 + wob, cx + s * 0.4, cy + s * 0.22 - wob], s * 0.22, col, s)
    cute_face(d, cx - s * 0.05, cy, s, t)


def cell(d, cx, cy, s, t, **o):
    circ(d, cx, cy, s * 0.42, (235, 80, 90), s)
    d.ellipse([cx - s * 0.22, cy - s * 0.12, cx + s * 0.22, cy + s * 0.12], fill=(205, 60, 70))
    cute_face(d, cx, cy + s * 0.05, s * 0.9, t + 1.3)


def scale(d, cx, cy, s, t, tilt=0.0, **o):
    a = math.radians(tilt)
    rrect(d, [cx - s * 0.05, cy - s * 0.3, cx + s * 0.05, cy + s * 0.4], s * 0.02, (150, 110, 70), s)
    rrect(d, [cx - s * 0.25, cy + s * 0.38, cx + s * 0.25, cy + s * 0.46], s * 0.02, (150, 110, 70), s)
    x1, y1 = cx - s * 0.45 * math.cos(a), cy - s * 0.3 - s * 0.45 * math.sin(a)
    x2, y2 = cx + s * 0.45 * math.cos(a), cy - s * 0.3 + s * 0.45 * math.sin(a)
    line(d, [(x1, y1), (x2, y2)], s, INK, lw(s) * 2)
    for x, y in ((x1, y1), (x2, y2)):
        line(d, [(x, y), (x - s * 0.12, y + s * 0.25)], s)
        line(d, [(x, y), (x + s * 0.12, y + s * 0.25)], s)
        d.chord([x - s * 0.16, y + s * 0.15, x + s * 0.16, y + s * 0.35], 0, 180, fill=(250, 200, 60), outline=INK, width=lw(s))


def toilet(d, cx, cy, s, t, **o):
    rrect(d, [cx - s * 0.12, cy - s * 0.45, cx + s * 0.3, cy - s * 0.05], s * 0.05, WHITE, s)
    d.ellipse([cx - s * 0.4, cy - s * 0.12, cx + s * 0.3, cy + s * 0.12], fill=WHITE, outline=INK, width=lw(s))
    poly(d, [(cx - s * 0.3, cy), (cx + s * 0.2, cy), (cx + s * 0.1, cy + s * 0.45), (cx - s * 0.2, cy + s * 0.45)], WHITE, s)


def car(d, cx, cy, s, t, **o):
    poly(d, [(cx - s * 0.5, cy + s * 0.1), (cx - s * 0.45, cy - s * 0.05), (cx - s * 0.2, cy - s * 0.1), (cx - s * 0.08, cy - s * 0.3),
             (cx + s * 0.25, cy - s * 0.3), (cx + s * 0.38, cy - s * 0.1), (cx + s * 0.5, cy - s * 0.05), (cx + s * 0.5, cy + s * 0.15),
             (cx - s * 0.5, cy + s * 0.15)], (230, 70, 80), s)
    poly(d, [(cx - s * 0.03, cy - s * 0.25), (cx + s * 0.09, cy - s * 0.25), (cx + s * 0.09, cy - s * 0.1), (cx - s * 0.15, cy - s * 0.1)],
         (160, 215, 250), s)
    poly(d, [(cx + s * 0.13, cy - s * 0.25), (cx + s * 0.23, cy - s * 0.25), (cx + s * 0.32, cy - s * 0.1), (cx + s * 0.13, cy - s * 0.1)],
         (160, 215, 250), s)
    for x in (-0.28, 0.3):
        circ(d, cx + s * x, cy + s * 0.15, s * 0.11, (50, 50, 60), s)
        circ(d, cx + s * x, cy + s * 0.15, s * 0.045, (200, 200, 210), s, False)


def pane(d, cx, cy, s, t, mode="ok", k=1.0, **o):
    box = [cx - s * 0.4, cy - s * 0.45, cx + s * 0.4, cy + s * 0.45]
    if mode == "shatter":
        rng = random.Random(5)
        n = 7
        cw, ch = s * 0.8 / n, s * 0.9 / n
        for i in range(n):
            for j in range(n):
                dx = rng.uniform(-1, 1) * s * 0.08 * k
                dy = (rng.uniform(0, 1) * s * 0.25 + j * 4) * k
                x0, y0 = box[0] + i * cw + dx, box[1] + j * ch + dy
                d.rectangle([x0 + 2, y0 + 2, x0 + cw - 2, y0 + ch - 2], fill=(190, 230, 250), outline=INK, width=2)
        return
    rrect(d, box, s * 0.04, (190, 230, 250), s)
    line(d, [(cx - s * 0.25, cy - s * 0.3), (cx - s * 0.05, cy - s * 0.38)], s, WHITE, lw(s) * 2)
    if mode == "web":
        ox, oy = cx + s * 0.05, cy
        for i in range(9):
            a = i / 9 * 2 * math.pi
            line(d, [(ox, oy), (ox + s * 0.38 * math.cos(a) * k, oy + s * 0.4 * math.sin(a) * k)], s, INK, max(2, lw(s) // 2))
        for r in (0.1, 0.22):
            pts = [(ox + s * r * math.cos(i / 9 * 2 * math.pi) * k, oy + s * r * math.sin(i / 9 * 2 * math.pi) * k) for i in range(10)]
            line(d, pts, s, INK, max(2, lw(s) // 2))


def layers(d, cx, cy, s, t, spread=1.0, **o):
    cols = [((190, 230, 250), "Cristal"), ((255, 210, 63), "Plástico"), ((190, 230, 250), "Cristal")]
    for i, (col, nm) in enumerate(cols):
        y = cy + (i - 1) * s * 0.22 * (0.5 + 0.5 * spread)
        poly(d, [(cx - s * 0.45, y), (cx + s * 0.25, y), (cx + s * 0.45, y - s * 0.1), (cx - s * 0.25, y - s * 0.1)], col, s)
        text_c(d, cx + s * 0.58, y - s * 0.02, nm, s * 0.09)


def fan(d, cx, cy, s, t, **o):
    circ(d, cx, cy, s * 0.45, (220, 240, 255), s)
    for i in range(3):
        a = i / 3 * 2 * math.pi + t * 8
        poly(d, [(cx, cy), (cx + s * 0.35 * math.cos(a - 0.3), cy + s * 0.35 * math.sin(a - 0.3)),
                 (cx + s * 0.35 * math.cos(a + 0.3), cy + s * 0.35 * math.sin(a + 0.3))], (90, 140, 230), s)
    circ(d, cx, cy, s * 0.06, INK, s, False)


def venus(d, cx, cy, s, t, face=True, **o):
    r = s * 0.48
    circ(d, cx, cy, r, (240, 200, 120), s)
    for k in range(4):
        y = cy - r * 0.6 + k * r * 0.4
        w = math.sqrt(max(0, r * r - (y - cy) ** 2)) * 0.9
        line(d, [(cx - w + i * w / 5, y + math.sin(i + t + k) * r * 0.05) for i in range(11)], s, (215, 160, 80), lw(s))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=lw(s))
    if face:
        cute_face(d, cx, cy + r * 0.15, s * 0.8, t + 0.7)


def calendar(d, cx, cy, s, t, txt="243", sub="días", **o):
    rrect(d, [cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy + s * 0.45], s * 0.06, WHITE, s)
    rrect(d, [cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy - s * 0.18], s * 0.06, (235, 80, 90), s)
    for x in (-0.2, 0.2):
        rrect(d, [cx + s * x - s * 0.03, cy - s * 0.48, cx + s * x + s * 0.03, cy - s * 0.32], s * 0.02, (150, 150, 165), s)
    text_c(d, cx, cy + s * 0.08, txt, s * 0.3)
    text_c(d, cx, cy + s * 0.33, sub, s * 0.1, (110, 110, 130), False)


def drop(d, cx, cy, s, t, col=(160, 165, 180), **o):
    pts = [(cx, cy - s * 0.45)]
    for i in range(17):
        a = math.pi * i / 16
        pts.append((cx + s * 0.3 * math.cos(a - math.pi / 2 + math.pi / 2) * 1, cy + s * 0.12 + s * 0.3 * math.sin(a)))
    poly(d, [(cx, cy - s * 0.45), (cx + s * 0.3, cy + s * 0.12)] + [(cx + s * 0.3 * math.cos(a), cy + s * 0.12 + s * 0.3 * math.sin(a))
                                                                     for a in [i * math.pi / 12 for i in range(13)]] +
         [(cx - s * 0.3, cy + s * 0.12)], col, s)


def arrow(d, cx, cy, s, t, ang=0.0, col=INK, **o):
    a = math.radians(ang)
    x0, y0 = cx - s * 0.45 * math.cos(a), cy - s * 0.45 * math.sin(a)
    x1, y1 = cx + s * 0.45 * math.cos(a), cy + s * 0.45 * math.sin(a)
    d.line([(x0, y0), (x1, y1)], fill=col, width=lw(s) * 3)
    h = s * 0.2
    d.polygon([(x1 + math.cos(a) * h * 0.4, y1 + math.sin(a) * h * 0.4), (x1 - h * math.cos(a - 0.6), y1 - h * math.sin(a - 0.6)),
               (x1 - h * math.cos(a + 0.6), y1 - h * math.sin(a + 0.6))], fill=col)


def curve_arrow(d, cx, cy, s, t, **o):
    r = s * 0.42
    a0 = t * 1.5
    d.arc([cx - r, cy - r, cx + r, cy + r], math.degrees(a0), math.degrees(a0) + 290, fill=INK, width=lw(s) * 2)
    a = a0 + math.radians(290)
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    h = s * 0.12
    tang = a + math.pi / 2
    d.polygon([(x + h * math.cos(tang), y + h * math.sin(tang)), (x + h * 0.7 * math.cos(a), y + h * 0.7 * math.sin(a)),
               (x - h * 0.7 * math.cos(a), y - h * 0.7 * math.sin(a))], fill=INK)


def cross(d, cx, cy, s, t, **o):
    for sgn in (1, -1):
        d.line([(cx - s * 0.4, cy - s * 0.4 * sgn), (cx + s * 0.4, cy + s * 0.4 * sgn)], fill=(230, 50, 60), width=lw(s) * 4)


def check(d, cx, cy, s, t, **o):
    d.line([(cx - s * 0.4, cy), (cx - s * 0.1, cy + s * 0.3), (cx + s * 0.45, cy - s * 0.35)], fill=(40, 170, 90), width=lw(s) * 4, joint="curve")


def qmark(d, cx, cy, s, t, **o):
    circ(d, cx, cy, s * 0.45, WHITE, s)
    text_c(d, cx, cy + s * 0.05, "?", s * 0.6)


def orbit(d, cx, cy, s, t, center="earth", body="moon", speed=0.6, locked=True, **o):
    R_ = s * 0.42
    d.ellipse([cx - R_, cy - R_ * 0.45, cx + R_, cy + R_ * 0.45], outline=(110, 110, 130), width=max(2, lw(s) // 2))
    a = t * speed
    bx, by = cx + R_ * math.cos(a), cy + R_ * 0.45 * math.sin(a)
    front = math.sin(a) > 0
    if not front:
        draw(body, d, bx, by, s * 0.22, t, face=False) if body != "moon" else moon(d, bx, by, s * 0.22, t)
    draw(center, d, cx, cy, s * 0.42, t, face=False) if center != "earth" else earth(d, cx, cy, s * 0.42, t)
    if front:
        draw(body, d, bx, by, s * 0.22, t, face=False) if body != "moon" else moon(d, bx, by, s * 0.22, t)
    if locked:
        ang = math.atan2(cy - by, cx - bx)
        mx, my = bx + s * 0.08 * math.cos(ang), by + s * 0.08 * math.sin(ang)
        d.ellipse([mx - s * 0.025, my - s * 0.025, mx + s * 0.025, my + s * 0.025], fill=(230, 50, 60), outline=INK, width=2)


ICONS = {k: v for k, v in globals().items() if callable(v) and k not in (
    "pf", "lw", "circ", "poly", "rrect", "line", "text_c", "cute_face", "star", "ImageFont")}


# ------------------------------------------------------------------ mascota
def mascot(d, cx, cy, s, t, mood="wow", **o):
    """El ojo del canal con expresiones: wow, think, happy, no, wink."""
    if mood == "no":
        cx += math.sin(t * 18) * s * 0.05
    bob = math.sin(t * 3) * s * 0.02
    cy += bob
    w, h = s * 0.5, s * 0.3
    top = [(cx - w + 2 * w * i / 20, cy - h * math.sin(math.pi * i / 20)) for i in range(21)]
    bot = [(cx + w - 2 * w * i / 20, cy + h * math.sin(math.pi * i / 20)) for i in range(21)]
    d.polygon(top + bot, fill=WHITE, outline=INK, width=lw(s) * 2)
    blink = (t % 2.8) < 0.13 or mood == "happy"
    if mood == "happy":
        d.arc([cx - s * 0.2, cy - s * 0.1, cx + s * 0.2, cy + s * 0.2], 200, 340, fill=INK, width=lw(s) * 2)
    elif blink:
        d.line([(cx - w * 0.8, cy), (cx + w * 0.8, cy)], fill=INK, width=lw(s) * 2)
    else:
        look = {"think": (-0.12, -0.08), "wow": (0, 0), "no": (0, 0), "wink": (0.05, 0)}.get(mood, (0, 0))
        r = s * (0.2 if mood == "wow" else 0.17)
        px, py = cx + look[0] * s, cy + look[1] * s
        d.ellipse([px - r, py - r, px + r, py + r], fill=YEL, outline=INK, width=lw(s))
        text_c(d, px, py + r * 0.05, "?", r * 1.3)
    by = cy - h - s * 0.1
    tilt = {"think": 0.12, "wow": -0.04, "no": 0.1, "happy": 0, "wink": 0.05}.get(mood, 0)
    d.line([(cx - s * 0.25, by + tilt * s), (cx + s * 0.25, by - tilt * s)], fill=INK, width=lw(s) * 3)
    bubble = {"wow": "!", "think": "?", "no": "NO", "happy": "", "wink": ""}.get(mood, "")
    if bubble and o.get("bubble", True):
        bx, byy = cx + s * 0.55, cy - s * 0.45
        rrect(d, [bx - s * 0.17, byy - s * 0.15, bx + s * 0.17, byy + s * 0.15], s * 0.08, WHITE, s)
        poly(d, [(bx - s * 0.12, byy + s * 0.1), (bx - s * 0.22, byy + s * 0.25), (bx - s * 0.02, byy + s * 0.13)], WHITE, s, False)
        text_c(d, bx, byy + s * 0.02, bubble, s * (0.18 if len(bubble) > 1 else 0.24))


def draw(name, d, cx, cy, s, t, **o):
    if name == "mascot":
        return mascot(d, cx, cy, s, t, **o)
    ICONS[name](d, cx, cy, s, t, **o)
