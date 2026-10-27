"""«La llave que pudo salvar el Titanic» — versión profesional.
14 planos ilustrados a pantalla completa, capas con paralaje, partículas, rótulos de cine y diseño de sonido."""
import math, random, subprocess, json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import render as R
from render import W, H, FPS, ease, lerp, clamp
import pro_sprites as S
import music3 as M
from styles import chunks_for, wrap
import edit_v2 as V2

GF = "/usr/share/fonts/truetype/"
F_CAP = GF + "google-fonts/Poppins-Bold.ttf"
F_SER = GF + "crosextra/Caladea-Bold.ttf"
F_SERR = GF + "crosextra/Caladea-Regular.ttf"
_F = {}


def f(path, size):
    k = (path, int(size))
    if k not in _F:
        _F[k] = ImageFont.truetype(path, max(8, int(size)))
    return _F[k]


YEL = (255, 210, 63)
WPS = 2.75

LINES = [
    "Una pequeña *llave* pudo haber cambiado la historia del Titanic.",
    "¿Qué abría… y por qué *no estaba* en el barco?",
    "Southampton, 10 de abril de 1912.",
    "Zarpa el barco más grande del mundo en su *primer viaje*.",
    "Muchos lo llamaban *insumergible*.",
    "Pero hubo un cambio de última hora.",
    "El oficial *David Blair* fue sustituido… y se bajó del barco.",
    "Sin darse cuenta, se llevó algo *en el bolsillo*.",
    "14 de abril. Noche sin luna y un frío helador.",
    "En lo alto del mástil, dos vigías buscan icebergs…",
    "…*a simple vista*.",
    "A las 23:40, Fleet ve una sombra en el agua.",
    "Toca la campana *tres veces* y avisa al puente: ¡iceberg justo delante!",
    "Apenas un minuto después… *el choque*.",
    "En menos de tres horas, el Titanic se hunde.",
    "Mueren *más de 1.500 personas*.",
    "¿Y la llave?",
    "Según la historia más conocida, abría la caja de los *prismáticos*.",
    "Fleet declaró después que, con prismáticos, lo habrían visto *a tiempo*.",
    "Aunque muchos expertos lo dudan.",
    "En 2007, esa llave se subastó por *90.000 libras*.",
    "Una llave pequeña… para una historia *gigante*.",
]
# plano: (nombre, primera frase, última frase, pausa extra al final)
SHOTS = [("night_open", 0, 1, 0.3), ("port_wide", 2, 2, 0.1), ("ship_depart", 3, 4, 0.3), ("gangway", 5, 7, 0.3),
         ("night_wide", 8, 8, 0.2), ("nest_close", 9, 10, 0.3), ("pov_iceberg", 11, 11, 0.1), ("bell", 12, 12, 0.0),
         ("impact", 13, 13, 0.9), ("sinking", 14, 15, 1.0), ("key_spot", 16, 16, 0.3), ("box_open", 17, 17, 0.3),
         ("fleet_quote", 18, 19, 0.3), ("auction", 20, 21, 1.6)]
HARD_CUT = set()


def dur(txt):
    n = len(re.findall(r"\w+", txt.replace("*", "")))
    return max(1.4, n / WPS + 0.35)


def timeline():
    t = 0.4
    caps, shots = [], []
    for name, a, b, pad in SHOTS:
        st = t
        ls = []
        for i in range(a, b + 1):
            d_ = dur(LINES[i])
            caps.append({"start": round(t, 2), "end": round(t + d_, 2), "text": LINES[i]})
            ls.append((t - st, t - st + d_))
            t += d_ + 0.06
        t += pad * 0.6
        shots.append({"name": name, "start": st, "end": t, "lines": ls})
    shots[0]["start"] = 0.0
    return shots, caps, t


# ------------------------------------------------------------------ recursos precalculados
RNG = random.Random(11)
STARS = [(RNG.uniform(0, W), RNG.uniform(0, 1150), RNG.uniform(0.8, 2.6), RNG.uniform(0, 6.28)) for _ in range(260)]
SPR = {}


def spr(name, *a, **k):
    key_ = (name, a, tuple(sorted(k.items())))
    if key_ not in SPR:
        SPR[key_] = getattr(S, name)(*a, **k)
    return SPR[key_]


def scaled(im, s):
    if abs(s - 1) < 1e-3:
        return im
    return im.resize((max(1, int(im.size[0] * s)), max(1, int(im.size[1] * s))), Image.BILINEAR)


def AC(dst, src, pos=(0, 0)):
    """Composición con mezcla real sobre lienzo RGB."""
    dst.paste(src, (int(pos[0]), int(pos[1])), src if src.mode == "RGBA" else None)


def paste(dst, im, cx, cy, s=1.0, alpha=1.0, rot=0.0):
    im = scaled(im, s)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 0.999:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    AC(dst, im, (cx - im.size[0] / 2, cy - im.size[1] / 2))


def paste_clip(dst, im, x, y):
    x0, y0 = max(0, -x), max(0, -y)
    if x0 >= im.size[0] or y0 >= im.size[1]:
        return
    crop = im.crop((x0, y0, im.size[0], im.size[1]))
    if x + x0 >= W or y + y0 >= H:
        return
    AC(dst, crop, (x + x0, y + y0))


GRADS = {}


def grad(key_, top, bot, power=1.0, h=H):
    if key_ not in GRADS:
        GRADS[key_] = S.vgrad(W, h, top, bot, power).convert("RGBA")
    return GRADS[key_]


