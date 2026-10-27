"""Motor cinematográfico común de «Ojo al dato» (estilo «Titanic pro»).

Cada vídeo es un módulo con:
  LINES  frases del guion (las *palabras* entre asteriscos salen en amarillo)
  SHOTS  [(nombre, primera_frase, última_frase, pausa)]
  FOCUS  {plano: (x, y[, zoom])} punto al que se acerca el encuadre suave
  FNS    {plano: función(img, t, T, L)} dibuja el plano (img RGB; textos grandes en td())
  AUDIO  dict con música, ambientes, efectos y base rítmica (ver build_audio)
  NOTIF  (plano, segundos) momento del banner «Suscríbete»
"""
import math, random, subprocess, json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as R
from render import W, H, FPS, ease, lerp, clamp
import pro_sprites as S
import music3 as M
from styles import chunks_for, wrap, parse_words
import edit_v2 as V2

GF = "/usr/share/fonts/truetype/"
F_CAP = GF + "google-fonts/Poppins-Bold.ttf"
F_SER = GF + "crosextra/Caladea-Bold.ttf"
F_SERR = GF + "crosextra/Caladea-Regular.ttf"
F_MONO = GF + "dejavu/DejaVuSansMono-Bold.ttf"
_F = {}


def f(path, size):
    k = (path, int(size))
    if k not in _F:
        _F[k] = ImageFont.truetype(path, max(8, int(size)))
    return _F[k]


YEL = (255, 210, 63)
RED = (230, 60, 66)
WHITE = (255, 255, 255)
WPS = 2.75
XF = 0.55
GLIDE = 0.75
ZOOM = 1.28
END_HOLD = 2.8
OUTRO_HOLD = 4.0   # cierre con la mascota (despedida + me gusta + seguir)


def end_hold(V):
    if getattr(V, "OUTRO", None):
        return V.OUTRO
    return OUTRO_HOLD if getattr(V, "NARRATOR", None) else END_HOLD

# ------------------------------------------------------------------ utilidades de dibujo
SPR = {}


def spr(fn, *a, **k):
    key_ = (getattr(fn, "__module__", ""), fn.__name__, a, tuple(sorted(k.items())))
    if key_ not in SPR:
        SPR[key_] = fn(*a, **k)
    return SPR[key_]


def glow(r, col, strength=1.0):
    return spr(S.glow, int(r), tuple(col), strength)


def scaled(im, s):
    if abs(s - 1) < 1e-3:
        return im
    return im.resize((max(1, int(im.size[0] * s)), max(1, int(im.size[1] * s))), Image.BILINEAR)


def AC(dst, src, pos=(0, 0)):
    """Composición con mezcla real sobre lienzo RGB (o RGBA de la capa superior)."""
    if dst.mode == "RGBA" and src.mode == "RGBA":
        dst.alpha_composite(src, (int(pos[0]), int(pos[1]))) if (pos[0] >= 0 and pos[1] >= 0) else dst.paste(src, (int(pos[0]), int(pos[1])), src)
        return
    dst.paste(src, (int(pos[0]), int(pos[1])), src if src.mode == "RGBA" else None)


def with_alpha(im, alpha):
    if alpha >= 0.999:
        return im
    a = im.getchannel("A").point(lambda v: int(v * alpha))
    im = im.copy()
    im.putalpha(a)
    return im


def paste(dst, im, cx, cy, s=1.0, alpha=1.0, rot=0.0, flip=False):
    if alpha <= 0.003:
        return
    im = scaled(im, s)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    im = with_alpha(im, alpha)
    dst.paste(im, (int(cx - im.size[0] / 2), int(cy - im.size[1] / 2)), im)


def paste_top(im, cx, cy, s=1.0, alpha=1.0, rot=0.0):
    """Pega un sprite en la capa fija (no se mueve con el encuadre)."""
    paste(TOP[0], im, cx, cy, s, alpha, rot)


GRADS = {}


def vgrad(key_, top, bot, power=1.0, h=H, w=W):
    k = ("g", key_, top, bot, power, h, w)
    if k not in GRADS:
        GRADS[k] = S.vgrad(w, h, top, bot, power).convert("RGBA")
    return GRADS[k]


def sky(img, top, bot, power=1.3, y=0, h=H):
    AC(img, vgrad("sky", top, bot, power, h), (0, y))


def cached(key_, maker):
    if key_ not in GRADS:
        GRADS[key_] = maker()
    return GRADS[key_]


def layer(key_, fn, ss=2, w=W, h=H):
    """Capa a pantalla completa dibujada con suavizado (fn(d, s) dibuja con coordenadas multiplicadas por s)."""
    def mk():
        im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
        fn(ImageDraw.Draw(im), ss)
        return im.resize((w, h), Image.LANCZOS)
    return cached(("layer", key_), mk)


def sprite(key_, w, h, fn, ss=3):
    """Sprite suavizado: fn(d, s) dibuja en un lienzo w×h con coordenadas multiplicadas por s."""
    return layer(("spr",) + tuple(key_ if isinstance(key_, tuple) else (key_,)), fn, ss, w, h)


def sc(pts, s):
    return [(x * s, y * s) for x, y in pts]


def sb(box, s):
    return [v * s for v in box]


def stars_list(seed, n, ymax):
    return cached(("stars", seed, n, ymax), lambda: [(random.Random(seed * 1000 + i).uniform(0, W),
                                                        random.Random(seed * 1000 + i + 7).uniform(0, ymax),
                                                        random.Random(seed * 1000 + i + 13).uniform(0.8, 2.6),
                                                        random.Random(seed * 1000 + i + 17).uniform(0, 6.28)) for i in range(n)])


def night_sky(img, t, horizon=1050, bright=1.0, top=(4, 8, 22), bot=(22, 36, 72), n=260, seed=11):
    sky(img, top, bot, 1.3)
    stars(img, t, horizon, bright, n, seed)


def stars(img, t, horizon=H, bright=1.0, n=260, seed=11, col=(230, 236, 255)):
    d = ImageDraw.Draw(img, "RGBA")
    for x, y, r, ph in stars_list(seed, n, max(10, horizon)):
        if y < horizon - 10:
            a = int(255 * bright * (0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 2.2 + ph))))
            d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))


def space_bg(img, t, seed=3, nebula=((90, 40, 140), (20, 80, 140)), n=420, drift=(0, 0)):
    sky(img, (2, 3, 10), (8, 10, 26), 1.0)

    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        rr = random.Random(seed)
        for col in nebula:
            for _ in range(7):
                x, y, r = rr.uniform(-100, W + 100), rr.uniform(0, H), rr.uniform(160, 420)
                dd.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=col + (38,))
        return im.filter(ImageFilter.GaussianBlur(90))

    AC(img, cached(("neb", seed, nebula), mk))
    d = ImageDraw.Draw(img, "RGBA")
    for x, y, r, ph in stars_list(seed + 50, n, H):
        x = (x + drift[0] * t * (r / 2.6)) % W
        y = (y + drift[1] * t * (r / 2.6)) % H
        a = int(255 * (0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 1.7 + ph))))
        d.ellipse([x - r * 0.8, y - r * 0.8, x + r * 0.8, y + r * 0.8], fill=(235, 240, 255, a))


def sea(img, t, horizon, top=(18, 30, 60), bot=(3, 6, 16), lines=(48, 70, 110), speed=1.0):
    AC(img, vgrad("sea", top, bot, 1.0, H - horizon), (0, horizon))
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(16):
        y = horizon + 8 + (k ** 1.55) * 9
        if y > H:
            break
        amp = 2 + k * 0.8
        ph = t * speed * (0.6 + k * 0.08) + k
        pts = [(x, y + amp * math.sin(x / (60 + k * 12) + ph)) for x in range(-20, W + 40, 40)]
        d.line(pts, fill=lines + (int(140 - k * 6),), width=max(1, int(1 + k * 0.25)))


def fog(img, t, y, alpha=60, speed=20, col=(200, 210, 230)):
    def mk():
        fg = Image.new("RGBA", (W * 2, 400), (0, 0, 0, 0))
        dd = ImageDraw.Draw(fg)
        rr = random.Random(2)
        for _ in range(26):
            x, yy, r = rr.uniform(0, W * 2), rr.uniform(120, 280), rr.uniform(80, 200)
            dd.ellipse([x - r * 2, yy - r * 0.5, x + r * 2, yy + r * 0.5], fill=col + (70,))
        return fg.filter(ImageFilter.GaussianBlur(40))

    fg = cached(("fog", col), mk)
    off = int((t * speed) % W)
    band = fg.crop((off, 0, off + W, 400))
    band.putalpha(band.getchannel("A").point(lambda v: int(min(255, v * alpha / 70))))
    AC(img, band, (0, int(y - 200)))


def particles(img, t, n=60, seed=4, col=(230, 240, 255), fall=40, size=(1.5, 3.5), alpha=150, sway=20, area=(0, 0, W, H)):
    rr = random.Random(seed)
    d = ImageDraw.Draw(img, "RGBA")
    x0a, y0a, x1a, y1a = area
    for _ in range(n):
        x0, y0 = rr.uniform(x0a, x1a), rr.uniform(y0a, y1a)
        sp = rr.uniform(0.5, 1.5) * fall
        r = rr.uniform(*size)
        x = x0a + (x0 - x0a + math.sin(t * 0.7 + x0) * sway) % (x1a - x0a)
        y = y0a + (y0 - y0a + t * sp) % (y1a - y0a)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (alpha,))


def smoke(img, t, sources, seed=1, col=(150, 150, 160), alpha=80, spread=(220, 140), grow=70, speed=0.35):
    d = ImageDraw.Draw(img, "RGBA")
    for si, (sx, sy, sc) in enumerate(sources):
        for k in range(10):
            ph = (t * speed + k / 10 + si * 0.13) % 1.0
            x = sx - ph * spread[0] * sc
            y = sy - ph * spread[1] * sc - math.sin(ph * 3 + si) * 10
            r = (14 + ph * grow) * sc
            a = int(alpha * (1 - ph))
            d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))


def vignette(img, strength=200):
    def mk():
        yy, xx = np.mgrid[0:H, 0:W]
        dist = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2)
        a = np.clip((dist - 0.55) / 0.6, 0, 1) ** 1.5 * strength
        v = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        v.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
        return v

    AC(img, cached(("vig", strength), mk))


def bottom_shade(img):
    def mk():
        ys = np.arange(H)
        prof = np.clip((ys - 1180) / 520, 0, 1) ** 1.2 * 190
        a = np.repeat(prof[:, None], W, axis=1).astype(np.uint8)
        v = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        v.putalpha(Image.fromarray(a, "L"))
        return v

    AC(img, cached(("bshade",), mk))


def overlay(img, col, a):
    if a > 0.003:
        AC(img, Image.new("RGBA", (W, H), tuple(col) + (int(255 * clamp(a)),)))


def letterbox(img, h=90):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, h], fill=(0, 0, 0))
    d.rectangle([0, H - h, W, H], fill=(0, 0, 0))


def flare(img, cx, cy, k, r=260, col=(255, 230, 170)):
    if k <= 0:
        return
    paste(img, glow(r, col, 0.9), cx, cy, 1.0, k)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(cx - r * 1.6 * k, cy), (cx + r * 1.6 * k, cy)], fill=(255, 240, 200, int(160 * k)), width=3)


def spotlight(img, t, cx=540, top=0, bottom=1300, w0=120, w1=560, alpha=70, col=(255, 236, 200), dust=True):
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.polygon([(cx - w0, top), (cx + w0, top), (cx + w1, bottom), (cx - w1, bottom)], fill=col + (alpha,))
        return im.filter(ImageFilter.GaussianBlur(30))

    AC(img, cached(("spot", cx, top, bottom, w0, w1, alpha, col), mk))
    if dust:
        particles(img, t, 50, 21, (255, 240, 210), 12, (1, 2.5), 120, area=(cx - w1, top, cx + w1, bottom))


