"""Escenas del vídeo del Tesla Roadster (a01) en 3 estilos elegidos por Iker el 21/10 de la hoja de 12:
7 · «minimal» (blanco, líneas finas, acento rojo), 8 · «vhs» (cinta de los 80: atardecer, líneas de barrido, letra VT323)
y 12 · «poster» (póster vintage: crema, rayos de sol, azul marino, rojo y mostaza, grano).
El coche que se ve es un Cybertruck (petición de Iker), aunque el guion habla del Roadster.
Cada módulo de vídeo pone TH = THEMES[...] antes de renderizar; las escenas leen colores y letras de ahí."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from render import ease, clamp, lerp

W, H = 1080, 1920
FD = "/home/claude/shorts-ingenieria/fonts/"
INTER_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
INTER_X = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
INTER = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INTER_R = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_F = {}


def F(name, size):
    p = name if name.startswith("/") else FD + name
    k = (p, size)
    if k not in _F:
        _F[k] = ImageFont.truetype(p, size)
    return _F[k]


THEMES = {
    "minimal": dict(bg=(248, 248, 246), ink=(28, 28, 32), soft=(150, 150, 158), car=(44, 46, 52), dark=(120, 124, 134),
                    tire=(44, 46, 52), hub=(222, 224, 228), light=(255, 255, 255), tail=(230, 40, 40), acc=(230, 40, 40),
                    acc2=(30, 30, 34), pc=[(214, 216, 222), (196, 198, 206)], pcd=(170, 172, 180), lw=5,
                    title=(INTER_X, 118), sub=(INTER, 40), lab=(INTER_B, 34), cap=(INTER_B, 70), big=INTER_X, align="left",
                    cap_col=(160, 160, 168), cap_hl=(20, 20, 22), stroke=0, gas=(200, 204, 214), sky=None),
    "vhs": dict(bg=(30, 26, 34), ink=(214, 204, 194), soft=(160, 140, 150), car=(198, 202, 210), dark=(44, 38, 56),
                tire=(26, 22, 30), hub=(150, 154, 162), light=(255, 250, 230), tail=(255, 70, 70), acc=(255, 190, 90),
                acc2=(255, 120, 150), pc=[(90, 120, 150), (150, 90, 120)], pcd=(40, 30, 44), lw=8,
                title=("vt323.ttf", 170), sub=("vt323.ttf", 70), lab=("vt323.ttf", 62), cap=("vt323.ttf", 112), big="vt323.ttf",
                align="center", cap_col=(255, 255, 255), cap_hl=(255, 190, 90), stroke=5, gas=(240, 232, 236),
                sky=((60, 40, 92), (232, 122, 92))),
    "poster": dict(bg=(244, 232, 206), ink=(34, 48, 78), soft=(170, 150, 120), car=(212, 212, 206), dark=(34, 48, 78),
                   tire=(34, 48, 78), hub=(244, 232, 206), light=(255, 252, 240), tail=(204, 62, 48), acc=(204, 62, 48),
                   acc2=(232, 170, 60), pc=[(244, 232, 206), (232, 170, 60)], pcd=(34, 48, 78), lw=10,
                   title=("bebas-neue.ttf", 230), sub=("bebas-neue.ttf", 68), lab=("bebas-neue.ttf", 64), cap=("bebas-neue.ttf", 128),
                   big="bebas-neue.ttf", align="center", cap_col=(244, 232, 206), cap_hl=(232, 170, 60), stroke=0,
                   gas=(255, 250, 238), sky=None),
}
TH = dict(THEMES["minimal"], name="minimal")
HEAD = {}
_C = {}


def use(name, head):
    TH.clear()
    TH.update(THEMES[name])
    TH["name"] = name
    HEAD.clear()
    HEAD.update(head)


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def pop(u):
    """Entrada con rebote (0 → 1 pasando por 1,08)."""
    u = clamp(u)
    return 1 - (1 - u) ** 3 * math.cos(u * 4.2) if u < 1 else 1.0


# ------------------------------------------------------------------ fondos
GROUND_Y = 1290


def bg(img, t, kind="day"):
    n = TH["name"]
    if n == "minimal":
        return
    if n == "vhs":
        k = ("vhs", kind)
        if k not in _C:
            if kind == "space":
                a = np.linspace(0, 1, H)[:, None, None]
                base = np.array((16, 10, 34)) * (1 - a) + np.array((60, 26, 70)) * a
                im = Image.fromarray(base.repeat(W, 1).astype(np.uint8))
                d = ImageDraw.Draw(im)
                r = random.Random(4)
                for _ in range(160):
                    x, y, s = r.randrange(W), r.randrange(H), r.choice((2, 2, 3, 4))
                    d.rectangle([x, y, x + s, y + s], fill=(255, 240, 230))
            else:
                a = np.clip(np.linspace(0, 1, H) / (GROUND_Y / H), 0, 1)[:, None, None]
                c0, c1 = np.array(TH["sky"][0]), np.array(TH["sky"][1])
                base = c0 * (1 - a) + c1 * a
                im = Image.fromarray(base.repeat(W, 1).astype(np.uint8))
                d = ImageDraw.Draw(im)
                d.ellipse([700, 820, 980, 1100], fill=(255, 200, 120))
                for y0 in range(980, 1100, 26):
                    d.rectangle([690, y0, 990, y0 + 8 + (y0 - 980) // 10], fill=tuple(int(v) for v in base[min(H - 1, y0), 0]))
                d.polygon([(0, GROUND_Y), (120, 1180), (260, 1230), (420, 1150), (600, 1240), (820, 1170), (1080, GROUND_Y)], fill=(70, 34, 70))
                d.rectangle([0, GROUND_Y, W, H], fill=(46, 32, 44))
                for k2 in range(12):
                    y = GROUND_Y + int((k2 / 12) ** 1.8 * (H - GROUND_Y))
                    d.line([(0, y), (W, y)], fill=(80, 50, 70), width=2)
            _C[k] = im
        img.paste(_C[k])
        return
    # póster: crema, rayos que giran despacio, sol mostaza y banda azul marino abajo
    d = ImageDraw.Draw(img)
    cream = TH["bg"]
    d.rectangle([0, 0, W, H], fill=cream)
    if kind == "space":
        d.rectangle([0, 0, W, H], fill=TH["ink"])
        r = random.Random(4)
        for _ in range(90):
            x, y, s = r.randrange(W), r.randrange(1400), r.choice((3, 4, 6))
            d.ellipse([x, y, x + s, y + s], fill=cream)
        d.ellipse([-300, 1250, 1380, 2600], fill=TH["acc2"])
        return
    a0 = t * 0.05
    for k in range(24):
        a = a0 + k * 2 * math.pi / 24
        d.polygon([(540, 960), (540 + math.cos(a) * 1900, 960 + math.sin(a) * 1900),
                   (540 + math.cos(a + 0.13) * 1900, 960 + math.sin(a + 0.13) * 1900)], fill=(236, 216, 180))
    if kind != "nosun":
        d.ellipse([260, 640, 820, 1200], fill=TH["acc2"])
    d.rectangle([0, 1400, W, H], fill=TH["ink"])


def ground(img, y=GROUND_Y, x0=0, x1=W):
    d = ImageDraw.Draw(img)
    if TH["name"] == "minimal":
        d.line([(x0, y), (x1, y)], fill=TH["ink"], width=TH["lw"])
    elif TH["name"] == "poster":
        d.rectangle([x0, y, x1, y + 14], fill=TH["ink"])


# ------------------------------------------------------------------ coche (Cybertruck) con giro
L_CAR = 5.68


def car_geo(cx, cy, sc, ang=0.0, facing=1):
    """(cx, cy): punto de apoyo (entre las ruedas, en el suelo). ang en grados (pantalla, + = horario)."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def T(x, y):
        u, v = (x - L_CAR / 2) * sc * facing, -y * sc
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)

    roof = lambda x: 1.30 + 0.56 * x / 3.06 if x < 3.06 else 1.86 - 0.86 * (x - 3.06) / 2.62
    g = {"body": [T(0, 0.62), T(0, 1.30), T(3.06, 1.86), T(5.68, 1.0), T(5.52, 0.56), T(5.0, 0.42), T(0.62, 0.42)],
         "arches": [], "wheels": [], "r": 0.47 * sc, "T": T}
    for wx in (0.90, 4.63):
        g["arches"].append([T(wx - 0.78, 0.40), T(wx - 0.48, 1.04), T(wx + 0.48, 1.04), T(wx + 0.78, 0.40)])
        g["wheels"].append(T(wx, 0.47))
    g["win"] = [T(2.0, 1.2), T(4.06, 1.2), T(4.06, roof(4.06) - 0.1), T(3.06, 1.76), T(1.78, roof(1.78) - 0.1)]
    g["pillar"] = [T(2.98, 1.2), T(2.98, roof(2.98) - 0.1)]
    g["light"] = [T(5.68, 1.0), T(4.9, roof(4.9))]
    g["tail"] = [T(0, 1.30), T(0, 1.12)]
    g["center"] = T(2.84, 0.95)
    return g


