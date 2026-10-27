"""Coches con más nivel para el estilo «pop» (pedido por Iker el 21/10: «mejora mucho las imágenes como la del coche, es muy
sosa, hazlo todo más visible y que enganche… hasta los movimientos del coche más fluidos»).

- roadster(): deportivo rojo de lado con curvas suaves (spline), pintura metalizada en tres tonos, línea de brillo,
  cristales con reflejos, faros y pilotos LED con resplandor, llantas de turbina con pinza de freno, luz de borde de neón
  (cian arriba, magenta detrás) y luz bajo el coche. Mismo lienzo y misma posición de ruedas que el dibujo antiguo
  (1000×330, ruedas en x=208/790, y=262), así que todas las escenas lo usan sin tocarlas.
- sedan(): coche genérico con el mismo acabado, para los coches de fondo.
- smooth_paste(): pega sprites con desenfoque de movimiento cuando se mueven (más fluido a la vista).
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from illus import Cv


def _spline(pts, n=10):
    """Catmull-Rom cerrado → polígono suave."""
    out = []
    m = len(pts)
    for i in range(m):
        p0, p1, p2, p3 = pts[(i - 1) % m], pts[i], pts[(i + 1) % m], pts[(i + 2) % m]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    return out


def _shade(c, k):
    return tuple(int(max(0, min(255, v * k))) for v in c)


def _tint(mask, col, a=1.0):
    lay = Image.new("RGBA", mask.size, col + (0,))
    lay.putalpha(mask.point(lambda v: int(v * a)))
    return lay


def wheel(r, ang=0.0, rim=(214, 218, 228), cal=(230, 30, 50)):
    s = 3
    R = int(r * s)
    im = Image.new("RGBA", (2 * R + 4, 2 * R + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = R + 2
    # neumático con flanco
    for k in range(12):
        rr = R - k * R * 0.012
        v = 14 + k * 3
        d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=(v, v, v + 2, 255))
    d.ellipse([c - R * 0.86, c - R * 0.86, c + R * 0.86, c + R * 0.86], fill=(34, 34, 38, 255))
    # pinza de freno
    d.pieslice([c - R * 0.62, c - R * 0.62, c + R * 0.62, c + R * 0.62], 200, 270, fill=cal + (255,))
    # llanta: aro y radios de turbina
    d.ellipse([c - R * 0.76, c - R * 0.76, c + R * 0.76, c + R * 0.76], outline=_shade(rim, 1.05) + (255,), width=int(R * 0.07))
    for k in range(10):
        a = ang + k * 2 * math.pi / 10
        a2 = a + 0.36
        p = [(c + math.cos(a) * R * 0.18, c + math.sin(a) * R * 0.18), (c + math.cos(a - 0.12) * R * 0.72, c + math.sin(a - 0.12) * R * 0.72),
             (c + math.cos(a2) * R * 0.72, c + math.sin(a2) * R * 0.72), (c + math.cos(a + 0.2) * R * 0.18, c + math.sin(a + 0.2) * R * 0.18)]
        lit = 0.75 + 0.35 * math.cos(a - 2.3)
        d.polygon(p, fill=_shade(rim, lit) + (255,))
    d.ellipse([c - R * 0.2, c - R * 0.2, c + R * 0.2, c + R * 0.2], fill=(52, 54, 62, 255))
    d.ellipse([c - R * 0.1, c - R * 0.1, c + R * 0.1, c + R * 0.1], fill=(150, 156, 168, 255))
    # brillo de la llanta
    hl = Image.new("L", im.size, 0)
    ImageDraw.Draw(hl).ellipse([c - R * 0.7, c - R * 0.72, c + R * 0.1, c - R * 0.05], fill=70)
    im.alpha_composite(_tint(hl.filter(ImageFilter.GaussianBlur(R * 0.12)), (255, 255, 255)))
    return im.resize((2 * r + 2, 2 * r + 2), Image.LANCZOS)


def roadster(body=(206, 24, 36), glass=(22, 26, 38), rim_cols=((0, 232, 255), (255, 46, 120)), glow=True):
    W_, H_ = 1000, 330
    c = Cv(W_, H_)
    base_y = 262
    outline = _spline([(24, 238), (40, 214), (120, 196), (250, 184), (370, 168), (432, 150), (500, 110), (560, 96), (640, 96),
                       (720, 116), (812, 150), (900, 170), (958, 186), (980, 214), (974, 248), (930, 260), (60, 262)], 8)
    hi, mid, lo = _shade(body, 1.35), body, _shade(body, 0.34)
    c.poly(outline, grad=(hi, mid), power=0.75)
    lower = [(p[0], p[1]) for p in outline]
    c.poly(lower, grad=((0, 0, 0, 0), lo + (215,)), power=2.2)
    # vierteaguas y cristales
    glass_pts = _spline([(452, 150), (506, 114), (562, 104), (636, 104), (708, 122), (760, 146), (700, 158), (470, 160)], 6)
    c.poly(glass_pts, grad=(_shade(glass, 2.6), glass), power=0.8)
    c.poly([(540, 108), (590, 106), (520, 156), (478, 156)], fill=(255, 255, 255, 46))
    c.poly([(610, 106), (632, 106), (572, 156), (556, 156)], fill=(255, 255, 255, 30))
    c.line([(588, 104), (582, 160)], _shade(body, 0.55) + (255,), 6)
    # puerta, maneta, toma de aire, retrovisor
    c.line([(470, 166), (462, 246)], (40, 4, 10, 170), 3)
    c.line([(700, 160), (716, 246)], (40, 4, 10, 170), 3)
    c.line([(612, 186), (652, 186)], (255, 255, 255, 120), 4)
    for k_ in range(3):
        c.line([(694 + k_ * 4, 206 + k_ * 9), (738 + k_ * 2, 202 + k_ * 9)], (30, 4, 10, 200), 3)
    c.poly([(436, 150), (462, 144), (470, 158), (444, 162)], grad=(_shade(body, 1.2), _shade(body, 0.6)))
    # faldón
    c.rect((60, 252, 940, 262), grad=((28, 28, 32), (10, 10, 12)), r=4)
    # faros y pilotos
    c.poly([(30, 226), (118, 208), (124, 214), (36, 234)], fill=(255, 250, 240, 255))
    c.poly([(918, 190), (978, 204), (976, 214), (920, 202)], fill=(255, 40, 60, 255))
    # pasos de rueda
    for wx, r in ((208, 60), (790, 62)):
        c.ellipse((wx - r - 8, base_y - r - 10, wx + r + 8, base_y + r + 6), fill=(10, 3, 6))
    im = c.done()
    arch = Image.new("L", (W_, H_), 0)
    for wx, r in ((208, 60), (790, 62)):
        ImageDraw.Draw(arch).ellipse([wx - r - 12, base_y - r - 14, wx + r + 12, base_y + r + 10], fill=255)
    # línea de brillo del lateral (desenfocada) + reflejo del capó
    hl = Image.new("L", (W_, H_), 0)
    hd = ImageDraw.Draw(hl)
    hd.line(_open_spline([(70, 214), (250, 196), (470, 182), (720, 178), (930, 192)]), fill=255, width=5)
    hd.ellipse([150, 186, 420, 204], fill=120)
    hl = ImageChops.multiply(hl.filter(ImageFilter.GaussianBlur(3)), im.getchannel("A"))
    hl = ImageChops.subtract(hl, arch)
    im.alpha_composite(_tint(hl, (255, 255, 255), 0.75))
    if rim_cols:
        a = im.getchannel("A")
        edge = ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(7)))
        ys = np.linspace(1, 0, H_)[:, None] ** 1.2 * np.ones((1, W_))
        top_m = Image.fromarray((ys * 255).astype(np.uint8), "L")
        e1 = ImageChops.multiply(edge, top_m).filter(ImageFilter.GaussianBlur(2))
        im.alpha_composite(_tint(e1, rim_cols[0], 0.95))
        xs = np.linspace(0, 1, W_)[None, :] ** 3 * np.ones((H_, 1))
        e2 = ImageChops.multiply(edge, Image.fromarray((xs * 255).astype(np.uint8), "L")).filter(ImageFilter.GaussianBlur(2))
        im.alpha_composite(_tint(e2, rim_cols[1], 0.8))
    # resplandor de faros y pilotos
    if glow:
        g = Image.new("L", (W_, H_), 0)
        gd = ImageDraw.Draw(g)
        gd.ellipse([0, 200, 150, 250], fill=200)
        g2 = Image.new("L", (W_, H_), 0)
        ImageDraw.Draw(g2).ellipse([900, 180, 1000, 228], fill=200)
        im = _under(im, _tint(g.filter(ImageFilter.GaussianBlur(16)), (255, 245, 220), 0.8))
        im = _under(im, _tint(g2.filter(ImageFilter.GaussianBlur(14)), (255, 30, 60), 0.9))
        # luz de neón bajo el coche
        u = Image.new("L", (W_, H_), 0)
        ImageDraw.Draw(u).ellipse([90, 286, 910, 326], fill=230)
        im = _under(im, _tint(u.filter(ImageFilter.GaussianBlur(14)), rim_cols[0] if rim_cols else (0, 232, 255), 0.85))
    # ruedas
    for wx, r in ((208, 58), (790, 60)):
        wh = wheel(r)
        im.alpha_composite(wh, (int(wx - wh.width / 2), int(base_y - wh.height / 2)))
    # sombra de contacto
    sh = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(sh).ellipse([60, 306, 940, 330], fill=190)
    im = _under(im, _tint(sh.filter(ImageFilter.GaussianBlur(8)), (0, 0, 0), 0.9))
    return im


def _open_spline(pts, n=10):
    sp = _spline(pts + [pts[-1], pts[0]], n)
    return sp[: (len(pts) - 1) * n]


def _under(im, lay):
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(lay)
    out.alpha_composite(im)
    return out


def sedan(w=300, h=110, col=(58, 66, 96)):
    """Coche genérico con volumen (mismo tamaño que car_sil)."""
    c = Cv(w, h)
    k = w / 300
    pts = _spline([(6, h - 26), (24, h - 50), (w * 0.28, h - 62), (w * 0.40, 18), (w * 0.70, 16), (w * 0.84, h - 58), (w - 10, h - 50),
                   (w - 4, h - 28), (w - 20, h - 22), (20, h - 22)], 6)
    c.poly(pts, grad=(_shade(col, 1.45), _shade(col, 0.55)), power=0.9)
    c.poly(_spline([(w * 0.42, 24), (w * 0.69, 22), (w * 0.80, h - 60), (w * 0.33, h - 60)], 5), grad=((120, 140, 175), (24, 28, 40)))
    c.line([(w * 0.56, 22), (w * 0.555, h - 60)], _shade(col, 0.5) + (255,), max(2, int(4 * k)))
    c.line([(14, h - 44), (w - 14, h - 46)], (255, 255, 255, 70), max(2, int(3 * k)))
    c.poly([(8, h - 36), (30, h - 42), (30, h - 34), (8, h - 30)], fill=(255, 245, 220, 230))
    c.poly([(w - 12, h - 44), (w - 4, h - 42), (w - 4, h - 34), (w - 14, h - 36)], fill=(255, 50, 60, 230))
    im = c.done()
    for wx in (w * 0.22, w * 0.78):
        wh = wheel(int(22 * k + 2), rim=(170, 176, 188), cal=(60, 64, 72))
        im.alpha_composite(wh, (int(wx - wh.width / 2), int(h - 24 - wh.height / 2)))
    return im


# ------------------------------------------------------------------ movimiento fluido
_LAST = {}
_CNT = {"gt": None, "n": {}}


def make_smooth_paste(paste, fps_getter, gt_getter):
    """Envuelve paste(dst, im, cx, cy, s, alpha, rot, flip): si un sprite grande se ha movido desde el fotograma anterior,
    lo pinta varias veces a lo largo del recorrido (desenfoque de movimiento). Cada aparición del mismo sprite dentro de un
    fotograma se sigue por separado (p. ej. tres coches iguales en fila)."""
    def sp(dst, im, cx, cy, s=1.0, alpha=1.0, rot=0.0, flip=False):
        gt = gt_getter()
        if _CNT["gt"] != gt:
            _CNT["gt"], _CNT["n"] = gt, {}
        k = _CNT["n"].get(id(im), 0)
        _CNT["n"][id(im)] = k + 1
        key_ = (id(im), k)
        prev = _LAST.get(key_)
        _LAST[key_] = (gt, cx, cy, rot, s)
        big = im.size[0] * s > 160
        if prev and big and abs(gt - prev[0] - 1.0 / fps_getter()) < 1e-3 and alpha > 0.05:
            dx, dy = cx - prev[1], cy - prev[2]
            dist = math.hypot(dx, dy)
            if 3.0 < dist < 400:
                n = int(min(7, 2 + dist / 7))
                for j in range(n):
                    f = (j + 1) / n
                    a_j = alpha if j == n - 1 else alpha * (0.18 + 0.5 * f) / 2.0
                    paste(dst, im, prev[1] + dx * f, prev[2] + dy * f, s, a_j, prev[3] + (rot - prev[3]) * f, flip)
                return
        paste(dst, im, cx, cy, s, alpha, rot, flip)
    return sp
