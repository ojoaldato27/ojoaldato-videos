"""Estilo «neón explicativo» (inspirado en 1Volt1Amp / 1Bit1Pixel, sin copiar):
fondo casi negro con cuadrícula técnica, dibujos de línea que se trazan solos y brillan, el mecanismo siempre a la vista.
Se apoya en cine.py (tiempos, encuadre suave, fundidos, subtítulos, banner, cierre y sonido)."""
from cine import *
from PIL import ImageChops

F_POP = GF + "google-fonts/Poppins-Bold.ttf"
F_POPM = GF + "google-fonts/Poppins-Medium.ttf"
F_INTB = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
F_INT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"

CY = (0, 229, 255)
YE = (255, 210, 63)
MG = (255, 61, 139)
GR = (61, 255, 139)
OR = (255, 140, 40)
WH = (235, 242, 255)
RD = (255, 64, 64)
BL = (80, 140, 255)
DIM = (60, 80, 120)


# ------------------------------------------------------------------ fondo y capa de neón
def bg(img, t, grid=True, top=(7, 9, 20), bot=(2, 3, 8), dust=True):
    sky(img, top, bot, 1.0)
    if grid:
        def mk():
            im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            for x in range(0, W + 1, 60):
                d.line([(x, 0), (x, H)], fill=(40, 60, 100, 34), width=1)
            for y in range(0, H + 1, 60):
                d.line([(0, y), (W, y)], fill=(40, 60, 100, 34), width=1)
            for x in range(0, W + 1, 300):
                d.line([(x, 0), (x, H)], fill=(40, 70, 120, 50), width=2)
            for y in range(0, H + 1, 300):
                d.line([(0, y), (W, y)], fill=(40, 70, 120, 50), width=2)
            return im
        AC(img, cached(("ngrid",), mk))
    if dust:
        particles(img, t, 36, 77, (90, 130, 220), -10, (1, 2.2), 80, 30)


def layer():
    im = Image.new("RGB", (W, H), (0, 0, 0))
    return im, ImageDraw.Draw(im)