def rays(img, t, cx, cy, n=12, col=(255, 230, 170), alpha=40, length=1400, width=0.09, spin=0.04):
    """Rayos de luz que giran despacio desde un punto."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(n):
        a = i / n * 2 * math.pi + t * spin
        p1 = (cx + math.cos(a - width) * length, cy + math.sin(a - width) * length)
        p2 = (cx + math.cos(a + width) * length, cy + math.sin(a + width) * length)
        d.polygon([(cx, cy), p1, p2], fill=col + (alpha,))
    AC(img, im.filter(ImageFilter.GaussianBlur(14)))


def mountains(img, y, amp, col, seed=1, rough=0.5, key_=None, peaks=5):
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        rr = random.Random(seed)
        pts = []
        ph = [rr.uniform(0, 6.28) for _ in range(4)]
        for x in range(-20, W + 30, 15):
            u = x / W
            h = (math.sin(u * peaks * 1.0 + ph[0]) * 0.5 + 0.5) * 0.6 + (math.sin(u * peaks * 2.3 + ph[1]) * 0.5 + 0.5) * 0.3 * rough + \
                (math.sin(u * peaks * 5.1 + ph[2]) * 0.5 + 0.5) * 0.15 * rough
            pts.append((x, y - h * amp))
        d.polygon(pts + [(W + 30, H), (-20, H)], fill=col)
        return im

    AC(img, cached(("mnt", y, amp, col, seed, rough, peaks), mk))


def pine(d, x, y, h, col):
    w = h * 0.36
    for k in range(4):
        yy = y - h * (k * 0.22)
        ww = w * (1 - k * 0.2)
        d.polygon([(x - ww, yy), (x + ww, yy), (x, yy - h * 0.42)], fill=col)
    d.rectangle([x - h * 0.03, y, x + h * 0.03, y + h * 0.08], fill=col)


def forest(img, y, col, n=40, hmin=80, hmax=200, seed=3, fallen=0.0, cx=540, key_=None):
    """Bosque de pinos; fallen>0 los tumba en dirección contraria a cx (onda expansiva)."""
    def mk():
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        rr = random.Random(seed)
        items = sorted([(rr.uniform(-40, W + 40), rr.uniform(0, 60), rr.uniform(hmin, hmax)) for _ in range(n)], key=lambda v: v[1])
        for x, dy, h in items:
            yy = y + dy
            if fallen <= 0:
                pine(d, x, yy, h, col)
            else:
                sgn = 1 if x >= cx else -1
                L = h * 0.95
                ang = math.radians(90 - 82 * fallen) * 1
                ex = x + sgn * L * math.cos(ang)
                ey = yy - L * math.sin(ang)
                tc = tuple(min(255, int(c * 0.5 + 60)) for c in col)
                wdt = max(4, int(h * 0.07))
                d.line([(x, yy), (ex, ey)], fill=tc, width=wdt)
                for k in range(1, 5):
                    u = k / 5
                    bx, by = x + (ex - x) * u, yy + (ey - yy) * u
                    d.line([(bx, by), (bx + sgn * 14 * (1 - u), by - 16 * (1 - u))], fill=tc, width=max(2, wdt // 2))
                d.rectangle([x - wdt * 0.6, yy - wdt * 1.4, x + wdt * 0.6, yy], fill=tc)
        return im

    AC(img, cached(("forest", y, col, n, hmin, hmax, seed, round(fallen, 2), cx), mk))


def ground(img, y, top, bot, h=None):
    AC(img, vgrad("ground", top, bot, 1.0, (h or H - y)), (0, y))


def clouds(img, t, y, col=(255, 255, 255), alpha=120, speed=12, seed=5, scale=1.0):
    def mk():
        im = Image.new("RGBA", (W * 2, 500), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        rr = random.Random(seed)
        for _ in range(14):
            cx_, cy_ = rr.uniform(0, W * 2), rr.uniform(150, 350)
            for k in range(6):
                r = rr.uniform(50, 110) * scale
                dd.ellipse([cx_ + k * 50 * scale - r, cy_ - r * 0.7, cx_ + k * 50 * scale + r, cy_ + r * 0.5], fill=col + (255,))
        return im.filter(ImageFilter.GaussianBlur(10))

    cl = cached(("cloud", col, seed, scale), mk)
    off = int((t * speed) % W)
    band = cl.crop((off, 0, off + W, 500))
    band.putalpha(band.getchannel("A").point(lambda v: int(v * alpha / 255)))
    AC(img, band, (0, int(y - 250)))


def shake(t, t0, amp=18, decay=5):
    if t < t0:
        return 0, 0
    k = math.exp(-(t - t0) * decay) * amp
    return math.sin(t * 61) * k, math.cos(t * 47) * k * 0.6


# ------------------------------------------------------------------ textos de cine (capa fija)
TOP = [None]


def td():
    return ImageDraw.Draw(TOP[0])


FRAME_TEXTS = []


def spaced(d, cx, y, txt, font, fill, track, anchor="c", shadow=True):
    if (len(fill) < 4 or fill[3] > 40) and getattr(font, "size", 0) >= 44:
        FRAME_TEXTS.append(txt)
    w = sum(d.textlength(ch, font=font) + track for ch in txt) - track
    x0 = cx - w / 2 if anchor == "c" else cx
    a = fill[3] if len(fill) > 3 else 255
    if shadow and a > 0:
        off = max(2, int(font.size * 0.05))
        x = x0
        for ch in txt:
            d.text((x + off, y + off), ch, font=font, fill=(0, 0, 0, int(a * 0.55)), stroke_width=max(1, off // 2),
                   stroke_fill=(0, 0, 0, int(a * 0.35)))
            x += d.textlength(ch, font=font) + track
    x = x0
    for ch in txt:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return w


def fade_k(t, t0, hold, fin=0.5, fout=0.5):
    if t < t0:
        return 0.0
    if hold is None:
        return ease(clamp((t - t0) / fin))
    return ease(clamp((t - t0) / fin)) * (1 - ease(clamp((t - t0 - hold) / fout)))


def lower_third(img, t, t0, line1, line2="", y=300, hold=3.2):
    if MUTE_HEADS[0] and y < 520:
        return
    k = fade_k(t, t0, hold)
    if k <= 0:
        return
    d = td()
    A = int(255 * k)
    w = spaced(d, W / 2, y, line1, f(F_SER, 44), (255, 255, 255, A), 7)
    lw_ = w * ease(clamp((t - t0) / 0.7))
    d.line([(W / 2 - lw_ / 2 - 20, y + 66), (W / 2 + lw_ / 2 + 20, y + 66)], fill=YEL + (A,), width=3)
    if line2:
        spaced(d, W / 2, y + 84, line2, f(F_SERR, 34), (220, 224, 235, int(A * 0.9)), 5)


MUTE_HEADS = [False]   # estilo docu sobre escenas antiguas: sus rótulos los sustituye la cabecera nueva


def title2(t, t0, l1, l2, y=300, s1=64, s2=86, hold=None, c1=WHITE, c2=YEL, track=8):
    if MUTE_HEADS[0]:
        return
    k = fade_k(t, t0, hold)
    if k <= 0:
        return
    d = td()
    if l1:
        spaced(d, W / 2, y, l1, f(F_SER, s1), c1 + (int(255 * k),), track)
    if l2:
        spaced(d, W / 2, y + s1 * 1.25, l2, f(F_SER, s2), c2 + (int(255 * k),), track)


def big(t, t0, txt, y=330, size=104, col=WHITE, hold=None, sub=None, subcol=(210, 214, 225), track=6, pop=True):
    if MUTE_HEADS[0] and y < 520:
        return
    k = fade_k(t, t0, hold, 0.35)
    if k <= 0:
        return
    d = td()
    sz = size * (lerp(1.18, 1.0, ease(clamp((t - t0) / 0.35))) if pop else 1.0)
    spaced(d, W / 2, y - (sz - size) * 0.5, txt, f(F_SER, sz), col + (int(255 * k),), track)
    if sub:
        spaced(d, W / 2, y + size * 1.15, sub, f(F_SER, 50), subcol + (int(255 * k),), 10)


def strike(t, t0, cx, y, w, col=RED, width=6):
    c = ease(clamp((t - t0) / 0.6))
    if c <= 0:
        return
    d = td()
    pts = [(cx - w / 2 + i * w / 10, y + (14 if i % 2 else -14)) for i in range(11)]
    n = max(2, int(len(pts) * c))
    d.line(pts[:n], fill=col + (255,), width=width)


def counter(t, t0, t1, v0, v1, fmt="{:,.0f}"):
    q = ease(clamp((t - t0) / max(0.01, t1 - t0)))
    v = v0 + (v1 - v0) * q
    return fmt.format(v).replace(",", ".")


def quote(t, t0, lines, author, y=380, size=66, col=WHITE):
    k = fade_k(t, t0, None, 0.6)
    if k <= 0:
        return
    d = td()
    A = int(255 * k)
    d.text((70, y - 170), "«", font=f(F_SER, 150), fill=YEL + (A,))
    for i, ln in enumerate(lines):
        spaced(d, W / 2 + 30, y + i * size * 1.2, ln, f(F_SER, size), col + (A,), 4)
    if author:
        spaced(d, W / 2 + 30, y + len(lines) * size * 1.2 + 24, author, f(F_SERR, 34), (210, 214, 225, A), 5)


def date_stamp(t, t0, txt, y=300, hold=None):
    if MUTE_HEADS[0]:
        return
    k = fade_k(t, t0, hold)
    if k <= 0:
        return
    d = td()
    spaced(d, W / 2, y, txt, f(F_SER, 52), (255, 255, 255, int(255 * k)), 10)
    w = d.textlength(txt, font=f(F_SER, 52)) + len(txt) * 10
    d.line([(W / 2 - w / 2, y - 18), (W / 2 + w / 2, y - 18)], fill=YEL + (int(255 * k),), width=3)
    d.line([(W / 2 - w / 2, y + 76), (W / 2 + w / 2, y + 76)], fill=YEL + (int(255 * k),), width=3)


# ------------------------------------------------------------------ sprites compartidos
SS = S.SS
P, B, canvas, done = S.P, S.B, S.canvas, S.done


def person(w=200, h=520, col=(14, 16, 24), hat=None, coat=False, dress=False, arm=0.0, step=0.0, hair=False):
    """Silueta humana sencilla. hat: None|'cap'|'top'|'bowler'; arm: ángulo del brazo derecho (rad)."""
    im, d = canvas(w, h)
    cx = w / 2
    sw = math.sin(step) * 22
    # piernas
    d.polygon(P([(cx - 26, 330), (cx + 4, 330), (cx - 6 + sw, h - 6), (cx - 30 + sw, h - 6)]), fill=col)
    d.polygon(P([(cx - 4, 330), (cx + 26, 330), (cx + 30 - sw, h - 6), (cx + 6 - sw, h - 6)]), fill=col)
    if dress:
        d.polygon(P([(cx - 46, 170), (cx + 46, 170), (cx + 80, 420), (cx - 80, 420)]), fill=col)
    body = [cx - 50, 150, cx + 50, 350] if not coat else [cx - 56, 150, cx + 56, 400]
    d.rounded_rectangle(B(body), radius=SS * 24, fill=col)
    d.ellipse(B([cx - 32, 66, cx + 32, 136]), fill=col)
    d.rectangle(B([cx - 14, 128, cx + 14, 156]), fill=col)
    if hair:
        d.ellipse(B([cx - 38, 58, cx + 38, 120]), fill=col)
        d.polygon(P([(cx - 38, 90), (cx + 38, 90), (cx + 44, 200), (cx - 44, 200)]), fill=col)
    if hat == "cap":
        d.rounded_rectangle(B([cx - 40, 56, cx + 40, 82]), radius=SS * 8, fill=col)
        d.rectangle(B([cx - 6, 76, cx + 52, 86]), fill=col)
    elif hat == "top":
        d.rectangle(B([cx - 30, 10, cx + 30, 76]), fill=col)
        d.rectangle(B([cx - 50, 70, cx + 50, 82]), fill=col)
    elif hat == "bowler":
        d.ellipse(B([cx - 34, 40, cx + 34, 96]), fill=col)
        d.rectangle(B([cx - 50, 76, cx + 50, 86]), fill=col)
    # brazos
    d.line(P([(cx - 44, 170), (cx - 62, 320)]), fill=col, width=SS * 20)
    ax, ay = cx + 44, 170
    ex, ey = ax + math.sin(arm) * 150, ay + math.cos(arm) * 150
    d.line(P([(ax, ay), (ex, ey)]), fill=col, width=SS * 20)
    d.ellipse(B([ex - 12, ey - 12, ex + 12, ey + 12]), fill=col)
    return done(im, w, h)


def paper(w=700, h=900, title="", lines=14, col=(242, 236, 222), ink=(40, 36, 30), seed=1, typed=None, stamp=None):
    """Hoja de papel con texto mecanografiado (typed: lista de líneas reales) o líneas simuladas."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 8, w - 1, h - 1], fill=(0, 0, 0, 60))
    d.rectangle([0, 0, w - 9, h - 9], fill=col + (255,))
    rr = random.Random(seed)
    y = 60
    if title:
        fnt = f(F_MONO, 34)
        tw = d.textlength(title, font=fnt)
        d.text(((w - 9 - tw) / 2, y), title, font=fnt, fill=ink)
        y += 80
    if typed:
        fnt = f(F_MONO, 26)
        for ln in typed:
            d.text((56, y), ln, font=fnt, fill=ink)
            y += 40
    else:
        for i in range(lines):
            ln = rr.uniform(0.55, 0.95) * (w - 130)
            if i % 5 == 4:
                ln *= 0.5
            d.rounded_rectangle([56, y + 10, 56 + ln, y + 22], radius=5, fill=ink + (150,))
            y += 44
    if stamp:
        fnt = f(F_SER, 64)
        st = Image.new("RGBA", (w, 200), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        tw = sd.textlength(stamp, font=fnt)
        sd.rounded_rectangle([(w - tw) / 2 - 24, 40, (w + tw) / 2 + 24, 150], radius=12, outline=(200, 40, 40, 220), width=6)
        sd.text(((w - tw) / 2, 52), stamp, font=fnt, fill=(200, 40, 40, 220))
        st = st.rotate(-12, resample=Image.BICUBIC)
        im.alpha_composite(st, (0, h - 300))
    return im


def newspaper(headline, sub="", date="", w=760, h=980, seed=2):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([10, 10, w - 1, h - 1], fill=(0, 0, 0, 70))
    d.rectangle([0, 0, w - 11, h - 11], fill=(236, 230, 214, 255))
    ink = (34, 30, 26)
    fm = f(F_SER, 64)
    name = "LE PETIT JOURNAL" if not date else date
    tw = d.textlength(name, font=f(F_SER, 40))
    d.text(((w - 11 - tw) / 2, 34), name, font=f(F_SER, 40), fill=ink)
    d.line([(40, 96), (w - 51, 96)], fill=ink, width=3)
    d.line([(40, 104), (w - 51, 104)], fill=ink, width=1)
    y = 130
    for ln in headline.split("\n"):
        fs = 76
        while d.textlength(ln, font=f(F_SER, fs)) > w - 110 and fs > 30:
            fs -= 2
        tw = d.textlength(ln, font=f(F_SER, fs))
        d.text(((w - 11 - tw) / 2, y), ln, font=f(F_SER, fs), fill=ink)
        y += fs * 1.12
    if sub:
        tw = d.textlength(sub, font=f(F_SERR, 34))
        d.text(((w - 11 - tw) / 2, y + 10), sub, font=f(F_SERR, 34), fill=ink)
        y += 70
    rr = random.Random(seed)
    y += 20
    d.rectangle([40, y, w / 2 - 20, y + 260], fill=(190, 182, 166))
    for col_x in (w / 2, ):
        yy = y
        for i in range(12):
            d.rounded_rectangle([col_x, yy + 6, col_x + rr.uniform(0.6, 1) * (w / 2 - 60), yy + 14], radius=3, fill=ink + (140,))
            yy += 22
    yy = y + 290
    while yy < h - 60:
        for cx in (40, w / 2):
            d.rounded_rectangle([cx, yy, cx + rr.uniform(0.7, 1) * (w / 2 - 70), yy + 8], radius=3, fill=ink + (120,))
        yy += 22
    return im


def globe_sprite(lon0, lat0, r, extra=(), ocean=(24, 60, 110), land=(70, 120, 90), rim=(120, 180, 240), night=False):
    """Globo en proyección ortográfica con los contornos de geo.py (+ polígonos extra)."""
    import geo
    w = int(r * 2 + 40)
    im, d = canvas(w, w)
    c = w / 2
    d.ellipse(B([c - r, c - r, c + r, c + r]), fill=ocean)
    l0, p0 = math.radians(lon0), math.radians(lat0)

    def v3(lo, la):
        l, p = math.radians(lo), math.radians(la)
        z = math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l - l0)
        x = math.cos(p) * math.sin(l - l0)
        y = math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0)
        return x, y, z

    def clip(poly):
        """Recorta el polígono al hemisferio visible (z >= 0) y sigue el borde del disco entre cortes."""
        vs = []
        for i in range(len(poly) - 1 + 1):
            a, b = poly[i], poly[(i + 1) % len(poly)]
            # subdivide para que los bordes largos sigan la esfera
            for k in range(4):
                u = k / 4
                vs.append(v3(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u))
        out = []
        n = len(vs)
        for i in range(n):
            A, Bv = vs[i], vs[(i + 1) % n]
            ina, inb = A[2] >= 0, Bv[2] >= 0
            if ina:
                out.append((A[0], A[1], False))
            if ina != inb:
                u = A[2] / (A[2] - Bv[2])
                x, y = A[0] + (Bv[0] - A[0]) * u, A[1] + (Bv[1] - A[1]) * u
                nn = math.hypot(x, y) or 1
                out.append((x / nn, y / nn, True))
        # entre una salida y la siguiente entrada, recorre el borde
        res = []
        m = len(out)
        for i in range(m):
            res.append((out[i][0], out[i][1]))
            if out[i][2] and out[(i + 1) % m][2] and i % 1 == 0:
                a1 = math.atan2(out[i][1], out[i][0])
                a2 = math.atan2(out[(i + 1) % m][1], out[(i + 1) % m][0])
                da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
                for k in range(1, 12):
                    aa = a1 + da * k / 12
                    res.append((math.cos(aa), math.sin(aa)))
        return [(c + x * r, c - y * r) for x, y in res]

    for poly in list(geo.LAND) + list(extra):
        pts = clip(poly)
        if len(pts) > 2:
            d.polygon(P(pts), fill=land)
    # sombreado esférico
    out = done(im, w, w)
    yy, xx = np.mgrid[0:w, 0:w]
    dd = np.sqrt((xx - c) ** 2 + (yy - c) ** 2) / r
    shade = np.clip((xx - c * 0.7) / (r * 2.2) + (yy - c * 0.7) / (r * 2.6), 0, 1) * 150 * (dd <= 1)
    sh = Image.new("RGBA", (w, w), (0, 0, 20, 0))
    sh.putalpha(Image.fromarray(shade.astype(np.uint8), "L"))
    out.alpha_composite(sh)
    rimim = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    ImageDraw.Draw(rimim).ellipse([c - r - 6, c - r - 6, c + r + 6, c + r + 6], outline=rim + (120,), width=8)
    out = Image.alpha_composite(rimim.filter(ImageFilter.GaussianBlur(8)), out)
    return out