def night_sky(img, t, horizon=1050, bright=1.0):
    AC(img, grad("nsky", (4, 8, 22), (22, 36, 72), 1.3))
    d = ImageDraw.Draw(img, "RGBA")
    for x, y, r, ph in STARS:
        if y < horizon - 10:
            a = int(255 * bright * (0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 2.2 + ph))))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(230, 236, 255, a))


def sea(img, t, horizon, top=(18, 30, 60), bot=(3, 6, 16), lines=(48, 70, 110), speed=1.0, day=False):
    key_ = ("sea", horizon, top, bot)
    if key_ not in GRADS:
        g = S.vgrad(W, H - horizon, top, bot).convert("RGBA")
        GRADS[key_] = g
    AC(img, GRADS[key_], (0, horizon))
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(16):
        y = horizon + 8 + (k ** 1.55) * 9
        if y > H:
            break
        amp = 2 + k * 0.8
        ph = t * speed * (0.6 + k * 0.08) + k
        pts = [(x, y + amp * math.sin(x / (60 + k * 12) + ph)) for x in range(-20, W + 40, 40)]
        d.line(pts, fill=lines + (int(140 - k * 6),), width=max(1, int(1 + k * 0.25)))


def fog(img, t, y, alpha=60, speed=20):
    key_ = ("fog",)
    if key_ not in GRADS:
        fg = Image.new("RGBA", (W * 2, 400), (0, 0, 0, 0))
        dd = ImageDraw.Draw(fg)
        rr = random.Random(2)
        for _ in range(26):
            x, yy, r = rr.uniform(0, W * 2), rr.uniform(120, 280), rr.uniform(80, 200)
            dd.ellipse([x - r * 2, yy - r * 0.5, x + r * 2, yy + r * 0.5], fill=(200, 210, 230, 70))
        GRADS[key_] = fg.filter(ImageFilter.GaussianBlur(40))
    fg = GRADS[key_]
    off = int((t * speed) % W)
    band = fg.crop((off, 0, off + W, 400))
    band.putalpha(band.getchannel("A").point(lambda v: int(v * alpha / 70)))
    AC(img, band, (0, int(y - 200)))


def particles(img, t, n=60, seed=4, col=(230, 240, 255), fall=40, size=(1.5, 3.5), alpha=150):
    rr = random.Random(seed)
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(n):
        x0, y0 = rr.uniform(0, W), rr.uniform(0, H)
        sp = rr.uniform(0.5, 1.5) * fall
        r = rr.uniform(*size)
        x = (x0 + math.sin(t * 0.7 + x0) * 20) % W
        y = (y0 + t * sp) % H
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (alpha,))


def smoke(img, t, sources, seed=1, dark=False):
    d = ImageDraw.Draw(img, "RGBA")
    col = (150, 150, 160) if not dark else (40, 44, 56)
    for si, (sx, sy, sc) in enumerate(sources):
        for k in range(10):
            ph = (t * 0.35 + k / 10) % 1.0
            x = sx - ph * 220 * sc
            y = sy - ph * 140 * sc - math.sin(ph * 3 + si) * 10
            r = (14 + ph * 70) * sc
            a = int((80 if not dark else 110) * (1 - ph))
            d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,))


def vignette(img, strength=200):
    key_ = ("vig", strength)
    if key_ not in GRADS:
        yy, xx = np.mgrid[0:H, 0:W]
        dist = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2)
        a = np.clip((dist - 0.55) / 0.6, 0, 1) ** 1.5 * strength
        v = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        v.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
        GRADS[key_] = v
    AC(img, GRADS[key_])


def bottom_shade(img):
    key_ = ("bshade",)
    if key_ not in GRADS:
        a = np.zeros((H, W), np.uint8)
        ys = np.arange(H)
        prof = np.clip((ys - 1180) / 520, 0, 1) ** 1.2 * 190
        a[:] = prof[:, None].astype(np.uint8)
        v = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        v.putalpha(Image.fromarray(a, "L"))
        GRADS[key_] = v
    AC(img, GRADS[key_])


def spaced(d, cx, y, txt, font, fill, track):
    w = sum(d.textlength(ch, font=font) + track for ch in txt) - track
    x = cx - w / 2
    for ch in txt:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return w


TOP = [None]


def td():
    return ImageDraw.Draw(TOP[0])


def lower_third(img, t, t0, line1, line2="", y=300, hold=3.2):
    if t < t0 or t > t0 + hold + 0.6:
        return
    k = ease(clamp((t - t0) / 0.5)) * (1 - ease(clamp((t - t0 - hold) / 0.5)))
    d = td()
    A = int(255 * k)
    w = spaced(d, W / 2, y, line1, f(F_SER, 44), (255, 255, 255, A), 7)
    lw_ = w * ease(clamp((t - t0) / 0.7))
    d.line([(W / 2 - lw_ / 2 - 20, y + 66), (W / 2 + lw_ / 2 + 20, y + 66)], fill=YEL + (A,), width=3)
    if line2:
        spaced(d, W / 2, y + 84, line2, f(F_SERR, 34), (220, 224, 235, int(A * 0.9)), 5)


def flare(img, cx, cy, k, r=260):
    if k <= 0:
        return
    g = spr("glow", r, (255, 230, 170), 0.9)
    paste(img, g, cx, cy, 1.0, k)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(cx - r * 1.6 * k, cy), (cx + r * 1.6 * k, cy)], fill=(255, 240, 200, int(160 * k)), width=3)


