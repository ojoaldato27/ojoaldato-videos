"""Estilo «pop» encima de la edición docu (pedido por Iker el 21/10: «me parecen muy sosos… cambia el fondo, ponle mejor
música, efectos, colores, todo mejóralo» y «coge las ideas de vídeos virales del estilo»).

Qué cambia respecto al docu:
- fondo vivo: degradado de color con auroras que se mueven, suelo de rejilla en perspectiva que avanza, partículas y grano;
- paleta por vídeo (los dorados de las escenas pasan al color de la paleta), más saturación y contraste, brillo (bloom) y viñeta;
- cortes secos con destello de 3 fotogramas, zoom de entrada del 20 % y separación RGB; sacudida en las palabras clave;
- subtítulos grandes en mayúsculas con contorno, entrada con rebote y la palabra que suena dentro de una caja de color;
- barra de progreso arriba;
- música electrónica original a 122 bpm (bombo, palmas, charles, bajo con «pumping», pads y arpegio), con parón y subidón
  a mitad del vídeo, y golpes/whoosh en cada corte. Todo sintetizado: sin licencias de terceros.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
from render import W, H, ease, lerp, clamp
import docu as DC
import music3 as M

PALS = {
    # Tesla / tecnología: neón cian + rojo + violeta
    "neon": dict(top=(20, 10, 44), mid=(7, 10, 32), bot=(2, 3, 12), a1=(255, 46, 99), a2=(0, 214, 255), a3=(150, 80, 255),
                 grid=(0, 200, 255), hl=(0, 232, 255), box=(0, 232, 255), boxtxt=(6, 10, 22), remap=133, bar=((0, 214, 255), (255, 46, 99))),
    # cálida para historia
    "sunset": dict(top=(48, 14, 40), mid=(20, 8, 30), bot=(6, 3, 12), a1=(255, 120, 40), a2=(255, 50, 120), a3=(255, 200, 60),
                   grid=(255, 140, 60), hl=(255, 214, 0), box=(255, 214, 0), boxtxt=(20, 10, 10), remap=None, bar=((255, 200, 0), (255, 60, 120))),
    # ciencia / espacio
    "cosmic": dict(top=(10, 16, 48), mid=(6, 8, 28), bot=(2, 2, 10), a1=(120, 80, 255), a2=(0, 255, 190), a3=(255, 70, 200),
                   grid=(90, 120, 255), hl=(0, 255, 190), box=(0, 255, 190), boxtxt=(4, 12, 18), remap=118, bar=((0, 255, 190), (120, 80, 255))),
}
P = {"pal": None, "gt": 0.0, "total": 90.0, "brk": None, "pu": [], "cuts": []}
HW, HH = W // 2, H // 2
_C = {}


def apply(g):
    """Activa el estilo para el módulo de vídeo (g = globals() del módulo)."""
    pal = PALS[g["POP"]]
    P["pal"] = pal
    DC.POP_BG[0] = bg
    DC.SUBC = pal["hl"]
    DC.CREAM = (255, 255, 255)


# ------------------------------------------------------------------ fondo
def _base(pal):
    k = ("base", pal["top"])
    if k not in _C:
        ys = np.linspace(0, 1, HH, dtype=np.float32)[:, None, None]
        top, mid, bot = (np.array(pal[x], np.float32) for x in ("top", "mid", "bot"))
        c = np.where(ys < 0.5, top * (1 - ys * 2) + mid * (ys * 2), mid * (1 - (ys - 0.5) * 2) + bot * ((ys - 0.5) * 2))
        _C[k] = Image.fromarray(np.repeat(c, HW, axis=1).astype(np.uint8), "RGB")
    return _C[k]


def _blob(r, col, a):
    k = ("blob", r, col, a)
    if k not in _C:
        s = 2 * r
        ys, xs = np.mgrid[0:s, 0:s].astype(np.float32)
        q = np.clip(1 - np.sqrt((xs - r) ** 2 + (ys - r) ** 2) / r, 0, 1) ** 1.8
        arr = np.zeros((s, s, 4), np.uint8)
        arr[..., :3] = col
        arr[..., 3] = (q * 255 * a).astype(np.uint8)
        _C[k] = Image.fromarray(arr, "RGBA")
    return _C[k]


def _strip(col, h=60, a=0.55):
    k = ("strip", col, h, a)
    if k not in _C:
        ys = np.linspace(-1, 1, h, dtype=np.float32)[:, None]
        q = np.exp(-(ys * 2.2) ** 2) * np.ones((1, HW), np.float32)
        arr = np.zeros((h, HW, 4), np.uint8)
        arr[..., :3] = col
        arr[..., 3] = (q * 255 * a).astype(np.uint8)
        _C[k] = Image.fromarray(arr, "RGBA")
    return _C[k]


def _grain(i):
    if "grain" not in _C:
        rng = np.random.default_rng(7)
        out = []
        for _ in range(6):
            n = np.clip(16 + rng.normal(0, 3.0, (HH, HW)), 0, 32).astype(np.uint8)
            out.append(Image.merge("RGB", [Image.fromarray(n)] * 3))
        _C["grain"] = out
    return _C["grain"][i % 6]


def bg(img, t, cx=540, cy=820, dust_n=70, seed=2):
    pal = P["pal"]
    g = P["gt"]
    b = _base(pal).copy()
    for col, r, a, sx, sy, ph, bx, by_ in ((pal["a1"], 330, 0.40, 0.050, 0.036, 0.0, 0.22, 0.30),
                                         (pal["a2"], 310, 0.34, 0.041, 0.057, 2.1, 0.78, 0.42),
                                         (pal["a3"], 280, 0.30, 0.063, 0.045, 4.0, 0.50, 0.18)):
        x = HW * (bx + 0.30 * math.sin(g * sx * 2 * math.pi + ph))
        y = HH * (by_ + 0.16 * math.sin(g * sy * 2 * math.pi + ph * 1.3))
        bl = _blob(r, col, a)
        b.paste(bl, (int(x - r), int(y - r)), bl)
    d = ImageDraw.Draw(b, "RGBA")
    vy, vx = int(HH * 0.60), HW // 2
    gc = pal["grid"]
    # suelo de rejilla que avanza hacia la cámara
    F = (HH - vy) * 0.85
    off = (g * 0.55) % 1.0
    for k in range(0, 16):
        z = 0.85 + (k + 1 - off) * 0.55
        yy = vy + F / z
        if yy > HH:
            continue
        al = int(110 * clamp(1 - (z - 0.85) / 8.0) ** 1.4)
        d.line([(0, yy), (HW, yy)], fill=gc + (al,), width=1 if z > 2.5 else 2)
    for i in range(-11, 12):
        d.line([(vx + i * 9, vy), (vx + i * 120, HH + 4)], fill=gc + (52,), width=1)
    # horizonte que brilla
    st = _strip(pal["a2"], 70, 0.45)
    b.paste(st, (0, vy - 35), st)
    d.line([(0, vy), (HW, vy)], fill=pal["a2"] + (150,), width=1)
    b = ImageChops.add(b, _grain(int(g * 30)), 1.0, -16)
    img.paste(b.resize((W, H), Image.BILINEAR))
    # partículas con paralaje
    dd = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(seed * 13 + 5)
    for j in range(46):
        layer = j % 3
        px, py = rng.uniform(0, W), rng.uniform(0, H)
        sp = (14, 32, 60)[layer]
        sz = (2.0, 3.4, 6.0)[layer] * rng.uniform(0.7, 1.3)
        x = (px + math.sin(g * 0.4 + j) * 20) % W
        y = (py - g * sp) % (H + 40) - 20
        col = (pal["a2"], pal["a1"], (255, 255, 255))[j % 3]
        tw = 0.55 + 0.45 * math.sin(g * 1.7 + j * 1.3)
        al = int((60, 95, 70)[layer] * tw)
        dd.ellipse([x - sz, y - sz, x + sz, y + sz], fill=col + (al,))


# ------------------------------------------------------------------ cámara
def cam(t, s_start):
    """Multiplicador de zoom y sacudida: zoom de entrada en cada corte y golpe/sacudida en las palabras clave."""
    u = t - s_start
    z = 1.0 + 0.20 * (1 - ease(clamp(u / 0.30))) if u >= 0 else 1.0
    dx = dy = 0.0
    for h in P["pu"]:
        v = t - h
        if 0 <= v < 0.22:
            amp = 11 * (1 - v / 0.22)
            dx += amp * math.sin(v * 95)
            dy += amp * math.cos(v * 77)
            z *= 1 + 0.05 * math.sin(math.pi * v / 0.22)
    return z, dx, dy


# ------------------------------------------------------------------ acabado de cada fotograma
def _vig():
    if "vig" not in _C:
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xs - W / 2) / (W * 0.62)) ** 2 + ((ys - H * 0.45) / (H * 0.62)) ** 2)
        q = 1 - 0.42 * np.clip(r - 0.55, 0, 1) ** 1.3
        v = (q * 255).astype(np.uint8)
        _C["vig"] = Image.merge("RGB", [Image.fromarray(v)] * 3)
    return _C["vig"]


_BLOOM_LUT = [min(255, max(0, v - 165) * 3) for v in range(256)] * 3
_HALF = [v // 2 for v in range(256)] * 3


def _remap(img, target):
    hsv = np.array(img.convert("HSV"))
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = (h >= 13) & (h <= 42) & (s > 60) & (v > 40)
    h[m] = target
    return Image.fromarray(hsv, "HSV").convert("RGB")


def _rgb_split(img, px):
    r, g, b = img.split()
    return Image.merge("RGB", (ImageChops.offset(r, px, 0), g, ImageChops.offset(b, -px, 0)))


def post(img, t, s_start):
    pal = P["pal"]
    if pal.get("remap") is not None:
        img = _remap(img, pal["remap"])
    img = ImageEnhance.Color(img).enhance(1.16)
    img = ImageEnhance.Contrast(img).enhance(1.07)
    sm = img.resize((W // 4, H // 4), Image.BILINEAR).point(_BLOOM_LUT)
    br = sm.filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR).point(_HALF)
    img = ImageChops.add(img, br)
    img = ImageChops.multiply(img, _vig())
    u = t - s_start
    near_p = any(0 <= t - h < 0.09 for h in P["pu"])
    if 0 <= u < 0.12 or near_p:
        img = _rgb_split(img, 9 if u < 0.12 else 5)
    if 0 <= u < 0.1:
        img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.42 * (1 - u / 0.1))
    return img


def progress(img, t):
    pal = P["pal"]
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, 9], fill=(255, 255, 255, 38))
    w = int(W * clamp(t / max(1.0, P["total"])))
    if w > 0:
        k = ("bar", pal["top"])
        if k not in _C:
            a, b = (np.array(c, np.float32) for c in pal["bar"])
            xs = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
            arr = (a * (1 - xs) + b * xs) * np.ones((9, 1, 1), np.float32)
            _C[k] = Image.fromarray(arr.astype(np.uint8), "RGB")
        img.paste(_C[k].crop((0, 0, w, 9)), (0, 0))


# ------------------------------------------------------------------ subtítulos «pop»
def chunks_t(caps, n=3):
    """Como docu.make_chunks pero guardando el tiempo de cada palabra: [(t0, t1, [(palabra, destacada, a, b)])]."""
    k = ("chunks", id(caps))
    if k in _C:
        return _C[k]
    chunks = []
    for line in DC.word_times(caps):
        cur = []
        for i, (w, hl, a, b) in enumerate(line):
            cur.append((w, hl, a, b))
            nxt = line[i + 1] if i + 1 < len(line) else None
            bare = w.lower().strip("¿¡,.:;…?!")
            end_p = w.endswith((",", ".", ":", ";", "…", "?", "!"))
            hl_break = nxt is not None and nxt[1] != hl and len(cur) >= 2
            if (len(cur) >= n and bare not in DC.STOP) or len(cur) >= n + 1 or end_p or hl_break:
                chunks.append(cur)
                cur = []
        if cur:
            chunks.append(cur)
    out = []
    for i, ch in enumerate(chunks):
        t0, t1 = ch[0][2], ch[-1][3]
        nxt = chunks[i + 1][0][2] if i + 1 < len(chunks) else t1 + 0.4
        out.append((t0, min(nxt, t1 + 0.35), [(w.replace("*", ""), hl, a, b) for w, hl, a, b in ch]))
    _C[k] = out
    return out


def _cap_layer(words, act, size=82):
    pal = P["pal"]
    fo = DC.caps_font(size, "Black")
    d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    ws = [(w.upper(), hl) for w, hl, _, _ in words]
    sp = d0.textlength(" ", font=fo) * 0.9 + 14
    widths = [d0.textlength(w, font=fo) for w, _ in ws]
    while (sum(widths) + sp * (len(ws) - 1) > 1900 or max(widths) > 940) and size > 56:
        size -= 4
        fo = DC.caps_font(size, "Black")
        sp = d0.textlength(" ", font=fo) * 0.9 + 14
        widths = [d0.textlength(w, font=fo) for w, _ in ws]
    lines, lw = [[]], 0
    for i, ((w, hl), wd) in enumerate(zip(ws, widths)):
        if lines[-1] and lw + sp + wd > 940:
            lines.append([])
            lw = 0
        lines[-1].append((i, w, hl, wd))
        lw += wd + (sp if len(lines[-1]) > 1 else 0)
    lh = int(size * 1.18)
    LH = 120 + lh * len(lines)
    lay = Image.new("RGBA", (W, LH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    yy = LH / 2 - (len(lines) - 1) * lh / 2
    stroke = max(6, size // 10)
    for ln in lines:
        tw = sum(x[3] for x in ln) + sp * (len(ln) - 1)
        x = W / 2 - tw / 2
        for i, w, hl, wd in ln:
            if i == act:
                pad_x, pad_y = 16, size * 0.16
                d.rounded_rectangle([x - pad_x, yy - size * 0.58 - pad_y + 4, x + wd + pad_x, yy + size * 0.50 + pad_y],
                                    radius=16, fill=pal["box"] + (255,))
                d.text((x, yy), w, font=fo, fill=pal["boxtxt"] + (255,), anchor="lm")
            else:
                col = pal["hl"] if hl else (255, 255, 255)
                d.text((x, yy), w, font=fo, fill=col + (255,), anchor="lm", stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
            x += wd + sp
        yy += lh
    sh = lay.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6))
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    out.alpha_composite(Image.merge("RGBA", (*[Image.new("L", lay.size, 0)] * 3, sh)), (0, 0))
    out.alpha_composite(lay)
    return out


def _back(x):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def draw_caption(img, t, caps, y=1480):
    cur = None
    for ci, c in enumerate(chunks_t(caps)):
        if c[0] - 0.02 <= t < c[1]:
            cur = (ci, c)
            break
    if not cur:
        return
    ci, (t0, t1, words) = cur
    act = 0
    for i, (_, _, a, _) in enumerate(words):
        if t >= a - 0.03:
            act = i
    k = ("cap", ci, act)
    if k not in _C:
        if len(_C) > 400:
            for kk in [x for x in _C if isinstance(x, tuple) and x[0] == "cap"][:200]:
                _C.pop(kk, None)
        _C[k] = _cap_layer(words, act)
    lay = _C[k]
    u = t - t0
    s = 0.72 + 0.28 * _back(clamp(u / 0.17))
    fade = 1 - clamp((t - (t1 - 0.06)) / 0.06)
    if fade <= 0:
        return
    if abs(s - 1) > 0.004:
        nw, nh = int(lay.width * s), int(lay.height * s)
        lay = lay.resize((nw, nh), Image.BILINEAR)
    if fade < 0.999:
        lay = DC._alpha(lay, fade)
    img.paste(lay, (int(W / 2 - lay.width / 2), int(y - lay.height / 2)), lay)


# ------------------------------------------------------------------ música original
SR = M.SR


def _t(d):
    return np.arange(int(d * SR)) / SR


def _saw(f, t, ph=0.0):
    return 2 * ((f * t + ph) % 1.0) - 1


def _kick():
    t = _t(0.45)
    f = 46 + 120 * np.exp(-t * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.0)
    click = np.zeros_like(t)
    rng = np.random.default_rng(3)
    nc = int(0.004 * SR)
    click[:nc] = M.hp(rng.standard_normal(nc), 2500) * np.linspace(1, 0, nc)
    return np.tanh((s + click * 0.35) * 1.6)


def _clap(rng):
    t = _t(0.28)
    x = rng.standard_normal(len(t))
    e = np.zeros_like(t)
    for kk, off in enumerate((0.0, 0.010, 0.021)):
        e += (t >= off) * np.exp(-np.clip(t - off, 0, None) * (70 if kk < 2 else 13))
    return M.hp(M.lp(x, 4200), 900) * e


def _hat(rng, open_=False):
    t = _t(0.24 if open_ else 0.05)
    return M.hp(rng.standard_normal(len(t)), 7500) * np.exp(-t * (13 if open_ else 75))


def _supersaw(fs, d, cut=1800):
    t = _t(d)
    x = np.zeros_like(t)
    for f in fs:
        for j, det in enumerate((0.991, 0.996, 1.0, 1.004, 1.009)):
            x += _saw(f * det, t, j * 0.17)
    x = M.lp(x / (5 * len(fs)), cut)
    e = np.minimum(1, t / 0.06) * np.minimum(1, (d - t) / 0.12)
    return x * e


def _bass(f, d):
    t = _t(d)
    x = 0.55 * _saw(f, t) + 0.9 * np.sin(2 * np.pi * f * t)
    x = M.lp(x, 420)
    return x * np.minimum(1, t / 0.004) * np.minimum(1, np.clip(d - t, 0, None) / 0.02)


def _pluck(f, d=0.3):
    t = _t(d)
    x = 0.5 * _saw(f, t) + np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return M.lp(x, 3200) * np.exp(-t * 13)


def _riser(rng, d):
    t = _t(d)
    x = M.hp(rng.standard_normal(len(t)), 1200) * (t / d) ** 2
    s = np.sin(2 * np.pi * np.cumsum(200 + 1400 * (t / d) ** 2) / SR) * (t / d) ** 2 * 0.4
    return x * 0.5 + s


def _boom(rng):
    t = _t(2.2)
    sub = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 9)) / SR) * np.exp(-t * 2.2)
    crash = M.hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 2.8) * 0.35
    return sub + crash


def music(dur, rng, bpm=122):
    """Pista original: intro con filtro abriéndose, groove, parón con subida antes de la mitad (P['brk']), subidón y final."""
    n = int((dur + 2) * SR)
    beat = 60.0 / bpm
    bar = beat * 4
    out = {k: np.zeros(n) for k in ("kick", "clap", "hat", "bass", "pad", "arp", "fx")}
    prog = [(220.0, [220.0, 261.63, 329.63]), (174.61, [174.61, 220.0, 261.63]),
            (261.63, [261.63, 329.63, 392.0]), (196.0, [196.0, 246.94, 293.66])]       # Am F C G
    brk = P.get("brk") or dur * 0.52
    b0, b1 = brk - 2 * bar, brk           # parón de 2 compases que termina en el banner
    end = dur - 2.0
    K = _kick()
    nbar = int(dur / bar) + 2
    for bi in range(nbar):
        tb = bi * bar
        if tb > dur + 1:
            break
        root, chord = prog[bi % 4]
        in_brk = b0 <= tb < b1
        in_end = tb >= end - bar
        cut = 600 + 1800 * clamp(tb / (2 * bar)) if tb < 2 * bar else (1200 if in_brk else 2300)
        M.add(out["pad"], _supersaw([f for f in chord], bar, cut), tb, 1.0)
        for s16 in range(16):
            ts = tb + s16 * beat / 4
            note = chord[(s16 * 2 + bi) % 3] * (2 if s16 % 4 in (1, 3) else 1)
            if not in_end:
                M.add(out["arp"], _pluck(note, 0.22), ts, 0.55 if not in_brk else 0.35)
        if in_brk or in_end:
            continue
        for bt in range(4):
            tk = tb + bt * beat
            M.add(out["kick"], K, tk, 1.0)
            if bt in (1, 3):
                M.add(out["clap"], _clap(rng), tk, 1.0)
            M.add(out["hat"], _hat(rng), tk + beat / 2, 1.0)
            M.add(out["hat"], _hat(rng), tk + beat * 0.25, 0.35)
            if tb >= brk and bt == 3:
                M.add(out["hat"], _hat(rng, True), tk + beat / 2, 0.6)
            for e8 in range(2):
                M.add(out["bass"], _bass(root / 4, beat / 2 * 0.92), tk + e8 * beat / 2, 1.0)
    # sidechain: todo «bombea» con el bombo
    sc = np.ones(n)
    dec = np.exp(-np.arange(int(0.28 * SR)) / SR / 0.09)
    for bi in range(nbar):
        for bt in range(4):
            tk = bi * bar + bt * beat
            if b0 <= tk < b1 or tk >= end - bar or tk > dur:
                continue
            i = int(tk * SR)
            m = min(len(dec), n - i)
            if m > 0:
                sc[i:i + m] = np.minimum(sc[i:i + m], 1 - 0.7 * dec[:m])
    # efectos de estructura: subida antes del subidón y golpe al volver
    M.add(out["fx"], _riser(rng, 2 * bar - 0.05), b0, 0.5)
    M.add(out["fx"], _boom(rng), b1, 0.9)
    M.add(out["fx"], _boom(rng), 0.0, 0.6)
    mix = (out["kick"] * 0.95 + out["clap"] * 0.32 + out["hat"] * 0.11 + (out["bass"] * 0.42 + out["pad"] * 0.30 + out["arp"] * 0.10) * sc
           + out["fx"] * 0.45)
    mix = M.hp(mix, 28)
    mix = np.tanh(mix * 1.2) / 1.2
    return mix[:n]
