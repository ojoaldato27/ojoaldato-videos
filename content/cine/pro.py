"""Piezas comunes del FORMATO «pro» (referencia: 09b · Microondas, Iker 30/10: «coge de referencia siempre el vídeo del
microondas»). Cada módulo nuevo hace `import pro`, llama a `pro.setup(globals(), traje, fondo)` al final y usa:
  pro.solid(img, fn)            pieza con sombra suave y luz de arriba (fn dibuja en una capa RGBA)
  pro.glow(img, x, y, rx, ry)   resplandor
  pro.ojo(img, x, y, sc, pose, t=t)   Ojo actuando, con sombra en el suelo
  pro.hook_text(img, [(texto, resaltado)], k)   pregunta/respuesta grande en pantalla
  pro.steam(img, x, y, t)       vapor
"""
import math
import cine
import flat3 as FL
from flat3 import W, H, F, pop
from render import ease, clamp, lerp
import flatkit7 as K
from flatkit7 import INK, RED
import ojo as OJ
from PIL import Image, ImageDraw, ImageFilter, ImageChops

WHITE = (255, 255, 255)
WARM = (255, 196, 92)
BLUE = (70, 130, 220)
TRAJE = ["c_fisico"]


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


_GRAD = {}


def _grad(h):
    h = max(2, int(h))
    if h not in _GRAD:
        col = Image.new("RGB", (1, h))
        al = Image.new("L", (1, h))
        for y in range(h):
            u = y / (h - 1)
            if u < 0.45:
                col.putpixel((0, y), (255, 255, 255))
                al.putpixel((0, y), int(70 * (1 - u / 0.45)))
            else:
                col.putpixel((0, y), (20, 16, 30))
                al.putpixel((0, y), int(60 * (u - 0.45) / 0.55))
        _GRAD[h] = (col, al)
    return _GRAD[h]