def proj_point(lon0, lat0, r, lo, la, w=None):
    l0, p0 = math.radians(lon0), math.radians(lat0)
    l, p = math.radians(lo), math.radians(la)
    x = math.cos(p) * math.sin(l - l0)
    y = math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l - l0)
    return x * r, -y * r


# Contornos aproximados extra (lon, lat)
AUSTRALIA = [(113.5, -22.0), (114.2, -26.3), (115.0, -30.0), (115.6, -33.6), (117.9, -35.1), (123.5, -33.9),
             (126.0, -32.3), (131.0, -31.5), (134.2, -32.8), (135.9, -34.9), (137.8, -33.0), (138.2, -35.6),
             (140.5, -38.0), (144.0, -38.4), (146.4, -39.1), (150.0, -37.5), (151.3, -33.8), (153.1, -30.5),
             (153.6, -28.0), (153.0, -25.0), (150.8, -22.6), (149.0, -20.5), (146.3, -18.9), (145.4, -16.4),
             (145.3, -14.9), (143.6, -14.0), (142.5, -10.7), (141.6, -13.0), (141.5, -16.5), (139.5, -17.5),
             (137.7, -16.0), (135.5, -15.0), (136.8, -12.2), (132.5, -11.4), (130.2, -12.5), (129.4, -15.0),
             (127.0, -14.0), (125.0, -15.0), (122.2, -17.2), (121.0, -19.5), (117.0, -20.6)]
SUMATRA = [(95.3, 5.6), (97.5, 5.2), (100.4, 2.2), (103.8, -1.0), (106.0, -3.2), (105.8, -5.8), (104.5, -5.9),
           (102.3, -4.0), (100.3, -1.0), (98.6, 1.7), (95.5, 4.0)]
JAVA = [(105.2, -6.8), (106.1, -5.9), (108.3, -6.3), (111.0, -6.4), (112.6, -6.9), (114.6, -7.7), (114.4, -8.7),
        (110.0, -8.1), (107.5, -7.6), (106.3, -7.4)]
BORNEO = [(109.0, 1.5), (110.5, 1.7), (113.0, 3.2), (115.5, 5.2), (117.0, 7.0), (119.2, 5.3), (118.0, 1.0),
          (116.5, -2.0), (116.0, -3.9), (114.5, -3.4), (111.0, -3.0), (109.9, -1.2)]
NEW_GUINEA = [(131.0, -1.4), (135.0, -3.3), (138.0, -1.8), (141.0, -2.6), (145.8, -4.9), (147.4, -7.6), (150.3, -10.6),
              (146.0, -8.1), (143.3, -9.1), (141.0, -9.1), (138.0, -8.4), (137.6, -5.2), (133.0, -4.0)]
SE_ASIA = [AUSTRALIA, SUMATRA, JAVA, BORNEO, NEW_GUINEA]


# ------------------------------------------------------------------ guion y tiempos
def dur(txt):
    n = len(re.findall(r"\w+", txt.replace("*", "")))
    return max(1.4, n / WPS + 0.35)


def is_docu(V):
    return getattr(V, "STYLE", None) == "docu"


VOICE_LEAD = 0.5


def timeline_docu(V):
    """Estilo docu: si hay locución (V.VOICE), los tiempos de cada línea y palabra salen de la voz."""
    import docu as DC
    lines = list(V.LINES) + ([V.OUTRO_LINE] if getattr(V, "OUTRO_LINE", None) else [])
    vp = getattr(V, "VOICE", None)
    caps, shots = [], []
    if vp and os.path.exists(vp):
        vp, _k = DC.fit_voice(vp)
        V._VOICE_FIT = vp
        key_ = ("align", vp, os.path.getmtime(vp), tuple(lines))
        wj = os.path.splitext(getattr(V, "VOICE"))[0] + "_words.json"
        if key_ not in GRADS:
            if os.path.exists(wj):     # tiempos exactos de la transcripción (escalados si la voz se aceleró)
                GRADS[key_] = DC.align_words(wj, lines, 1.0 / _k)
            else:
                GRADS[key_] = DC.align(vp, lines)
        al = GRADS[key_]
        lead = VOICE_LEAD
        for i, line in enumerate(V.LINES):
            a, b, ws = al[i]
            caps.append({"start": round(a + lead, 3), "end": round(b + lead, 3), "text": line,
                         "words": [(w, hl, w0 + lead, w1 + lead) for w, hl, w0, w1 in ws]})
        if getattr(V, "OUTRO_LINE", None):
            oa, ob, _ = al[-1]
            o0 = oa + lead - 0.3
            V.OUTRO = max(getattr(V, "OUTRO_MIN", 4.0), ob - oa + 1.3)   # OUTRO_MIN: para llegar a 1 min (Iker, 21/10)
        else:
            o0 = caps[-1]["end"] + 0.35
            V.OUTRO = None
    else:
        t = 0.5
        for i, line in enumerate(V.LINES):
            d_ = dur(line)
            caps.append({"start": round(t, 2), "end": round(t + d_, 2), "text": line})
            nxt = next((sh for sh in V.SHOTS if sh[1] == i + 1), None)
            t += d_ + 0.06 + (nxt and 0.18 or 0)
        o0 = caps[-1]["end"] + 0.35
        V.OUTRO = None
    for k, (name, a, b, pad) in enumerate(V.SHOTS):
        st = 0.0 if k == 0 else caps[a]["start"] - 0.22
        shots.append({"name": name, "start": st, "a": a, "b": b})
    for k, s in enumerate(shots):
        s["end"] = shots[k + 1]["start"] if k + 1 < len(shots) else o0 + end_hold(V)
        s["lines"] = [(caps[i]["start"] - s["start"], caps[i]["end"] - s["start"]) for i in range(s["a"], s["b"] + 1)]
    total = o0 + end_hold(V)
    return shots, caps, total


def timeline(V):
    if is_docu(V):
        return timeline_docu(V)
    t = 0.4
    caps, shots = [], []
    for name, a, b, pad in V.SHOTS:
        st = t
        ls = []
        for i in range(a, b + 1):
            d_ = dur(V.LINES[i])
            caps.append({"start": round(t, 2), "end": round(t + d_, 2), "text": V.LINES[i]})
            ls.append((t - st, t - st + d_))
            t += d_ + 0.06
        t += pad * 0.6
        shots.append({"name": name, "start": st, "end": t, "lines": ls})
    shots[0]["start"] = 0.0
    if getattr(V, "NARRATOR", None) or getattr(V, "OUTRO", None):
        # el cierre empieza cuando acaba la última frase, no encima de ella
        t = max(t, caps[-1]["end"] + 0.35 + end_hold(V))
        shots[-1]["end"] = t
    return shots, caps, t


def cut_points(s):
    pts = []
    for a, b in s["lines"]:
        pts.append(a)
        if b - a > 3.4:
            pts.append((a + b) / 2)
    return sorted(pts)


def zoom_at(V, s, tl):
    if s["name"] not in V.FOCUS:
        return 0.0
    cps = cut_points(s)
    k = sum(1 for c in cps if c <= tl) - 1
    if k < 0:
        return 0.0
    tgt = lambda i: float(max(0, i) % 2)
    cur, prev = tgt(k), (tgt(k - 1) if k > 0 else 0.0)
    p = clamp((tl - cps[k]) / GLIDE)
    p = p * p * (3 - 2 * p)
    return lerp(prev, cur, p)


def reframe(V, img, s, tl):
    q = zoom_at(V, s, tl)
    if q < 0.002:
        return img
    fv = V.FOCUS[s["name"]]
    fx, fy = fv[0], fv[1]
    zmax = fv[2] if len(fv) > 2 else ZOOM
    z = lerp(1.0, zmax, q)
    cx, cy = lerp(W / 2, fx, q), lerp(H / 2, fy, q)
    cw, ch = W / z, H / z
    x0 = min(max(0, cx - cw / 2), W - cw)
    y0 = min(max(0, cy - ch / 2), H - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)


# ------------------------------------------------------------------ subtítulos
def caption(img, chunk, t_in, dur=1.0):
    """Subtítulos que aparecen palabra a palabra, cada una con un pequeño rebote (las destacadas, más)."""
    d = ImageDraw.Draw(img)
    size = 80
    fnt = f(F_CAP, size)
    lines = wrap(d, chunk, fnt, 920)
    lh = int(size * 1.2)
    words = [w for ln in lines for w in ln]
    lens = [len(w[0]) + 2 for w in words]
    tot = max(1, sum(lens))
    span = max(0.25, min(dur * 0.85, dur - 0.12))
    starts, acc = [], 0
    for L_ in lens:
        starts.append(span * acc / tot)
        acc += L_
    y = 1520 - len(lines) * lh / 2
    k = 0
    for ln in lines:
        widths = [d.textlength(w, font=fnt) for w, _ in ln]
        sp = d.textlength(" ", font=fnt)
        x = (W - (sum(widths) + sp * (len(ln) - 1))) / 2
        for (wd, hl), wdt in zip(ln, widths):
            u = t_in - starts[k]
            k += 1
            if u >= 0:
                p = ease(clamp(u / 0.15))
                sc = 1 + (0.38 if hl else 0.22) * (1 - p)
                cx, cy = x + wdt / 2, y + size * 0.62 + (1 - p) * 10
                ff = f(F_CAP, int(size * sc))
                col = YEL if hl else (255, 255, 255)
                d.text((cx + 3, cy + 5), wd, font=ff, fill=(0, 0, 0), anchor="mm")
                d.text((cx, cy), wd, font=ff, fill=col, anchor="mm", stroke_width=6, stroke_fill=(10, 10, 14))
            x += wdt + sp
        y += lh