# ------------------------------------------------------------------ planos
def sh_night_open(img, t, T, L):
    night_sky(img, t)
    hz = 1080
    fog(img, t, hz - 40, 40, 14)
    shipn = spr("ship", True, True)
    s = 0.78 + 0.05 * (t / T)
    bob = math.sin(t * 0.9) * 3
    sx = 540 + 30 * math.sin(t * 0.2)
    sy = hz - (380 - 240) * s + bob
    smoke(img, t, [(sx + (300 - 500 - 27) * s, sy - 220 * s - 20, s * 0.8), (sx + (425 - 500 - 27) * s, sy - 220 * s - 20, s * 0.8),
                   (sx + (550 - 500 - 27) * s, sy - 220 * s - 20, s * 0.8)], dark=True)
    paste(img, shipn, sx, sy, s)
    sea(img, t, hz)
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(40):
        x = sx + (k / 40 - 0.5) * 760 * s
        y = hz + 20 + (k * 37 % 90)
        a = int(90 + 60 * math.sin(t * 3 + k))
        d.line([(x, y), (x + 14, y)], fill=(255, 210, 140, max(0, a)), width=3)
    fog(img, t * 1.3, hz + 80, 55, 26)
    particles(img, t, 50, 4, fall=25, alpha=110)
    # título del gancho
    if t < 3.4:
        k = ease(clamp(t / 0.5)) * (1 - ease(clamp((t - 2.8) / 0.6)))
        dd = td()
        spaced(dd, W / 2, 300, "LA LLAVE QUE PUDO", f(F_SER, 64), (255, 255, 255, int(255 * k)), 8)
        spaced(dd, W / 2, 380, "SALVAR EL TITANIC", f(F_SER, 86), YEL + (int(255 * k),), 8)
    # la llave aparece con la pregunta
    a0 = L[1][0] - 0.2
    if t > a0:
        k = ease(clamp((t - a0) / 0.6))
        flare(img, 540, 560, k * (0.6 + 0.4 * math.sin(t * 4) ** 2), 240)
        paste(img, spr("key"), 540, 560, 0.85 + 0.05 * math.sin(t * 2), k, rot=8 * math.sin(t * 1.2))
    vignette(img)


def day_sky(img, horizon=1000):
    AC(img, grad("dsky", (92, 132, 190), (255, 196, 150), 1.4))
    paste(img, spr("glow", 420, (255, 220, 160), 0.8), 860, horizon - 120)


def crowd(img, t, y0, n=70, seed=6):
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(seed)
    for i in range(n):
        x = rr.uniform(-20, W + 20)
        y = y0 + rr.uniform(0, 160)
        s = 0.7 + (y - y0) / 160 * 0.6
        c = (24 + int(rr.uniform(0, 20)),) * 3
        d.ellipse([x - 14 * s, y - 40 * s, x + 14 * s, y - 12 * s], fill=c)
        d.rounded_rectangle([x - 24 * s, y - 14 * s, x + 24 * s, y + 70 * s], radius=int(16 * s), fill=c)
        if rr.random() < 0.35:
            wv = math.sin(t * 7 + i) * 12 * s
            d.line([(x + 18 * s, y), (x + 34 * s + wv, y - 50 * s)], fill=c, width=int(10 * s))
            d.ellipse([x + 28 * s + wv, y - 62 * s, x + 42 * s + wv, y - 48 * s], fill=(240, 240, 240))


def gulls(img, t, seed=8, n=6):
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(seed)
    for i in range(n):
        x = (rr.uniform(0, W) + t * rr.uniform(30, 70)) % (W + 100) - 50
        y = rr.uniform(260, 700) + math.sin(t + i) * 10
        s = rr.uniform(0.8, 1.4)
        fl = math.sin(t * 9 + i) * 10 * s
        d.line([(x - 26 * s, y - fl), (x - 6 * s, y), (x, y + 4 * s), (x + 6 * s, y), (x + 26 * s, y - fl)], fill=(40, 40, 50, 220),
               width=int(4 * s))


def sh_port_wide(img, t, T, L):
    hz = 1080
    day_sky(img, hz)
    gulls(img, t)
    for i, x in enumerate((90, 260)):
        paste(img, spr("crane"), x, hz - 260, 0.9 + i * 0.1)
    shipd = spr("ship", False, False)
    s = 1.05
    sx = 740 + t * 18
    sy = hz - (380 - 240) * s
    smoke(img, t, [(sx + (300 - 527) * s, sy - 230 * s, 1.0), (sx + (425 - 527) * s, sy - 230 * s, 1.0),
                   (sx + (550 - 527) * s, sy - 230 * s, 1.0)])
    paste(img, shipd, sx, sy, s)
    sea(img, t, hz, (60, 100, 130), (20, 40, 60), (140, 180, 205), 0.8)
    AC(img, grad("quay", (60, 58, 64), (30, 30, 34), 1.0, 520), (0, 1400))
    crowd(img, t, 1380)
    lower_third(img, t, 0.4, "SOUTHAMPTON", "10 DE ABRIL DE 1912", 300, max(2.0, T - 1.4))
    vignette(img, 150)