def car(img, cx, cy, sc, ang=0.0, facing=1, body=None, alpha=255, spin=0.0):
    g = car_geo(cx, cy, sc, ang, facing)
    d = ImageDraw.Draw(img, "RGBA")
    b = (body or TH["car"]) + (alpha,)
    dk = TH["dark"] + (alpha,)
    if TH["name"] != "minimal":
        d.polygon([(x + 6, y + 8) for x, y in g["body"]], fill=(0, 0, 0, int(50 * alpha / 255)))
    d.polygon(g["body"], fill=b)
    if TH["name"] == "poster":
        d.line(g["body"] + [g["body"][0]], fill=TH["ink"] + (alpha,), width=6, joint="curve")
    for a in g["arches"]:
        d.polygon(a, fill=dk)
    d.polygon(g["win"], fill=dk)
    d.line(g["pillar"], fill=b, width=max(4, int(g["r"] * 0.18)))
    r = g["r"]
    for (x, y) in g["wheels"]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=TH["tire"] + (alpha,))
        d.ellipse([x - r * 0.56, y - r * 0.56, x + r * 0.56, y + r * 0.56], fill=TH["hub"] + (alpha,))
        for k in range(3):
            a = spin + k * 2 * math.pi / 3
            d.line([(x, y), (x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5)], fill=TH["tire"] + (alpha,), width=max(3, int(r * 0.12)))
    d.line(g["light"], fill=TH["light"] + (alpha,), width=max(4, int(r * 0.2)))
    d.line(g["tail"], fill=TH["tail"] + (alpha,), width=max(5, int(r * 0.3)))
    return g


