"""Cybertruck · estilo «documental oscuro minimalista» (elegido por Iker el 21/10)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from c01_cyber import *          # noqa: F401,F403
import vid2, dark as DK
from docu import font, caps_font
from render import W, H, ease, clamp, lerp

TITLE = "Cybertruck_oscuro"
FRAME = vid2.frame
BG = (6, 7, 10)
TRANS_POOL = ["zoom_in", "whip", "iris", "glitch", "spin", "push", "whip_r"]
TRANS_SEED = 7
FOCUS_PT = {"hook": (470, 1000), "press": (540, 1010), "musk": (540, 900), "score": (540, 960), "fold": (540, 1000),
            "stage": (540, 1150), "ball": (560, 980), "orders": (540, 900)}
CAM_PUSH = 0.06
SHAKE = 10
AUDIO = {"music": [("hook", "tension")], "gains": {"tension": 0.9}, "amb": {}, "bed": [], "bpm": 96,
         "sfx": [("press+0.85", "impact", 0.12), ("ball+0.75", "glass", 0.12), ("ball+1.55", "glass", 0.10), ("orders+0.2", "riser", 0.06)]}
SERIF = DK.SERIF
INTER = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
_C = {}


def _bg(beam_x=560, fog_y=1180, key="a"):
    k = ("bg", beam_x, fog_y)
    if k not in _C:
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        base = np.full((H, W, 3), BG, np.float32)
        beam = np.clip(1 - np.abs((xs - beam_x) - (ys - 300) * 0.16) / (170 + ys * 0.26), 0, 1) * np.clip((ys - 140) / 850, 0, 1) * (ys < fog_y + 60)
        base += beam[..., None] * np.array((120, 128, 140), np.float32) * 0.5
        base += np.clip(1 - np.abs(ys - fog_y) / 230, 0, 1)[..., None] * np.array((26, 30, 36), np.float32)
        base += np.random.default_rng(2).normal(0, 2.4, (H, W, 1))
        im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        d.rectangle([0, fog_y + 20, W, H], fill=(5, 6, 8))
        d.line([(0, fog_y + 20), (W, fog_y + 20)], fill=(40, 44, 52), width=2)
        _C[k] = im
    return _C[k]


def _truck(s=1.0, ox=40, oy=880):
    k = ("truck", s, ox, oy)
    if k not in _C:
        _C[k] = DK._car_layer(DK.CYBER, s, ox, oy)
    return _C[k]


def _glow_line(img, pts, col, w, k=1.0, blur=10):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).line(pts, fill=col + (int(255 * k),), width=w, joint="curve")
    g = lay.filter(ImageFilter.GaussianBlur(blur))
    img.paste(g, (0, 0), g)
    img.paste(lay, (0, 0), lay)


def _text(img, xy, txt, fo, col=(235, 235, 235), k=1.0, anchor="mm"):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text(xy, txt, font=fo, fill=col + (int(255 * k),), anchor=anchor)
    img.paste(lay, (0, 0), lay)


def _pill(img, cx, cy, txt, k=1.0):
    if k <= 0:
        return
    fo = font(INTER_B, 24)
    d0 = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    tw = d0.textlength(txt, font=fo) + 7 * len(txt)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([cx - tw / 2 - 26, cy - 26, cx + tw / 2 + 26, cy + 26], radius=26, outline=(200, 205, 215, int(200 * k)), width=2)
    x = cx - tw / 2
    for ch in txt:
        d.text((x, cy), ch, font=fo, fill=(220, 224, 232, int(255 * k)), anchor="lm")
        x += d0.textlength(ch, font=fo) + 7
    img.paste(lay, (0, 0), lay)


# ------------------------------------------------------------------ escenas
def sh_hook(img, t, T, L):
    img.paste(_bg())
    lay, m, glow, (fpt, rpt) = _truck()
    img.paste(lay, (0, 0), lay)
    k = ease(clamp((t - 0.4) / 0.4))
    if k > 0:
        g = glow.filter(ImageFilter.GaussianBlur(12))
        a = g.getchannel("A").point(lambda v: int(v * k))
        g.putalpha(a)
        img.paste(g, (0, 0), g)
        img.paste(g, (0, 0), g)
    # la «regla»: una línea de luz recorre el techo
    u = ease(clamp((t - 1.2) / 1.1))
    if u > 0:
        P = [(40 + x, 880 + y) for x, y in ((2, 176), (440, 44), (998, 134))]
        L1 = math.dist(P[0], P[1])
        L2 = math.dist(P[1], P[2])
        dist = u * (L1 + L2)
        if dist <= L1:
            pts = [P[0], (P[0][0] + (P[1][0] - P[0][0]) * dist / L1, P[0][1] + (P[1][1] - P[0][1]) * dist / L1)]
        else:
            f = (dist - L1) / L2
            pts = [P[0], P[1], (P[1][0] + (P[2][0] - P[1][0]) * f, P[1][1] + (P[2][1] - P[1][1]) * f)]
        _glow_line(img, [(x, y - 26) for x, y in pts], (255, 255, 255), 3, 1.0, 8)
        for x, y in pts[-1:]:
            DKglow(img, x, y - 26)
    _pill(img, 540, 1360, "TESLA CYBERTRUCK", ease(clamp((t - 0.7) / 0.5)))


def DKglow(img, x, y, r=40, col=(255, 255, 255)):
    lay = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([r - 6, r - 6, r + 6, r + 6], fill=col + (255,))
    lay = lay.filter(ImageFilter.GaussianBlur(10))
    img.paste(lay, (int(x - r), int(y - r)), lay)


def sh_press(img, t, T, L):
    img.paste(_bg(540, 1240))
    d = ImageDraw.Draw(img, "RGBA")
    hit = 0.85
    y = lerp(500, 880, ease(clamp(t / hit)) ** 2) if t < hit else 880
    # columnas y cabezal de la prensa
    for x in (170, 870):
        d.rectangle([x, 300, x + 40, 1250], fill=(16, 17, 20))
        d.line([(x, 300), (x, 1250)], fill=(70, 74, 82), width=2)
    d.rectangle([150, y - 220, 930, y], fill=(14, 15, 18))
    d.line([(150, y - 220), (930, y - 220)], fill=(120, 126, 136), width=3)
    d.line([(150, y), (930, y)], fill=(90, 94, 104), width=2)
    # chapa de acero sobre la base
    d.rectangle([200, 1080, 880, 1100], fill=(60, 64, 72))
    d.line([(200, 1080), (880, 1080)], fill=(220, 226, 236), width=2)
    d.rectangle([150, 1100, 930, 1250], fill=(12, 13, 16))
    if t >= hit:
        u = t - hit
        # el cabezal se agrieta
        rng = random.Random(3)
        for k in range(9):
            x0 = 300 + k * 60 + rng.uniform(-20, 20)
            pts = [(x0, y)]
            for j in range(5):
                pts.append((pts[-1][0] + rng.uniform(-30, 30), pts[-1][1] - 40))
            grow = clamp(u / 0.35)
            n = 1 + int(grow * 5)
            _glow_line(img, pts[:n + 1], (255, 255, 255), 3, 1.0, 6)
        # chispas
        for j in range(30):
            a = rng.uniform(math.pi * 1.05, math.pi * 1.95)
            sp = rng.uniform(300, 900)
            px = 540 + math.cos(a) * sp * u * 1.2 + rng.uniform(-200, 200)
            py = 1080 + math.sin(a) * sp * u + 900 * u * u
            al = int(255 * clamp(1 - u / 0.9))
            if al > 0:
                d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 220, 160, al))
        if u < 0.12:
            d.rectangle([0, 0, W, H], fill=(255, 255, 255, int(120 * (1 - u / 0.12))))
    _pill(img, 540, 1380, "ACERO ULTRADURO «30X»", ease(clamp((t - 1.3) / 0.4)))


def sh_musk(img, t, T, L):
    img.paste(_bg(540, 1300))
    fo = font(SERIF, 96, "Italic")
    words = ["«No", "se", "puede", "estampar.»"]
    d0 = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    lines = [["«No", "se", "puede"], ["estampar.»"]]
    y = 820
    idx = 0
    for ln in lines:
        tw = sum(d0.textlength(w, font=fo) for w in ln) + 26 * (len(ln) - 1)
        x = W / 2 - tw / 2
        for w in ln:
            k = ease(clamp((t - 0.3 - idx * 0.22) / 0.35))
            _text(img, (x, y + 20 * (1 - k)), w, fo, (240, 240, 240), k, "lm")
            x += d0.textlength(w, font=fo) + 26
            idx += 1
        y += 130
    k = ease(clamp((t - 1.4) / 0.5))
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(390, 1110), (390 + 300 * k, 1110)], fill=(200, 205, 215, 200), width=2)
    _text(img, (540, 1160), "ELON MUSK · 24 NOV 2019", font(INTER, 26), (160, 166, 178), k)


def sh_score(img, t, T, L):
    img.paste(_bg(540, 1240))
    cx, y0 = 540, 1000
    u = ease(clamp((t - 0.2) / 0.8))         # marca con láser
    f = ease(clamp((t - 1.2) / 0.9))         # se dobla
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([160, y0, cx, y0 + 26], fill=(70, 74, 84))
    d.line([(160, y0), (cx, y0)], fill=(220, 226, 236), width=2)
    ang = -72 * f
    L_ = 380
    a = math.radians(ang)
    p1 = (cx + math.cos(a) * L_, y0 + math.sin(a) * L_)
    p2 = (p1[0] - math.sin(a) * -26, p1[1] + math.cos(a) * 26)
    d.polygon([(cx, y0), p1, p2, (cx, y0 + 26)], fill=(70, 74, 84))
    d.line([(cx, y0), p1], fill=(220, 226, 236), width=2)
    if u > 0 and f < 0.98:
        _glow_line(img, [(cx, y0 + 26), (cx, y0 + 26 - 18 * u)], (255, 90, 70), 6, 1 - f, 10)
        DKglow(img, cx, y0 + 18, 50, (255, 90, 70))
    _pill(img, 540, 1360, "MARCA PROFUNDA POR DENTRO", ease(clamp((t - 0.5) / 0.4)))


def _lerp_poly(A, B, u):
    n = max(len(A), len(B))

    def res(P):
        out = []
        for k in range(n):
            f = k * (len(P) - 1) / (n - 1)
            i = int(f)
            j = min(i + 1, len(P) - 1)
            w = f - i
            out.append((P[i][0] * (1 - w) + P[j][0] * w, P[i][1] * (1 - w) + P[j][1] * w))
        return out
    a, b = res(A), res(B)
    return [(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u) for (x0, y0), (x1, y1) in zip(a, b)]


def sh_fold(img, t, T, L):
    img.paste(_bg())
    ox, oy = 40, 880
    body = [(ox + x, oy + y) for x, y in DK.CYBER["body"]]
    flat = [(ox + 20 + k * 960 / (len(body) - 1), oy + 230 + (k % 2) * 8) for k in range(len(body))]
    flat = sorted(flat, key=lambda p: p[0])
    sheet = flat + [(p[0], p[1] + 14) for p in reversed(flat)]
    u = ease(clamp((t - 0.2) / 1.4))
    poly = _lerp_poly(sheet, body + [body[0]], u)
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon(poly, fill=(12, 13, 16))
    _glow_line(img, poly + [poly[0]], (220, 228, 240), 2, 0.9, 5)
    if u > 0.98:
        lay, m, glow, _ = _truck()
        k = ease(clamp((t - 1.6) / 0.4))
        l2 = lay.copy()
        l2.putalpha(l2.getchannel("A").point(lambda v: int(v * k)))
        img.paste(l2, (0, 0), l2)
    _pill(img, 540, 1360, "SOLO PLANOS Y ARISTAS", ease(clamp((t - 1.0) / 0.4)))


def sh_stage(img, t, T, L):
    img.paste(_bg(540, 1260))
    d = ImageDraw.Draw(img, "RGBA")
    # focos
    for k, x in enumerate((260, 540, 820)):
        a = ease(clamp((t - 0.1 - k * 0.15) / 0.3))
        cone = Image.new("L", (W, H), 0)
        ImageDraw.Draw(cone).polygon([(x - 20, 180), (x + 20, 180), (x + 220, 1240), (x - 220, 1240)], fill=int(55 * a))
        img.paste((230, 236, 255), (0, 0), cone.filter(ImageFilter.GaussianBlur(30)))
    lay, m, glow, _ = _truck(0.72, 180, 1000)
    img.paste(lay, (0, 0), lay)
    g = glow.filter(ImageFilter.GaussianBlur(10))
    img.paste(g, (0, 0), g)
    # público
    rng = random.Random(5)
    for k in range(26):
        x = 20 + k * 41 + rng.uniform(-6, 6)
        y = 1300 + rng.uniform(-10, 10) + (k % 2) * 30
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=(3, 3, 5))
        d.rectangle([x - 34, y + 18, x + 34, y + 120], fill=(3, 3, 5))
    _text(img, (540, 420), "2019", font(SERIF, 150, "Italic"), (235, 235, 235), ease(clamp((t - 0.4) / 0.5)))
    _text(img, (540, 520), "LOS ÁNGELES · PRESENTACIÓN", font(INTER, 26), (160, 166, 178), ease(clamp((t - 0.7) / 0.5)))


def _crack(img, cx, cy, k, seed=1, R=260):
    rng = random.Random(seed)
    for j in range(14):
        a = j * 2 * math.pi / 14 + rng.uniform(-0.2, 0.2)
        pts = [(cx, cy)]
        r = 0
        while r < R * k:
            r += rng.uniform(25, 50)
            aa = a + rng.uniform(-0.25, 0.25)
            pts.append((cx + math.cos(aa) * r, cy + math.sin(aa) * r))
        _glow_line(img, pts, (235, 240, 255), 2, 1.0, 4)
    for rr in (40, 90):
        if k > rr / R:
            ImageDraw.Draw(img, "RGBA").ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(230, 236, 255, 160), width=2)


def sh_ball(img, t, T, L):
    img.paste(_bg(600, 1300))
    d = ImageDraw.Draw(img, "RGBA")
    # dos ventanillas en primer plano
    for k, (x0, x1) in enumerate(((180, 520), (560, 900))):
        d.polygon([(x0, 820), (x1, 760 if k == 0 else 800), (x1, 1160), (x0, 1160)], fill=(18, 22, 30))
        d.line([(x0, 820), (x1, 760 if k == 0 else 800)], fill=(150, 160, 180), width=2)
        d.line([(x0 + 40, 1100), (x0 + 140, 860)], fill=(255, 255, 255, 30), width=14)
    hit1, hit2 = 0.75, 1.55
    for hit, cx, seed in ((hit1, 360, 2), (hit2, 740, 5)):
        if t < hit:
            if t > hit - 0.6:
                u = (t - (hit - 0.6)) / 0.6
                bx = lerp(-80, cx, ease(u))
                by = lerp(900, 980, u)
                for j in range(6):
                    tx = bx - j * 26
                    d.ellipse([tx - 26, by - 26, tx + 26, by + 26], fill=(200, 204, 214, int(160 / (j + 1))))
                d.ellipse([bx - 28, by - 28, bx + 28, by + 28], fill=(190, 194, 204))
                d.ellipse([bx - 16, by - 18, bx - 2, by - 4], fill=(255, 255, 255))
        else:
            _crack(img, cx, 980, ease(clamp((t - hit) / 0.25)), seed, 220)
            if t - hit < 0.1:
                d.rectangle([0, 0, W, H], fill=(255, 255, 255, int(110 * (1 - (t - hit) / 0.1))))
    if t > hit2 + 0.1:
        _text(img, (540, 520), "Dos.", font(SERIF, 130, "Italic"), (240, 240, 240), ease(clamp((t - hit2 - 0.1) / 0.4)))


def sh_orders(img, t, T, L):
    img.paste(_bg(540, 1300))
    u = ease(clamp((t - 0.2) / 1.5))
    n = int(round(250000 * u / 1000) * 1000) if u < 1 else 250000
    txt = f"{n:,}".replace(",", ".")
    _text(img, (540, 900), txt, font(SERIF, 170, "Italic"), (245, 245, 245))
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(240, 1010), (240 + 600 * u, 1010)], fill=(220, 226, 236, 220), width=2)
    _text(img, (540, 1070), "RESERVAS EN POCOS DÍAS", font(INTER, 28), (165, 170, 182), ease(clamp((t - 0.8) / 0.5)))
    _text(img, (540, 1120), "con una señal de 100 $", font(SERIF, 34, "Italic"), (130, 136, 148), ease(clamp((t - 1.1) / 0.5)))


FNS = {"hook": sh_hook, "press": sh_press, "musk": sh_musk, "score": sh_score, "fold": sh_fold, "stage": sh_stage, "ball": sh_ball,
       "orders": sh_orders}


# ------------------------------------------------------------------ subtítulos y cierre
def CAPTION(img, t, chunks, y=1490):
    cur = next((c for c in chunks if c[0] - 0.02 <= t < c[1]), None)
    if not cur:
        return
    t0, t1, words = cur
    fo = font(INTER_B, 60)
    d0 = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    ws = [w for w, _, _, _ in words]
    sp = d0.textlength(" ", font=fo)
    tw = sum(d0.textlength(w, font=fo) for w in ws) + sp * (len(ws) - 1)
    if tw > 960:
        fo = font(INTER_B, 48)
        sp = d0.textlength(" ", font=fo)
        tw = sum(d0.textlength(w, font=fo) for w in ws) + sp * (len(ws) - 1)
    k = ease(clamp((t - t0) / 0.14)) * (1 - clamp((t - (t1 - 0.06)) / 0.06))
    lay = Image.new("RGBA", (W, 160), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = W / 2 - tw / 2
    for w, hl, a, b in words:
        on = t >= a - 0.03
        col = (255, 255, 255) if on else (120, 124, 134)
        if hl and on:
            col = (255, 236, 200)
        d.text((x, 80), w, font=fo, fill=col + (int(255 * k),), anchor="lm")
        x += d0.textlength(w, font=fo) + sp
    img.paste(lay, (0, int(y - 80 + (1 - k) * 12)), lay)


def OUTRO_FN(img, u, D):
    out = Image.new("RGB", (W, H), BG)
    out.paste(_bg(540, 1400))
    k1 = ease(clamp(u / 0.6))
    _text(out, (540, 820), "Si no lo sabías…", font(SERIF, 64, "Italic"), (200, 200, 205), k1)
    k2 = ease(clamp((u - 0.8) / 0.6))
    _text(out, (540, 930), "ahora ya lo sabes.", font(SERIF, 92, "Italic"), (250, 250, 250), k2)
    k3 = ease(clamp((u - 1.6) / 0.5))
    if k3 > 0:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        fo = font(INTER_B, 30)
        d.rounded_rectangle([250, 1120, 520, 1190], radius=35, outline=(230, 230, 235, int(255 * k3)), width=2)
        d.text((385, 1155), "♥  ME GUSTA", font=fo, fill=(230, 230, 235, int(255 * k3)), anchor="mm")
        follow = u > 2.4
        d.rounded_rectangle([560, 1120, 830, 1190], radius=35, fill=(245, 245, 245, int(255 * k3)) if follow else None,
                            outline=(245, 245, 245, int(255 * k3)), width=2)
        d.text((695, 1155), "✓ SIGUIENDO" if follow else "+  SEGUIR", font=fo, fill=((10, 10, 12) if follow else (245, 245, 245)) + (int(255 * k3),), anchor="mm")
        d.text((540, 1250), "@ojoaldato.ya", font=font(INTER, 26), fill=(140, 146, 158, int(255 * k3)), anchor="mm")
        out.paste(lay, (0, 0), lay)
    if u < 0.35:
        out = Image.blend(img, out, ease(u / 0.35))
    return out