def sh_ship_depart(img, t, T, L):
    hz = 1120
    day_sky(img, hz)
    gulls(img, t, 9, 4)
    shipd = spr("ship", False, False)
    s = 1.4
    sx = 340 + t * 42
    sy = hz - (380 - 240) * s
    smoke(img, t, [(sx + (300 - 527) * s, sy - 230 * s, 1.4), (sx + (425 - 527) * s, sy - 230 * s, 1.4),
                   (sx + (550 - 527) * s, sy - 230 * s, 1.4)])
    paste(img, shipd, sx, sy, s)
    sea(img, t, hz, (50, 92, 124), (14, 30, 48), (160, 198, 216), 1.4)
    d = ImageDraw.Draw(img, "RGBA")
    bx = sx + (955 - 500) * s
    for k in range(12):
        ph = (t * 1.6 + k / 12) % 1.0
        d.ellipse([bx - 30 - ph * 160, hz - 10 + ph * 30 - 12, bx - 30 - ph * 160 + 40, hz - 10 + ph * 30 + 12],
                  fill=(255, 255, 255, int(200 * (1 - ph))))
    a0 = L[1][0] + 0.4
    if t > a0:
        k = ease(clamp((t - a0) / 0.5))
        dd = td()
        wtxt = spaced(dd, W / 2, 330, "«INSUMERGIBLE»", f(F_SER, 96), (255, 255, 255, int(255 * k)), 6)
        c = ease(clamp((t - a0 - 1.0) / 0.6))
        if c > 0:
            pts = [(W / 2 - wtxt / 2 + i * wtxt / 10, 380 + (14 if i % 2 else -14) * c) for i in range(11)]
            n = max(2, int(len(pts) * c))
            dd.line(pts[:n], fill=(230, 50, 60, 255), width=6)
    vignette(img, 150)


def hull_wall(img, x1):
    key_ = ("hull", x1)
    if key_ not in GRADS:
        im = Image.new("RGBA", (x1, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, x1, H], fill=(14, 14, 18))
        for y in range(80, H, 120):
            d.line([(0, y), (x1, y)], fill=(26, 26, 32), width=3)
            for x in range(20, x1, 40):
                d.ellipse([x - 3, y + 10 - 3, x + 3, y + 10 + 3], fill=(32, 32, 38))
        for y in (300, 620):
            for x in range(70, x1 - 40, 130):
                d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(40, 40, 46))
                d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=(255, 205, 130))
        d.rectangle([x1 - 160, 820, x1 - 20, 1060], fill=(255, 196, 120))
        GRADS[key_] = im
    AC(img, GRADS[key_])


def sh_gangway(img, t, T, L):
    AC(img, grad("dusk", (40, 34, 80), (240, 130, 90), 1.2))
    paste(img, spr("glow", 380, (255, 170, 110), 0.8), 820, 1000)
    sea(img, t, 1180, (50, 50, 90), (20, 20, 40), (120, 110, 160), 0.6)
    AC(img, grad("quay2", (50, 44, 54), (22, 20, 26), 1.0, 520), (0, 1400))
    hull_wall(img, 470)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon([(450, 1060), (470, 1040), (1080, 1420), (1080, 1460)], fill=(60, 50, 44))
    for k in range(14):
        x = 470 + k * 44
        y = 1040 + (x - 470) * 0.62
        d.line([(x, y), (x, y - 60)], fill=(80, 70, 60), width=4)
    d.line([(470, 980), (1080, 1360)], fill=(90, 80, 70), width=5)
    s0, s1 = L[1][0], L[1][1] + 0.3
    q = ease(clamp((t - s0) / max(0.5, s1 - s0)))
    ox = lerp(520, 900, q)
    oy = 1040 + (ox - 470) * 0.62 - 230
    paste(img, spr("officer", phase=round((t * 6) % 6.28, 1)), ox, oy, 0.95)
    lower_third(img, t, s0 + 0.2, "DAVID BLAIR", "SEGUNDO OFICIAL", 300, 3.4)
    a0 = L[2][0] + 0.8
    if t > a0:
        k = ease(clamp((t - a0) / 0.4))
        dark = Image.new("RGBA", (W, H), (0, 0, 0, int(150 * k)))
        AC(img, dark)
        paste(img, spr("glow", 300, (255, 220, 160), 0.6), ox, oy, 1.0, k)
        paste(img, spr("officer", phase=1.0), ox, oy, 0.95)
        flare(img, ox + 45, oy + 10, k * (0.7 + 0.3 * math.sin(t * 6)), 90)
        paste(img, spr("key"), ox + 45, oy + 10, 0.16, k)
    vignette(img, 170)


def sh_night_wide(img, t, T, L):
    night_sky(img, t, 1240, 1.1)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(160):
        rr = random.Random(i)
        x = rr.uniform(0, W)
        y = 200 + x * 0.55 + rr.gauss(0, 70)
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(200, 210, 255, 90))
    sea(img, t, 1240)
    shipn = spr("ship", True, True)
    s = 0.26
    sx = 340 + t * 12
    paste(img, shipn, sx, 1240 - (380 - 240) * s, s)
    particles(img, t, 80, 7, fall=30, alpha=120)
    lower_third(img, t, 0.3, "14 DE ABRIL DE 1912", "MAR EN CALMA · NOCHE SIN LUNA", 300, max(2.4, T - 1.2))
    vignette(img)


def breath(img, t, x, y, seed):
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(6):
        ph = ((t * 0.5 + k / 6 + seed * 0.3) % 1.0)
        r = 6 + ph * 26
        bx, by = x + 40 + ph * 70, y + 10 - ph * 30
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(220, 230, 255, int(45 * (1 - ph))))