def parked(img, x, y, w, col, dark=None):
    d = ImageDraw.Draw(img)
    h = w * 0.34
    dark = dark or TH["pcd"]
    d.rounded_rectangle([x - w / 2, y - h, x + w / 2, y - h * 0.35], radius=int(w * 0.07), fill=col)
    d.rounded_rectangle([x - w * 0.28, y - h * 1.55, x + w * 0.24, y - h * 0.9], radius=int(w * 0.09), fill=col)
    d.rounded_rectangle([x - w * 0.22, y - h * 1.42, x + w * 0.18, y - h * 1.0], radius=int(w * 0.05), fill=dark)
    for wx in (x - w * 0.3, x + w * 0.3):
        d.ellipse([wx - h * 0.33, y - h * 0.62, wx + h * 0.33, y + 0.04 * h], fill=TH["tire"])


def puff(img, x, y, ang, k, size=60, n=7, seed=1):
    """Chorro de gas frío: círculos que salen en la dirección ang y se desvanecen."""
    if k <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(seed)
    col = TH["gas"]
    for i in range(n):
        u = (i + 1) / n
        dist = size * 2.2 * u
        px = x + math.cos(ang) * dist + rr.uniform(-8, 8)
        py = y + math.sin(ang) * dist + rr.uniform(-8, 8)
        r = size * (0.3 + 0.6 * u)
        a = int(230 * k * (1 - u * 0.7))
        if TH["name"] == "minimal":
            d.ellipse([px - r, py - r, px + r, py + r], outline=TH["soft"] + (a,), width=3)
        else:
            d.ellipse([px - r, py - r, px + r, py + r], fill=col + (a,))


def speed_lines(img, x0, y0, x1, y1, k, n=5, seed=3):
    if k <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    r = random.Random(seed)
    for i in range(n):
        y = y0 + (y1 - y0) * (i + 0.5) / n + r.uniform(-10, 10)
        ln = r.uniform(0.5, 1.0) * (x1 - x0) * k
        d.line([(x1 - ln, y), (x1, y)], fill=TH["soft"] + (int(220 * k),), width=max(4, TH["lw"] - 2))


# ------------------------------------------------------------------ textos
def _tw(d, s, fo):
    return d.textlength(s, font=fo)


def text(img, xy, s, fo, col, anchor="mm", stroke=None, alpha=255):
    d = ImageDraw.Draw(img, "RGBA")
    st = TH["stroke"] if stroke is None else stroke
    d.text(xy, s, font=fo, fill=col + (alpha,), anchor=anchor, stroke_width=st, stroke_fill=(30, 20, 40, alpha) if st else None)


NAMES = {"tesla": "Tesla", "roadster": "Roadster", "spacex": "SpaceX", "brabham": "Brabham", "bt46b": "BT46B", "musk": "Musk",
         "performance": "Performance", "thrust": "Thrust", "rocket": "Rocket"}


def nice(s):
    """«EL NUEVO TESLA ROADSTER» → «El nuevo Tesla Roadster» (para el estilo minimal)."""
    out = []
    for i, w in enumerate(s.lower().split(" ")):
        w = NAMES.get(w.strip(",·"), w) if w.strip(",·") in NAMES else w
        out.append(w[:1].upper() + w[1:] if i == 0 else w)
    return " ".join(out)


def head(img, t, i, t_hide=None, inv=False):
    """Título del plano (HEAD del vídeo original) arriba, con entrada en cascada."""
    if i not in HEAD:
        return
    title, sub = HEAD[i]
    k = ease(clamp(t / 0.35))
    if t_hide is not None:
        k *= 1 - ease(clamp((t - t_hide[0]) / 0.25)) * (1 - ease(clamp((t - t_hide[1]) / 0.3)))
    if k <= 0.01:
        return
    tf, ts = F(*TH["title"]), F(*TH["sub"])
    d = ImageDraw.Draw(img)
    size = TH["title"][1]
    while _tw(d, title, tf) > 960 and size > 40:
        size -= 6
        tf = F(TH["title"][0], size)
    ss = TH["sub"][1]
    while _tw(d, sub, ts) > 960 and ss > 24:
        ss -= 4
        ts = F(TH["sub"][0], ss)
    a = int(255 * k)
    dy = (1 - k) * 30
    if TH["align"] == "left":
        text(img, (70, 190 + dy), title, tf, TH["ink"], "lm", alpha=a)
        text(img, (74, 290 + dy), nice(sub), ts, TH["soft"], "lm", alpha=a)
        ImageDraw.Draw(img, "RGBA").rectangle([70, 330 + dy, 70 + 90 * k, 338 + dy], fill=TH["acc"] + (a,))
    elif TH["name"] == "vhs":
        text(img, (W / 2, 200 + dy), title.upper(), tf, (255, 255, 255), alpha=a)
        text(img, (W / 2, 300 + dy), sub, ts, TH["acc"], alpha=a)
    else:
        text(img, (W / 2, 210 + dy), title.upper(), tf, TH["bg"] if inv else TH["ink"], alpha=a)
        text(img, (W / 2, 335 + dy), "— " + sub + " —", ts, TH["acc"], alpha=a)