def solid(img, fn, sh=0.32, off=(14, 22), blur=22, light=True):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn(lay)
    a = lay.getchannel("A")
    bb = a.getbbox()
    if not bb:
        return
    if sh:
        sm = a.resize((W // 6, H // 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(blur / 6))
        s = sm.resize((W, H), Image.BILINEAR).point(lambda v: int(v * sh))
        shadow = Image.new("RGBA", (W, H), (50, 36, 24, 0))
        shadow.putalpha(s)
        img.paste(shadow, off, shadow)
    if light:
        x0, y0, x1, y1 = bb
        col, al = _grad(y1 - y0)
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gc = col.resize((x1 - x0, y1 - y0))
        gc.putalpha(ImageChops.multiply(al.resize((x1 - x0, y1 - y0)), a.crop(bb)))
        g.paste(gc, (x0, y0))
        lay = Image.alpha_composite(lay, g)
    img.paste(lay, (0, 0), lay)


_GLOW = None


def glow(img, cx, cy, rx, ry, col=WARM, a=1.0):
    global _GLOW
    if a <= 0.01 or rx < 2 or ry < 2:
        return
    if _GLOW is None:
        g = Image.new("L", (128, 128), 0)
        d = ImageDraw.Draw(g)
        for r in range(64, 0, -1):
            d.ellipse([64 - r, 64 - r, 64 + r, 64 + r], fill=int(255 * (1 - r / 64) ** 1.6))
        _GLOW = g
    m = _GLOW.resize((int(rx * 2), int(ry * 2)), Image.BILINEAR).point(lambda v: int(v * clamp(a)))
    c = Image.new("RGBA", m.size, col + (0,))
    c.putalpha(m)
    img.paste(c, (int(cx - rx), int(cy - ry)), c)


def ojo_c(img, cx, cy, sc, pose="point", ang=0.0):
    f = OJ.figure(pose, TRAJE[0], 0.0, (0.05, 0.0), 0.0)
    ff = f.resize((max(1, int(f.width * sc)), max(1, int(f.height * sc))), Image.BILINEAR)
    if abs(ang) > 0.01:
        ff = ff.rotate(math.degrees(ang), expand=True, resample=Image.BICUBIC)
    x, y = int(cx - ff.width / 2), int(cy - ff.height / 2)
    if img.mode == "RGBA":
        img.alpha_composite(ff, (max(0, x), max(0, y)))
    else:
        img.paste(ff, (x, y), ff)


def ojo_feet(img, x, y, sc, pose="point", ang=0.0):
    f = OJ.figure(pose, TRAJE[0], 0.0, (0.05, 0.0), 0.0)
    ojo_c(img, x, y - f.height * sc * 0.45, sc, pose, ang)


def ojo(img, x, y, sc, pose="point", ang=0.0, t=0.0):
    bob = 4 * math.sin(t * 3.2)
    K.D(img).ellipse([x - 90 * sc, y - 14 * sc, x + 90 * sc, y + 14 * sc], fill=(40, 30, 20, 60))
    solid(img, lambda L: ojo_feet(L, x, y + bob, sc, pose, ang), sh=0.0, light=False)


def steam(img, x, y, t, n=3, h=220, a=170):
    d = K.D(img)
    for i in range(n):
        ph = (t * 0.7 + i / n) % 1
        xx = x + (i - (n - 1) / 2) * 50
        y0 = y - h * ph
        pts = [(xx + 18 * math.sin(yy / 28 + t * 4 + i), yy) for yy in range(int(y0 - 120), int(y0), 8)]
        if len(pts) > 1:
            d.line(pts, fill=(255, 255, 255, int(a * math.sin(math.pi * ph))), width=14, joint="curve")


def hook_text(img, lines, k, y=440, size=104):
    if k <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    fo = F(FL.INTER_X, size)
    yy = y
    for s, hl in lines:
        tw = d.textlength(s, font=fo)
        if hl:
            d.rounded_rectangle([540 - tw / 2 - 26, yy - size * 0.62, 540 + tw / 2 + 26, yy + size * 0.62], radius=22, fill=RED + (255,))
            d.text((540, yy), s, font=fo, fill=WHITE, anchor="mm")
        else:
            d.text((540, yy), s, font=fo, fill=INK, anchor="mm", stroke_width=12, stroke_fill=WHITE)
        yy += size * 1.32
    sc = lerp(1.25, 1.0, ease(clamp(k * 3)))
    a = clamp(k)
    if abs(sc - 1) > 0.01:
        lay = lay.resize((int(W * sc), int(H * sc)), Image.BILINEAR)
        lay = lay.crop(((lay.width - W) // 2, int(y * sc - y), (lay.width - W) // 2 + W, int(y * sc - y) + H))
    if a < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.paste(lay, (0, 0), lay)


def chain(img, t, steps, ks, y=840, drawers=None):
    """Respuesta en pasos (regla del 30/10: final claro en 2-3 pasos). steps = [(etiqueta, color)], ks = progreso de
    cada paso (0..1), drawers = funciones fn(capa, cx, cy, s) que dibujan el icono de cada paso."""
    n = len(steps)
    xs = [540 + (i - (n - 1) / 2) * 350 for i in range(n)]
    for i, ((lab, col), k) in enumerate(zip(steps, ks)):
        if k <= 0:
            continue

        def card(Lr, i=i, k=k):
            d = K.D(Lr)
            s = pop(k)
            d.rounded_rectangle([xs[i] - 140 * s, y - 140 * s, xs[i] + 140 * s, y + 140 * s], radius=36, fill=WHITE, outline=INK, width=6)
            if drawers:
                drawers[i](Lr, xs[i], y, s)
        solid(img, card)
        FL.pill(img, xs[i], y + 200, lab, k, col=col)
        if i:
            d = K.D(img)
            xa = (xs[i - 1] + xs[i]) / 2
            d.polygon([(xa - 26, y - 22), (xa + 20, y), (xa - 26, y + 22)], fill=INK + (int(255 * k),))


def fondo_dof(base, tint=(250, 244, 234)):
    """Fondo del tema desenfocado (profundidad de campo) con viñeta y banda clara para subtítulos."""
    top = base.convert("RGB").filter(ImageFilter.GaussianBlur(6))
    img = Image.blend(top, Image.new("RGB", (W, H), tint), 0.18)
    v = Image.new("L", (W, H), 0)
    dv = ImageDraw.Draw(v)
    for i in range(40):
        a = int(60 * (i / 40) ** 2)
        dv.rounded_rectangle([i * 6, i * 9, W - i * 6, H - i * 9], radius=80, outline=60 - a, width=7)
    img = Image.composite(Image.new("RGB", (W, H), (40, 30, 20)), img, v.filter(ImageFilter.GaussianBlur(30)).point(lambda x: int(x * 0.9)))
    ImageDraw.Draw(img, "RGBA").rounded_rectangle([20, 1480, W - 20, 1680], radius=30, fill=(252, 249, 243, 235))
    return img


def setup(g, traje, fondo_img, names):
    """Ajustes del formato pro y envoltorio de fondo para cada plano."""
    TRAJE[0] = traje
    cine.VOICE_LEAD = 0.2
    bg = fondo_dof(fondo_img)

    def con_fondo(fn):
        def run(img, t, T, L):
            img.paste(bg, (0, 0))
            fn(img, t, T, L)
            img.paste(bg.crop((0, 1470, W, H)), (0, 1470))
        return run
    g["FNS"] = {n: con_fondo(g["sh_" + n]) for n in names}
    g.setdefault("FOCUS_PT", {n: (540, 860) for n in names})