def sh_nest_close(img, t, T, L):
    night_sky(img, t, 2000, 1.2)
    s = 1.35
    cx, cy = 540, 980 + 20 * math.sin(t * 0.5)
    paste(img, spr("crows_nest"), cx, cy, s)
    particles(img, t, 70, 9, fall=35, alpha=140)
    lower_third(img, t, 0.3, "FREDERICK FLEET · REGINALD LEE", "VIGÍAS", 300, 3.4)
    a0 = L[1][0]
    if t > a0:
        k = ease(clamp((t - a0) / 0.4))
        paste(img, spr("binoculars"), 820, 1170, 0.45, k * 0.9)
        d = ImageDraw.Draw(img, "RGBA")
        d.line([(730, 1100), (910, 1240)], fill=(235, 60, 70, int(255 * k)), width=10)
    vignette(img)


def sh_pov_iceberg(img, t, T, L):
    night_sky(img, t, 1100, 0.6)
    q = ease(clamp(t / T))
    paste(img, spr("iceberg"), 560, 1100 - 260 * (0.35 + 0.6 * q), 0.35 + 0.6 * q, 0.15 + 0.8 * q)
    sea(img, t, 1100)
    fog(img, t, 1070, 70, 18)
    lower_third(img, t, 0.2, "23:40", "", 300, max(1.5, T - 0.8))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, 90], fill=(0, 0, 0, 255))
    d.rectangle([0, H - 90, W, H], fill=(0, 0, 0, 255))
    vignette(img, 230)


BELL_TIMES = (0.25, 0.85, 1.45)


def sh_bell(img, t, T, L):
    AC(img, grad("bellbg", (10, 14, 30), (2, 3, 8), 1.0))
    rot = sum(math.exp(-(t - b) * 4) * math.sin((t - b) * 14) * 18 for b in BELL_TIMES if t >= b)
    paste(img, spr("glow", 340, (255, 200, 120), 0.5), 540, 900)
    paste(img, spr("bell"), 540, 900, 2.0, 1.0, rot)
    d = ImageDraw.Draw(img, "RGBA")
    for b in BELL_TIMES:
        if t >= b:
            ph = clamp((t - b) / 0.9)
            r = 260 + ph * 420
            d.ellipse([540 - r, 940 - r, 540 + r, 940 + r], outline=(255, 230, 170, int(200 * (1 - ph))), width=8)
    a0 = L[0][0] + 1.9
    if t > a0:
        k = ease(clamp((t - a0) / 0.3))
        d = td()
        spaced(d, W / 2, 260, "¡ICEBERG", f(F_SER, 96), (255, 255, 255, int(255 * k)), 6)
        spaced(d, W / 2, 370, "JUSTO DELANTE!", f(F_SER, 96), YEL + (int(255 * k),), 6)
    vignette(img, 200)


def sh_impact(img, t, T, L):
    hit = max(0.6, L[0][1] - 0.5)
    sxk = 0
    if t > hit:
        sxk = math.exp(-(t - hit) * 5) * 18
    night_sky(img, t, 1080, 0.8)
    shipn = spr("ship", True, True)
    s = 0.95
    sx = lerp(220, 380, ease(clamp(t / hit))) + (math.sin(t * 60) * sxk)
    sy = 1080 - (380 - 240) * s + math.cos(t * 50) * sxk * 0.5
    paste(img, spr("iceberg"), 900, 1080 - 220, 0.9)
    paste(img, shipn, sx, sy, s)
    sea(img, t, 1080)
    d = ImageDraw.Draw(img, "RGBA")
    if t > hit:
        u = t - hit
        rr = random.Random(5)
        for _ in range(26):
            vx, vy = rr.uniform(-260, 80), rr.uniform(-520, -180)
            x = 790 + vx * u
            y = 900 + vy * u + 700 * u * u
            r = rr.uniform(6, 16)
            if y < 1100:
                d.polygon([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], fill=(220, 236, 250, 230))
        fl = math.exp(-u * 6)
        AC(img, Image.new("RGBA", (W, H), (255, 255, 255, int(200 * fl))))
    vignette(img, 200)


def sh_sinking(img, t, T, L):
    night_sky(img, t, 1080, 0.8)
    q = ease(clamp(t / (T - 0.6)))
    lit = t < T * 0.55 or (T * 0.55 <= t < T * 0.6 and int(t * 20) % 2)
    shipn = spr("ship", True, bool(lit))
    s = 0.95
    ang = -14 * q
    sx = 520
    sy = 1080 - (380 - 240) * s + 160 * q
    paste(img, shipn, sx, sy, s, 1.0, ang)
    sea(img, t, 1080)
    fog(img, t, 1100, 50, 10)
    particles(img, t, 60, 12, fall=25, alpha=110)
    lower_third(img, t, 0.4, "2 HORAS Y 40 MINUTOS", "DEL CHOQUE AL HUNDIMIENTO", 300, max(2.0, L[0][1] - 0.6))
    a0 = L[1][0]
    if t > a0:
        k = ease(clamp((t - a0) / 0.8))
        d = td()
        spaced(d, W / 2, 330, "MÁS DE 1.500", f(F_SER, 104), (255, 255, 255, int(255 * k)), 6)
        spaced(d, W / 2, 450, "VIDAS", f(F_SER, 60), (210, 214, 225, int(255 * k)), 14)
    vignette(img, 220)


def spotlight(img, t, cx=540, top=0, bottom=1300, w0=120, w1=560, alpha=70):
    key_ = ("spot", cx, top, bottom, w0, w1)
    if key_ not in GRADS:
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.polygon([(cx - w0, top), (cx + w0, top), (cx + w1, bottom), (cx - w1, bottom)], fill=(255, 236, 200, alpha))
        GRADS[key_] = im.filter(ImageFilter.GaussianBlur(30))
    AC(img, GRADS[key_])
    particles(img, t, 50, 21, (255, 240, 210), 12, (1, 2.5), 120)


