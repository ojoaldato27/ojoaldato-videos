"""Motor de edición v3: seis identidades de edición completas.
viral · doc · mystery · creative · premium · exp
Cada una cambia fondo, paleta, tipografía, cámara, transiciones, subtítulos, capítulos, post-procesado y sonido."""
import math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import render as R
from render import W, H, FPS, C, ease, lerp, mix, clamp, font
from styles import chunks_for, wrap
import edit_v2 as V2

GF = "/usr/share/fonts/truetype/"
FONTS = {"caladea": GF + "crosextra/Caladea-Bold.ttf", "caladea_r": GF + "crosextra/Caladea-Regular.ttf",
         "caladea_i": GF + "crosextra/Caladea-Italic.ttf", "bask": GF + "baskerville/GFSBaskerville.otf",
         "poppins": GF + "google-fonts/Poppins-Bold.ttf", "poppins_m": GF + "google-fonts/Poppins-Medium.ttf",
         "mono": GF + "dejavu/DejaVuSansMono-Bold.ttf", "mono_r": GF + "dejavu/DejaVuSansMono.ttf"}
_FC = {}


def ff(name, size):
    k = (name, size)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(FONTS[name], size)
    return _FC[k]


# ------------------------------------------------------------------ paletas
def pal(land_fill, land_line, cyan, orange, red, green, panel, track, grat, globe, g_fill, a_fill, region, dash,
        bag, bag_line, win2, win3, cabin, lw):
    return dict(land_fill=land_fill, land_line=land_line, cyan=cyan, orange=orange, red=red, green=green, panel=panel,
                track=track, grat=grat, globe=globe, g_fill=g_fill, a_fill=a_fill, region=region, dash=dash, bag=bag,
                bag_line=bag_line, win2=win2, win3=win3, cabin=cabin, lw=lw)


PALS = {
    "doc": pal((30, 38, 48), (176, 168, 150), (215, 190, 140), (215, 140, 80), (200, 80, 70), (120, 180, 140),
               (16, 20, 28), (50, 56, 66), (26, 32, 42), (18, 24, 32), (70, 100, 120), (150, 95, 60), (150, 145, 130),
               (190, 185, 170), (90, 70, 60), (215, 190, 140), (150, 145, 130), (100, 100, 95), (22, 28, 36), 2),
    "mystery": pal((20, 20, 24), (110, 110, 118), (200, 210, 220), (200, 60, 50), (230, 40, 50), (180, 200, 190),
                   (10, 10, 12), (40, 40, 44), (18, 18, 22), (12, 12, 14), (60, 64, 72), (110, 30, 30), (120, 120, 128),
                   (150, 150, 158), (50, 20, 24), (230, 40, 50), (120, 120, 128), (70, 70, 76), (14, 14, 16), 2),
    "creative": pal((255, 252, 245), (24, 32, 80), (40, 80, 255), (255, 110, 90), (235, 60, 70), (30, 170, 120),
                    (255, 255, 255), (220, 210, 190), (232, 224, 208), (255, 250, 240), (120, 160, 255), (255, 130, 100),
                    (90, 90, 120), (24, 32, 80), (255, 110, 90), (24, 32, 80), (60, 70, 120), (120, 130, 170),
                    (255, 255, 255), 4),
    "premium": pal((36, 38, 44), (120, 124, 134), (150, 200, 255), (255, 160, 80), (255, 90, 90), (90, 220, 150),
                   (24, 25, 30), (50, 52, 60), (26, 27, 32), (24, 26, 30), (90, 140, 220), (230, 140, 70),
                   (150, 154, 164), (190, 194, 204), (60, 60, 70), (255, 210, 63), (150, 154, 164), (90, 94, 104),
                   (24, 25, 30), 3),
    "exp": pal((8, 26, 10), (170, 255, 60), (255, 40, 170), (255, 140, 0), (255, 40, 90), (170, 255, 60), (6, 10, 6),
               (30, 60, 30), (14, 30, 14), (6, 16, 8), (120, 20, 90), (60, 110, 20), (140, 200, 120), (200, 255, 160),
               (60, 10, 50), (255, 40, 170), (140, 200, 120), (80, 130, 70), (6, 12, 6), 3),
}
THEMES = {
    "viral": V2.THEMES["pop"],
    "doc": dict(bg=(12, 16, 22), grid=(30, 36, 46), fg=(236, 230, 218), muted=(150, 145, 132), accent=(226, 182, 104),
                comp=(215, 190, 140), tens=(215, 140, 80), steel=(150, 150, 140)),
    "mystery": dict(bg=(6, 6, 8), grid=(20, 20, 24), fg=(225, 225, 230), muted=(120, 120, 128), accent=(230, 40, 50),
                    comp=(200, 210, 220), tens=(200, 60, 50), steel=(140, 140, 150)),
    "creative": dict(bg=(246, 239, 226), grid=(232, 224, 208), fg=(24, 32, 80), muted=(110, 110, 140),
                     accent=(40, 80, 255), comp=(255, 110, 90), tens=(255, 110, 90), steel=(60, 70, 120)),
    "premium": dict(bg=(15, 16, 19), grid=(30, 31, 36), fg=(245, 245, 247), muted=(150, 150, 158),
                    accent=(255, 210, 63), comp=(150, 200, 255), tens=(255, 160, 80), steel=(150, 154, 164)),
    "exp": dict(bg=(4, 4, 6), grid=(14, 30, 14), fg=(235, 255, 225), muted=(120, 170, 110), accent=(170, 255, 60),
                comp=(255, 40, 170), tens=(255, 140, 0), steel=(140, 200, 120)),
}
LABEL = {
    "viral": None,
    "doc": lambda s, w: ff("caladea_r" if w in ("Semi", "Mono") else "caladea", int(s * 1.05)),
    "mystery": lambda s, w: ff("mono_r" if w in ("Semi", "Mono") else "caladea", int(s * (0.85 if w in ("Semi", "Mono") else 1.05))),
    "creative": lambda s, w: ff("poppins_m" if w in ("Semi", "Mono") else "poppins", int(s * 0.95)),
    "premium": lambda s, w: font(s, "Semi" if w == "Mono" else w),
    "exp": lambda s, w: ff("mono", int(s * 0.85)),
}
STYLE_INFO = {
    "viral": "Viral ultradinámica", "doc": "Cinematográfica documental", "mystery": "Misterio y suspense",
    "creative": "Visual creativa", "premium": "Redes sociales premium", "exp": "Experimental",
}