def pill(img, cx, cy, s, k=1.0, col=None):
    if k <= 0:
        return
    fo = F(*TH["lab"])
    d = ImageDraw.Draw(img, "RGBA")
    w = _tw(d, s, fo) + 64
    h = TH["lab"][1] + 40
    a = int(255 * clamp(k))
    sc = 0.85 + 0.15 * pop(k)
    w, h = w * sc, h * sc
    if TH.get("narr") and cy > 1150:
        cx = min(max(cx, 300 + w / 2), W - 20 - w / 2)
    n = TH["name"]
    if n == "minimal":
        d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(h / 2), fill=(col or TH["ink"]) + (a,))
        d.text((cx, cy), s, font=fo, fill=(255, 255, 255, a), anchor="mm")
    elif n == "vhs":
        d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=(20, 14, 28, int(a * 0.85)), outline=(col or TH["acc"]) + (a,), width=4)
        d.text((cx, cy - 4), s, font=fo, fill=(255, 255, 255, a), anchor="mm")
    else:
        d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=(col or TH["acc"]) + (a,))
        d.rectangle([cx - w / 2 + 8, cy - h / 2 + 8, cx + w / 2 - 8, cy + h / 2 - 8], outline=TH["bg"] + (a,), width=3)
        d.text((cx, cy + 2), s, font=fo, fill=TH["bg"] + (a,), anchor="mm")


def big(img, cx, cy, s, size, col, k=1.0, fo=None):
    """Número o palabra grande que entra con rebote."""
    if k <= 0:
        return
    fo = fo or F(TH["big"], size)
    key = ("big", s, size, col, TH["name"], id(fo))
    if key not in _C:
        d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
        w = int(_tw(d0, s, fo)) + 40
        hh = int(size * 1.4) + 40
        lay = Image.new("RGBA", (w, hh), (0, 0, 0, 0))
        dd = ImageDraw.Draw(lay)
        st = TH["stroke"]
        if TH["name"] == "poster":
            dd.text((w / 2 + 8, hh / 2 + 8), s, font=fo, fill=TH["ink"] + (255,), anchor="mm")
        dd.text((w / 2, hh / 2), s, font=fo, fill=col + (255,), anchor="mm", stroke_width=st, stroke_fill=(30, 20, 40) if st else None)
        _C[key] = lay
    lay = _C[key]
    sc = pop(k)
    if sc <= 0.02:
        return
    l2 = lay.resize((max(1, int(lay.width * sc)), max(1, int(lay.height * sc))), Image.BILINEAR)
    if k < 1:
        a = l2.split()[3].point(lambda v: int(v * clamp(k * 2)))
        l2.putalpha(a)
    img.paste(l2, (int(cx - l2.width / 2), int(cy - l2.height / 2)), l2)