def sh_key_spot(img, t, T, L):
    AC(img, grad("blk", (8, 8, 12), (2, 2, 4), 1.0))
    spotlight(img, t)
    k = ease(clamp(t / 0.6))
    rot = 12 * math.sin(t * 0.9)
    flare(img, 540 + 120 * math.sin(t * 1.4), 760, 0.4 * k, 200)
    paste(img, spr("key"), 540, 780, 1.2 + 0.03 * math.sin(t * 2), k, rot)
    vignette(img, 220)


BOX_STATES = 10


def sh_box_open(img, t, T, L):
    AC(img, grad("blk", (8, 8, 12), (2, 2, 4), 1.0))
    spotlight(img, t, 540, 0, 1300, 160, 620, 60)
    q = ease(clamp((t - 0.6) / 1.6))
    st = round(q * (BOX_STATES - 1)) / (BOX_STATES - 1)
    if q > 0.3:
        k = ease(clamp((q - 0.3) / 0.7))
        paste(img, spr("glow", 300, (255, 220, 150), 0.7), 540, 900, 1.0, k)
        paste(img, spr("binoculars"), 540, 940 - 150 * k, 0.9, k)
    paste(img, spr("box", lid=round(st, 2)), 540, 1060, 1.1)
    paste(img, spr("key"), 540 + 240, 1280, 0.35, 1.0, -20)
    lower_third(img, t, L[0][0] + 1.6, "LA CAJA DE LOS PRISMÁTICOS", "DE LOS VIGÍAS", 300, 3.4)
    vignette(img, 200)


def sh_fleet_quote(img, t, T, L):
    night_sky(img, t, 2000, 0.9)
    paste(img, spr("crows_nest"), 250, 1180, 0.9, 0.55)
    d = td()
    k = ease(clamp((t - 0.3) / 0.6))
    A = int(255 * k)
    d.text((70, 250), "«", font=f(F_SER, 150), fill=YEL + (A,))
    spaced(d, W / 2 + 40, 420, "PODRÍAMOS HABERLO", f(F_SER, 66), (255, 255, 255, A), 4)
    spaced(d, W / 2 + 40, 500, "VISTO ANTES»", f(F_SER, 66), (255, 255, 255, A), 4)
    spaced(d, W / 2 + 40, 600, "— FREDERICK FLEET, 1912", f(F_SERR, 34), (210, 214, 225, A), 5)
    a1 = L[1][0]
    if t > a1:
        q = ease(clamp((t - a1) / 0.6))
        spaced(d, W / 2 + 40, 760, "¿HABRÍA CAMBIADO ALGO?", f(F_SER, 50), (230, 120, 120, int(255 * q)), 4)
    particles(img, t, 60, 14, fall=30, alpha=120)
    vignette(img, 200)


def sh_auction(img, t, T, L):
    AC(img, grad("auc", (40, 24, 18), (10, 6, 4), 1.0))
    spotlight(img, t, 540, 0, 1300, 140, 560, 55)
    paste(img, spr("cushion"), 540, 1060, 1.1)
    paste(img, spr("key"), 540, 990, 0.8)
    hit = max(0.8, L[0][1] - 0.4)
    if t < hit - 0.4:
        ang = 0.5
    elif t < hit:
        ang = lerp(0.5, -0.15, ease((t - (hit - 0.4)) / 0.4))
    else:
        ang = -0.15 + 0.15 * ease(clamp((t - hit) / 0.5))
    paste(img, spr("gavel", ang=round(ang, 2)), 860, 760, 1.0)
    d = td()
    lower_third(img, t, 0.3, "SUBASTA · 2007", "", 300, max(2.0, hit - 0.2))
    if t > hit:
        k = ease(clamp((t - hit) / 0.4))
        AC(img, Image.new("RGBA", (W, H), (255, 240, 200, int(120 * math.exp(-(t - hit) * 6)))))
        v = int(90000 * ease(clamp((t - hit) / 1.0)))
        spaced(d, W / 2, 360, f"{v:,}".replace(",", ".") + " £", f(F_SER, 120), YEL + (int(255 * k),), 6)
    end = T - 2.6
    if t > end:
        k = ease(clamp((t - end) / 0.8))
        d2 = td()
        d2.rectangle([0, 0, W, H], fill=(0, 0, 0, int(200 * k)))
        R.eye_icon(d2, 540, 820, 300 * (0.9 + 0.1 * k), (255, 255, 255), YEL, (14, 15, 18))
        spaced(d2, W / 2, 1010, "SI AÚN NO LO SABÍAS…", f(F_SER, 52), (255, 255, 255, int(255 * k)), 6)
        spaced(d2, W / 2, 1090, "@nolosabias_datos", f(F_SERR, 40), (220, 220, 230, int(255 * k)), 3)
    vignette(img, 200)


SHOT_FN = {k[0]: globals()["sh_" + k[0]] for k in SHOTS}
FOCUS = {"night_open": (540, 980), "port_wide": (720, 880), "ship_depart": (520, 760), "gangway": (760, 860),
         "night_wide": (420, 1180), "nest_close": (540, 760), "pov_iceberg": (560, 900), "impact": (760, 900),
         "sinking": (520, 1000), "box_open": (540, 1000), "auction": (640, 960), "fleet_quote": (300, 1150)}
ZOOM = 1.28


def cut_points(s):
    pts = []
    for a, b in s["lines"]:
        pts.append(a)
        if b - a > 3.4:
            pts.append((a + b) / 2)
    return sorted(pts)