# ------------------------------------------------------------------ fondos y overlays
def vgrad(top, bot):
    ys = np.linspace(0, 1, H)[:, None, None]
    arr = np.broadcast_to(np.array(top) + (np.array(bot) - np.array(top)) * ys, (H, W, 3)).copy()
    return Image.fromarray(arr.astype(np.uint8))


def radial_alpha(cx, cy, r_in, r_out, inner=0, outer=255):
    yy, xx = np.mgrid[0:H, 0:W]
    dist = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 0.8) ** 2)
    k = np.clip((dist - r_in) / (r_out - r_in), 0, 1)
    return Image.fromarray((inner + (outer - inner) * k).astype(np.uint8), "L")


def make_bg(style):
    if style == "viral":
        return V2.bg_pop()
    if style == "doc":
        img = vgrad((22, 28, 38), (6, 8, 12))
        haze = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(haze).ellipse([-200, -400, W + 200, 700], fill=(120, 90, 60, 50))
        img = img.convert("RGBA")
        img.alpha_composite(haze.filter(ImageFilter.GaussianBlur(160)))
        return img.convert("RGB")
    if style == "mystery":
        img = vgrad((12, 12, 16), (3, 3, 5))
        fog = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(fog)
        for i in range(7):
            dd.ellipse([-300 + i * 180, 1200 + (i % 3) * 120, 300 + i * 180, 1600 + (i % 3) * 120], fill=(60, 60, 70, 30))
        img = img.convert("RGBA")
        img.alpha_composite(fog.filter(ImageFilter.GaussianBlur(80)))
        return img.convert("RGB")
    if style == "creative":
        return Image.new("RGB", (W, H), THEMES["creative"]["bg"])
    if style == "premium":
        img = vgrad((24, 25, 30), (10, 10, 12))
        d = ImageDraw.Draw(img)
        for x in range(40, W, 80):
            for y in range(40, H, 80):
                d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(40, 41, 48))
        return img
    if style == "exp":
        return Image.new("RGB", (W, H), (4, 4, 6))