# ------------------------------------------------------------------ solo palabras clave (la voz narra el resto)
KW_STOP = {"porque", "cuando", "aunque", "entonces", "despues", "después", "mientras", "también", "tambien", "siempre", "nunca",
           "exactamente", "realidad", "alrededor", "imagina", "esas", "esos", "estas", "estos", "puede", "pueden", "tiene",
           "tienen", "hasta", "sobre", "dentro", "fuera", "muchos", "muchas", "poquito", "solo", "todas", "todos", "otra"}
KW_SLOTS = [(330, 560, 0, "pop"), (760, 1460, 0, "pop"), (540, 1250, 0, "pop"), (750, 640, 0, "pop"),
            (320, 1600, 0, "pop"), (540, 1700, 0, "pop"), (310, 1300, 0, "pop"), (770, 1150, 0, "pop"),
            (300, 1460, 0, "pop"), (780, 1620, 0, "pop"), (540, 1540, 0, "pop"), (720, 1340, 0, "pop")]


def _kw_from_line(text):
    words = parse_words(text)
    phrases, cur, st = [], [], 0
    for i, (w, hl) in enumerate(words):
        if hl:
            if not cur:
                st = i
            cur.append(w)
        elif cur:
            phrases.append((" ".join(cur), st))
            cur = []
    if cur:
        phrases.append((" ".join(cur), st))
    if phrases:
        return phrases, len(words)
    best = None
    for i, (w, hl) in enumerate(words):
        nw = _norm(w)
        if _emoji_for(w) and len(nw) >= 4:
            best = (w, i)
            break
    if not best:
        cands = [(len(_norm(w)), i, w) for i, (w, _) in enumerate(words) if len(_norm(w)) >= 8 and w.lower().strip("¿¡.,…:;!?") not in KW_STOP]
        if cands:
            _, i, w = max(cands)
            best = (w, i)
    return ([best] if best else []), len(words)


def keyword_plan(V, shots, caps, total):
    if getattr(V, "_kw", None) is not None:
        return V._kw
    saved_top, saved_texts = TOP[0], list(FRAME_TEXTS)
    try:
        return _keyword_plan(V, shots, caps, total)
    finally:
        TOP[0] = saved_top
        FRAME_TEXTS[:] = saved_texts


def _keyword_plan(V, shots, caps, total):
    hy = getattr(V, "HYPE", None)
    hy_line = hy["line"] if hy else -1
    import inspect, ast, textwrap
    lits = {}
    for x in shots:
        try:
            tree = ast.parse(textwrap.dedent(inspect.getsource(V.FNS[x["name"]])))
            strs = [n_.value for n_ in ast.walk(tree) if isinstance(n_, ast.Constant) and isinstance(n_.value, str)]
        except Exception:
            strs = []
        lits[x["name"]] = [m_ for m_ in strs if len(m_) >= 2 and m_.upper() == m_ and any(ch.isalpha() or ch.isdigit() for ch in m_)]

    def dup_static(txt, sh):
        # contra los textos escritos en el código del plano: comparación literal (como en la versión aprobada)
        kw = _kw_words_basic(txt)
        return any(len(kw & _kw_words_basic(h)) / len(kw) > 0.5 for h in lits.get(sh, []))

    over = getattr(V, "KW_OVERRIDE", {})
    plan, k, zc = [], 0, {}
    for li, c in enumerate(caps):
        if li == hy_line or c["start"] > total - end_hold(V) - 0.6:
            continue
        phrases, n = _kw_from_line(c["text"])
        if li in over:
            phrases = [(o, phrases[i][1] if i < len(phrases) else 0) for i, o in enumerate(over[li])]
        dur_ = c["end"] - c["start"]
        for ph, wi in phrases:
            txt = ph.replace("*", "").strip(" ,.;:…!?¿¡«»")
            if not txt:
                continue
            t0 = c["start"] + dur_ * 0.9 * wi / max(1, n)
            t1 = max(t0 + 1.4, c["end"] + 0.25)
            sh = next((x["name"] for x in shots if x["start"] <= t0 + 0.05 < x["end"]), None)
            if getattr(V, "KW_STATIC", not getattr(V, "KW_PROBE", True)) and dup_static(txt.upper(), sh):
                continue
            zones = getattr(V, "KW_ZONES", {}).get(sh) or getattr(V, "KW_DEFAULT", [1, 8, 10, 9, 4, 5, 11])
            if zones:
                cnt = k
                slot = KW_SLOTS[zones[cnt % len(zones)]]
                if plan and slot == plan[-1]["slot"] and len(zones) > 1:
                    cnt += 1
                    slot = KW_SLOTS[zones[cnt % len(zones)]]
                zc[sh] = cnt + 1
            else:
                slot = KW_SLOTS[k % len(KW_SLOTS)]
            if getattr(V, "KW_PROBE", True):
                ims, dup_rt = [], False
                for tt in (t0 + 0.3, t0 + 0.9, min(t1, t0 + 1.7) - 0.1):
                    im_, texts_ = _kw_probe(V, shots, tt)
                    if _kw_on_screen(txt.upper(), texts_):
                        dup_rt = True
                        break
                    ims.append(im_)
                if dup_rt:
                    continue
                prev = plan[-1]["slot"] if plan else None
                cands = [slot]
                for z in list(zones or []) + KW_LOW:
                    if KW_SLOTS[z] not in cands and KW_SLOTS[z] != prev:
                        cands.append(KW_SLOTS[z])
                narr = None
                if getattr(V, "NARRATOR", None):
                    import narrator as NR
                    narr = NR.box(V, sh)
                best = None
                for s_ in cands:
                    s2, scl = _kw_fit(txt.upper(), k % 3, s_, narr)
                    sc_ = max(_kw_busy(im_, txt.upper(), k % 3, s2, scl) for im_ in ims)
                    if sc_ < 0.05:
                        best = (sc_, s2, scl)
                        break
                    if best is None or sc_ < best[0] - 0.01:
                        best = (sc_, s2, scl)
                slot = best[1]
                busy = best[0]
                kscl = best[2]
            else:
                busy, kscl = 0, 1.0
            plan.append({"t0": t0, "t1": t1, "txt": txt.upper(), "slot": slot, "style": 1 if busy > 0.1 else k % 3, "sc": kscl})
            k += 1
    for i in range(len(plan) - 1):
        if plan[i + 1]["t0"] < plan[i]["t1"] + 0.2:
            plan[i]["t1"] = max(plan[i]["t0"] + 0.6, plan[i + 1]["t0"] - 0.2)
    if hy:
        h0 = shots[0]["start"] + shots[0]["lines"][hy_line][0]
        for it in plan:
            if it["t0"] < h0 < it["t1"] + 0.25:
                it["t1"] = max(it["t0"] + 0.5, h0 - 0.3)
    V._kw = plan
    return plan