def framing(s, tl):
    if s["name"] not in FOCUS:
        return 0
    k = sum(1 for c in cut_points(s) if c <= tl) - 1
    return max(0, k) % 2


GLIDE = 0.75


def zoom_at(s, tl):
    """Factor de encuadre continuo: se desliza suavemente entre plano general y plano cercano."""
    if s["name"] not in FOCUS:
        return 0.0
    cps = cut_points(s)
    k = sum(1 for c in cps if c <= tl) - 1
    if k < 0:
        return 0.0
    tgt = lambda i: float(max(0, i) % 2)
    cur, prev = tgt(k), tgt(k - 1) if k > 0 else 0.0
    p = clamp((tl - cps[k]) / GLIDE)
    p = p * p * (3 - 2 * p)
    return lerp(prev, cur, p)


def reframe(img, s, tl):
    q = zoom_at(s, tl)
    if q < 0.002:
        return img
    z = lerp(1.0, ZOOM, q)
    fx, fy = FOCUS[s["name"]]
    cx, cy = lerp(W / 2, fx, q), lerp(H / 2, fy, q)
    cw, ch = W / z, H / z
    x0 = min(max(0, cx - cw / 2), W - cw)
    y0 = min(max(0, cy - ch / 2), H - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BICUBIC)


# ------------------------------------------------------------------ subtítulos
def caption(img, chunk, t_in):
    d = ImageDraw.Draw(img)
    a = ease(clamp(t_in / 0.15))
    size = 80
    fnt = f(F_CAP, size)
    lines = wrap(d, chunk, fnt, 920)
    lh = int(size * 1.2)
    y = 1520 - len(lines) * lh / 2 + (1 - a) * 18
    for ln in lines:
        widths = [d.textlength(w, font=fnt) for w, _ in ln]
        sp = d.textlength(" ", font=fnt)
        x = (W - (sum(widths) + sp * (len(ln) - 1))) / 2
        for (wd, hl), wdt in zip(ln, widths):
            col = YEL if hl else (255, 255, 255)
            d.text((x + 3, y + 5), wd, font=fnt, fill=(0, 0, 0))
            d.text((x, y), wd, font=fnt, fill=col, stroke_width=6, stroke_fill=(10, 10, 14))
            x += wdt + sp
        y += lh


# ------------------------------------------------------------------ audio
def build_audio(shots, total, path):
    rng = np.random.default_rng(3)
    n = int((total + 1) * M.SR)
    sr = M.SR
    doc, _ = M.track("doc", total + 1, rng)
    mys, _ = M.track("mystery", total + 1, rng)
    doc, mys = doc[:n], mys[:n]
    tt = np.arange(n) / sr
    by = {s["name"]: s for s in shots}
    t_ten0, t_ten1 = by["night_wide"]["start"], by["sinking"]["start"]
    w_m = np.clip((tt - t_ten0) / 2.0, 0, 1) * np.clip((t_ten1 + 3 - tt) / 2.0, 0, 1)
    music = doc * (1 - w_m) * 0.9 + mys * w_m * 1.1
    music = music / (np.max(np.abs(music)) + 1e-9) * 0.5
    # silencio respetuoso tras el hundimiento y antes de la revelación
    duck = np.ones(n)
    for a, b in ((by["sinking"]["start"] + by["sinking"]["lines"][1][0] - 0.2, by["key_spot"]["start"] + 0.6),):
        ia, ib = int(a * sr), int(b * sr)
        duck[ia:ib] = 0.25
    music *= duck
    # ambiente de mar en planos nocturnos y de mar
    noise = M.lp(rng.standard_normal(n), 420) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * tt))
    sea_mask = np.zeros(n)
    for nm in ("night_open", "port_wide", "ship_depart", "night_wide", "nest_close", "pov_iceberg", "impact", "sinking", "fleet_quote"):
        s = by[nm]
        sea_mask[int(s["start"] * sr):int(s["end"] * sr)] = 1
    sea_mask = np.convolve(sea_mask, np.ones(int(0.5 * sr)) / (0.5 * sr), mode="same")
    amb = noise / (np.max(np.abs(noise)) + 1e-9) * 0.22 * sea_mask
    fx = np.zeros(n)

    def add(sig, t0, g):
        M.add(fx, sig, t0, g)

    # transiciones
    for s in shots[1:]:
        add(M.fx_whoosh(rng, 0.6, False), s["start"] - 0.15, 0.12)
    # bocina del barco al zarpar
    tt2 = np.arange(int(2.6 * sr)) / sr
    horn = sum(np.sign(np.sin(2 * np.pi * fq * tt2)) * g for fq, g in ((82, 0.6), (123, 0.4)))
    horn = M.lp(horn, 600) * np.minimum(1, tt2 / 0.15) * np.minimum(1, (2.6 - tt2) / 0.4)
    add(horn, by["ship_depart"]["start"] + 0.3, 0.25)
    # brillo de la llave
    for nm, off in (("night_open", by["night_open"]["lines"][1][0]), ("gangway", by["gangway"]["lines"][2][0] + 0.8),
                    ("key_spot", 0.2), ("auction", 0.3)):
        for j, fq in enumerate((2093, 2637, 3136)):
            add(M.fx_ding(fq), by[nm]["start"] + off + j * 0.07, 0.05)
    # latidos ante el iceberg
    for k in range(6):
        add(M.fx_heart(), by["pov_iceberg"]["start"] + k * 0.75, 0.45)
    # campana x3
    for b in BELL_TIMES:
        tb = np.arange(int(1.6 * sr)) / sr
        sig = sum(np.sin(2 * np.pi * fq * tb) * np.exp(-tb * dk) * g for fq, dk, g in
                  ((880, 2.5, 1.0), (1320 * 1.007, 3.5, 0.5), (2210, 5, 0.3), (3070, 7, 0.2)))
        add(sig, by["bell"]["start"] + b, 0.32)
    # choque
    imp = by["impact"]
    hit = imp["start"] + max(0.6, imp["lines"][0][1] - 0.5)
    add(M.fx_riser(rng, 1.2), hit, 0.18)
    add(M.fx_impact(rng), hit, 0.55)
    tr = np.arange(int(3 * sr)) / sr
    add(M.lp(rng.standard_normal(len(tr)), 150) * np.exp(-tr * 1.2), hit + 0.1, 0.5)
    # revelación
    add(M.fx_riser(rng, 1.4), by["key_spot"]["start"], 0.16)
    add(M.fx_swell(rng, 1.6), by["box_open"]["start"] + 1.9, 0.2)
    # martillo de subasta
    auc = by["auction"]
    gh = auc["start"] + max(0.8, auc["lines"][0][1] - 0.4)
    tg = np.arange(int(0.25 * sr)) / sr
    knock = (M.lp(rng.standard_normal(len(tg)), 1800) * 0.7 + np.sin(2 * np.pi * 140 * tg)) * np.exp(-tg * 30)
    add(knock, gh, 0.6)
    add(M.fx_ding(1568), gh + 0.05, 0.1)
    # golpe suave en cada cambio de encuadre
    for s in shots:
        if s["name"] in FOCUS:
            for c in cut_points(s)[1:]:
                add(M.fx_whoosh(rng, 0.7, True), s["start"] + c - 0.1, 0.04)
    # base rítmica suave (se apaga en el hundimiento y vuelve en la subasta)
    beat = 60 / 96
    bed = np.zeros(n)
    for a, b in ((2.0, by["sinking"]["start"]), (by["auction"]["start"], total - 2.5)):
        tb = a
        k = 0
        while tb < b:
            M.add(bed, M.kick(0.3, 110, 46, 12), tb, 0.5)
            M.add(bed, M.hat(rng, 0.04), tb + beat / 2, 0.08)
            if k % 2 == 1:
                M.add(bed, M.lp(M.snare(rng, 0.15), 2500), tb, 0.12)
            tb += beat
            k += 1
    mix = music + amb + fx + bed * 0.6
    mix = mix[: int(total * sr)]
    fade = int(1.5 * sr)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix /= np.max(np.abs(mix)) + 1e-9
    st = np.stack([mix, np.roll(mix, 160)], axis=1) * 0.88
    from scipy.io import wavfile
    wavfile.write(path, sr, (st * 32767).astype(np.int16))


