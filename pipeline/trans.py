"""Transiciones variadas (21/10, Iker: «transiciones más dinámicas, no las mismas todo el rato, que haga zoom y se meta en
otro sitio, innova»). Cada corte usa una distinta y nunca se repite la anterior.

apply(kind, A, B, u, focus) mezcla el plano saliente A con el entrante B (u de 0 a 1):
  zoom_in  · la cámara se mete en un punto de A y B aparece desde ese punto en un círculo que crece
  whip     · barrido lateral con desenfoque de movimiento
  spin     · A gira y crece mientras B entra girando al revés
  iris     · círculo que se abre desde el centro
  glitch   · franjas desplazadas y separación RGB
  push     · A sube y B entra desde abajo
  scribble · un trazo de rotulador gordo va tapando A y deja ver B (estilo dibujado)
  paper    · B entra como una hoja que cae girando, con sombra (estilo dibujado)
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W, H = 1080, 1920


def ease_in(x):
    return x * x * x


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_io(x):
    return 3 * x * x - 2 * x * x * x


def _zoom(img, z, fx, fy):
    cw, ch = W / z, H / z
    x0 = fx - fx / z
    y0 = fy - fy / z
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)


def _circle(cx, cy, r):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    return m


def _shift(img, dx, dy=0):
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(img, (int(dx), int(dy)))
    return out


def zoom_in(A, B, u, focus):
    fx, fy = focus
    za = 1 + 7 * ease_in(u)
    a = _zoom(A, za, fx, fy)
    a2 = _zoom(A, za * 1.06, fx, fy)
    a = Image.blend(a, a2, 0.5)                                         # rastro de zoom
    zb = 1.6 - 0.6 * ease_out(u)
    b = _zoom(B, zb, fx, fy)
    r = (math.hypot(W, H)) * ease_in(min(1, u * 1.15))
    m = _circle(fx, fy, r).filter(ImageFilter.GaussianBlur(18))
    return Image.composite(b, a, m)


def whip(A, B, u, focus, direction=1):
    e = ease_io(u)
    off = e * W * direction
    acc = None
    for k in range(5):
        o = off + (k - 2) * 26 * math.sin(math.pi * u) * direction
        fr = _shift(A, -o)
        fr.paste(B, (int(W * direction - o), 0))
        acc = fr if acc is None else Image.blend(acc, fr, 1 / (k + 1))
    return acc


def spin(A, B, u, focus):
    e = ease_io(u)
    if u < 0.5:
        k = e / 0.5 if e < 0.5 else 1
        im = A.rotate(-30 * ease_in(u * 2), resample=Image.BILINEAR, expand=False)
        im = _zoom(im, 1 + 1.2 * ease_in(u * 2), W / 2, H / 2)
    else:
        v = (u - 0.5) * 2
        im = B.rotate(30 * (1 - ease_out(v)), resample=Image.BILINEAR, expand=False)
        im = _zoom(im, 1 + 1.2 * (1 - ease_out(v)), W / 2, H / 2)
    return im


def iris(A, B, u, focus):
    fx, fy = focus
    r = math.hypot(W, H) * ease_io(u)
    m = _circle(fx, fy, r)
    d = ImageDraw.Draw(m)
    out = Image.composite(B, A, m)
    ring = Image.new("L", (W, H), 0)
    ImageDraw.Draw(ring).ellipse([fx - r, fy - r, fx + r, fy + r], outline=255, width=10)
    out.paste((255, 255, 255), (0, 0), ring.filter(ImageFilter.GaussianBlur(3)))
    return out


def glitch(A, B, u, focus):
    rng = random.Random(int(u * 30))
    base = A if u < 0.5 else B
    out = base.copy()
    other = B if u < 0.5 else A
    amp = math.sin(math.pi * u)
    y = 0
    while y < H:
        hh = rng.randint(20, 140)
        if rng.random() < 0.55 * amp:
            src = other if rng.random() < 0.5 else base
            dx = int(rng.uniform(-180, 180) * amp)
            band = src.crop((0, y, W, min(H, y + hh)))
            out.paste(band, (dx, y))
        y += hh
    r, g, b = out.split()
    s = int(24 * amp)
    return Image.merge("RGB", (ImageChops.offset(r, s, 0), g, ImageChops.offset(b, -s, 0)))


def push(A, B, u, focus):
    e = ease_io(u)
    out = Image.new("RGB", (W, H))
    out.paste(A, (0, int(-e * H)))
    out.paste(B, (0, int(H - e * H)))
    return out


def scribble(A, B, u, focus):
    """Trazo de rotulador en zigzag que va pintando B encima de A."""
    pts = []
    rows = 9
    for k in range(rows):
        y = -80 + k * (H + 160) / (rows - 1)
        pts += [(-120, y), (W + 120, y + 110)] if k % 2 == 0 else [(W + 120, y), (-120, y + 110)]
    total = len(pts) - 1
    upto = ease_io(u) * total
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    n = int(upto)
    seg = pts[: n + 1]
    if n < total:
        f = upto - n
        x0, y0 = pts[n]
        x1, y1 = pts[n + 1]
        seg.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f))
    if len(seg) > 1:
        d.line(seg, fill=255, width=330, joint="curve")
    return Image.composite(B, A, m)


def paper(A, B, u, focus):
    e = ease_out(u)
    ang = 14 * (1 - e)
    y = -H * (1 - e)
    b = B.convert("RGBA").rotate(ang, resample=Image.BICUBIC, expand=False)
    out = A.copy()
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rectangle([30, int(y) + 40, W + 30, int(y) + H + 40], fill=110)
    out.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(30)))
    out.paste(b, (0, int(y)), b)
    return out


KINDS = {"zoom_in": zoom_in, "whip": whip, "spin": spin, "iris": iris, "glitch": glitch, "push": push, "scribble": scribble, "paper": paper}


def zoom_out(A, B, u, focus):
    """El plano A se encoge hacia el centro y deja ver B, que se asienta desde un poco más grande."""
    e = ease_in(u)
    b = _zoom(B, 1.35 - 0.35 * ease_out(u), W / 2, H / 2)
    sc = max(0.02, 1 - 0.92 * e)
    a = A.resize((max(1, int(W * sc)), max(1, int(H * sc))), Image.BILINEAR).rotate(12 * e, expand=True, resample=Image.BILINEAR)
    m = Image.new("L", a.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, a.width - 1, a.height - 1], radius=int(60 * sc) + 2, fill=255)
    m = m.rotate(0)
    b.paste(a, (int(W / 2 - a.width / 2), int(H / 2 - a.height / 2)), m if a.size == m.size else None)
    return b


def flash(A, B, u, focus):
    """Fogonazo blanco: A se quema a blanco y de ahí sale B."""
    wht = Image.new("RGB", (W, H), (255, 255, 255))
    if u < 0.5:
        return Image.blend(A, wht, ease_in(u * 2))
    return Image.blend(wht, B, ease_out((u - 0.5) * 2))


def drop(A, B, u, focus):
    """B cae desde arriba y rebota un poco sobre A."""
    if u < 0.75:
        e = ease_in(u / 0.75)
        y = -H + H * e
    else:
        v = (u - 0.75) / 0.25
        y = -60 * math.sin(math.pi * v)
    out = A.copy()
    out.paste(B, (0, int(y)))
    return out


def fall(A, B, u, focus):
    """Caída: todo sube (la cámara baja) con estela, como si cayéramos al siguiente plano."""
    e = ease_io(u)
    acc = None
    for k in range(4):
        o = e * H + (k - 1.5) * 40 * math.sin(math.pi * u)
        fr = Image.new("RGB", (W, H))
        fr.paste(A, (0, int(-o)))
        fr.paste(B, (0, int(H - o)))
        acc = fr if acc is None else Image.blend(acc, fr, 1 / (k + 1))
    return acc


KINDS.update({"zoom_out": zoom_out, "flash": flash, "drop": drop, "fall": fall})


def apply(kind, A, B, u, focus=(540, 960)):
    u = max(0.0, min(1.0, u))
    if kind == "whip_r":
        return whip(A, B, u, focus, -1)
    return KINDS[kind](A, B, u, focus)


def plan(n, pool, seed=3):
    """Lista de n transiciones del pool sin repetir dos seguidas."""
    rng = random.Random(seed)
    out, last = [], None
    for _ in range(n):
        k = rng.choice([p for p in pool if p != last])
        out.append(k)
        last = k
    return out


# ------------------------------------------------------------------ transiciones suaves (Iker, 29/10: «más fluido, no tanto pum pum»)
def suave(A, B, u, focus):
    """La escena se acerca despacio a su detalle mientras se funde con la siguiente, que llega asentándose."""
    fx, fy = focus
    e = ease_io(u)
    a = _zoom(A, 1 + 0.35 * e, fx, fy)
    b = _zoom(B, 1.18 - 0.18 * e, 540, 820)
    return Image.blend(a, b, e)


def suave_out(A, B, u, focus):
    """La siguiente escena llega desde un primer plano y se abre, fundida."""
    fx, fy = focus
    e = ease_io(u)
    a = _zoom(A, 1 + 0.12 * e, fx, fy)
    b = _zoom(B, 1.45 - 0.45 * ease_out(u), 540, 820)
    return Image.blend(a, b, e)


def deriva(A, B, u, focus, direction=1):
    """Paneo lento lateral con fundido: la cámara se desliza de una escena a la otra (sin bordes negros)."""
    e = ease_io(u)
    z = 1.14
    fa = 540 + direction * 540 * e
    fb = 540 - direction * 540 * (1 - e)
    a = _zoom(A, 1 + (z - 1) * e, fa, 960)
    b = _zoom(B, z - (z - 1) * e, fb, 960)
    return Image.blend(a, b, e)


KINDS.update({"suave": suave, "suave_out": suave_out, "deriva": deriva, "deriva_r": lambda A, B, u, f: deriva(A, B, u, f, -1)})