def _kw_img(txt, style):
    def mk():
        tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        size = 124
        lines = [txt]
        while tmp.textlength(txt, font=f(F_CAP, size)) > 880 and size > 84:
            size -= 4
        if tmp.textlength(txt, font=f(F_CAP, size)) > 880:
            ws = txt.split(" ")
            best = None
            for j in range(1, len(ws)):
                a_, b_ = " ".join(ws[:j]), " ".join(ws[j:])
                m = max(tmp.textlength(a_, font=f(F_CAP, size)), tmp.textlength(b_, font=f(F_CAP, size)))
                if best is None or m < best[0]:
                    best = (m, [a_, b_])
            lines = best[1]
            while max(tmp.textlength(x, font=f(F_CAP, size)) for x in lines) > 880 and size > 60:
                size -= 4
        fnt = f(F_CAP, size)
        lh = int(size * 1.08)
        tw = int(max(tmp.textlength(x, font=fnt) for x in lines)) + 90
        th = lh * len(lines) + 70
        im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if style == 1:
            d.rounded_rectangle([18, 22, tw - 18, th - 18], radius=26, fill=(0, 0, 0, 110))
            d.rounded_rectangle([10, 10, tw - 26, th - 30], radius=26, fill=YEL + (255,))
        for j, ln in enumerate(lines):
            y = 35 + j * lh + lh / 2 - (8 if style == 1 else 0)
            if style == 1:
                d.text((tw / 2 - 8, y), ln, font=fnt, fill=(16, 16, 20), anchor="mm")
            else:
                col = YEL if style == 0 else (255, 255, 255)
                d.text((tw / 2 + 5, y + 8), ln, font=fnt, fill=(0, 0, 0, 170), anchor="mm")
                d.text((tw / 2, y), ln, font=fnt, fill=col + (255,), anchor="mm", stroke_width=max(6, size // 14), stroke_fill=(10, 10, 14))
        return im
    return cached(("kw", txt, style), mk)


KW_WEAK = {"unos", "unas", "casi", "del", "los", "las", "que", "con", "por", "para", "mas", "muy", "una", "uno"}
KW_SYN = {"cm": "centimetros", "centimetro": "centimetros", "mm": "milimetros", "milimetro": "milimetros",
          "km": "kilometros", "kilometro": "kilometros", "m": "metros", "metro": "metros", "segundo": "segundos",
          "minuto": "minutos", "hora": "horas", "grado": "grados"}


def _kw_words_basic(txt):
    ws = {w for w in (_norm(x) for x in txt.split()) if len(w) >= 3 and w not in KW_WEAK}
    return ws or {_norm(txt)}


KW_NUM = {"dos": "2", "tres": "3", "cuatro": "4", "cinco": "5", "seis": "6", "siete": "7", "ocho": "8", "nueve": "9",
          "diez": "10", "once": "11", "doce": "12", "veinte": "20", "treinta": "30", "cien": "100", "mil": "1000"}


def _kw_words(txt):
    ws = set()
    for x in re.split(r"[\s\-–—/·,]+", txt):
        w = _norm(x)
        w = KW_NUM.get(w, KW_SYN.get(w, w))
        if len(w) > 4 and w.endswith("s"):
            w = w[:-1]
        if len(w) >= 6 and not w.isdigit():
            w = w[:5]
        if w.isdigit() or (len(w) >= 3 and w not in KW_WEAK):
            ws.add(w)
    return ws or {_norm(txt)}


KW_LOW = [1, 8, 10, 9, 4, 5, 11, 2, 6, 7]


def _kw_probe(V, shots, t):
    """Dibuja el plano (sin palabras clave) en el instante t: devuelve la imagen y los rótulos que salen."""
    si = next((k for k, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
    FRAME_TEXTS.clear()
    img, top = draw_shot(V, shots[si], t)
    im = img.copy()
    im.paste(top, (0, 0), top)
    if getattr(V, "NARRATOR", None):
        import narrator as NR
        im = im.convert("RGB")
        NR.draw(im, V, t, shots, CAPS_[0], shots[-1]["end"])
    return im, list(FRAME_TEXTS)


def _kw_fit(txt, style, slot, narr):
    """Si la palabra clave pisaría al narrador, se aparta a su derecha y, si no cabe, se encoge (hasta un 60 %)."""
    kim = _kw_img(txt, style)
    w, h = kim.size
    x, y = slot[:2]
    hw = w / 2 + 10
    x = min(max(x, 24 + hw), W - 24 - hw) if hw * 2 < W - 48 else W / 2
    if not narr:
        return slot, 1.0
    if x + w / 2 < narr[0] or x - w / 2 > narr[2] or y + h / 2 < narr[1] or y - h / 2 > narr[3]:
        return (x, y, 0, "pop"), 1.0
    if narr[0] <= 10:
        left = narr[2] + 16
        scl = max(0.6, min(1.0, (W - 24 - left) / w))
        return (left + w * scl / 2, y, 0, "pop"), scl
    right = narr[0] - 16
    scl = max(0.6, min(1.0, (right - 24) / w))
    return (right - w * scl / 2, y, 0, "pop"), scl


def _kw_busy(im, txt, style, slot, scl=1.0):
    """Cuánto detalle (rótulos, líneas, dibujo) hay debajo de la palabra clave en ese hueco: 0 = fondo liso."""
    kim = _kw_img(txt, style)
    x, y = slot[:2]
    kw_, kh_ = kim.size[0] * scl, kim.size[1] * scl
    hw = kw_ / 2 + 10
    x = min(max(x, 24 + hw), W - 24 - hw) if hw * 2 < W - 48 else W / 2
    box = (int(x - kw_ / 2 + 30 * scl), int(y - kh_ / 2 + 25 * scl), int(x + kw_ / 2 - 30 * scl), int(y + kh_ / 2 - 25 * scl))
    e = im.crop(box).convert("L").filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(9))
    sm = e.resize((max(1, e.size[0] // 24), max(1, e.size[1] // 24)), Image.BOX)
    px = np.asarray(sm)
    return float((px > 40).mean())


def _kw_overlap(txt, heads):
    kw = _kw_words(txt)
    for h in heads:
        hw = _kw_words(h)
        if len(kw & hw) / len(kw) > 0.5:
            return True
    return False


def _kw_on_screen(txt, heads):
    """Repetida si más de la mitad de sus palabras ya están en un rótulo grande, o entre todos los que hay en pantalla."""
    if _kw_overlap(txt, heads):
        return True
    kw = _kw_words(txt)
    allw = set()
    for h in heads:
        allw |= _kw_words(h)
    return len(kw) > 1 and len(kw & allw) / len(kw) > 0.5


def _kw_dup(txt):
    return _kw_on_screen(txt, FRAME_TEXTS)


def draw_keywords(img, t, plan):
    for it in plan:
        u = t - it["t0"]
        if u < 0 or t > it["t1"] + 0.22:
            continue
        if "dup" not in it or u < 0.04:
            it["dup"] = _kw_dup(it["txt"])
        if it["dup"]:
            continue
        x, y, rot, mode = it["slot"]
        kim = _kw_img(it["txt"], it["style"])
        sc0 = it.get("sc", 1.0)
        hw = kim.size[0] * sc0 / 2 + 10
        x = min(max(x, 24 + hw), W - 24 - hw) if hw * 2 < W - 48 else W / 2
        p = clamp(u / 0.14)
        out = clamp((t - it["t1"]) / 0.18)
        al = clamp(u / 0.08) * (1 - out)
        sc = 1 + 0.12 * (1 - ease(p))
        dx = dy = 0.0
        r = 0
        paste(img, kim, x + dx, y + dy, sc * sc0, al, r)


# ------------------------------------------------------------------ pegatinas emoji según lo que se dice
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
EMOJI_STEMS = [
    ("calor", "🔥"), ("calien", "🔥"), ("quema", "🔥"), ("fuego", "🔥"), ("hielo", "🧊"), ("frio", "❄️"), ("enfri", "❄️"),
    ("congel", "❄️"), ("nevera", "❄️"), ("sudor", "💧"), ("agua", "💧"), ("vapor", "💨"), ("=aire", "💨"), ("=gas", "💨"),
    ("bateria", "🔋"), ("electr", "⚡"), ("corriente", "⚡"), ("voltio", "⚡"), ("pulso", "⚡"), ("condensador", "⚡"),
    ("detonador", "💥"), ("senal", "📡"), ("ondas", "📡"), ("wifi", "📶"), ("radio", "📶"), ("milisegund", "⏱️"),
    ("microsegund", "⏱️"), ("milmillon", "⏱️"), ("segundo", "⏱️"), ("minutos", "⏱️"), ("reloj", "⏰"), ("levantes", "⏰"),
    ("euro", "💸"), ("multa", "💸"), ("cobrar", "💸"), ("patente", "📜"), ("autopista", "🛣️"),
    ("autovia", "🛣️"), ("frenada", "🛑"), ("movil", "📱"), ("pantalla", "📱"), ("mapa", "🗺️"), ("choque", "💥"),
    ("chocar", "💥"), ("chocando", "💥"), ("golpe", "💥"), ("revienta", "💥"), ("explosion", "💥"), ("bomba", "💣"),
    ("accidente", "😱"), ("degrada", "⚠️"), ("hinch", "⚠️"), ("dano", "⚠️"), ("parpadeo", "👁️"), ("=luz", "💡"),
    ("iman", "🧲"), ("magnet", "🧲"), ("satelite", "🛰️"), ("einstein", "🤯"), ("relatividad", "🤯"), ("gravedad", "🌍"),
    ("dedo", "👆"), ("tocas", "👆"), ("guante", "🧤"), ("salchicha", "🌭"), ("palomita", "🍿"), ("maiz", "🌽"),
    ("comida", "🍲"), ("chocolat", "🍫"), ("=qr", "🔳"), ("cuadradito", "🔳"), ("bits", "💻"), ("ordenador", "💻"),
    ("letras", "🔤"), ("japon", "🗾"), ("fichas", "⚫"), ("nitrogeno", "🧪"), ("azida", "🧪"), ("quimica", "🧪"),
    ("aceleracion", "🚀"), ("salta", "🚀"), ("cohete", "🚀"), ("velocidad", "💨"), ("rapidisimo", "⚡"), ("tortuga", "🐢"),
    ("lento", "🐢"), ("noche", "🌙"), ("cuidandose", "💚"), ("salvar", "❤️"), ("remolino", "🌀"), ("bobina", "🌀"),
    ("olla", "🍳"), ("sarten", "🍳"), ("cocina", "🍳"), ("compresor", "🔊"), ("zumbido", "🔊"), ("ruido", "🔊"),
    ("cientific", "🔬"), ("imagenes", "🎥"), ("invento", "💡"), ("molecula", "⚛️"), ("airbag", "🎈"), ("presion", "🎈"),
    ("espuma", "☁️"), ("almidon", "☁️"), ("cinturon", "🔒"), ("energia", "⚡"), ("consumo", "⛽"),
    ("ganas", "🤔"), ("merece", "🤔"), ("guarda", "📦"),
]


def _norm(w):
    import unicodedata
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)


def _emoji_for(word, extra=()):
    nw = _norm(word)
    if not nw:
        return None
    for stem, e in list(extra) + EMOJI_STEMS:
        if stem.startswith("="):
            if nw == stem[1:]:
                return e
        elif nw.startswith(stem):
            return e
    return None


STK_SLOTS = [(260, 760), (820, 720), (250, 1040), (830, 1000)]


def _stk_busy(im, sl):
    x, y = sl
    e = im.crop((x - 75, y - 75, x + 75, y + 75)).convert("L").filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(9))
    sm = e.resize((6, 6), Image.BOX)
    return float((np.asarray(sm) > 40).mean())


def sticker_plan(V, shots, chunks, total):
    if getattr(V, "_stk", None) is not None:
        return V._stk
    saved_top, saved_texts = TOP[0], list(FRAME_TEXTS)
    try:
        return _sticker_plan(V, shots, chunks, total)
    finally:
        TOP[0] = saved_top
        FRAME_TEXTS[:] = saved_texts


def _sticker_plan(V, shots, chunks, total):
    plan, last, used, slot = [], -9, {}, 0
    hy = getattr(V, "HYPE", None)
    hw = None
    if hy:
        a_, b_ = shots[0]["lines"][hy["line"]]
        hw = (shots[0]["start"] + a_ - 0.2, shots[0]["start"] + b_ + 0.6)
    extra = getattr(V, "STICKER_EXTRA", ())
    for cs, ce, g in chunks:
        words = V2.glue(g)
        lens = [len(w[0]) + 2 for w in words]
        tot = max(1, sum(lens))
        span = max(0.25, min((ce - cs) * 0.85, ce - cs - 0.12))
        acc = 0
        for (w, hl), L_ in zip(words, lens):
            tw = cs + span * acc / tot
            acc += L_
            e = _emoji_for(w, extra)
            if not e or tw - last < 1.4 or tw > total - end_hold(V) - 0.8 or tw < 0.8:
                continue
            if hw and hw[0] - 1.5 <= tw <= hw[1]:
                continue
            if used.get(e, -9) > tw - 4:
                continue
            choice = STK_SLOTS[slot % len(STK_SLOTS)]
            prev = plan[-1][2] if plan and tw - plan[-1][0] < 2.0 else None
            cands = [sl for sl in [choice] + STK_SLOTS if sl != prev]
            cands = list(dict.fromkeys(cands))
            if CAPS_[0] is not None:
                act = [it for it in keyword_plan(V, shots, CAPS_[0], total) if it["t0"] - 0.3 <= tw <= it["t1"] + 0.3]
                if act:
                    kx, ky = act[-1]["slot"][:2]
                    cands = sorted([sl for sl in STK_SLOTS if sl != prev] or STK_SLOTS,
                                   key=lambda sl: -((sl[0] - kx) ** 2 + (sl[1] - ky) ** 2))[:3]
                    choice = cands[0]
            if getattr(V, "KW_PROBE", True):
                im_, _ = _kw_probe(V, shots, tw + 0.8)
                rest = [sl for sl in STK_SLOTS if sl not in cands and sl != prev]
                scs = [(_stk_busy(im_, sl), j, sl) for j, sl in enumerate(cands + rest)]
                ok = [x for x in scs if x[0] < 0.12]
                choice = (ok[0] if ok else min(scs))[2]
            plan.append((tw, e, choice))
            slot += 1
            last = tw
            used[e] = tw
    V._stk = plan
    return plan


def _emoji_img(e):
    def mk():
        im = Image.new("RGBA", (190, 170), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), e, font=ImageFont.truetype(EMOJI_FONT, 109), embedded_color=True)
        bb = im.getbbox() or (0, 0, 10, 10)
        em = im.crop(bb)
        pad = 40
        out = Image.new("RGBA", (em.size[0] + 2 * pad, em.size[1] + 2 * pad), (0, 0, 0, 0))
        sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
        a = em.getchannel("A").point(lambda v: int(v * 0.55))
        sh.paste(Image.new("RGBA", em.size, (0, 0, 0, 255)), (pad + 6, pad + 10), a)
        out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        out.alpha_composite(em, (pad, pad))
        return out.resize((int(out.size[0] * 1.45), int(out.size[1] * 1.45)), Image.LANCZOS)
    return cached(("emoji", e), mk)


def draw_stickers(img, t, plan):
    for ts_, e, (sx, sy) in plan:
        u = t - ts_
        if u < 0 or u > 1.8:
            continue
        p = clamp(u / 0.32)
        c1 = 1.9
        s_ = 1 + (c1 + 1) * (p - 1) ** 3 + c1 * (p - 1) ** 2 if p > 0 else 0
        al = 1 - clamp((u - 1.45) / 0.3)
        rot = math.sin(u * 7) * 4 * (1 - p)
        y = sy - u * 8
        paste(img, glow(150, (255, 255, 255), 0.5), sx, y, 1.0, 0.35 * al * clamp(u / 0.2))
        if s_ > 0.02:
            paste(img, _emoji_img(e), sx, y, max(0.05, s_), al, rot)
        if u < 0.55:
            d = ImageDraw.Draw(img, "RGBA")
            q = ease(u / 0.55)
            for k in range(8):
                a = k / 8 * 2 * math.pi + 0.3
                r = 60 + 110 * q
                x2, y2 = sx + math.cos(a) * r, y + math.sin(a) * r
                st = 12 * (1 - q) + 3
                col = YEL if k % 2 else (255, 255, 255)
                d.polygon([(x2, y2 - st), (x2 + st * 0.35, y2), (x2, y2 + st), (x2 - st * 0.35, y2)], fill=col + (int(230 * (1 - q)),))
                d.polygon([(x2 - st, y2), (x2, y2 + st * 0.35), (x2 + st, y2), (x2, y2 - st * 0.35)], fill=col + (int(230 * (1 - q)),))


def end_card(t_end_in):
    k = ease(clamp(t_end_in / 0.8))
    d2 = td()
    d2.rectangle([0, 0, W, H], fill=(0, 0, 0, int(205 * k)))
    R.eye_icon(d2, 540, 800, 300 * (0.9 + 0.1 * k), (255, 255, 255), YEL, (14, 15, 18))
    spaced(d2, W / 2, 990, "SI AÚN NO LO SABÍAS…", f(F_SER, 52), (255, 255, 255, int(255 * k)), 6)
    spaced(d2, W / 2, 1070, "@ojoaldato.ya", f(F_SERR, 40), (220, 220, 230, int(255 * k)), 3)
    k2 = ease(clamp((t_end_in - 0.6) / 0.6))
    spaced(d2, W / 2, 1180, "MÁNDASELO A QUIEN NO LO SEPA", f(F_SER, 34), YEL + (int(255 * k2),), 5)


# ------------------------------------------------------------------ audio
A_MIN = M.A_MIN
C_MAJ = [[261.63, 329.63, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66]]
NOIR = [[146.83, 174.61, 220.0, 261.63], [196.0, 246.94, 293.66, 349.23], [130.81, 164.81, 196.0, 246.94],
        [220.0, 277.18, 329.63, 392.0]]


def loop_chords(dur_, bar, fn, gain, chords):
    buf = np.zeros(int((dur_ + 4) * M.SR))
    t0, k = 0.0, 0
    while t0 < dur_:
        for fq in chords[k % len(chords)]:
            M.add(buf, fn(fq, bar + 0.8), t0, gain)
        t0 += bar
        k += 1
    return buf


def music_bed(style, dur_, rng):
    n = int((dur_ + 2) * M.SR)
    if style == "pop":
        import pop as POP
        m = POP.music(dur_, rng)
        return m[:n] if len(m) >= n else np.pad(m, (0, n - len(m)))
    if style in ("doc", "mystery", "creative", "premium", "viral", "exp"):
        m, _ = M.track(style, dur_, rng)
        return m[:n] if len(m) >= n else np.pad(m, (0, n - len(m)))
    m = np.zeros(n)
    t = np.arange(n) / M.SR
    if style == "drone":
        drone = np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 55.4 * t) + 0.25 * np.sin(2 * np.pi * 82.6 * t)
        m += M.lp(drone, 300) * 0.35 * (0.8 + 0.2 * np.sin(2 * np.pi * 0.07 * t))
        m += np.sin(2 * np.pi * (1244 + 6 * np.sin(2 * np.pi * 0.3 * t)) * t) * 0.015 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t))
    elif style == "warm":
        bar = 60 / 64 * 4
        m += loop_chords(dur_, bar, lambda fq, d: M.rhodes(fq, d), 0.32, C_MAJ)[:n]
        m += loop_chords(dur_, bar, lambda fq, d: M.pad(fq / 2, d, 0.6), 0.5, C_MAJ)[:n]
        tb, k = 1.0, 0
        mel = [659.25, 587.33, 523.25, 587.33, 659.25, 783.99, 659.25, 587.33]
        while tb < dur_:
            M.add(m, M.pluck(mel[k % len(mel)], 1.6, 3.2), tb, 0.03)
            tb += bar / 2
            k += 1
    elif style == "space":
        bar = 60 / 60 * 4
        m += loop_chords(dur_, bar * 2, lambda fq, d: M.pad(fq, d, 1.2), 0.6, [[220.0, 329.63, 493.88], [174.61, 261.63, 440.0],
                                                                                [196.0, 293.66, 440.0], [164.81, 246.94, 392.0]])[:n]
        tb, k = 0.5, 0
        arp = [880.0, 1318.5, 1760.0, 1318.5, 987.77, 1318.5]
        while tb < dur_:
            M.add(m, M.pluck(arp[k % len(arp)], 1.2, 4.5), tb, 0.022)
            tb += 60 / 60 / 2
            k += 1
        m += np.sin(2 * np.pi * 41.2 * t) * 0.05
    elif style == "tension":
        m += music_bed("drone", dur_, rng) * 0.8
        beat = 60 / 100
        tb, k = 0.0, 0
        while tb < dur_:
            fq = [110.0, 110.0, 116.54, 110.0][(k // 8) % 4]
            M.add(m, M.lp(M.sq(fq, beat / 2 * 0.8, 9), 700), tb, 0.08)
            tb += beat / 2
            k += 1
    elif style == "playful":
        bpm = 112
        beat = 60 / bpm
        m += loop_chords(dur_, beat * 4, lambda fq, d: M.pad(fq, d, 0.7), 0.25, C_MAJ)[:n]
        tb, k = 0.3, 0
        mel = [523.25, 659.25, 783.99, 659.25, 587.33, 698.46, 880.0, 698.46]
        while tb < dur_:
            if k % 2 == 0:
                M.add(m, M.pluck(C_MAJ[(k // 8) % 4][0] / 2, 0.25, 14), tb, 0.22)
            M.add(m, M.pluck(mel[k % 8], 0.3, 13), tb + beat / 4, 0.045)
            tb += beat / 2
            k += 1
    elif style == "noir":
        beat = 60 / 84
        m += loop_chords(dur_, beat * 4, lambda fq, d: M.rhodes(fq, d), 0.22, NOIR)[:n]
        tb, k = 0.0, 0
        while tb < dur_:
            M.add(m, M.lp(rng.standard_normal(int(0.12 * M.SR)) * np.exp(-np.arange(int(0.12 * M.SR)) / M.SR * 30), 6000), tb, 0.025)
            M.add(m, M.lp(rng.standard_normal(int(0.08 * M.SR)) * np.exp(-np.arange(int(0.08 * M.SR)) / M.SR * 40), 6000), tb + beat * 0.66, 0.018)
            bass = NOIR[(k // 4) % 4][0] / 2
            M.add(m, M.lp(M.pluck(bass * (1.5 if k % 2 else 1.0), beat, 5), 400), tb, 0.18)
            tb += beat
            k += 1
    elif style == "epic":
        m += music_bed("doc", dur_, rng) * 0.9
        beat = 60 / 70
        tb = 0.0
        while tb < dur_:
            M.add(m, M.kick(0.6, 80, 40, 5), tb, 0.35)
            M.add(m, M.kick(0.5, 90, 45, 6), tb + beat * 1.5, 0.2)
            tb += beat * 2
    return m[:n]


def fx_softpop():
    SR = M.SR
    tb = np.arange(int(0.16 * SR)) / SR
    f = 520 + 380 * (1 - np.exp(-tb * 40))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * np.clip(tb / 0.16, 0, 1)) ** 2 * np.exp(-tb * 14)


def fx_trans_soft(rng, d=0.6):
    """Transición suave: soplo grave y redondo, sin agudos ni golpe."""
    SR = M.SR
    n = int(d * SR)
    u = np.arange(n) / n
    air = M.lp(M.lp(rng.standard_normal(n), 700), 700)
    f = 80 + 120 * np.sin(np.pi * u)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.45
    sig = (air + tone) * np.sin(np.pi * u) ** 2.2
    return sig / (np.max(np.abs(sig)) + 1e-9)


def fx_trans(rng, d=0.5, up=False):
    """Transición cinematográfica: soplo grave y cálido + «whoom» tonal + golpe sub al final (sustituye al siseo)."""
    SR = M.SR
    n = int(d * SR)
    u = np.arange(n) / n
    x = rng.standard_normal(n)
    low, mid = M.lp(x, 420), M.lp(x, 1900)
    m = np.sin(np.pi * u) ** 1.5
    air = low * (1 - m) + mid * m
    env = np.sin(np.pi * np.clip(u / 0.85, 0, 1)) ** 2
    f = (70 + 230 * np.sin(np.pi * u)) if not up else (90 + 340 * u ** 1.4)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + np.sin(4 * np.pi * np.cumsum(f) / SR) * 0.12
    sig = (air * 0.9 + tone) * env
    ts = np.arange(int(0.42 * SR)) / SR
    sub = np.sin(2 * np.pi * np.cumsum(62 - 18 * ts / 0.42) / SR) * np.exp(-ts * 9) * 0.9
    out = np.zeros(n + len(sub))
    out[:n] += sig
    i0 = int(0.62 * n)
    out[i0:i0 + len(sub)] += sub
    return out / (np.max(np.abs(out)) + 1e-9)


def fx_glide(rng, d=0.7):
    """Movimiento de cámara suave: oleaje grave y apagado, casi sin agudos."""
    SR = M.SR
    n = int(d * SR)
    u = np.arange(n) / n
    air = M.lp(rng.standard_normal(n), 320)
    f = 55 + 45 * np.sin(np.pi * u)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    sig = (air * 0.8 + tone * 0.6) * np.sin(np.pi * u) ** 2
    return sig / (np.max(np.abs(sig)) + 1e-9)


def fx(kind, rng):
    SR = M.SR
    if kind == "whoosh":
        return fx_trans_soft(rng, 0.6)
    if kind == "whoosh_up":
        return fx_trans_soft(rng, 0.55)
    if kind == "whoosh_old":
        return M.fx_whoosh(rng, 0.6, False)
    if kind == "riser":
        return M.fx_riser(rng, 1.2)
    if kind == "riser_long":
        return M.fx_riser(rng, 2.2)
    if kind == "impact":
        return M.fx_impact(rng)
    if kind in ("boom", "rumble"):
        tr = np.arange(int((4.5 if kind == "boom" else 3.0) * SR)) / SR
        r = M.lp(rng.standard_normal(len(tr)), 140) * np.exp(-tr * (0.9 if kind == "boom" else 1.4)) * 2.2
        if kind == "boom":
            r[: len(M.fx_impact(rng))] += M.fx_impact(rng) * 1.2
        return r
    if kind == "ding":
        return M.fx_ding(1568)
    if kind == "chime":
        out = np.zeros(int(1.0 * SR))
        for j, fq in enumerate((2093, 2637, 3136)):
            M.add(out, M.fx_ding(fq), j * 0.07, 0.6)
        return out
    if kind == "heart":
        return M.fx_heart()
    if kind == "bell":
        tb = np.arange(int(1.6 * SR)) / SR
        return sum(np.sin(2 * np.pi * fq * tb) * np.exp(-tb * dk) * g for fq, dk, g in
                   ((880, 2.5, 1.0), (1320 * 1.007, 3.5, 0.5), (2210, 5, 0.3), (3070, 7, 0.2)))
    if kind == "bigbell":
        tb = np.arange(int(3.0 * SR)) / SR
        return sum(np.sin(2 * np.pi * fq * tb) * np.exp(-tb * dk) * g for fq, dk, g in
                   ((196, 0.9, 1.0), (392 * 1.004, 1.3, 0.5), (588, 2.0, 0.3), (1050, 3, 0.15)))
    if kind == "knock":
        tg = np.arange(int(0.25 * SR)) / SR
        return (M.lp(rng.standard_normal(len(tg)), 1800) * 0.7 + np.sin(2 * np.pi * 140 * tg)) * np.exp(-tg * 30)
    if kind == "swell":
        return M.fx_swell(rng, 1.6)
    if kind == "paper":
        return M.fx_paper(rng)
    if kind == "click":
        return M.fx_click()
    if kind == "pop":
        return M.fx_pop()
    if kind == "glitch":
        return M.fx_glitch(rng)
    if kind == "notif":
        return M.fx_notif()
    if kind == "tick":
        tg = np.arange(int(0.05 * SR)) / SR
        return np.sin(2 * np.pi * 3200 * tg) * np.exp(-tg * 160) * 0.6 + M.hp(rng.standard_normal(len(tg)), 4000) * np.exp(-tg * 200) * 0.3
    if kind == "type":
        out = np.zeros(int(1.3 * SR))
        tt_ = 0.0
        while tt_ < 1.2:
            tk = fx("tick", rng) * 0.8
            tk[: int(0.03 * SR)] += M.lp(rng.standard_normal(int(0.03 * SR)), 2000) * 0.4
            M.add(out, tk, tt_, 1.0)
            tt_ += rng.uniform(0.07, 0.15)
        M.add(out, M.fx_ding(2600) * 0.4, 1.15, 1.0)
        return out
    if kind == "shutter":
        out = np.zeros(int(0.3 * SR))
        M.add(out, fx("tick", rng), 0, 1.0)
        M.add(out, M.lp(rng.standard_normal(int(0.08 * SR)), 3000) * np.exp(-np.arange(int(0.08 * SR)) / SR * 50), 0.06, 0.7)
        return out
    if kind == "beep":
        tg = np.arange(int(0.16 * SR)) / SR
        return np.sin(2 * np.pi * 1000 * tg) * np.minimum(1, (0.16 - tg) / 0.02) * 0.5
    if kind == "static":
        tg = np.arange(int(0.9 * SR)) / SR
        return M.hp(rng.standard_normal(len(tg)), 1500) * 0.35 * np.minimum(1, tg / 0.05) * np.minimum(1, (0.9 - tg) / 0.2)
    if kind == "rattle":
        out = np.zeros(int(1.2 * SR))
        for j in range(12):
            tg = np.arange(int(0.06 * SR)) / SR
            M.add(out, (M.lp(rng.standard_normal(len(tg)), 2500) + np.sin(2 * np.pi * 120 * tg)) * np.exp(-tg * 60), j * 0.085, 0.7)
        return out
    if kind == "horn":
        tt2 = np.arange(int(2.6 * SR)) / SR
        h = sum(np.sign(np.sin(2 * np.pi * fq * tt2)) * g for fq, g in ((82, 0.6), (123, 0.4)))
        return M.lp(h, 600) * np.minimum(1, tt2 / 0.15) * np.minimum(1, (2.6 - tt2) / 0.4)
    if kind == "train":
        tt2 = np.arange(int(2.2 * SR)) / SR
        h = sum(np.sin(2 * np.pi * fq * tt2) * g for fq, g in ((311.1, 0.5), (370.0, 0.4), (466.2, 0.3)))
        return M.lp(h, 1800) * np.minimum(1, tt2 / 0.1) * np.minimum(1, (2.2 - tt2) / 0.5) * 0.7
    if kind == "clack":
        out = np.zeros(int(3.0 * SR))
        for j in range(8):
            for off in (0.0, 0.12):
                M.add(out, fx("knock", rng) * 0.5, j * 0.36 + off, 1.0)
        return out
    if kind == "crackle":
        out = np.zeros(int(2.0 * SR))
        for j in range(40):
            M.add(out, fx("tick", rng) * rng.uniform(0.2, 0.7), rng.uniform(0, 1.9), 1.0)
        return out
    if kind == "drill":
        tg = np.arange(int(3.0 * SR)) / SR
        sig = np.sin(2 * np.pi * (90 + 6 * np.sin(2 * np.pi * 3 * tg)) * tg) + 0.5 * np.sign(np.sin(2 * np.pi * 45 * tg))
        return M.lp(sig, 900) * 0.4 * np.minimum(1, tg / 0.3) * np.minimum(1, (3 - tg) / 0.5)
    if kind == "zap":
        tg = np.arange(int(0.35 * SR)) / SR
        buzz = np.sign(np.sin(2 * np.pi * 120 * tg)) * 0.5 + M.hp(rng.standard_normal(len(tg)), 2000) * 0.6
        return M.lp(buzz, 5000) * np.exp(-tg * 9) * (0.6 + 0.4 * (rng.random(len(tg)) > 0.5))
    if kind == "blip":
        tg = np.arange(int(0.12 * SR)) / SR
        return np.sin(2 * np.pi * np.cumsum(900 + 1800 * tg / 0.12) / SR) * np.exp(-tg * 25)
    if kind == "blip_down":
        tg = np.arange(int(0.12 * SR)) / SR
        return np.sin(2 * np.pi * np.cumsum(2400 - 1500 * tg / 0.12) / SR) * np.exp(-tg * 25)
    if kind == "draw":
        tg = np.arange(int(0.8 * SR)) / SR
        return M.lp(M.hp(rng.standard_normal(len(tg)), 3000), 9000) * 0.25 * np.sin(np.pi * tg / 0.8) ** 2
    if kind == "hum_on":
        tg = np.arange(int(1.2 * SR)) / SR
        return (np.sin(2 * np.pi * 100 * tg) + 0.4 * np.sin(2 * np.pi * 200 * tg)) * 0.4 * np.minimum(1, tg / 0.05) * np.exp(-tg * 1.2)
    if kind == "ring":
        tg = np.arange(int(3.2 * SR)) / SR
        return np.sin(2 * np.pi * 5800 * tg) * 0.12 * np.minimum(1, tg / 0.05) * np.exp(-tg * 0.9)
    if kind == "thud":
        tg = np.arange(int(0.5 * SR)) / SR
        return M.kick(0.5, 70, 35, 7) + M.lp(rng.standard_normal(len(tg)), 400) * np.exp(-tg * 12) * 0.4
    if kind == "gavel":
        out = fx("knock", rng)
        o2 = np.zeros(int(0.8 * SR))
        M.add(o2, out, 0, 1.0)
        M.add(o2, M.fx_ding(1568) * 0.15, 0.05, 1.0)
        return o2
    if kind == "glass":                          # cristal que se agrieta y se rompe
        tg = np.arange(int(1.2 * SR)) / SR
        crack = M.hp(rng.standard_normal(len(tg)), 3500) * np.exp(-tg * 9)
        out = crack * 0.8
        for j in range(14):
            M.add(out, M.fx_ding(2400 + rng.uniform(0, 3600)) * rng.uniform(0.05, 0.16), 0.04 + rng.uniform(0, 0.7), 1.0)
        return out
    raise ValueError(kind)


AMB = {}


def amb_sig(kind, n, rng):
    SR = M.SR
    tt = np.arange(n) / SR
    if kind == "sea":
        x = M.lp(rng.standard_normal(n), 420) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * tt))
    elif kind == "wind":
        x = M.lp(M.hp(rng.standard_normal(n), 250), 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * tt) ** 2)
    elif kind == "room":
        x = M.lp(rng.standard_normal(n), 250) * 0.5
    elif kind == "crowd":
        x = M.lp(M.hp(rng.standard_normal(n), 300), 1800) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 0.9 * tt) * np.sin(2 * np.pi * 0.37 * tt)))
    elif kind == "space":
        x = np.sin(2 * np.pi * 40 * tt) * 0.5 + M.lp(rng.standard_normal(n), 900) * 0.25
    elif kind == "rain":
        x = M.hp(rng.standard_normal(n), 2500) * 0.6
    elif kind == "fire":
        x = M.lp(rng.standard_normal(n), 300) * 0.7
        for _ in range(int(n / SR * 12)):
            i = rng.integers(0, n - 200)
            x[i:i + 200] += M.hp(rng.standard_normal(200), 2000) * rng.uniform(0.5, 2.0)
    elif kind == "birds":
        x = M.lp(rng.standard_normal(n), 300) * 0.3
        for _ in range(int(n / SR * 1.5)):
            i = rng.integers(0, n - SR)
            seg = np.arange(int(0.12 * SR)) / SR
            fq = rng.uniform(2500, 4200)
            chirp = np.sin(2 * np.pi * (fq + 1500 * seg / 0.12) * seg) * np.sin(np.pi * seg / 0.12)
            x[i:i + len(chirp)] += chirp * 0.4
    elif kind == "hum":
        x = np.sin(2 * np.pi * 100 * tt) * 0.5 + np.sin(2 * np.pi * 200 * tt) * 0.2 + M.lp(rng.standard_normal(n), 400) * 0.2
    elif kind == "road":
        x = M.lp(rng.standard_normal(n), 250) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * tt)) + np.sin(2 * np.pi * 70 * tt) * 0.15
    elif kind == "city":
        x = M.lp(rng.standard_normal(n), 600) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.05 * tt))
    else:
        raise ValueError(kind)
    return x / (np.max(np.abs(x)) + 1e-9)