# ------------------------------------------------------------------ render
def render(out_mp4, only_times=None):
    shots, caps, total = timeline()
    chunks = []
    for c in caps:
        chunks += chunks_for(c["text"], c["start"], c["end"], n=3)
    wav = out_mp4.replace(".mp4", ".wav") if out_mp4 else None
    pipe = None
    if not only_times:
        build_audio(shots, total, wav)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
               "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", out_mp4]
        pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = [int(x * FPS) for x in only_times] if only_times else range(int(total * FPS))
    shots_out = []
    notif_t = shots[4]["start"] + 1.2
    XF = 0.55
    for i in frames:
        t = i / FPS
        si = next((k for k, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
        s = shots[si]
        img = Image.new("RGB", (W, H), (0, 0, 0))
        TOP[0] = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        top = TOP[0]
        SHOT_FN[s["name"]](img, t - s["start"], s["end"] - s["start"], s["lines"])
        img = reframe(img, s, t - s["start"])
        if si > 0 and t - s["start"] < XF and s["name"] not in HARD_CUT:
            p = shots[si - 1]
            pim = Image.new("RGB", (W, H), (0, 0, 0))
            TOP[0] = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            SHOT_FN[p["name"]](pim, t - p["start"], p["end"] - p["start"], p["lines"])
            pim = reframe(pim, p, t - p["start"])
            img = Image.blend(pim, img, ease((t - s["start"]) / XF))
        AC(img, top)
        bottom_shade(img)
        out = img.convert("RGB")
        for cs, ce, g in chunks:
            if cs <= t < ce:
                caption(out, V2.glue(g), t - cs)
        d = ImageDraw.Draw(out)
        if s["name"] != "auction" or t - s["start"] < s["end"] - s["start"] - 2.6:
            R.eye_icon(d, 92, 112, 58, (255, 255, 255), YEL, (14, 15, 18))
            d.text((132, 95), "@nolosabias_datos", font=f(F_CAP, 28), fill=(235, 235, 240))
        out = V2.notif_banner(out, t - notif_t, "nolosabias_datos", "Suscríbete para más historias que no sabías")
        if pipe is None:
            shots_out.append(out)
            continue
        pipe.stdin.write(out.tobytes())
    if pipe is None:
        return shots_out
    pipe.stdin.close()
    if pipe.wait() != 0:
        raise RuntimeError("ffmpeg falló")
    # subtítulos .srt para la voz
    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(out_mp4.replace(".mp4", ".srt"), "w") as fh:
        for k, c in enumerate(caps, 1):
            fh.write(f"{k}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text'].replace('*', '')}\n\n")
    return out_mp4


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/shorts-ingenieria/output/titanic_pro.mp4"
    render(out)
    print(json.dumps({"total": timeline()[2]}))