class FX:
    """Overlays precalculados por estilo."""

    def __init__(self, style):
        self.style = style
        rng = np.random.default_rng(3)
        self.grain = []
        if style in ("doc", "mystery"):
            for _ in range(6):
                n = rng.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)
                g = Image.fromarray(n, "L").resize((W, H), Image.NEAREST)
                lay = Image.merge("RGBA", (g, g, g, Image.new("L", (W, H), 14 if style == "doc" else 18)))
                self.grain.append(lay)
        if style == "doc":
            self.vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            self.vig.putalpha(radial_alpha(540, 900, 520, 1250, 0, 170))
        if style == "mystery":
            self.spots = []
            for r in (430, 520, 640, 800):
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                lay.putalpha(radial_alpha(540, 860, r, r + 520, 0, 235))
                self.spots.append(lay)
        if style == "exp":
            sl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(sl)
            for y in range(0, H, 4):
                d.line([(0, y), (W, y)], fill=(0, 0, 0, 70))
            self.scan = sl

    def post(self, img, i, t, key_boost, events):
        st = self.style
        if st in ("doc", "mystery"):
            base = img.convert("RGBA")
            if st == "doc":
                base.alpha_composite(self.vig)
            else:
                k = min(3, int(key_boost * 3.99))
                base.alpha_composite(self.spots[k])
            base.alpha_composite(self.grain[(i // 2) % len(self.grain)])
            img = base.convert("RGB")
            if st == "doc":
                d = ImageDraw.Draw(img)
                d.rectangle([0, 0, W, 64], fill=(0, 0, 0))
                d.rectangle([0, H - 64, W, H], fill=(0, 0, 0))
        if st == "exp":
            if events.get("rgb", 0) > 0:
                a = events["rgb"]
                r, g, b = img.split()
                off = int(14 * a)
                r = ImageChops.offset(r, off, 0)
                b = ImageChops.offset(b, -off, 0)
                img = Image.merge("RGB", (r, g, b))
            base = img.convert("RGBA")
            base.alpha_composite(self.scan)
            img = base.convert("RGB")
        if st == "mystery" and events.get("flicker"):
            img = Image.eval(img, lambda v: int(v * 0.55))
        return img


# ------------------------------------------------------------------ subtítulos
def words_line(d, chunk, f):
    return " ".join(w for w, _ in chunk), d.textlength(" ".join(w for w, _ in chunk), font=f)


def cap_doc(img, text, t_in, t_left):
    """Subtítulo discreto de documental: frase completa, serif, fundido."""
    a = min(ease(t_in / 0.3), ease(t_left / 0.25))
    if a <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    f = ff("caladea_r", 54)
    fb = ff("caladea_i", 54)
    words = []
    for w in text.split():
        words.append((w.replace("*", ""), "*" in w))
    lines = wrap(d, words, f, 880)
    y = 1660 - len(lines) * 66
    for ln in lines:
        tw = sum(d.textlength(w + " ", font=(fb if h else f)) for w, h in ln)
        x = (W - tw) / 2
        for w, h in ln:
            fnt = fb if h else f
            col = (226, 182, 104) if h else (238, 232, 220)
            d.text((x + 2, y + 3), w, font=fnt, fill=(0, 0, 0, int(200 * a)))
            d.text((x, y), w, font=fnt, fill=col + (int(255 * a),))
            x += d.textlength(w + " ", font=fnt)
        y += 66


def spaced(d, xy, txt, f, fill, track):
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track


def spaced_len(d, txt, f, track):
    return sum(d.textlength(ch, font=f) + track for ch in txt) - track


def cap_mystery(img, chunk, t_in):
    d = ImageDraw.Draw(img, "RGBA")
    a = ease(t_in / 0.25)
    track = lerp(14, 5, ease(t_in / 0.5))
    f = ff("caladea", 72)
    words = [(w.upper(), h or w.endswith("?")) for w, h in chunk]
    lines, cur = [], []
    for w in words:
        test = " ".join(x for x, _ in cur + [w])
        if spaced_len(d, test, f, track) > 900 and cur:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    lines.append(cur)
    y = 1520 - len(lines) * 45
    for ln in lines:
        tw = spaced_len(d, " ".join(w for w, _ in ln), f, track)
        x = (W - tw) / 2
        for wd, hl in ln:
            col = (230, 40, 50) if hl else (232, 232, 236)
            spaced(d, (x + 3, y + 4), wd, f, (0, 0, 0, int(220 * a)), track)
            spaced(d, (x, y), wd, f, col + (int(255 * a),), track)
            x += spaced_len(d, wd + " ", f, track) + track
        y += 92


def cap_creative(img, chunk, t_in):
    """Jerarquía tipográfica: la palabra clave enorme en su propia línea."""
    d = ImageDraw.Draw(img, "RGBA")
    key = [w for w, h in chunk if h]
    rest = [w for w, h in chunk if not h]
    y = 1440
    fs = ff("poppins", 64)
    if rest:
        txt = " ".join(rest)
        a = ease(t_in / 0.18)
        tw = d.textlength(txt, font=fs)
        d.text(((W - tw) / 2, y + (1 - a) * 20), txt, font=fs, fill=(24, 32, 80, int(255 * a)))
        y += 84
    if key:
        txt = " ".join(key).upper()
        size = 128 if len(txt) < 12 else 96
        fk = ff("poppins", size)
        tw = d.textlength(txt, font=fk)
        while tw > 960:
            size -= 8
            fk = ff("poppins", size)
            tw = d.textlength(txt, font=fk)
        k = ease((t_in - 0.08) / 0.25)
        x0 = (W - tw) / 2
        d.rectangle([x0 - 16, y + size * 0.62, x0 - 16 + (tw + 32) * k, y + size * 1.08], fill=(255, 110, 90, 255))
        d.text((x0, y), txt, font=fk, fill=(40, 80, 255, int(255 * clamp(k * 2))))


def cap_premium(img, chunk, t_in, cdur):
    """Palabra a palabra dentro de cada bloque; clave en amarillo."""
    d = ImageDraw.Draw(img)
    f = font(88, "Black")
    lines = wrap(d, chunk, f, 900)
    nwords = sum(len(l) for l in lines)
    per = max(0.12, cdur / max(1, nwords) * 0.6)
    y = 1530 - len(lines) * 50
    idx = 0
    for ln in lines:
        x = (W - d.textlength(" ".join(w for w, _ in ln), font=f)) / 2
        for wd, hl in ln:
            vis = t_in >= idx * per
            if vis:
                k = ease((t_in - idx * per) / 0.12)
                col = (255, 210, 63) if hl else (255, 255, 255)
                col = mix((60, 60, 60), col, k)
                d.text((x + 3, y + 5), wd, font=f, fill=(0, 0, 0))
                d.text((x, y), wd, font=f, fill=col)
            x += d.textlength(wd + " ", font=f)
            idx += 1
        y += 100


def cap_exp(img, chunk, t_in):
    d = ImageDraw.Draw(img)
    f = ff("mono", 66)
    txt_words = [(w.upper(), h) for w, h in chunk]
    total = " ".join(w for w, _ in txt_words)
    nvis = int(t_in * 45) + 1
    lines = wrap(d, txt_words, f, 900)
    y = 1500 - len(lines) * 46
    shown = 0
    last = None
    for ln in lines:
        lt = " ".join(w for w, _ in ln)
        x = (W - d.textlength(lt, font=f)) / 2
        for wd, hl in ln:
            if shown >= nvis:
                break
            vis = wd[: max(0, nvis - shown)]
            tw = d.textlength(vis, font=f)
            if hl:
                d.rectangle([x - 8, y - 4, x + tw + 8, y + 80], fill=(170, 255, 60))
                d.text((x, y), vis, font=f, fill=(4, 4, 6))
            else:
                d.rectangle([x - 8, y - 4, x + tw + 8, y + 80], fill=(4, 4, 6))
                d.text((x, y), vis, font=f, fill=(170, 255, 60))
            shown += len(wd) + 1
            last = (x + tw, y)
            x += d.textlength(wd + " ", font=f)
        y += 92
    if (int(t_in * 4) % 2) == 0 and last:
        d.rectangle([last[0] + 14, last[1] + 4, last[0] + 40, last[1] + 72], fill=(170, 255, 60))


# ------------------------------------------------------------------ capítulos
def chapter(img, style, txt, idx, t_in):
    d = ImageDraw.Draw(img, "RGBA")
    a = ease(t_in / 0.4)
    A = int(255 * a)
    if style == "viral":
        V2.sticker(img, txt, t_in)
    elif style == "doc":
        f = ff("caladea_r", 32)
        s = f"—  {txt.upper()}  —"
        x = (W - spaced_len(d, s, f, 6)) / 2
        spaced(d, (x, 210), s, f, (226, 182, 104, A), 6)
    elif style == "mystery":
        f = ff("mono", 28)
        d.text((60, 200), f"EXPEDIENTE {idx:02d} · {txt.upper()}", font=f, fill=(230, 40, 50, A))
    elif style == "creative":
        d.ellipse([60, 196, 128, 264], fill=(40, 80, 255, A))
        f = ff("poppins", 34)
        n = f"{idx:02d}"
        d.text((94 - d.textlength(n, font=f) / 2, 206), n, font=f, fill=(255, 255, 255, A))
        d.text((146, 206), txt, font=f, fill=(24, 32, 80, A))
    elif style == "premium":
        f = font(32, "Semi")
        tw = d.textlength(txt, font=f)
        d.rounded_rectangle([60, 200, 60 + tw + 76, 252], radius=26, fill=(30, 31, 36, int(230 * a)))
        d.ellipse([82, 218, 98, 234], fill=(255, 210, 63, A))
        d.text((112, 206), txt, font=f, fill=(245, 245, 247, A))
    elif style == "exp":
        f = ff("mono", 30)
        cur = "_" if int(t_in * 3) % 2 == 0 else " "
        d.text((60, 200), f"[{idx:02d}] {txt.upper().replace(' ', '_')}{cur}", font=f, fill=(170, 255, 60, A))


# ------------------------------------------------------------------ cámara y transiciones
CFG = {
    "viral": dict(trans="whip", tdur=0.22, glow=False, shadow=(22, 20, 35), cut_every=1, punch=0.05,
                  framings=[(1.0, 0.45, 0.5), (1.08, 0.40, 0.4), (1.04, 0.48, 0.6), (1.10, 0.42, 0.5)], flash=0.45,
                  key_gap=2.5, key_zoom=0.05),
    "doc": dict(trans="cross", tdur=0.7, glow=True, glow_k=1, kenburns=0.07),
    "mystery": dict(trans="dip", tdur=0.5, glow=True, glow_k=2, kenburns=0.05, key_gap=5.0),
    "creative": dict(trans="iris", tdur=0.45, glow=False, shadow=(24, 32, 80), key_gap=4.0, key_zoom=0.04),
    "premium": dict(trans="slide", tdur=0.32, glow=True, glow_k=1, key_gap=4.5, key_zoom=0.06),
    "exp": dict(trans="glitch", tdur=0.25, glow=True, glow_k=2, key_gap=6.0, pulse=0.02, bpm=128),
}


def zoom_crop(lay, z, fx=0.5, fy=0.45):
    if z <= 1.001:
        return lay
    zw, zh = int(W * z), int(H * z)
    big = lay.resize((zw, zh), Image.BILINEAR)
    ox, oy = int((zw - W) * fx), int((zh - H) * fy)
    return big.crop((ox, oy, ox + W, oy + H))


def render_scene(sc, t):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    R.SCENES[sc["type"]](ImageDraw.Draw(lay), max(0.0, t), sc.get("params", {}), lay)
    return lay


def key_moments(chunks, gap):
    out, last = [], -99
    for cs, ce, g in chunks:
        if any(h for _, h in g) and cs - last >= gap:
            out.append((cs, ce))
            last = cs
    return out


def plan_audio(script):
    """SFX y silencios estratégicos según el estilo."""
    st = script["style"]
    cfg = CFG[st]
    chunks = all_chunks(script)
    keys = key_moments(chunks, cfg.get("key_gap", 4.5))
    scenes = [sc["start"] for sc in script["scenes"] if sc["start"] > 0]
    chaps = [c["start"] for c in script.get("chapters", []) if c["start"] > 0]
    sfx, duck = [], []
    if st == "viral":
        for i, (cs, ce, g) in enumerate(chunks):
            sfx.append((cs, "ding" if any(h for _, h in g) else ("pop" if i % 2 else "pop_low")))
        sfx += [(s, "whoosh") for s in scenes]
        sfx += [(c, "riser") for c in chaps]
        sfx += [(k[0], "impact") for k in keys[::3]]
    elif st == "doc":
        sfx += [(s, "whoosh_down") for s in scenes]
        big = [k for k in keys if any(ch.isdigit() for ch in "".join(w for c in chunks if c[0] == k[0] for w, _ in c[2]))]
        sfx += [(k[0], "swell") for k in big[:4]]
    elif st == "mystery":
        for k in keys:
            sfx += [(k[0], "riser"), (k[0], "impact")]
            duck.append((k[0] - 0.55, k[0]))
        for cs, ce, g in chunks:
            if g[-1][0].endswith("?"):
                sfx.append((cs, "click"))
        sfx += [(s, "whoosh_down") for s in scenes]
    elif st == "creative":
        for i, (cs, ce, g) in enumerate(chunks):
            if any(h for _, h in g):
                sfx.append((cs, "ding"))
            elif i % 3 == 0:
                sfx.append((cs, "paper"))
        sfx += [(s, "whoosh") for s in scenes]
    elif st == "premium":
        for cs, ce in keys:
            sfx.append((cs, "pop"))
        sfx += [(s, "whoosh_down") for s in scenes]
    elif st == "exp":
        for i, (cs, ce, g) in enumerate(chunks):
            sfx.append((cs, "click"))
        sfx += [(s, "glitch") for s in scenes]
        sfx += [(c, "riser") for c in chaps]
        sfx += [(k[0], "impact") for k in keys]
    sfx += [(nt["t"], "notif") for nt in script.get("notifs", [])]
    return sfx, duck


def all_chunks(script):
    ch = []
    for c in sorted(script["captions"], key=lambda c: c["start"]):
        ch += chunks_for(c["text"], c["start"], c["end"], n=script.get("chunk_n", 3))
    return ch


def render_v3(script, out_mp4, audio_wav, only_times=None):
    st = script["style"]
    cfg = CFG[st]
    V2.CALM = False
    import scenes_nls, scenes_planes
    R.SCENES.update(scenes_nls.SCENES)
    R.SCENES.update(scenes_planes.SCENES)
    import scenes_sun
    R.SCENES.update(scenes_sun.SCENES)
    if st == "viral":
        scenes_planes.set_palette("pop")
        R.CURRENT_THEME = "pop"
    else:
        scenes_planes.PALETTES[st] = PALS[st]
        scenes_planes.set_palette(st)
        R.CURRENT_THEME = st
    C.update(THEMES[st])
    R.LABEL_FONT = LABEL[st]
    bg = make_bg(st)
    fx = FX(st)
    dur = script["duration"]
    n = int(dur * FPS)
    offset_y = 100
    scenes = script["scenes"]
    chunks = all_chunks(script)
    keys = key_moments(chunks, cfg.get("key_gap", 4.5))
    cuts = sorted({sc["start"] for sc in scenes} | ({cs for cs, ce, g in chunks} if cfg.get("cut_every") else set()))
    chap_idx = {c["text"]: i + 1 for i, c in enumerate(script.get("chapters", []))}
    rng = random.Random(5)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", audio_wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
           "-shortest", "-movflags", "+faststart", out_mp4]
    pipe = None if only_times else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = [int(x * FPS) for x in only_times] if only_times else range(n)
    shots = []
    wm = script.get("watermark", "")
    beat = 60 / cfg.get("bpm", 120) * 4
    for i in frames:
        t = i / FPS
        si = next((k for k, sc in enumerate(scenes) if sc["start"] <= t < sc["end"]), len(scenes) - 1)
        sc = scenes[si]
        ts = t - sc["start"]
        sdur = sc["end"] - sc["start"]
        lay = render_scene(sc, ts)
        cur = None
        for cs, ce, g in chunks:
            if cs <= t < ce:
                cur = (cs, ce, g)
        is_key = bool(cur and any(h for _, h in cur[2]))
        key_boost = 1 - ease((t - cur[0]) / 0.6) if is_key else 0.0
        # ---- cámara
        z, fxp, fyp = 1.0, 0.5, 0.45
        static = sc["type"] in ("title", "top_card", "outro_nls", "quiz", "quiz_end")
        if st == "viral":
            ci = max([k for k, c in enumerate(cuts) if c <= t] or [0])
            fz, fyp, fxp = cfg["framings"][ci % len(cfg["framings"])]
            if static:
                fz, fyp, fxp = 1.0, 0.45, 0.5
            sc_cut = t - cuts[ci]
            z = fz + cfg["punch"] * (1 - ease(sc_cut / 0.2))
        if cfg.get("kenburns") and not static:
            k = ts / max(1.0, sdur)
            z = 1 + cfg["kenburns"] * k
            fxp = lerp(0.42, 0.58, k) if si % 2 else lerp(0.58, 0.42, k)
        for ks, ke in keys if cfg.get("key_zoom") else []:
            if ks <= t < ke + 0.6:
                up = ease(clamp((t - ks) / 0.4))
                down = 1 - ease(clamp((t - ke) / 0.6))
                z += cfg["key_zoom"] * up * down
        if cfg.get("pulse"):
            pb = (t % beat) / beat
            z += cfg["pulse"] * math.exp(-pb * 12)
        lay = zoom_crop(lay, z, fxp, fyp)
        # ---- transición de entrada
        events = {}
        tr, td = cfg["trans"], cfg["tdur"]
        if si > 0 and ts < td:
            k = ease(ts / td)
            prev = scenes[si - 1]
            if tr == "whip":
                dirn = 1 if si % 2 else -1
                dx = int((1 - k) * W * 0.55 * dirn)
                blurred = lay.resize((W // 16, H), Image.BILINEAR).resize((W, H), Image.BILINEAR)
                lay = Image.blend(lay, blurred, 0.85 * (1 - k))
                moved = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                moved.alpha_composite(lay.crop((max(0, -dx), 0, min(W, W - dx), H)), (max(0, dx), 0))
                lay = moved
            elif tr in ("cross", "iris"):
                pl = render_scene(prev, t - prev["start"])
                if cfg.get("kenburns"):
                    pl = zoom_crop(pl, 1 + cfg["kenburns"], 0.5, 0.45)
                if tr == "cross":
                    lay = Image.blend(pl, lay, k)
                else:
                    m = Image.new("L", (W, H), 0)
                    r = 1400 * k
                    ImageDraw.Draw(m).ellipse([540 - r, 860 - r, 540 + r, 860 + r], fill=255)
                    pl.paste(lay, (0, 0), m)
                    ring = ImageDraw.Draw(pl)
                    ring.ellipse([540 - r, 860 - r, 540 + r, 860 + r], outline=(255, 110, 90, 255), width=14)
                    lay = pl
            elif tr == "dip":
                a = lay.getchannel("A").point(lambda v, kk=k: int(v * kk))
                lay.putalpha(a)
            elif tr == "slide":
                moved = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                dy = int((1 - k) * 160)
                moved.alpha_composite(lay.crop((0, 0, W, H - dy)), (0, dy))
                a = moved.getchannel("A").point(lambda v, kk=k: int(v * kk))
                moved.putalpha(a)
                lay = moved
            elif tr == "glitch":
                out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                y = 0
                rr = random.Random(int(t * 100))
                while y < H:
                    hgt = rr.randint(20, 140)
                    dx = int(rr.uniform(-1, 1) * 120 * (1 - k))
                    band = lay.crop((0, y, W, min(H, y + hgt)))
                    out.alpha_composite(band, (max(0, dx), y)) if dx >= 0 else out.alpha_composite(
                        band.crop((-dx, 0, W, band.size[1])), (0, y))
                    y += hgt
                lay = out
                events["rgb"] = 1 - k
        if st == "mystery" and sdur - ts < 0.25 and si < len(scenes) - 1:
            a = lay.getchannel("A").point(lambda v, kk=(sdur - ts) / 0.25: int(v * kk))
            lay.putalpha(a)
        if st == "exp" and is_key and t - cur[0] < 0.18:
            events["rgb"] = max(events.get("rgb", 0), 1 - (t - cur[0]) / 0.18)
        if st == "mystery":
            for ks, ke in keys:
                if 0 <= t - ks < 0.12 and int((t - ks) * FPS) % 2 == 1:
                    events["flicker"] = True
        # ---- sacudida en impactos (solo viral)
        sx = sy = 0
        if st == "viral" and is_key and t - cur[0] < 0.2:
            a = 1 - (t - cur[0]) / 0.2
            sx, sy = int(rng.uniform(-1, 1) * 8 * a), int(rng.uniform(-1, 1) * 8 * a)
        shifted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shifted.alpha_composite(lay.crop((max(0, -sx), 0, W - max(0, sx), H - offset_y - abs(sy))),
                                (max(0, sx), max(0, offset_y + sy)))
        lay = shifted
        # ---- fondo (parallax / tipografía gigante)
        fr = bg.convert("RGBA")
        if st == "creative":
            dd = ImageDraw.Draw(fr, "RGBA")
            for j, (bx, by, br, col) in enumerate(((180, 400, 260, (255, 210, 190, 255)), (900, 1250, 330, (205, 220, 255, 255)),
                                                    (300, 1650, 200, (255, 236, 170, 255)))):
                ox = 40 * math.sin(t * 0.35 + j * 2)
                oy = 30 * math.cos(t * 0.27 + j)
                dd.ellipse([bx + ox - br, by + oy - br, bx + ox + br, by + oy + br], fill=col)
            if cur:
                kw = [w for w, h in cur[2] if h]
                if kw:
                    big = ff("poppins", 300)
                    txt = kw[0].upper().strip(",.:…")
                    tw = dd.textlength(txt, font=big)
                    xx = (W - tw) / 2 + 80 - 160 * clamp((t - cur[0]) / max(0.5, cur[1] - cur[0]))
                    dd.text((xx, 1090), txt, font=big, fill=(232, 222, 202, 255))
        if st == "exp":
            dd = ImageDraw.Draw(fr, "RGBA")
            off = (t * 120) % 80
            for j in range(14):
                yy = 1300 + j * 50 + off * (j / 14)
                dd.line([(0, yy), (W, yy)], fill=(20, 60, 20, 255), width=2)
            for xx in range(-600, W + 600, 120):
                dd.line([(540, 1300), (xx, H)], fill=(20, 60, 20, 255), width=2)
        if cfg["glow"]:
            q = 4 if st == "premium" else 2
            glow = lay.resize((W // q, H // q), Image.BILINEAR).filter(ImageFilter.GaussianBlur(20 // q)).resize((W, H), Image.BILINEAR)
            for _ in range(cfg.get("glow_k", 1)):
                fr.alpha_composite(glow)
            if key_boost > 0.05 and st in ("mystery", "exp", "premium"):
                g2 = glow.copy()
                g2.putalpha(glow.getchannel("A").point(lambda v: int(v * key_boost)))
                fr.alpha_composite(g2)
        else:
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sh.alpha_composite(lay.crop((0, 0, W - 7, H - 8)), (7, 8))
            black = Image.new("RGBA", (W, H), cfg["shadow"] + (0,))
            black.putalpha(sh.getchannel("A").point(lambda v: int(v * 0.2)))
            fr.alpha_composite(black)
        fr.alpha_composite(lay)
        img = fr.convert("RGB")
        if st == "viral" and si > 0 and ts < 0.12:
            img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), cfg["flash"] * (1 - ts / 0.12))
        img = fx.post(img, i, t, key_boost, events)
        # ---- capítulos
        for ch in script.get("chapters", []):
            if ch["start"] <= t < ch["end"]:
                if not (sc["type"] == "flight" and sc["params"].get("hud", True) and st in ("exp", "mystery", "premium", "doc")):
                    chapter(img, st, ch["text"], chap_idx[ch["text"]], t - ch["start"])
        # ---- subtítulos
        if st == "doc":
            for c in script["captions"]:
                if c["start"] <= t < c["end"]:
                    cap_doc(img, c["text"], t - c["start"], c["end"] - t)
        elif cur:
            g = V2.glue(cur[2])
            ti = t - cur[0]
            if st == "viral":
                if is_key:
                    V2.burst(img, ti)
                V2.cap_pop(img, g, ti)
            elif st == "mystery":
                cap_mystery(img, g, ti)
            elif st == "creative":
                cap_creative(img, g, ti)
            elif st == "premium":
                cap_premium(img, g, ti, cur[1] - cur[0])
            elif st == "exp":
                cap_exp(img, g, ti)
        d = ImageDraw.Draw(img)
        if wm:
            ink = C["fg"] if st not in ("creative",) else (24, 32, 80)
            R.eye_icon(d, 100, 140, 66, ink, (255, 210, 63), (14, 15, 18))
            fnt = LABEL[st](32, "Semi") if LABEL[st] else font(32, "Semi")
            d.text((148, 122), wm, font=fnt, fill=C["muted"])
        for nt in script.get("notifs", []):
            img = V2.notif_banner(img, t - nt["t"], nt["title"], nt["body"])
        d = ImageDraw.Draw(img)
        if st != "doc":
            d.rectangle([0, H - 10, W * (t / dur), H], fill=C["accent"])
        if pipe is None:
            shots.append(img)
            continue
        pipe.stdin.write(img.tobytes())
    R.LABEL_FONT = None
    if pipe is None:
        return shots
    pipe.stdin.close()
    if pipe.wait() != 0:
        raise RuntimeError("ffmpeg falló")
    return out_mp4
