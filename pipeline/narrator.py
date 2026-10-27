"""Narrador de los vídeos: el stickman con el ojo del logo como cabeza (ver content/avatar/avatar.py).
Sprites cacheados por pose, párpado y mirada; el motor solo los pega, los balancea y los anima al hablar."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import cine
from cine import F_CAP

SS = 2
INK = (243, 240, 232)
BG = (14, 15, 18)
YEL = (255, 210, 63)
W0, H0 = 1000, 1200


class Pen:
    def __init__(self):
        self.im = Image.new("RGBA", (W0 * SS, H0 * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def stroke(self, pts, w=26, col=INK):
        P_ = self.P(pts)
        ww = int(w * SS)
        self.d.line(P_, fill=col, width=ww, joint="curve")
        for x, y in (P_[0], P_[-1]):
            self.d.ellipse([x - ww / 2, y - ww / 2, x + ww / 2, y + ww / 2], fill=col)

    def curve(self, p0, p1, p2, w=26, col=INK, n=20):
        pts = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
                (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]) for u in [i / n for i in range(n + 1)]]
        self.stroke(pts, w, col)

    def dot(self, x, y, r, col=INK):
        self.d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=col)

    def poly(self, pts, col):
        self.d.polygon(self.P(pts), fill=col)

    def paste(self, layer):
        self.im.alpha_composite(layer)
        self.d = ImageDraw.Draw(self.im)


def almond(cx, cy, s, open_k=1.0, n=40):
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        x = cx - s / 2 + s * u
        dy = s * 0.21 * 4 * u * (1 - u) * open_k
        top.append((x, cy - dy))
        bot.append((x, cy + dy))
    return top, bot


def eye_head(p, cx, cy, s, look=(0, 0), open_k=1.0, lid=0.0, brow=None, iris_r=0.19):
    top, bot = almond(cx, cy, s, open_k)
    Wd, Hd = p.im.size
    mask = Image.new("L", (Wd, Hd), 0)
    ImageDraw.Draw(mask).polygon(p.P(top + bot[::-1]), fill=255)
    lay = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.polygon(p.P(top + bot[::-1]), fill=BG + (255,))
    ix, iy, r = cx + look[0] * s, cy + look[1] * s, s * iris_r
    ld.ellipse([(ix - r) * SS, (iy - r) * SS, (ix + r) * SS, (iy + r) * SS], fill=YEL + (255,))
    fnt = ImageFont.truetype(F_CAP, int(r * 1.55 * SS))
    ld.text((ix * SS, (iy + r * 0.04) * SS), "?", font=fnt, fill=BG + (255,), anchor="mm")
    if lid > 0:
        y_l = cy - s * 0.21 * open_k + lid * s * 0.42 * open_k
        ld.rectangle([0, 0, Wd, y_l * SS], fill=BG + (255,))
    clip = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    clip.paste(lay, (0, 0), mask)
    p.paste(clip)
    w = s * 0.045
    p.stroke(top, w)
    p.stroke(bot, w)
    if 0 < lid < 0.98:
        y_l = cy - s * 0.21 * open_k + lid * s * 0.42 * open_k
        xs = [x for x, y in top if y <= y_l + 1]
        if xs:
            p.curve((min(xs) + 6, y_l + 2), (cx, y_l + 10), (max(xs) - 6, y_l + 2), w * 0.9)
    if brow:
        tilt, hgt = brow
        y0 = cy - s * 0.21 * open_k - hgt
        p.curve((cx - s * 0.30, y0 + tilt), (cx, y0 - 24), (cx + s * 0.30, y0 - tilt), w * 1.1)


def body(p, neck, hip, arms, legs, w=26):
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


LEGS = lambda hip: [[hip, (430, 920), (410, 1060)], [hip, (570, 920), (600, 1060)]]


def _pose(p, pose, lid, look, talk):
    """talk: -1…1, gesto suave del brazo mientras habla (0 = reposo)."""
    cx, hy = 500, 330
    neck, hip = (cx, hy + 100), (cx, 760)
    sh = (cx, 520)
    if pose == "wave":
        eye_head(p, cx, hy, 380, look=look, lid=lid)
        body(p, neck, hip, [[sh, (680, 460), (790, 330 - 20 * talk)], [sh, (380, 610), (330, 720)]], LEGS(hip))
        p.curve((770, 270), (815, 245), (850, 275), 10, YEL)
        p.curve((780, 230), (840, 190), (890, 240), 10, YEL)
    elif pose == "point":
        eye_head(p, cx, hy, 380, look=(0.07, 0.0), lid=lid)
        body(p, neck, hip, [[sh, (690, 470), (880, 400 - 16 * talk)], [sh, (390, 620 - 30 * talk), (350, 730 - 50 * talk)]], LEGS(hip))
    elif pose == "think":
        eye_head(p, cx, hy, 380, look=(0.06, -0.05), lid=lid)
        body(p, neck, hip, [[sh, (640, 600), (560, 470)], [sh, (380, 610), (330, 720)]], LEGS(hip))
        for x, y, r in ((680, 200, 16), (730, 140, 24)):
            p.dot(x, y, r, INK)
        p.d.ellipse([720 * SS, 0 * SS, 960 * SS, 130 * SS], outline=INK, width=int(10 * SS))
        p.d.text((840 * SS, 66 * SS), "?", font=ImageFont.truetype(F_CAP, int(80 * SS)), fill=YEL, anchor="mm")
    elif pose == "surprise":
        eye_head(p, cx, hy + 10, 380, open_k=1.3, iris_r=0.17, look=(0.03, 0), lid=lid * 0.6)
        body(p, (cx, hy + 135), (cx, 780), [[(cx, 540), (360, 440), (300, 300)], [(cx, 540), (640, 440), (700, 300)]],
             [[(cx, 780), (420, 930), (380, 1070)], [(cx, 780), (580, 930), (620, 1070)]])
        for x, y, r in ((220, 220, 34), (800, 200, 40), (170, 380, 22)):
            sparkle(p, x, y, r)
    elif pose == "bye":
        eye_head(p, cx, hy, 380, look=(0.0, 0.02), lid=lid)
        hx = 790 + 46 * talk
        body(p, neck, hip, [[sh, (690, 450), (hx, 300)], [sh, (380, 610), (330, 720)]], LEGS(hip))
        for i, r in enumerate((60, 95)):
            p.d.arc([(hx - r) * SS, (300 - r) * SS, (hx + r) * SS, (300 + r) * SS], 200 + 10 * talk, 250 + 10 * talk, fill=YEL, width=int(9 * SS))
    elif pose == "smirk":
        eye_head(p, cx, hy, 380, look=(0.05, 0.03), lid=max(lid, 0.36), brow=(38, 30))
        body(p, neck, hip, [[sh, (400, 600), (470, 700)], [sh, (610, 600), (530, 700)]], LEGS(hip))
    elif pose == "flag":
        eye_head(p, cx, hy, 380, look=(0.06, 0.0), lid=lid, brow=(10, 40))
        body(p, neck, hip, [[sh, (650, 450), (720, 300 - 14 * talk)], [sh, (380, 610), (330, 720)]], LEGS(hip))
        p.stroke([(720, 300 - 14 * talk), (740, 40)], 12, (200, 200, 205))
        for i in range(4):
            for j in range(3):
                col = (250, 250, 250, 255) if (i + j) % 2 else (20, 20, 24, 255)
                x0, y0 = 742 + i * 50, 40 + j * 50
                p.poly([(x0, y0), (x0 + 50, y0), (x0 + 50, y0 + 50), (x0, y0 + 50)], col)


def figure(pose, lid=0.0, look=(0.06, 0.0), talk=0.0):
    def mk():
        p = Pen()
        _pose(p, pose, lid, look, talk)
        im = p.im.resize((W0 // 2, H0 // 2), Image.LANCZOS)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([150, 520, 350, 552], fill=(0, 0, 0, 150))
        out = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im)
        return out
    return cine.cached(("narr", pose, round(lid, 2), look, talk), mk)


# ------------------------------------------------------------------ en el vídeo
POS = {"left": (165, 1655), "right": (915, 1655)}   # (x centro, y de referencia) en el lienzo 1080×1920
SCALE = 0.8                                          # sprite de 500×600 → 400×480 px
BOX = {"left": (0, 1180, 345, 1640), "right": (735, 1180, 1080, 1640)}   # zona que ocupa: las palabras clave no la pisan


def box(V, shot_name):
    cfg = getattr(V, "NARRATOR", None)
    if not cfg:
        return None
    side = (cfg.get(shot_name) or cfg.get("*") or ("point", "left"))[1]
    b = BOX[side]
    sc = getattr(V, "NARRATOR_SCALE", SCALE)      # mascota más pequeña en vídeos con dibujos que bajan mucho
    return (b[0], int(b[3] - (b[3] - b[1]) * sc / SCALE), b[2], b[3])


XF = 0.35   # fundido entre poses


def _vis(V, t, shots):
    """Visibilidad 0-1: en el estilo docu la mascota solo sale en algunos planos (None = no sale), con fundidos."""
    cfg = V.NARRATOR
    si = next((k for k, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
    on = lambda k: 0 <= k < len(shots) and (cfg.get(shots[k]["name"], cfg.get("*", ("point", "left"))) is not None)
    if not on(si):
        return 0.0
    s = shots[si]
    k = 1.0
    if si > 0 and not on(si - 1):
        k = min(k, _smooth((t - s["start"]) / 0.45))
    if si + 1 < len(shots) and not on(si + 1):
        k = min(k, _smooth((s["end"] - t) / 0.45))
    return k


def _pose_at(V, t, shots):
    cfg = V.NARRATOR
    si = next((k for k, s in enumerate(shots) if s["start"] <= t < s["end"]), len(shots) - 1)
    s = shots[si]
    pose, side = (cfg.get(s["name"]) or cfg.get("*") or ("point", "left"))[:2]
    hy = getattr(V, "HYPE", None)
    if hy:
        a_, b_ = shots[0]["lines"][hy["line"]]
        if shots[0]["start"] + a_ - 0.1 <= t <= shots[0]["start"] + b_ + 0.3:
            pose = "surprise"
    return pose, side


def _smooth(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def _speech_env(t, caps):
    """0 en silencio, 1 hablando, con entradas y salidas de 0,3 s (sin saltos)."""
    for c in caps or []:
        if c["start"] - 0.3 <= t < c["end"] + 0.3:
            return _smooth(min((t - c["start"] + 0.3) / 0.3, (c["end"] + 0.3 - t) / 0.3))
    return 0.0


def state(V, t, shots, caps, total):
    if not getattr(V, "NARRATOR", None):
        return None
    if t - (total - cine.end_hold(V)) > 0:
        return None
    pose, side = _pose_at(V, t, shots)
    return pose, side, _speech_env(t, caps) > 0.5, None


def _sprite(pose, t, env):
    ph = (t + 0.7) % 3.3
    lid = 1.0 if ph < 0.06 else (0.55 if ph < 0.12 else 0.0)
    talk = round(env * math.sin(t * 2 * math.pi * 0.8) * 8) / 8      # brazo que va y viene, despacio
    return figure(pose, lid, (0.06, 0.0), talk)


def draw(img, V, t, shots, caps, total):
    if not getattr(V, "NARRATOR", None):
        return
    end_in = t - (total - cine.end_hold(V))
    if end_in > 0:
        return            # en el cierre lo dibuja outro()
    out_k = _vis(V, t, shots)
    if out_k <= 0.01:
        return
    pose, side = _pose_at(V, t, shots)
    env = _speech_env(t, caps)
    x, yf = getattr(V, "NARRATOR_POS", POS)[side]
    sc = getattr(V, "NARRATOR_SCALE", SCALE)
    # respiración lenta + leve asentimiento al empezar cada frase
    bob = math.sin(t * 1.7) * 4
    for c in caps or []:
        if c["start"] <= t < c["start"] + 0.6:
            bob += math.sin((t - c["start"]) / 0.6 * math.pi) * 7
    k_in = cine.ease(cine.clamp(t / 0.6))
    y = yf - 600 * sc * 0.5 + bob + (1 - k_in) * 90
    alpha = k_in * out_k
    prev, _ = _pose_at(V, max(0.0, t - XF), shots)
    if prev != pose:
        lo, hi = max(0.0, t - XF), t
        for _ in range(7):
            mid = (lo + hi) / 2
            if _pose_at(V, mid, shots)[0] == pose:
                hi = mid
            else:
                lo = mid
        q = _smooth((t - hi) / XF)
        cine.paste(img, _sprite(prev, t, env), x, y, sc, alpha * (1 - q))
        cine.paste(img, _sprite(pose, t, env), x, y, sc, alpha * q)
    else:
        cine.paste(img, _sprite(pose, t, env), x, y, sc, alpha)
    if env > 0.02 and pose != "surprise":
        d = ImageDraw.Draw(img, "RGBA")
        hx, hyy = x + 95 * sc + 18, y - 135 * sc
        for i in range(2):
            a = int(170 * env * alpha * (0.6 + 0.4 * math.sin(t * 3.2 + i * 1.3)))
            r = 22 + i * 18
            d.arc([hx - r, hyy - r, hx + r, hyy + r], -40, 40, fill=YEL + (a,), width=5)



# ------------------------------------------------------------------ cierre: se despide y pide me gusta / seguir
def _heart(d, cx, cy, s, fill, outline=None, w=0):
    r = s * 0.29
    pts = [(cx - s * 0.56, cy - s * 0.12), (cx, cy + s * 0.5), (cx + s * 0.56, cy - s * 0.12)]
    if fill:
        d.ellipse([cx - s * 0.5, cy - s * 0.42, cx - s * 0.5 + 2 * r, cy - s * 0.42 + 2 * r], fill=fill)
        d.ellipse([cx + s * 0.5 - 2 * r, cy - s * 0.42, cx + s * 0.5, cy - s * 0.42 + 2 * r], fill=fill)
        d.polygon(pts, fill=fill)
    if outline:
        d.arc([cx - s * 0.5, cy - s * 0.42, cx - s * 0.5 + 2 * r, cy - s * 0.42 + 2 * r], 140, 360, fill=outline, width=w)
        d.arc([cx + s * 0.5 - 2 * r, cy - s * 0.42, cx + s * 0.5, cy - s * 0.42 + 2 * r], 180, 40, fill=outline, width=w)
        d.line([pts[0], pts[1], pts[2]], fill=outline, width=w, joint="curve")


def _pop(u):
    """0→1 con un pequeño rebote al final."""
    u = max(0.0, min(1.0, u))
    c1 = 1.7
    return 1 + (c1 + 1) * (u - 1) ** 3 + c1 * (u - 1) ** 2


def _pill(top, cx, cy, w, h, k, fill, outline, txt, txt_col, icon):
    if k <= 0.01:
        return
    lay = Image.new("RGBA", (int(w + 40), int(h + 40)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=h / 2, fill=fill, outline=outline, width=6 if outline else 0)
    fnt = ImageFont.truetype(F_CAP, 40)
    tw = d.textlength(txt, font=fnt)
    gx = 20 + w / 2 - (tw + 64) / 2
    icon(d, gx + 24, 20 + h / 2)
    d.text((gx + 64, 20 + h / 2 + 2), txt, font=fnt, fill=txt_col, anchor="lm")
    if abs(k - 1) > 1e-3:
        lay = lay.resize((max(2, int(lay.size[0] * k)), max(2, int(lay.size[1] * k))), Image.BILINEAR)
    top.alpha_composite(lay, (int(cx - lay.size[0] / 2), int(cy - lay.size[1] / 2)))


def outro(V, e, hold):
    top = cine.TOP[0]
    kf = cine.clamp(e / 0.35)
    if kf > 0:   # los rótulos del último plano se apagan rápido para no mezclarse con los del cierre
        top.putalpha(top.getchannel("A").point(lambda v: int(v * (1 - kf))))
    k = cine.ease(cine.clamp(e / 0.6))
    top.alpha_composite(Image.new("RGBA", top.size, (8, 9, 12, int(215 * k))))
    lay = Image.new("RGBA", top.size, (0, 0, 0, 0))   # todo el cierre en una capa aparte: nada "agujerea" el fondo
    d = ImageDraw.Draw(lay)
    # textos de arriba
    k1 = cine.ease(cine.clamp((e - 0.25) / 0.5))
    docu_ = getattr(V, "STYLE", None) == "docu"
    if docu_:
        import docu as DC
        d.text((cine.W / 2, 250), "Si aún no lo sabías…", font=DC.title_font(64), fill=DC.CREAM + (int(255 * k1),), anchor="mm")
    else:
        cine.spaced(d, cine.W / 2, 250, "SI AÚN NO LO SABÍAS…", cine.f(cine.F_SER, 50), (255, 255, 255, int(255 * k1)), 6)
    k2 = _pop((e - 0.55) / 0.45)
    if k2 > 0 and docu_:
        d.text((cine.W / 2, 352 - (1 - min(1, k2)) * 30), "¡Ya lo sabes!", font=DC.title_font(112), fill=DC.GOLD + (int(255 * min(1, k2 * 1.2)),), anchor="mm")
    elif k2 > 0:
        cine.spaced(d, cine.W / 2, 320 - (1 - min(1, k2)) * 30, "¡YA LO SABES!", cine.f(cine.F_SER, 84), YEL + (int(255 * min(1, k2 * 1.2)),), 6)
    # el narrador viene al centro y se despide con la mano
    m = _smooth(e / 0.7)
    s0 = getattr(V, "NARRATOR_SCALE", SCALE)
    sc = s0 + (1.15 - s0) * m
    px, pyf = getattr(V, "NARRATOR_POS", POS)["left"]
    x = px + (540 - px) * m
    y_left = pyf - 600 * s0 * 0.5 + math.sin((e + 0.0) * 1.7) * 4
    y_c = 1290 - 230 * 1.15
    y = y_left + (y_c - y_left) * m
    talk = round(math.sin(e * 2 * math.pi * 1.6) * 8) / 8 if e > 0.5 else 0.0
    ph = (e + 1.2) % 2.6
    lid = 1.0 if ph < 0.06 else (0.55 if ph < 0.12 else 0.0)
    spr = figure("bye" if e > 0.35 else "wave", lid, (0.0, 0.02), talk)
    im = spr.resize((int(spr.size[0] * sc), int(spr.size[1] * sc)), Image.BILINEAR)
    lay.alpha_composite(im, (int(x - im.size[0] / 2), int(y - im.size[1] / 2)))
    # bocadillo
    kb = _pop((e - 0.8) / 0.4)
    if kb > 0.01:
        bub = Image.new("RGBA", (460, 260), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bub)
        bd.rounded_rectangle([10, 10, 440, 190], radius=40, fill=(250, 248, 240, 255))
        bd.polygon([(360, 182), (420, 182), (450, 250)], fill=(250, 248, 240, 255))
        fnt = ImageFont.truetype(F_CAP, 46)
        bd.text((225, 72), "¡Dale a like", font=fnt, fill=(16, 16, 20), anchor="mm")
        bd.text((225, 132), "y sígueme!", font=fnt, fill=(16, 16, 20), anchor="mm")
        bub = bub.resize((max(2, int(460 * kb)), max(2, int(260 * kb))), Image.BILINEAR)
        lay.alpha_composite(bub, (int(300 - bub.size[0] / 2), int(690 - bub.size[1] / 2)))
    # botones
    t_like, t_tap, t_fol, t_ok = 1.1, 1.8, 1.4, 2.6
    liked = e > t_tap
    k_like = _pop((e - t_like) / 0.4) * (1 + 0.14 * math.sin(cine.clamp((e - t_tap) / 0.3) * math.pi))

    def heart_icon(dd, cx, cy):
        if liked:
            _heart(dd, cx, cy, 44, (240, 64, 84, 255))
        else:
            _heart(dd, cx, cy, 44, None, (255, 255, 255, 255), 6)

    _pill(lay, 300, 1430, 380, 112, k_like, (20, 22, 28, 235), (240, 64, 84, 255) if liked else (255, 255, 255, 255), "ME GUSTA",
          (255, 255, 255, 255), heart_icon)
    if liked and e - t_tap < 0.6:
        u = (e - t_tap) / 0.6
        r = 40 + 80 * u
        d.ellipse([180 - r, 1430 - r, 180 + r, 1430 + r], outline=(240, 64, 84, int(200 * (1 - u))), width=6)
    ok = e > t_ok
    k_fol = _pop((e - t_fol) / 0.4) * (1 + 0.14 * math.sin(cine.clamp((e - t_ok) / 0.3) * math.pi))

    def plus_icon(dd, cx, cy):
        col = YEL + (255,) if ok else (16, 16, 20, 255)
        if ok:
            dd.line([(cx - 18, cy), (cx - 5, cy + 14), (cx + 20, cy - 14)], fill=col, width=8, joint="curve")
        else:
            dd.line([(cx - 18, cy), (cx + 18, cy)], fill=col, width=8)
            dd.line([(cx, cy - 18), (cx, cy + 18)], fill=col, width=8)

    _pill(lay, 760, 1430, 400, 112, k_fol, (34, 36, 44, 240) if ok else YEL + (255,), YEL + (255,) if ok else None,
          "SIGUIENDO" if ok else "SEGUIR", YEL + (255,) if ok else (16, 16, 20, 255), plus_icon)
    # firma
    k3 = cine.ease(cine.clamp((e - 1.0) / 0.5))
    cine.spaced(d, cine.W / 2, 1560, "@ojoaldato.ya", cine.f(cine.F_SERR, 40), (220, 220, 230, int(255 * k3)), 3)
    k4 = cine.ease(cine.clamp((e - 2.9) / 0.5))
    cine.spaced(d, cine.W / 2, 1640, "MÁNDASELO A QUIEN NO LO SEPA", cine.f(cine.F_SER, 34), YEL + (int(255 * k4),), 5)
    top.alpha_composite(lay)