def stamp(img, cx, cy, s, k, col=None):
    if k <= 0:
        return
    col = col or TH["acc"]
    fo = F(TH["big"], 120 if TH["name"] != "minimal" else 96)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    w = int(_tw(d0, s, fo)) + 80
    hh = int(fo.size * 1.2) + 60
    st = Image.new("RGBA", (w + 20, hh + 20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rounded_rectangle([10, 10, w + 10, hh + 10], radius=16, outline=col + (240,), width=12)
    sd.text((w / 2 + 10, hh / 2 + 10), s, font=fo, fill=col + (240,), anchor="mm")
    sc = lerp(1.6, 1.0, ease(clamp(k)))
    st = st.resize((int(st.width * sc), int(st.height * sc)), Image.BILINEAR).rotate(-8, expand=True, resample=Image.BICUBIC)
    img.paste(st, (int(cx - st.width / 2), int(cy - st.height / 2)), st)


def dotted_arc(img, cx, cy, r, a0, a1, k, col=None, w=None):
    if k <= 0:
        return
    d = ImageDraw.Draw(img)
    col = col or TH["acc"]
    n = int(40 * abs(a1 - a0) / math.pi) + 2
    for i in range(int(n * k)):
        a = a0 + (a1 - a0) * i / n
        if i % 2 == 0:
            p = (cx + math.cos(a) * r, cy + math.sin(a) * r)
            q = (cx + math.cos(a + (a1 - a0) / n) * r, cy + math.sin(a + (a1 - a0) / n) * r)
            d.line([p, q], fill=col, width=w or max(5, TH["lw"]))


# ------------------------------------------------------------------ piezas
def rocket(img, x, y_base, s=1.0):
    d = ImageDraw.Draw(img)
    w, h = 120 * s, 760 * s
    body = TH["car"] if TH["name"] != "minimal" else (226, 228, 232)
    d.rectangle([x - w / 2, y_base - h, x + w / 2, y_base], fill=body)
    d.polygon([(x - w / 2, y_base - h), (x, y_base - h - 170 * s), (x + w / 2, y_base - h)], fill=body)
    d.rectangle([x - w / 2, y_base - h * 0.95, x - w * 0.15, y_base], fill=TH["dark"] if TH["name"] != "minimal" else (196, 198, 204))
    for yy in (y_base - h * 0.85, y_base - 80 * s):
        d.polygon([(x - w / 2, yy), (x - w / 2 - 50 * s, yy + 90 * s), (x - w / 2, yy + 90 * s)], fill=TH["ink"])
        d.polygon([(x + w / 2, yy), (x + w / 2 + 50 * s, yy + 90 * s), (x + w / 2, yy + 90 * s)], fill=TH["ink"])
    tx = x + w / 2 + 110 * s
    d.rectangle([tx - 30 * s, y_base - h - 60 * s, tx + 30 * s, y_base], outline=TH["ink"], width=max(3, int(5 * s)))
    for k in range(10):
        yy = y_base - k * (h + 60 * s) / 10
        d.line([(tx - 30 * s, yy), (tx + 30 * s, yy - (h + 60 * s) / 10)], fill=TH["ink"], width=max(2, int(4 * s)))


def fan(img, x, y, r, t, col=None):
    d = ImageDraw.Draw(img, "RGBA")
    col = col or TH["ink"]
    d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=max(4, int(r * 0.12)))
    for k in range(5):
        a = t * 14 + k * 2 * math.pi / 5
        p = [(x, y), (x + math.cos(a) * r * 0.85, y + math.sin(a) * r * 0.85), (x + math.cos(a + 0.5) * r * 0.75, y + math.sin(a + 0.5) * r * 0.75)]
        d.polygon(p, fill=col)
    d.ellipse([x - r * 0.18, y - r * 0.18, x + r * 0.18, y + r * 0.18], fill=TH["acc"])


def f1(img, cx, cy, s=1.0, t=0.0, gray=0.0):
    """F1 de 1978 de lado (morro a la derecha) con el ventilador detrás."""
    d = ImageDraw.Draw(img, "RGBA")
    red = TH["acc"] if TH["name"] != "minimal" else (220, 44, 44)
    if gray > 0:
        red = tuple(int(lerp(c, 150, gray)) for c in red)
    wht = (250, 250, 250) if TH["name"] != "poster" else TH["bg"]
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.polygon([P(-380, -20), P(-380, -120), P(-200, -120), P(-120, -70), P(330, -50), P(440, -10), P(440, 20), P(-380, 20)], fill=red)
    d.polygon([P(-120, -60), P(300, -44), P(300, -20), P(-120, -24)], fill=wht)
    d.rectangle([*P(-70, -120), *P(20, -70)], fill=TH["ink"])
    d.ellipse([*P(-50, -150), *P(10, -95)], fill=TH["acc2"])
    d.rectangle([*P(400, 10), *P(470, 30)], fill=red)
    for wx, r in ((-250, 95), (300, 75)):
        x, y = P(wx, 40 - r * 0.2)
        d.ellipse([x - r * s, y - r * s, x + r * s, y + r * s], fill=TH["tire"])
        d.ellipse([x - r * s * 0.45, y - r * s * 0.45, x + r * s * 0.45, y + r * s * 0.45], fill=TH["hub"])
    fx, fy = P(-410, -70)
    fan(img, fx, fy, 70 * s, t, TH["ink"])


def tank(img, x, y, level, k=1.0):
    d = ImageDraw.Draw(img)
    w, h = 220, 520
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], radius=100, fill=TH["car"] if TH["name"] != "minimal" else (236, 236, 238), outline=TH["ink"], width=TH["lw"])
    lv = (h - 70) * level
    d.rounded_rectangle([x - w / 2 + 34, y + h / 2 - 34 - lv, x + w / 2 - 34, y + h / 2 - 34], radius=40,
                        fill=(110, 200, 240) if TH["name"] != "poster" else TH["acc2"])
    d.rectangle([x - 26, y - h / 2 - 40, x + 26, y - h / 2 + 6], fill=TH["ink"])