def at(spec, by):
    """'plano', 'plano+0.5', 'plano@L1', 'plano@L1e-0.2', 'plano@end' o un número absoluto."""
    if isinstance(spec, (int, float)):
        return float(spec)
    m = re.match(r"^([a-z0-9_]+)(?:@(?:L(\d+)(e?)|(end)))?([+-][\d.]+)?$", spec)
    if not m:
        raise ValueError(spec)
    nm, li, le, en, off = m.groups()
    s = by[nm]
    t = s["start"]
    if li is not None:
        a, b = s["lines"][int(li)]
        t += b if le else a
    elif en:
        t = s["end"]
    return t + (float(off) if off else 0.0)


def smooth(x, k):
    """Media móvil rápida (suma acumulada) de ancho k, misma longitud que x."""
    c = np.cumsum(np.concatenate([np.zeros(1), x]))
    y = (c[k:] - c[:-k]) / k
    pad = k // 2
    return np.concatenate([np.full(pad, y[0]), y, np.full(len(x) - len(y) - pad, y[-1])])


def build_audio(V, shots, total, path, seed=3, chunks=None):
    rng = np.random.default_rng(seed)
    sr = M.SR
    n = int((total + 1) * sr)
    tt = np.arange(n) / sr
    by = {s["name"]: s for s in shots}
    A = V.AUDIO
    # música por tramos con fundido de 2 s
    segs = A.get("music", [("_0", "doc")])
    if getattr(V, "POP", None) and getattr(V, "NOTIF", None):
        import pop as POP
        POP.P["brk"] = at(V.NOTIF[0], by) + V.NOTIF[1]      # el subidón de la música cae con el banner de seguir
    beds = {}
    music = np.zeros(n)
    starts = [0.0 if (i == 0) else at(nm, by) for i, (nm, _) in enumerate(segs)]
    for i, (nm, style) in enumerate(segs):
        if style not in beds:
            beds[style] = music_bed(style, total + 1, rng)[:n]
            if len(beds[style]) < n:
                beds[style] = np.pad(beds[style], (0, n - len(beds[style])))
        a = starts[i]
        b = starts[i + 1] if i + 1 < len(segs) else total + 5
        w = np.clip((tt - a + 1.0) / 2.0, 0, 1) * np.clip((b + 1.0 - tt) / 2.0, 0, 1)
        if i == 0:
            w = np.clip((b + 1.0 - tt) / 2.0, 0, 1)
        gain = A.get("gains", {}).get(style, 1.0)
        music += beds[style] * w * gain
    music = music / (np.max(np.abs(music)) + 1e-9) * 0.5
    duck = np.ones(n)
    for d0, d1, lvl in A.get("duck", []):
        ia, ib = int(at(d0, by) * sr), int(at(d1, by) * sr)
        ramp = int(0.4 * sr)
        seg = np.full(max(0, ib - ia), lvl)
        if len(seg) > 2 * ramp:
            seg[:ramp] = np.linspace(1, lvl, ramp)
            seg[-ramp:] = np.linspace(lvl, 1, ramp)
        duck[ia:ib] = np.minimum(duck[ia:ib], seg[: max(0, min(ib, n) - ia)])
    hy = getattr(V, "HYPE", None)
    if hy:
        h0 = shots[0]["start"] + shots[0]["lines"][hy["line"]][0]
        ia, ib, ic = int(max(0, h0 - 0.5) * sr), int(h0 * sr), int((h0 + 0.7) * sr)
        duck[ia:ib] *= np.linspace(1, 0.3, ib - ia)
        duck[ib:ic] *= np.linspace(1.15, 1, ic - ib)
    music *= duck
    # ambientes
    amb = np.zeros(n)
    for kind, names in A.get("amb", {}).items():
        mask = np.zeros(n)
        for nm in names:
            s = by[nm]
            mask[int(s["start"] * sr):int(s["end"] * sr)] = 1
        mask = smooth(mask, int(0.5 * sr))
        g = {"sea": 0.22, "wind": 0.2, "room": 0.08, "crowd": 0.12, "space": 0.12, "rain": 0.12, "fire": 0.16,
             "birds": 0.12, "city": 0.14, "hum": 0.06, "road": 0.16}[kind]
        amb += amb_sig(kind, n, rng) * mask * g
    fxb = np.zeros(n)

    def add(sig, t0, g):
        M.add(fxb, sig, t0, g)

    for s in shots[1:]:
        if getattr(V, "POP", None) or getattr(V, "CUT_SFX", False):
            # corte seco: whoosh que llega justo al corte + golpe grave
            add(fx_trans_soft(rng, 0.45), s["start"] - 0.24, 0.13)
            add(M.lp(M.kick(0.3, 90, 40, 10), 900), s["start"], 0.16)
        else:
            add(fx_trans_soft(rng, 0.6), s["start"] - 0.32, 0.07)
    if getattr(V, "POP", None) or getattr(V, "CUT_SFX", False):
        for h in docu_beats(V)[1]:
            add(M.lp(fx_softpop(), 3500), h, 0.05)      # «pop» en las palabras clave (rompe el ritmo cada pocos segundos)
    for s in shots:
        if s["name"] in V.FOCUS:
            for c in cut_points(s)[1:]:
                add(fx_glide(rng, 0.7), s["start"] + c - 0.15, 0.03)
    hy = getattr(V, "HYPE", None)
    if hy:
        h0 = shots[0]["start"] + shots[0]["lines"][hy["line"]][0]
        rl = min(1.3, h0)
        if rl > 0.2:
            add(M.lp(M.fx_riser(rng, rl), 3000), h0 - rl + 0.02, 0.07)
        add(M.lp(M.fx_impact(rng), 1500), h0, 0.22)
        add(fx("boom", rng), h0, 0.06)
        for dl in hy.get("delay", [0])[1:]:
            add(M.lp(M.fx_impact(rng), 1500), h0 + dl, 0.13)
    HARSH = {"glitch", "zap", "static", "beep", "shutter", "crackle", "drill", "horn", "knock", "clack", "type", "rattle", "train",
             "boom", "impact", "riser", "riser_long", "tick"}
    for spec, kind, g in A.get("sfx", []):
        add(fx(kind, rng), at(spec, by), g * (0.38 if kind in HARSH else 0.65))
    if chunks is not None:
        for ts_, e, _ in sticker_plan(V, shots, chunks, total):
            add(fx_softpop(), ts_, 0.04)
    if CAPS_[0] is not None and getattr(V, "CAPTIONS", "keywords") == "keywords" and not is_docu(V):
        for it in keyword_plan(V, shots, CAPS_[0], total):
            add(M.lp(fx_softpop(), 2500), it["t0"], 0.035)
    ui = np.zeros(n)          # sonidos de interfaz que no se tapan con la voz
    if is_docu(V):
        if getattr(V, "FOLLOW", None):
            tf = at(V.FOLLOW, by)
            add(fx_softpop(), tf + 0.05, 0.06)
            add(M.lp(fx_softpop(), 3000), tf + 1.42, 0.09)
        elif getattr(V, "NOTIF", None):
            nt = at(V.NOTIF[0], by) + V.NOTIF[1]
            M.add(ui, M.fx_notif(), nt + 0.05, 1.0)
    else:
        nt = at(V.NOTIF[0], by) + V.NOTIF[1]
        add(M.fx_notif(), nt + 0.05, 0.2)
    if getattr(V, "NARRATOR", None) and not getattr(V, "END_CARD", None):
        e0 = total - end_hold(V)
        for dt, g in ((0.8, 0.07), (1.1, 0.06), (1.4, 0.06), (1.8, 0.09), (2.6, 0.09)):
            add(fx_softpop(), e0 + dt, g)
    fxb = M.lp(fxb, 6000)
    # base rítmica suave
    bed = np.zeros(n)
    beat = 60 / A.get("bpm", 96)
    for a_, b_ in A.get("bed", []):
        tb, k = at(a_, by), 0
        b_t = at(b_, by) if b_ != "end" else total - 2.5
        while tb < b_t:
            M.add(bed, M.kick(0.3, 110, 46, 12), tb, 0.5)
            M.add(bed, M.hat(rng, 0.04), tb + beat / 2, 0.08)
            if k % 2 == 1:
                M.add(bed, M.lp(M.snare(rng, 0.15), 2500), tb, 0.12)
            tb += beat
            k += 1
    vp = getattr(V, "_VOICE_FIT", None) or getattr(V, "VOICE", None)
    if is_docu(V) and vp and os.path.exists(vp):
        import docu as DC
        vx, vsr = DC.load_audio(vp, sr)
        voice = np.zeros(n)
        i0 = int(VOICE_LEAD * sr)
        vx = vx[: max(0, n - i0)]
        voice[i0:i0 + len(vx)] = vx / (np.max(np.abs(vx)) + 1e-9)
        env = smooth(np.abs(voice), int(0.05 * sr))
        act = smooth((env > 0.03).astype(float), int(0.35 * sr))
        g = 1 - getattr(V, "MUSIC_DUCK", 0.72 if getattr(V, "POP", None) else 0.6) * np.clip(act * 1.6, 0, 1)   # pop: música ~15 dB bajo la voz
        music = music * getattr(V, "MUSIC_GAIN", 1.0)            # 21/10: Iker quiere la música de fondo más presente
        uim = ui / (np.max(np.abs(ui)) + 1e-9) * 0.42 if np.any(ui) else ui
        mix = (music + amb + fxb + bed * 0.42) * g * 0.75 + voice * 0.9 + uim
    else:
        mix = music + amb + fxb + bed * 0.42
    mix = mix[: int(total * sr)]
    fade = int(1.5 * sr)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix /= np.max(np.abs(mix)) + 1e-9
    st = np.stack([mix, np.roll(mix, 160)], axis=1) * 0.88
    from scipy.io import wavfile
    wavfile.write(path, sr, (st * 32767).astype(np.int16))