def finish(img, lay, glow=1.0):
    """Aplica el brillo de neón: halo ancho + halo cercano + línea nítida (suma de luz)."""
    small = lay.resize((W // 4, H // 4), Image.BILINEAR)
    g1 = small.filter(ImageFilter.GaussianBlur(7)).resize((W, H), Image.BILINEAR)
    g2 = lay.resize((W // 2, H // 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR)
    if glow != 1.0:
        g1 = g1.point(lambda v: min(255, int(v * glow)))
    out = ImageChops.add(img, g1)
    out = ImageChops.add(out, g1)
    out = ImageChops.add(out, g2)
    out = ImageChops.lighter(out, lay)
    img.paste(out)


# ------------------------------------------------------------------ trazos
def plen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def partial(pts, k):
    if k >= 0.999:
        return list(pts)
    if k <= 0 or len(pts) < 2:
        return pts[:1]
    tot = plen(pts) * k
    out = [pts[0]]
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        L_ = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + L_ >= tot:
            u = (tot - acc) / (L_ or 1)
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
            return out
        out.append(b)
        acc += L_
    return out


def line(d, pts, col, w=6, k=1.0):
    pp = partial(pts, k)
    if len(pp) >= 2:
        d.line(pp, fill=col, width=int(w), joint="curve")
        r = w / 2
        for x, y in (pp[0], pp[-1]):
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def circle(d, cx, cy, r, col, w=6, k=1.0, start=-90):
    if k <= 0:
        return
    if k >= 0.999:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=int(w))
    else:
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 360 * k, fill=col, width=int(w))


def dot(d, x, y, r, col):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def rect(d, x0, y0, x1, y1, col, w=6, k=1.0):
    line(d, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], col, w, k)


def rrect_pts(x0, y0, x1, y1, r, n=6):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    pts.append(pts[0])
    return pts


def rrect(d, x0, y0, x1, y1, r, col, w=6, k=1.0):
    line(d, rrect_pts(x0, y0, x1, y1, r), col, w, k)


def arrow(d, p0, p1, col, w=6, k=1.0, head=26):
    if k <= 0:
        return
    x = p0[0] + (p1[0] - p0[0]) * k
    y = p0[1] + (p1[1] - p0[1]) * k
    d.line([p0, (x, y)], fill=col, width=int(w))
    a = math.atan2(y - p0[1], x - p0[0])
    for s_ in (-1, 1):
        d.line([(x, y), (x - math.cos(a + s_ * 0.5) * head, y - math.sin(a + s_ * 0.5) * head)], fill=col, width=int(w))


def sine(d, x0, x1, y, amp, wl, ph, col, w=5, k=1.0, step=6):
    pts = [(x, y + amp * math.sin((x - x0) / wl * 2 * math.pi + ph)) for x in range(int(x0), int(x1) + 1, step)]
    line(d, pts, col, w, k)


def label(d, x, y, txt, size, col, font=None, anchor="mm"):
    d.text((x, y), txt, font=f(font or F_MONO, size), fill=col, anchor=anchor)


def dashed(d, p0, p1, col, w=4, dash=18, gap=14, off=0.0):
    L_ = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if L_ <= 0:
        return
    ux, uy = (p1[0] - p0[0]) / L_, (p1[1] - p0[1]) / L_
    s_ = -((off) % (dash + gap))
    while s_ < L_:
        a, b = max(0, s_), min(L_, s_ + dash)
        if b > a:
            d.line([(p0[0] + ux * a, p0[1] + uy * a), (p0[0] + ux * b, p0[1] + uy * b)], fill=col, width=int(w))
        s_ += dash + gap


# ------------------------------------------------------------------ textos con brillo (capa fija)
def _gtext(txt, size, col, font):
    fnt = f(font, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bb = tmp.textbbox((0, 0), txt, font=fnt)
    w, h = bb[2] - bb[0] + 120, bb[3] - bb[1] + 120
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((60 - bb[0], 60 - bb[1]), txt, font=fnt, fill=col + (255,))
    gl = im.filter(ImageFilter.GaussianBlur(max(6, size * 0.16)))
    base = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    base.alpha_composite(gl)
    base.alpha_composite(gl)
    core = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(core).text((60 - bb[0], 60 - bb[1]), txt, font=fnt, fill=tuple(min(255, c + 70) for c in col) + (255,))
    base.alpha_composite(core)
    return base


def gtext(txt, size, col, font=None, cache=True):
    font = font or F_POP
    if cache:
        return spr(_gtext, txt, int(size), tuple(col), font)
    return _gtext(txt, int(size), tuple(col), font)


def gtitle(t, t0, txt, y=300, size=90, col=CY, hold=None, font=None, pop=True, cache=True, x=W / 2):
    k = fade_k(t, t0, hold, 0.35)
    if k <= 0:
        return
    s_ = lerp(1.15, 1.0, ease(clamp((t - t0) / 0.35))) if pop else 1.0
    im = gtext(txt, size, col, font, cache)
    paste(TOP[0], im, x, y + im.size[1] / 2 - 60, s_, k)


def gtitle2(t, t0, l1, l2, y=280, s1=56, s2=96, c1=WH, c2=CY, hold=None):
    k = fade_k(t, t0, hold, 0.4)
    if k <= 0:
        return
    if l1:
        paste(TOP[0], gtext(l1, s1, c1, F_POPM), W / 2, y + 20, 1.0, k)
    if l2:
        paste(TOP[0], gtext(l2, s2, c2), W / 2, y + s1 * 1.1 + 40, 1.0, k)


def chip(t, t0, txt, x, y, col=CY, size=36, hold=None):
    """Etiqueta técnica con caja (estilo pantalla)."""
    k = fade_k(t, t0, hold, 0.3)
    if k <= 0:
        return
    d = td()
    fnt = f(F_MONO, size)
    tw = d.textlength(txt, font=fnt)
    a = int(255 * k)
    d.rounded_rectangle([x - tw / 2 - 22, y - size * 0.8, x + tw / 2 + 22, y + size * 0.8], radius=12, fill=(4, 8, 18, int(200 * k)),
                        outline=col + (a,), width=3)
    d.text((x, y), txt, font=fnt, fill=col + (a,), anchor="mm")


# ------------------------------------------------------------------ iconos de línea
def car_pts(x, y, s=1.0):
    """Perfil de coche (hacia la derecha), origen en el centro de la base."""
    P_ = [(-1.0, 0.0), (-1.0, -0.32), (-0.82, -0.40), (-0.5, -0.42), (-0.3, -0.72), (0.25, -0.74), (0.5, -0.45), (0.92, -0.38),
          (1.02, -0.22), (1.02, 0.0)]
    return [(x + px * 200 * s, y + py * 200 * s) for px, py in P_]


def car(d, x, y, s, col, k=1.0, wheel_rot=0.0, w=6):
    line(d, car_pts(x, y, s), col, w, k)
    if k > 0.6:
        kk = (k - 0.6) / 0.4
        for wx in (-0.6, 0.62):
            cx, cy = x + wx * 200 * s, y
            circle(d, cx, cy, 44 * s, col, w, kk)
            for j in range(3):
                a = wheel_rot + j * 2.094
                d.line([(cx, cy), (cx + math.cos(a) * 30 * s, cy + math.sin(a) * 30 * s)], fill=col, width=max(2, int(w * 0.6)))
        line(d, [(x - 0.26 * 200 * s, y - 0.66 * 200 * s), (x + 0.2 * 200 * s, y - 0.68 * 200 * s), (x + 0.4 * 200 * s, y - 0.46 * 200 * s),
                 (x - 0.36 * 200 * s, y - 0.46 * 200 * s), (x - 0.26 * 200 * s, y - 0.66 * 200 * s)], col, max(3, w - 2), kk)


def speedo(d, cx, cy, r, val, vmax=200, col=CY, needle=YE, w=6, k=1.0):
    a0, a1 = 135, 405
    d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + (a1 - a0) * k, fill=col, width=int(w))
    for v in range(0, vmax + 1, 20):
        a = math.radians(a0 + (a1 - a0) * v / vmax)
        r1, r2 = r - 14, r - (44 if v % 40 == 0 else 28)
        d.line([(cx + math.cos(a) * r1, cy + math.sin(a) * r1), (cx + math.cos(a) * r2, cy + math.sin(a) * r2)], fill=col, width=4)
        if v % 40 == 0:
            label(d, cx + math.cos(a) * (r - 84), cy + math.sin(a) * (r - 84), str(v), 34, col)
    a = math.radians(a0 + (a1 - a0) * clamp(val / vmax))
    d.line([(cx, cy), (cx + math.cos(a) * (r - 40), cy + math.sin(a) * (r - 40))], fill=needle, width=10)
    dot(d, cx, cy, 16, needle)


def water(d, x, y, s, ang, col_o=MG, col_h=WH, w=5):
    """Molécula de agua dibujada en línea: O grande y dos H a 104,5°."""
    ro, rh, L_ = 34 * s, 20 * s, 58 * s
    circle(d, x, y, ro, col_o, w)
    label(d, x, y, "O", int(30 * s), col_o, F_POP)
    for sg in (-1, 1):
        a = ang + sg * math.radians(52)
        hx, hy = x + math.cos(a) * L_, y + math.sin(a) * L_
        d.line([(x + math.cos(a) * ro, y + math.sin(a) * ro), (hx - math.cos(a) * rh, hy - math.sin(a) * rh)], fill=col_h, width=w)
        circle(d, hx, hy, rh, col_h, w)
        label(d, hx, hy, "H", int(20 * s), col_h, F_POP)


def building(d, x, y, floors, col, w=4, k=1.0, fh=40, bw=150):
    n = int(floors * k)
    for i in range(n):
        yy = y - (i + 1) * fh
        rect(d, x - bw / 2, yy, x + bw / 2, yy + fh, col, w)
        for wx in (-40, 0, 40):
            d.rectangle([x + wx - 10, yy + 12, x + wx + 10, yy + 28], outline=col, width=2)


def end_card_neon(t_end_in):
    k = ease(clamp(t_end_in / 0.8))
    d2 = td()
    d2.rectangle([0, 0, W, H], fill=(2, 4, 10, int(215 * k)))
    R.eye_icon(d2, 540, 790, 300 * (0.9 + 0.1 * k), (255, 255, 255), YE, (14, 15, 18))
    paste(TOP[0], gtext("SI AÚN NO LO SABÍAS…", 56, WH), W / 2, 1010, 1.0, k)
    d2.text((W / 2, 1100), "@ojoaldato.ya", font=f(F_MONO, 38), fill=(200, 210, 230, int(255 * k)), anchor="mm")
    k2 = ease(clamp((t_end_in - 0.6) / 0.6))
    paste(TOP[0], gtext("MÁNDASELO A QUIEN NO LO SEPA", 40, CY), W / 2, 1200, 1.0, k2)