def satellite(img, x, y, ang, s=1.0):
    lay = Image.new("RGBA", (int(620 * s), int(300 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, cy = lay.width / 2, lay.height / 2
    gold = TH["acc2"] if TH["name"] != "minimal" else (210, 212, 218)
    d.rectangle([cx - 70 * s, cy - 70 * s, cx + 70 * s, cy + 70 * s], fill=gold, outline=TH["ink"], width=max(3, int(5 * s)))
    for sx in (-1, 1):
        x0 = cx + sx * 90 * s
        x1 = cx + sx * 300 * s
        d.rectangle([min(x0, x1), cy - 40 * s, max(x0, x1), cy + 40 * s], fill=TH["soft"] if TH["name"] == "poster" else TH["ink"])
        for kk in range(1, 6):
            xx = x0 + (x1 - x0) * kk / 6
            d.line([(xx, cy - 40 * s), (xx, cy + 40 * s)], fill=TH["soft"], width=3)
        d.line([(cx + sx * 70 * s, cy), (x0, cy)], fill=TH["ink"], width=max(3, int(6 * s)))
    lay = lay.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(lay, (int(x - lay.width / 2), int(y - lay.height / 2)), lay)


def flame_x(img, x, y, k):
    if k <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    a = int(255 * k)
    s = 0.7 + 0.3 * pop(k)
    d.polygon([(x, y - 110 * s), (x + 60 * s, y), (x + 40 * s, y + 70 * s), (x - 40 * s, y + 70 * s), (x - 60 * s, y)], fill=TH["acc2"] + (a,) if TH["name"] != "minimal" else (200, 200, 206, a))
    d.polygon([(x, y - 40 * s), (x + 25 * s, y + 20 * s), (x, y + 60 * s), (x - 25 * s, y + 20 * s)], fill=TH["acc"] + (a,))
    if k > 0.6:
        q = clamp((k - 0.6) / 0.4)
        d.line([(x - 100, y - 100), (x - 100 + 200 * q, y - 100 + 200 * q)], fill=TH["ink"] + (a,), width=16)
        if q >= 1:
            d.line([(x + 100, y - 100), (x - 100, y + 100)], fill=TH["ink"] + (a,), width=16)


def stopwatch(img, x, y, r, frac, val):
    d = ImageDraw.Draw(img)
    body = TH["bg"] if TH["name"] != "vhs" else (40, 30, 52)
    d.rectangle([x - 34, y - r - 70, x + 34, y - r + 10], fill=TH["ink"])
    d.ellipse([x - r - 16, y - r - 16, x + r + 16, y + r + 16], fill=TH["ink"])
    d.ellipse([x - r, y - r, x + r, y + r], fill=body)
    for k in range(60):
        a = k * math.pi / 30
        r0 = r * (0.86 if k % 5 else 0.78)
        d.line([(x + math.cos(a) * r0, y + math.sin(a) * r0), (x + math.cos(a) * r * 0.94, y + math.sin(a) * r * 0.94)], fill=TH["ink"], width=4 if k % 5 else 7)
    if frac > 0:
        d.pieslice([x - r * 0.7, y - r * 0.7, x + r * 0.7, y + r * 0.7], -90, -90 + 360 * frac, fill=TH["acc"] + ())
    a = -math.pi / 2 + frac * 2 * math.pi
    d.line([(x, y), (x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8)], fill=TH["ink"], width=10)
    d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=TH["ink"])
    text(img, (x, y + r * 0.42), val, F(TH["big"], 84 if TH["name"] != "minimal" else 64), TH["ink"] if TH["name"] != "vhs" else (255, 255, 255), stroke=0)


def bills(img, x, y, n, s=1.0):
    d = ImageDraw.Draw(img)
    g1 = (120, 190, 120) if TH["name"] != "poster" else TH["acc2"]
    for i in range(n):
        yy = y - i * 34 * s
        d.rectangle([x - 220 * s + i * 4, yy - 56 * s, x + 220 * s + i * 4, yy], fill=g1, outline=TH["ink"], width=4)
        d.ellipse([x - 26 * s + i * 4, yy - 46 * s, x + 26 * s + i * 4, yy - 10 * s], outline=TH["ink"], width=3)


def clock(img, x, y, r, t):
    d = ImageDraw.Draw(img)
    d.ellipse([x - r, y - r, x + r, y + r], fill=TH["bg"] if TH["name"] != "vhs" else (40, 30, 52), outline=TH["ink"], width=12)
    for k in range(12):
        a = k * math.pi / 6
        d.line([(x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8), (x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92)], fill=TH["ink"], width=6)
    a1, a2 = -math.pi / 2 + t * 9, -math.pi / 2 + t * 0.75
    d.line([(x, y), (x + math.cos(a1) * r * 0.75, y + math.sin(a1) * r * 0.75)], fill=TH["acc"], width=8)
    d.line([(x, y), (x + math.cos(a2) * r * 0.5, y + math.sin(a2) * r * 0.5)], fill=TH["ink"], width=12)
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=TH["ink"])


# ================================================================== marca «Ojo al dato» (21/10): narrador, subtítulos, cierre
BRAND = {"handle": "ojoaldato.ya", "yt": "ojoaldatoya", "name": "Ojo al dato",
         "icon": "/home/claude/shorts-ingenieria/marca/OJO_perfil_1080.png"}
MARK = (240, 72, 38)                          # rojo-anaranjado del marcador («como con fluorescente»)
OJO_BOX = (-15, 1165, 0.6)                     # x, y y escala del narrador (abajo a la izquierda, encima de los subtítulos)
POSES = ["point", "think", "point", "surprise", "smirk"]


def brand_icon():
    if "icon" not in _C:
        try:
            _C["icon"] = Image.open(BRAND["icon"]).convert("RGB")
        except Exception:
            _C["icon"] = None
    return _C["icon"]


def _speaking(t):
    import cine, pop as POP
    caps = cine.CAPS_[0]
    if caps is None:
        return False
    for t0, t1, words in POP.chunks_t(caps):
        if t0 - 0.05 <= t <= t1:
            return any(a - 0.03 <= t <= b + 0.06 for w, hl, a, b in words)
    return False


def _narr_fig(V, pose, t, lid, talk):
    import ojo
    look = {"think": (0.06, -0.05), "surprise": (0.03, 0.0)}.get(pose, (0.08, 0.0))
    # la mirada se mueve un poco sola (más natural que fija)
    look = (round(look[0] + 0.03 * math.sin(t * 0.9), 2), round(look[1] + 0.02 * math.sin(t * 0.6 + 1), 2))
    return ojo.figure(pose, getattr(V, "OJO_TRAJE", None), lid, look, talk)


def NARR(img, V, t, shots, si):
    """Ojo explicando todo el vídeo. Movimientos naturales (21/10, Iker): respira y se balancea un poco siempre,
    gesticula suave mientras habla, mira a los lados, parpadea a ratos irregulares y pasa de una pose a otra fundiendo."""
    name = shots[si]["name"]
    poses = getattr(V, "OJO_POSES", {})
    pose = poses.get(name) or POSES[si % len(POSES)]
    spk = _speaking(t)
    talk = round(0.7 * math.sin(t * 4.6) * (1 if spk else 0.15), 1)
    lid = 0.9 if ((t * 1.0) % 4.3) < 0.11 or ((t + 1.7) % 6.1) < 0.09 else 0.0
    f = _narr_fig(V, pose, t, lid, talk)
    # fundido con la pose del plano anterior
    dt = t - shots[si]["start"]
    if si > 0 and dt < 0.3:
        pname = shots[si - 1]["name"]
        ppose = poses.get(pname) or POSES[(si - 1) % len(POSES)]
        if ppose != pose:
            f0 = _narr_fig(V, ppose, t, lid, talk)
            f = Image.blend(f0, f, ease(clamp(dt / 0.3)))
    x, y, s = OJO_BOX
    breath = 1 + 0.012 * math.sin(t * 2.1)
    sway = 2.2 * math.sin(t * 1.25) + (1.5 * math.sin(t * 4.6) if spk else 0)
    bob = (3.5 * abs(math.sin(t * 4.6)) if spk else 0) + 2 * math.sin(t * 2.1)
    sc = s
    ff = f.resize((int(f.width * sc), int(f.height * sc * breath)), Image.BILINEAR)
    ff = ff.rotate(sway, center=(ff.width / 2, ff.height * 0.95), resample=Image.BICUBIC)
    img.paste(ff, (int(x + (f.width * s - ff.width) / 2), int(y + (f.height * s - ff.height) - bob)), ff)
    side_prop(img, t, x + f.width * s * 0.5 + 105, y + f.height * s * 0.18 - bob, pose)


PROPS = ["atom", "bulb", "!", "star", "?", "atom", "bulb", "!"]


def side_prop(img, t, cx, cy, pose=""):
    """Algo junto a la cabeza que aparece poco rato y va cambiando (21/10, Iker: «que no tenga la misma cosa todo el rato»)."""
    per, on = 5.5, 1.3
    slot, ph = int(t // per), t % per
    if ph > on or pose in ("think", "surprise"):
        return
    k = pop(clamp(ph / 0.25)) * (1 - ease(clamp((ph - on + 0.25) / 0.25)))
    if k <= 0.02:
        return
    kind = PROPS[slot % len(PROPS)]
    d = ImageDraw.Draw(img, "RGBA")
    r = 34 * k
    if kind == "atom":
        for a in range(3):
            ang = a * math.pi / 3 + t
            pts = [(cx + math.cos(u) * r * 1.3 * math.cos(ang) - math.sin(u) * r * 0.45 * math.sin(ang),
                    cy + math.cos(u) * r * 1.3 * math.sin(ang) + math.sin(u) * r * 0.45 * math.cos(ang)) for u in [i * 0.3 for i in range(22)]]
            d.line(pts, fill=(28, 28, 32), width=4)
        d.ellipse([cx - 7 * k, cy - 7 * k, cx + 7 * k, cy + 7 * k], fill=(230, 40, 40))
    elif kind == "bulb":
        d.ellipse([cx - r, cy - r * 1.1, cx + r, cy + r * 0.8], fill=(255, 214, 60), outline=(28, 28, 32), width=4)
        d.rectangle([cx - r * 0.4, cy + r * 0.7, cx + r * 0.4, cy + r * 1.15], fill=(140, 140, 150), outline=(28, 28, 32))
        for a in range(5):
            ang = -math.pi / 2 + (a - 2) * 0.5
            d.line([(cx + math.cos(ang) * r * 1.4, cy - r * 0.15 + math.sin(ang) * r * 1.4),
                    (cx + math.cos(ang) * r * 1.8, cy - r * 0.15 + math.sin(ang) * r * 1.8)], fill=(255, 190, 40), width=4)
    elif kind == "star":
        pts = []
        for i in range(10):
            rr = r * (1.2 if i % 2 == 0 else 0.5)
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        d.polygon(pts, fill=(255, 204, 48), outline=(28, 28, 32))
    else:
        d.text((cx, cy), kind, font=F(INTER_X, int(80 * k) + 1), fill=(230, 40, 40), anchor="mm")


def CAPTION(img, t, chunks, y=1580):
    """Subtítulos palabra a palabra. En el estilo minimal, las palabras clave van en blanco sobre un marcador
    rojo-anaranjado que se pinta de golpe («pum»); el resto en casi negro."""
    cur = next((c for c in chunks if c[0] - 0.02 <= t < c[1]), None)
    if not cur:
        return
    t0, t1, words = cur
    n = TH["name"]
    up = n != "minimal"
    d = ImageDraw.Draw(img)
    ws = [((w.upper() if up else w), hl, a) for w, hl, a, b in words]
    pad = 16 if n == "minimal" else 0
    size = TH["cap"][1]
    while True:
        fo = F(TH["cap"][0], size)
        sp = d.textlength(" ", font=fo)
        tw = sum(d.textlength(w, font=fo) + (2 * pad if hl else 0) for w, hl, _ in ws) + sp * (len(ws) - 1)
        if tw <= 1000 or size <= 30:
            break
        size -= 6
    x = W / 2 - tw / 2
    yy = 1580
    for j, (w, hl, a) in enumerate(ws):
        ww = d.textlength(w, font=fo)
        nxt_hl = j + 1 < len(ws) and ws[j + 1][1] and t >= ws[j + 1][2] - 0.04
        if t >= a - 0.04:
            k = ease(clamp((t - a + 0.04) / 0.12))
            if n == "minimal":
                if hl:
                    x0, x1 = x, x + ww + 2 * pad + (sp + 2 if nxt_hl else 0)     # palabras clave seguidas: un solo marcador
                    y0, y1 = yy - size * 0.62, yy + size * 0.52
                    xr = x0 + (x1 - x0) * clamp(k * 1.25)
                    d.polygon([(x0 + 6, y0), (xr, y0 - 4), (xr - 6, y1), (x0, y1 + 4)], fill=MARK)
                    d.text((x + pad, yy + (1 - k) * 10), w, font=fo, fill=(255, 255, 255), anchor="lm")
                else:
                    d.text((x, yy + (1 - k) * 14), w, font=fo, fill=(28, 28, 32), anchor="lm")
            else:
                d.text((x, yy + (1 - k) * 14), w, font=fo, fill=TH["cap_hl"] if hl else TH["cap_col"], anchor="lm",
                       stroke_width=TH["stroke"], stroke_fill=(30, 20, 40) if TH["stroke"] else None)
        x += ww + (2 * pad if hl else 0) + sp


def make_outro(traje=None):
    """Cierre de «Ojo al dato»: Ojo se despide (con el traje del vídeo), «¡Ojo al dato!», botones y el @."""
    def OUTRO_FN(img, u, D):
        import ojo
        out = Image.new("RGB", (W, H), TH["bg"])
        bg(out, u)
        n = TH["name"]
        talk = round(math.sin(u * 6) * 5) / 5
        f = ojo.figure("bye", traje, 0.9 if (u % 2.6) < 0.12 else 0.0, (0.0, 0.02), talk)
        k0 = pop(clamp(u / 0.4))
        sc = 1.15 * max(0.05, k0)
        ff = f.resize((int(f.width * sc), int(f.height * sc)), Image.BILINEAR)
        out.paste(ff, (int(540 - ff.width / 2), int(1180 - ff.height * 0.93)), ff)
        k1 = clamp((u - 0.25) / 0.35)
        if n == "minimal":
            fo = F(INTER_X, 120)
            dd = ImageDraw.Draw(out)
            if k1 > 0:
                a = int(255 * clamp(k1 * 2))
                tw_ = dd.textlength("¡Ojo al dato!", font=fo)
                lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
                ld = ImageDraw.Draw(lay)
                ld.text((540, 100), "¡Ojo al dato!", font=fo, fill=(20, 20, 22, a), anchor="mm")
                img_k = pop(k1)
                lay = lay.resize((W, max(1, int(200 * img_k))), Image.BILINEAR)
                out.paste(lay, (0, int(250 - lay.height / 2)), lay)
        else:
            big(out, 540, 250, "¡OJO AL DATO!", 150, TH["acc"], k1)
        d = ImageDraw.Draw(out, "RGBA")
        kb = ease(clamp((u - 0.6) / 0.3))
        if kb > 0:
            p1, p2 = u > 1.3, u > 1.9
            fo = F(INTER_B, 40) if n == "minimal" else F(*TH["lab"])
            for i, (txt, on) in enumerate((("Me gusta", p1), ("Siguiendo" if p2 else "+ Seguir", p2))):
                x = 300 + i * 480
                yb = 1300 + (1 - kb) * 40
                fill = MARK if on else ((255, 255, 255) if n == "minimal" else TH["bg"])
                tc = (255, 255, 255) if on else TH["ink"]
                sq = 0.94 if (on and ((1.3 < u < 1.45) if i == 0 else (1.9 < u < 2.05))) else 1.0
                w2, h2 = 200 * sq, 64 * sq
                d.rounded_rectangle([x - w2, yb - h2, x + w2, yb + h2], radius=int(h2), fill=fill, outline=TH["ink"], width=5)
                if i == 0:
                    hx, hy, hs = x - 120, yb, 22
                    hc = (255, 255, 255) if on else MARK
                    d.ellipse([hx - hs, hy - hs, hx, hy], fill=hc)
                    d.ellipse([hx, hy - hs, hx + hs, hy], fill=hc)
                    d.polygon([(hx - hs, hy - hs / 2), (hx + hs, hy - hs / 2), (hx, hy + hs)], fill=hc)
                    d.text((x + 24, yb), txt, font=fo, fill=tc, anchor="mm")
                else:
                    d.text((x, yb), txt, font=fo, fill=tc, anchor="mm")
        hx_ = ease(clamp((u - 0.9) / 0.4))
        if hx_ > 0:
            text(out, (540, 1440), "@" + BRAND["handle"], F(INTER, 44) if n == "minimal" else F(*TH["sub"]), TH["soft"], alpha=int(255 * hx_), stroke=0)
        return out
    return OUTRO_FN