# ------------------------------------------------------------------ render
def draw_shot(V, s, t):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    TOP[0] = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    MUTE_HEADS[0] = bool(getattr(V, "DOCU_SKIN", False))
    if getattr(V, "POP", None):
        import pop as POP
        POP.P["gt"] = t
    V.FNS[s["name"]](img, t - s["start"], s["end"] - s["start"], s["lines"])
    MUTE_HEADS[0] = False
    if is_docu(V) and getattr(V, "DOCU_SKIN", False):
        import docu as DC
        img = Image.blend(img, DC._bg_base(540, 860), 0.28)       # mismo azul noche que los vídeos nuevos
        top_ = cached(("skin_top",), lambda: _skin_top())
        AC(img, top_)
        bottom_shade(img)        # que los subtítulos se lean sobre cualquier dibujo
    if is_docu(V):
        q = ease(clamp((t - s["start"]) / max(1.0, s["end"] - s["start"])))
        z = 1.0 + 0.035 * q
        fx_, fy_ = getattr(V, "PUSH", {}).get(s["name"], (540, 820))
        if getattr(V, "BEATS", False):
            # ritmo: cambio de encuadre rápido cada ~1,3 s (al empezar un grupo de subtítulos) y golpe en las palabras clave
            fr, pu = docu_beats(V)
            bs = [b for b in fr if s["start"] + 0.25 < b < s["end"] - 0.15]
            k = sum(1 for b in bs if b <= t)
            P = [(1.0, 0, 0), (1.10, -28, -12), (1.05, 36, 18), (1.14, 6, -24)]
            cur = P[k % 4]
            prv = P[(k - 1) % 4] if k > 0 else P[0]
            u = ease(clamp((t - bs[k - 1]) / 0.26)) if k > 0 else 1.0
            z *= lerp(prv[0], cur[0], u)
            fx_ += lerp(prv[1], cur[1], u)
            fy_ += lerp(prv[2], cur[2], u)
            for h in pu:
                if 0 <= t - h < 0.32:
                    z *= 1 + 0.035 * math.sin(math.pi * (t - h) / 0.32)
        if getattr(V, "POP", None):
            import pop as POP
            if not POP.P["pu"]:
                POP.P["pu"] = list(docu_beats(V)[1])
            zm, dx_, dy_ = POP.cam(t, s["start"])
            z *= zm
            fx_ += dx_
            fy_ += dy_
        cw, ch = W / z, H / z
        x0 = min(max(0, fx_ - cw / 2), W - cw)
        y0 = min(max(0, fy_ - ch / 2), H - ch)
        img = img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BICUBIC)
        return img, TOP[0]
    return reframe(V, img, s, t - s["start"]), TOP[0]


