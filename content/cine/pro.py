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


# ------------------------------------------------------------------ «MÁS VISUAL Y MÁS VIRAL» (Iker, 02/11)
# Nada quieto (partículas siempre), estímulo cada <=1,8 s (emoji o destello con «pop»), cámara viva con parallax
# (el fondo se desliza por detrás) y Ojo que reacciona a cada dato clave (salta y se sorprende).
NOW = [0.0]
EV = {}
_EMO = {}
DEF_EMOJI = ["👀", "🤯", "⚡", "💡", "🔥", "😮"]


def _emoji(ch, size=120):
    if ch not in _EMO:
        from PIL import ImageFont
        try:
            fo = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
            im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((80, 80), ch, font=fo, embedded_color=True, anchor="mm")
            im = im.crop(im.getbbox() or (0, 0, 160, 160))
        except Exception:
            im = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        _EMO[ch] = im
    im = _EMO[ch]
    return im.resize((max(1, int(im.width * size / 128)), max(1, int(im.height * size / 128))), Image.BILINEAR)


def events(V, shots, total):
    """Momentos de estímulo: palabras clave («kw») y rellenos («fill») para que no pase más de 1,8 s sin cambio."""
    if "e" in EV:
        return EV["e"]
    end = total - cine.end_hold(V) - 0.4
    kws = [t for t in cine.docu_beats(V)[1] if 0.6 < t < end]
    cuts = [s["start"] for s in shots[1:]]
    ev = [(t, "kw") for t in kws]
    fixed = sorted(set([0.6] + kws + cuts + [end]))
    for a, b in zip(fixed, fixed[1:]):
        n = int((b - a) / 1.8)
        for j in range(1, n + 1):
            ev.append((a + (b - a) * j / (n + 1), "fill"))
    ev.sort()
    by_shot = {}
    for t, k in ev:
        si = next((i for i, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
        by_shot.setdefault(shots[si]["name"], []).append((t, k))
    EV["e"] = (ev, by_shot)
    return EV["e"]


def react(t=None):
    """0..1 durante 0,5 s después de cada palabra clave (para que Ojo reaccione)."""
    t = NOW[0] if t is None else t
    for te, k in EV.get("e", ([], {}))[0]:
        if k == "kw" and 0 <= t - te < 0.5:
            return (t - te) / 0.5
    return None


def ojo(img, x, y, sc, pose="point", ang=0.0, t=0.0):
    bob = 4 * math.sin(t * 3.2)
    u = react()
    hop = 0.0
    if u is not None:
        hop = -46 * sc * math.sin(math.pi * u)
        if u < 0.6 and pose not in ("wave",):
            pose = "surprise"
    K.D(img).ellipse([x - 90 * sc * (1 + hop / 300), y - 14 * sc, x + 90 * sc * (1 + hop / 300), y + 14 * sc], fill=(40, 30, 20, 60))
    solid(img, lambda L: ojo_feet(L, x, y + bob + hop, sc, pose, ang), sh=0.0, light=False)
    if u is not None and u < 0.8:                       # marcas de sorpresa alrededor de la cabeza
        f = OJ.figure(pose, TRAJE[0], 0.0, (0.05, 0.0), 0.0)
        hy = y + bob + hop - f.height * sc * 0.82
        d = K.D(img)
        a = int(255 * (1 - u / 0.8))
        for k_, da in enumerate((-0.9, 0.0, 0.9)):
            r0, r1 = 90 * sc + 20 * u, 140 * sc + 30 * u
            ca, sa = math.sin(da), -math.cos(da)
            d.line([(x + ca * r0, hy + sa * r0), (x + ca * r1, hy + sa * r1)], fill=RED + (a,), width=max(4, int(12 * sc)))


def _particles(img, kind, t):
    if kind == "congreso":
        cols = [(236, 190, 60), (255, 236, 180)]
    else:
        cols = [(255, 214, 140), (255, 240, 210)]
    for i in range(12):                                   # bokeh: motas de luz que flotan (siempre algo moviéndose)
        sp = 18 + (i * 37) % 30
        x = (i * 211 + 90 + 40 * math.sin(t * 0.4 + i)) % (W + 200) - 100
        y = 1440 - ((t * sp + i * 157) % 1100)
        r = 22 + (i * 13) % 40
        glow(img, x, y, r, r, cols[i % 2], 0.22 + 0.12 * math.sin(t * 1.3 + i))
    d = K.D(img)
    if kind == "congreso":                                # papelitos que caen despacio
        for i in range(9):
            y = 380 + ((t * (40 + i * 7) + i * 131) % 1100)
            x = (i * 127 + 60 + 50 * math.sin(t * 0.9 + i * 2)) % W
            a = t * 2.2 + i
            w, h = 22, 12 * abs(math.cos(a)) + 2
            pts = [(x + dx * math.cos(a * 0.6) - dy * math.sin(a * 0.6), y + dx * math.sin(a * 0.6) + dy * math.cos(a * 0.6))
                   for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
            d.polygon(pts, fill=[(230, 40, 40, 150), (255, 255, 255, 200), (236, 190, 60, 170)][i % 3])
    else:                                                 # chispitas que titilan
        for i in range(10):
            x = (i * 173 + 120) % W
            y = 420 + (i * 271) % 980
            a = max(0.0, math.sin(t * 2.4 + i * 1.7))
            if a > 0.3:
                r = 10 * a
                d.line([(x - r, y), (x + r, y)], fill=(255, 255, 255, int(200 * a)), width=3)
                d.line([(x, y - r), (x, y + r)], fill=(255, 255, 255, int(200 * a)), width=3)


def _star(img, x, y, k, col=WARM):
    s = 46 * pop(clamp(k * 2.5)) * (1 - clamp((k - 0.6) / 0.4))
    if s < 1:
        return
    d = K.D(img)
    pts = []
    for j in range(8):
        r = s if j % 2 == 0 else s * 0.3
        a = j * math.pi / 4 + k
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    d.polygon(pts, fill=col + (230,), outline=INK + (200,))


def _stimuli(img, name, g):
    t = NOW[0]
    ev = EV.get("e", ([], {}))[1].get(name, [])
    emo = g.get("EMOJI", {}).get(name) or DEF_EMOJI
    ne = g.get("NO_EMOJI", {"q", "answer"})
    j = 0
    for te, k in ev:
        u = (t - te) / 1.2
        if k == "kw":
            j += 1
        if not 0 <= u < 1:
            continue
        side = 1 if (int(te * 10) % 2) else -1
        if k == "kw" and name not in ne:
            sc = pop(clamp(u * 4)) * (1 - clamp((u - 0.75) / 0.25) * 0.3)
            e = _emoji(emo[(j - 1) % len(emo)], int(150 * sc) + 1)
            e = e.rotate(-12 * side * (1 - u), expand=True, resample=Image.BICUBIC)
            a = 1 - clamp((u - 0.7) / 0.3)
            if a < 1:
                e.putalpha(e.getchannel("A").point(lambda v: int(v * a)))
            x, y = 540 + side * 330, 560 - 70 * ease(u)
            img.paste(e, (int(x - e.width / 2), int(y - e.height / 2)), e)
        else:
            x = 540 + side * (260 + (int(te * 37) % 120))
            y = 620 + (int(te * 53) % 300)
            _star(img, x, y, u * 1.2 / 0.6 if u < 0.5 else 2.0)


def setup(g, traje, fondo_img, names, particles=None):
    """Ajustes del formato pro y envoltorio de fondo (con parallax, partículas y estímulos) para cada plano."""
    TRAJE[0] = traje
    cine.VOICE_LEAD = 0.2
    bg = fondo_dof(fondo_img)
    big = bg.resize((int(W * 1.1), int(H * 1.1)), Image.BILINEAR)
    kind = particles or g.get("PARTICLES", "cocina")

    def con_fondo(fn, name):
        def run(img, t, T, L):
            T_ = NOW[0]
            ox = (big.width - W) / 2 + 42 * math.sin(T_ * 0.23)          # el fondo se desliza despacio: profundidad
            oy = (big.height - H) / 2 + 30 * math.sin(T_ * 0.17 + 1.0)
            img.paste(big.crop((int(ox), int(oy), int(ox) + W, int(oy) + H)), (0, 0))
            _particles(img, kind, T_)
            fn(img, t, T, L)
            _stimuli(img, name, g)
            img.paste(bg.crop((0, 1470, W, H)), (0, 1470))
        return run
    g["FNS"] = {n: con_fondo(g["sh_" + n], n) for n in names}
    g.setdefault("FOCUS_PT", {n: (540, 860) for n in names})
    base_frame = g.get("FRAME") or __import__("vid2").frame

    def frame(V, shots, chunks, total, i):
        NOW[0] = i / cine.FPS
        events(V, shots, total)
        return base_frame(V, shots, chunks, total, i)
    g["FRAME"] = frame
    if not getattr(cine, "_viral_audio", False):              # «pop» suave en cada aparición (sin siseos)
        cine._viral_audio = True
        orig = cine.build_audio

        def build_audio(V, shots, total, *a, **k):
            ev, _ = events(V, shots, total)
            V.AUDIO = dict(V.AUDIO)
            V.AUDIO["sfx"] = list(V.AUDIO.get("sfx", [])) + [(round(t, 3), "pop", 0.045 if k_ == "kw" else 0.025) for t, k_ in ev]
            return orig(V, shots, total, *a, **k)
        cine.build_audio = build_audio