def _hype_line(txt, col, size):
    fnt = f(F_SER, size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    tw = int(tmp.textlength(txt, font=fnt)) + 80
    th = int(size * 1.5)
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((tw / 2, th / 2), txt, font=fnt, fill=col + (255,), anchor="mm")
    gl = im.copy().filter(ImageFilter.GaussianBlur(16))
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    sh = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((tw / 2 + 6, th / 2 + 8), txt, font=fnt, fill=(0, 0, 0, 200), anchor="mm")
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    for _ in range(2):
        out.alpha_composite(gl)
    d = ImageDraw.Draw(out)
    d.text((tw / 2, th / 2), txt, font=fnt, fill=col + (255,), anchor="mm", stroke_width=max(4, size // 18), stroke_fill=(12, 12, 16, 255))
    return out


def _hype_assets(V):
    hy = V.HYPE
    key_ = ("hype", V.TITLE)
    if key_ in GRADS:
        return GRADS[key_]
    lines = hy["text"]
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ims = []
    for i, ln in enumerate(lines):
        size = 132
        while tmp.textlength(ln, font=f(F_SER, size)) > 960 and size > 60:
            size -= 4
        col = YEL if (i == len(lines) - 1) else WHITE
        ims.append(_hype_line(ln, col, size))
    ys = np.arange(H)[:, None]
    a = (np.clip(1 - ys / H, 0, 1) * 110 + 95).astype(np.uint8)
    ov = np.zeros((H, W, 4), np.uint8)
    ov[..., 3] = np.broadcast_to(a, (H, W))
    q = _hype_line("?", YEL, 820)
    GRADS[key_] = (ims, Image.fromarray(ov, "RGBA"), q)
    return GRADS[key_]


def hype_card(img, V, u, D):
    """La pregunta del inicio a lo grande: escena oscurecida, rayos, «?» gigante y texto que entra de golpe."""
    hy = V.HYPE
    ims, ov, q = _hype_assets(V)
    delays = hy.get("delay", [0] * len(ims))
    k = clamp(u / 0.12) * (1 - clamp((u - D) / 0.35))
    if k <= 0:
        return img
    if 0 <= u < 0.45:
        amp = 16 * (1 - u / 0.45)
        dx, dy = math.sin(u * 95) * amp, math.cos(u * 80) * amp
        z = 1 + 0.05 * (1 - u / 0.45)
        cw, ch = W / z, H / z
        x0, y0 = (W - cw) / 2 + dx, (H - ch) / 2 + dy
        img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)
    AC(img, with_alpha(ov, k))
    cy = 660
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    for i in range(16):
        a = i / 16 * 2 * math.pi + u * 0.35
        p1 = (540 + math.cos(a - 0.07) * 1500, cy + math.sin(a - 0.07) * 1500)
        p2 = (540 + math.cos(a + 0.07) * 1500, cy + math.sin(a + 0.07) * 1500)
        ld.polygon([(540, cy), p1, p2], fill=YEL + (int(34 * k),))
    AC(img, lay.filter(ImageFilter.GaussianBlur(14)))
    qs = 1.0 + 0.04 * math.sin(u * 3)
    paste(img, q, 540 + 30, cy + 10, qs, 0.16 * k, -8)
    tot_h = sum(im_.size[1] * 0.78 for im_ in ims)
    y = cy - tot_h / 2
    for i, im_ in enumerate(ims):
        ui = u - (delays[i] if i < len(delays) else 0)
        h_ = im_.size[1] * 0.78
        if ui >= 0:
            p = clamp(ui / 0.26)
            back = 1 + 2.2 * (p - 1) ** 3 + 1.2 * (p - 1) ** 2
            sc = lerp(1.6, 1.0, back) if p < 1 else 1.0 + 0.012 * math.sin(ui * 6)
            sc *= 1 + 0.08 * clamp((u - D) / 0.35)
            al = clamp(ui / 0.1) * (1 - clamp((u - D) / 0.35))
            paste(img, im_, 540, y + h_ / 2, sc, al)
            if ui < 0.14:
                overlay(img, (255, 255, 255), 0.32 * (1 - ui / 0.14))
            if i == len(ims) - 1:
                bw = min(760, im_.size[0] - 120) * ease(clamp((ui - 0.15) / 0.3))
                d = ImageDraw.Draw(img, "RGBA")
                by_ = y + h_ + 12
                d.rounded_rectangle([540 - bw / 2, by_, 540 + bw / 2, by_ + 10], radius=5, fill=YEL + (int(240 * al),))
        y += h_
    return img


def _skin_top():
    """Oscurece la franja de arriba para que la cabecera nueva se lea sobre cualquier escena antigua."""
    ys = np.arange(H)
    prof = np.clip(1 - ys / 520, 0, 1) ** 1.6 * 200
    a = np.repeat(prof[:, None], W, axis=1).astype(np.uint8)
    v = Image.new("RGBA", (W, H), (9, 12, 25, 0))
    v.putalpha(Image.fromarray(a, "L"))
    return v


def docu_beats(V):
    """Momentos de cambio de encuadre (uno cada >=1,2 s, al empezar un grupo de subtítulos) y golpes (palabras clave)."""
    key_ = ("beats", V.TITLE, id(CAPS_[0]))
    if key_ not in GRADS:
        import docu as DC
        ch = DC.make_chunks(CAPS_[0])
        fr, last = [], -9
        for t0, t1, ws in ch:
            if t0 - last >= 1.2:
                fr.append(t0)
                last = t0
        pu = [t0 for t0, t1, ws in ch if any(hl for _, hl in ws)]
        GRADS[key_] = (fr, pu)
    return GRADS[key_]


def frame_docu(V, shots, chunks, total, i):
    import docu as DC
    t = i / FPS
    FRAME_TEXTS.clear()
    si = next((k for k, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
    s = shots[si]
    img, top = draw_shot(V, s, t)
    xf_ = getattr(V, "XF", XF)
    if si > 0 and t - s["start"] < xf_:
        p = shots[si - 1]
        pim, ptop = draw_shot(V, p, t)
        q = ease((t - s["start"]) / xf_)
        img = Image.blend(pim, img, q)
        top = Image.blend(ptop, top, q)
    TOP[0] = top
    o0 = total - end_hold(V)
    end_in = t - o0
    key_ = ("heads", V.TITLE, id(CAPS_[0]))
    if key_ not in GRADS:
        GRADS[key_] = DC.head_entries(V, CAPS_[0])
    if end_in > 0:
        import narrator as NR
        NR.outro(V, end_in, end_hold(V))
    AC(img, TOP[0])
    DC.draw_head(img, t, GRADS[key_], fade_out_at=o0)
    if end_in < 0:
        DC.channel_label(img)
    if getattr(V, "NARRATOR", None):
        import narrator as NR
        NR.draw(img, V, t, shots, CAPS_[0], total)
    POPV = getattr(V, "POP", None)
    if POPV:
        import pop as POP
        POP.P["total"] = total
        img = POP.post(img, t, s["start"] if si > 0 else -9)
    fo = getattr(V, "FOLLOW", None)
    by = {x["name"]: x for x in shots}
    if fo and end_in < 0:
        DC.follow_card(img, t - (at(fo, by)))
    elif getattr(V, "NOTIF", None) and end_in < 0:
        # notificación tipo iPhone que baja desde arriba (la de siempre), con su sonido
        img = V2.notif_banner(img, t - (at(V.NOTIF[0], by) + V.NOTIF[1]), "@ojoaldato.ya",
                              getattr(V, "NOTIF_TEXT", "Suscríbete para más historias que no sabías"))
    if end_in < 0.2:
        # CAP_Y = {plano: y} baja el subtítulo en los planos cuyo dibujo ocupa la franja de 1500
        if POPV:
            POP.draw_caption(img, t, CAPS_[0], y=getattr(V, "CAP_Y", {}).get(s["name"], 1480))
        else:
            DC.draw_caption(img, t, chunks, y=getattr(V, "CAP_Y", {}).get(s["name"], 1500))
    if POPV and end_in < 0:
        POP.progress(img, t)
    return img


def frame(V, shots, chunks, total, i):
    if getattr(V, "FRAME", None):            # estilos nuevos (vid2.py): oscuro minimalista, monigotes Paint…
        return V.FRAME(V, shots, chunks, total, i)
    if is_docu(V):
        return frame_docu(V, shots, chunks, total, i)
    t = i / FPS
    FRAME_TEXTS.clear()
    si = next((k for k, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
    s = shots[si]
    img, top = draw_shot(V, s, t)
    if si > 0 and t - s["start"] < XF:
        p = shots[si - 1]
        pim, ptop = draw_shot(V, p, t)
        q = ease((t - s["start"]) / XF)
        img = Image.blend(pim, img, q)
        top = Image.blend(ptop, top, q)
    TOP[0] = top
    end_in = t - (total - end_hold(V))
    if end_in > 0:
        if getattr(V, "END_CARD", None):
            V.END_CARD(end_in)
        elif getattr(V, "NARRATOR", None):
            import narrator as NR
            NR.outro(V, end_in, end_hold(V))
        else:
            end_card(end_in)
    AC(img, TOP[0])
    hy = getattr(V, "HYPE", None)
    if hy and end_in < 0:
        a_, b_ = shots[0]["lines"][hy["line"]]
        t0_ = shots[0]["start"] + a_
        if t0_ - 0.02 <= t <= shots[0]["start"] + b_ + 0.4:
            img = hype_card(img, V, t - t0_, b_ - a_ + 0.05)
    bottom_shade(img)
    if getattr(V, "NARRATOR", None):
        import narrator as NR
        NR.draw(img, V, t, shots, CAPS_[0], total)
    if end_in < -0.3:
        draw_stickers(img, t, sticker_plan(V, shots, chunks, total))
    out = img
    if getattr(V, "CAPTIONS", "keywords") == "full":
        if end_in < 0.4:
            for cs, ce, g in chunks:
                if cs <= t < ce:
                    caption(out, V2.glue(g), t - cs, ce - cs)
    elif end_in < 0:
        draw_keywords(out, t, keyword_plan(V, shots, CAPS_[0], total))
    d = ImageDraw.Draw(out)
    if end_in < 0:
        R.eye_icon(d, 92, 112, 58, (255, 255, 255), YEL, (14, 15, 18))
        d.text((132, 95), "@ojoaldato.ya", font=f(F_CAP, 28), fill=(235, 235, 240))
    by = {x["name"]: x for x in shots}
    notif_t = at(V.NOTIF[0], by) + V.NOTIF[1]
    out = V2.notif_banner(out, t - notif_t, "@ojoaldato.ya", getattr(V, "NOTIF_TEXT", "Suscríbete para más historias que no sabías"))
    return out


CAPS_ = [None]


def render(V, out_mp4, only_times=None, preset="medium"):
    shots, caps, total = timeline(V)
    CAPS_[0] = caps
    chunks = []
    if is_docu(V):
        import docu as DC
        chunks = DC.make_chunks(caps)
    else:
        for c in caps:
            chunks += chunks_for(c["text"], c["start"], c["end"], n=3)
    if only_times:
        return [frame(V, shots, chunks, total, int(x * FPS)) for x in only_times]
    wav = out_mp4.replace(".mp4", ".wav")
    build_audio(V, shots, total, wav, chunks=None if is_docu(V) else chunks)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", preset, "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", out_mp4]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        pipe.stdin.write(frame(V, shots, chunks, total, i).tobytes())
    pipe.stdin.close()
    if pipe.wait() != 0:
        raise RuntimeError("ffmpeg falló")

    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

    with open(out_mp4.replace(".mp4", ".srt"), "w") as fh:
        for k, c in enumerate(caps, 1):
            fh.write(f"{k}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text'].replace('*', '')}\n\n")
    os.remove(wav)
    return total


def sheet(V, times, path, cols=4, scale=0.25):
    ims = render(V, None, only_times=times)
    w, h = int(W * scale), int(H * scale)
    rows = (len(ims) + cols - 1) // cols
    out = Image.new("RGB", (w * cols, h * rows))
    for i, im in enumerate(ims):
        out.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    out.save(path)
    return path
