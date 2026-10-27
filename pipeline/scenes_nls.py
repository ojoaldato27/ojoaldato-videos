"""Escenas de la cuenta Ojo al dato. Todo dibujado con código (sin material de terceros)."""
import math
import random
import render as R
from render import W, ease, prog, lerp, mix, clamp, font, arrow


def C(k):
    return R.C[k]


def neon():
    return R.CURRENT_THEME == "neon"


def paper():
    return R.CURRENT_THEME == "paper"


PAL = {
    "panel": {"paper": (226, 216, 196), "x": (22, 26, 34)},
    "grid1": {"paper": (200, 188, 164), "x": (40, 44, 54)},
    "grid2": {"paper": (200, 188, 164), "x": (52, 56, 66)},
    "faint": {"paper": (150, 138, 118), "x": (95, 98, 108)},
    "wind": {"paper": (40, 90, 160), "x": (77, 216, 255)},
    "outline": {"paper": (90, 80, 66), "x": None},
}


def pal(name):
    return PAL[name]["paper" if paper() else "x"]


def nf(col, a=70):
    """Relleno translúcido en el estilo neón; sólido en el resto."""
    return tuple(col[:3]) + (a,) if neon() else col


def tcenter(d, y, txt, size, col, weight="Black"):
    hook = getattr(R, "LABEL_FONT", None)
    if hook:
        f = hook(size, weight)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col)
        return
    if neon():
        weight = "Mono"
        size = int(size * 0.85)
    if paper():
        import styles
        f = styles.serif(int(size * 1.1))
    else:
        f = font(size, weight)
    d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col)


def label(d, x, y, txt, size, col, weight="Semi", anchor="l"):
    hook = getattr(R, "LABEL_FONT", None)
    if neon() and not hook:
        weight = "Mono"
        size = int(size * 0.9)
    if hook:
        f = hook(size, weight)
    elif paper():
        import styles
        f = styles.serif(int(size * 1.05))
    else:
        f = font(size, weight)
    w = d.textlength(txt, font=f)
    x0 = x - w / 2 if anchor == "c" else (x - w if anchor == "r" else x)
    d.text((x0, y), txt, font=f, fill=col)


def polyline_partial(d, pts, k, col, width):
    """Dibuja la fracción k (0-1) de una polilínea; devuelve el punto final y el ángulo."""
    if k <= 0 or len(pts) < 2:
        return pts[0], 0.0
    n = (len(pts) - 1) * clamp(k)
    i = int(n)
    part = pts[: i + 1]
    if i < len(pts) - 1:
        a, b = pts[i], pts[i + 1]
        f = n - i
        part.append((lerp(a[0], b[0], f), lerp(a[1], b[1], f)))
    if len(part) >= 2:
        d.line(part, fill=col, width=width, joint="curve")
    p, q = part[-2], part[-1]
    return part[-1], math.atan2(q[1] - p[1], q[0] - p[0])


def dashed(d, pts, col, width, dash=22, gap=16):
    acc, on = 0.0, True
    for a, b in zip(pts, pts[1:]):
        seg = math.dist(a, b)
        pos = 0.0
        while pos < seg:
            step = min((dash if on else gap) - acc, seg - pos)
            if on:
                t0, t1 = pos / seg, (pos + step) / seg
                d.line([(lerp(a[0], b[0], t0), lerp(a[1], b[1], t0)),
                        (lerp(a[0], b[0], t1), lerp(a[1], b[1], t1))], fill=col, width=width)
            pos += step
            acc += step
            if acc >= (dash if on else gap) - 1e-6:
                acc, on = 0.0, not on


def plane(d, x, y, ang, s, col):
    """Avión esquemático visto desde arriba, apuntando según ang."""
    shape = [(1.0, 0), (0.55, 0.08), (0.15, 0.08), (-0.25, 0.62), (-0.42, 0.62), (-0.18, 0.08),
             (-0.62, 0.08), (-0.78, 0.30), (-0.9, 0.30), (-0.82, 0), (-0.9, -0.30), (-0.78, -0.30),
             (-0.62, -0.08), (-0.18, -0.08), (-0.42, -0.62), (-0.25, -0.62), (0.15, -0.08), (0.55, -0.08)]
    ca, sa = math.cos(ang), math.sin(ang)
    d.polygon([(x + s * (px * ca - py * sa), y + s * (px * sa + py * ca)) for px, py in shape], fill=col)


# ---------------- geografía ----------------
def vec(lat, lon):
    la, lo = math.radians(lat), math.radians(lon)
    return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))


def great_circle(a, b, n=80):
    va, vb = vec(*a), vec(*b)
    ang = math.acos(max(-1, min(1, sum(x * y for x, y in zip(va, vb)))))
    out = []
    for i in range(n + 1):
        t = i / n
        w1, w2 = math.sin((1 - t) * ang) / math.sin(ang), math.sin(t * ang) / math.sin(ang)
        p = [w1 * x + w2 * y for x, y in zip(va, vb)]
        out.append((math.degrees(math.asin(p[2])), math.degrees(math.atan2(p[1], p[0]))))
    return out


MAP = {"x0": 90, "y0": 330, "x1": 990, "y1": 960, "lon0": -135, "lon1": 15, "lat0": 18, "lat1": 72}


def merc_y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def map_xy(lat, lon):
    m = MAP
    x = m["x0"] + (lon - m["lon0"]) / (m["lon1"] - m["lon0"]) * (m["x1"] - m["x0"])
    yt, yb = merc_y(m["lat1"]), merc_y(m["lat0"])
    y = m["y0"] + (yt - merc_y(lat)) / (yt - yb) * (m["y1"] - m["y0"])
    return x, y


def sc_mercator_route(d, t, p, img):
    a, b = p["from"], p["to"]
    k = ease(t / 0.6)
    m = MAP
    d.rounded_rectangle([m["x0"], m["y0"], m["x1"], m["y1"]], radius=24,
                        fill=nf(mix(C("bg"), pal("panel"), k), 160),
                        outline=mix(C("bg"), C("comp") if neon() else (pal("outline") or C("grid")), k), width=3)
    grid = mix(C("bg"), pal("grid1"), k)
    for lon in range(-130, 16, 10):
        x, _ = map_xy(0, lon)
        d.line([(x, m["y0"] + 4), (x, m["y1"] - 4)], fill=grid, width=1)
    for lat in range(20, 71, 10):
        _, y = map_xy(lat, 0)
        d.line([(m["x0"] + 4, y), (m["x1"] - 4, y)], fill=grid, width=1)
    for name, la, lo in p.get("regions", []):
        x, y = map_xy(la, lo)
        label(d, x, y, name, 30, mix(C("bg"), pal("faint"), k), "Semi", "c")
    # recta del mapa (loxodrómica)
    pa, pb = map_xy(*a), map_xy(*b)
    s1 = ease(prog(t, 0.6, 1.8))
    if s1 > 0:
        dashed(d, [pa, (lerp(pa[0], pb[0], s1), lerp(pa[1], pb[1], s1))], C("muted"), 6)
    # ruta real (ortodrómica)
    s2 = prog(t, p.get("arc_at", 2.4), p.get("arc_at", 2.4) + 2.6)
    if s2 > 0:
        pts = [map_xy(la, lo) for la, lo in great_circle(a, b)]
        end, ang = polyline_partial(d, pts, ease(s2), C("accent"), 9)
        plane(d, end[0], end[1], ang, 34, C("fg"))
    for (la, lo), nm in ((a, p["from_name"]), (b, p["to_name"])):
        x, y = map_xy(la, lo)
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=C("fg"))
        label(d, x, y + 22, nm, 36, mix(C("bg"), C("fg"), k), "Black", "c")


def sc_globe_route(d, t, p, img):
    cx, cy, r = 540, 660, 340
    k = ease(t / 0.7)
    lat0, lon0 = math.radians(p.get("view_lat", 50)), math.radians(p.get("view_lon", -60))

    def proj(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        x = math.cos(la) * math.sin(lo - lon0)
        y = math.cos(lat0) * math.sin(la) - math.sin(lat0) * math.cos(la) * math.cos(lo - lon0)
        z = math.sin(lat0) * math.sin(la) + math.cos(lat0) * math.cos(la) * math.cos(lo - lon0)
        return cx + r * x, cy - r * y, z

    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=nf(mix(C("bg"), pal("panel"), k), 150),
              outline=mix(C("bg"), C("comp") if neon() else C("fg"), k), width=5)
    grid = mix(C("bg"), pal("grid2"), k)
    for lat in range(-60, 81, 20):
        seg = []
        for lon in range(-180, 181, 4):
            x, y, z = proj(lat, lon)
            if z > 0:
                seg.append((x, y))
            elif len(seg) > 1:
                d.line(seg, fill=grid, width=2)
                seg = []
            else:
                seg = []
        if len(seg) > 1:
            d.line(seg, fill=grid, width=2)
    for lon in range(-180, 180, 20):
        seg = []
        for lat in range(-90, 91, 3):
            x, y, z = proj(lat, lon)
            if z > 0:
                seg.append((x, y))
            elif len(seg) > 1:
                d.line(seg, fill=grid, width=2)
                seg = []
            else:
                seg = []
        if len(seg) > 1:
            d.line(seg, fill=grid, width=2)
    a, b = p["from"], p["to"]
    s = ease(prog(t, 0.8, 3.0))
    pts = [proj(la, lo)[:2] for la, lo in great_circle(a, b)]
    if s > 0:
        end, ang = polyline_partial(d, pts, s, C("accent"), 10)
        plane(d, end[0], end[1], ang, 32, C("fg"))
    for (la, lo), nm in ((a, p["from_name"]), (b, p["to_name"])):
        x, y, _ = proj(la, lo)
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=C("fg"))
        label(d, x, y + 20, nm, 34, mix(C("bg"), C("fg"), k), "Black", "c")


def sc_distance_bars(d, t, p, img):
    rows = p["rows"]  # [texto, km, es_acento]
    mx = max(r[1] for r in rows)
    for i, (txt, km, acc) in enumerate(rows):
        y = 470 + i * 230
        q = ease(prog(t, 0.2 + i * 0.6, 1.4 + i * 0.6))
        col = C("accent") if acc else C("muted")
        label(d, 110, y, txt, 40, mix(C("bg"), C("fg"), q), "Semi")
        w = (860 * km / mx) * q
        d.rounded_rectangle([110, y + 64, 110 + max(w, 1), y + 134], radius=14,
                            fill=nf(mix(C("bg"), col, q), 90), outline=mix(C("bg"), col, q), width=4)
        val = f"{int(km * q):,} km".replace(",", ".")
        label(d, 110, y + 146, val, 46, mix(C("bg"), col, q), "Black")
    if "note" in p and t > 2.2:
        q = ease(prog(t, 2.2, 2.9))
        tcenter(d, 960, p["note"], 64, mix(C("bg"), C("accent"), q))


# ---------------- cielo ----------------
RAINBOW = [(255, 70, 70), (255, 150, 60), (255, 220, 70), (90, 220, 110), (70, 160, 255), (140, 100, 255)]


def sc_sun_scatter(d, t, p, img):
    k = ease(t / 0.6)
    sx, sy = 190, 400
    d.ellipse([sx - 95, sy - 95, sx + 95, sy + 95], fill=mix(C("bg"), (255, 214, 90), k))
    ex, ey = 960, 1010
    L = math.dist((sx, sy), (ex, ey))
    ux, uy = (ex - sx) / L, (ey - sy) / L
    nx, ny = -uy, ux
    s = ease(prog(t, 0.4, 1.4))
    for i, col in enumerate(RAINBOW):
        off = (i - 2.5) * 9
        x0, y0 = sx + ux * 110 + nx * off, sy + uy * 110 + ny * off
        d.line([(x0, y0), (x0 + ux * (L - 140) * s, y0 + uy * (L - 140) * s)], fill=col, width=7)
    # moléculas de aire y azul dispersado
    rng = random.Random(4)
    mols = [(0.35, -60), (0.5, 70), (0.62, -40), (0.75, 55), (0.86, -70)]
    sc = prog(t, 1.6, 3.4)
    for j, (f, off) in enumerate(mols):
        mx_ = sx + ux * L * f + nx * off
        my_ = sy + uy * L * f + ny * off
        d.ellipse([mx_ - 14, my_ - 14, mx_ + 14, my_ + 14], outline=mix(C("bg"), C("fg"), k), width=4)
        if sc > 0:
            for a_ in range(6):
                ang = rng.uniform(0, 2 * math.pi)
                ln = 90 * ease(clamp(sc * 1.4 - j * 0.12))
                if ln > 5:
                    arrow(d, mx_, my_, mx_ + math.cos(ang) * ln, my_ + math.sin(ang) * ln,
                          (70, 160, 255), 5, 16)
    if t > 0.8:
        label(d, sx, sy + 110, "Sol", 34, mix(C("bg"), C("fg"), ease(prog(t, 0.8, 1.3))), "Black", "c")


def sc_scatter_bars(d, t, p, img):
    base = 1000
    blue, red = p.get("blue", 5.98), 1.0
    q = ease(prog(t, 0.3, 1.8))
    hmax = 560
    for x, val, col, nm, nmx in ((330, blue, (70, 160, 255), "Azul", "450 nm"),
                                 (750, red, (255, 80, 70), "Rojo", "700 nm")):
        h = hmax * val / blue * q
        d.rounded_rectangle([x - 110, base - h, x + 110, base], radius=18, fill=col)
        label(d, x, base + 20, nm, 46, C("fg"), "Black", "c")
        label(d, x, base + 76, nmx, 32, C("muted"), "Semi", "c")
    if t > 1.8:
        a = ease(prog(t, 1.8, 2.4))
        label(d, 330, base - hmax - 80, "x6", 64, mix(C("bg"), C("accent"), a), "Black", "c")
    label(d, 540, 300, "Cuánto se dispersa cada color", 40, C("muted"), "Semi", "c")


def sc_sunset_path(d, t, p, img):
    k = prog(t, 0.6, 3.6)
    # cielo que pasa de azul a naranja
    sky = mix((40, 90, 170), (230, 110, 50), ease(k))
    d.rectangle([60, 300, 1020, 1040], fill=mix(C("bg"), sky, 0.55))
    # Tierra y atmósfera
    ecx, ecy, er = 540, 2150, 1300
    d.ellipse([ecx - er - 120, ecy - er - 120, ecx + er + 120, ecy + er + 120], fill=mix(C("bg"), (120, 170, 230), 0.35))
    d.ellipse([ecx - er, ecy - er, ecx + er, ecy + er], fill=(30, 60, 45))
    ox, oy = 540, ecy - er
    # posición del sol: de arriba al horizonte
    ang = lerp(-math.pi / 2, -0.08, ease(k))
    sx, sy = ox + 900 * math.cos(ang) + 0, oy + 700 * math.sin(ang)
    sx = lerp(ox, 980, ease(k))
    sy = lerp(360, oy - 40, ease(k))
    d.ellipse([sx - 50, sy - 50, sx + 50, sy + 50], fill=mix((255, 230, 120), (255, 120, 50), ease(k)))
    # rayo hasta el observador; tramo dentro de la atmósfera resaltado
    d.line([(sx, sy), (ox, oy)], fill=mix((255, 240, 180), (255, 140, 60), ease(k)), width=8)
    d.ellipse([ox - 16, oy - 32, ox + 16, oy], fill=C("fg"))
    label(d, ox, oy + 10, "Tú", 34, C("fg"), "Black", "c")
    atm_len = 1 + 37 * ease(k) ** 3
    tag = "Mediodía" if k < 0.3 else ("Atardecer" if k > 0.85 else "")
    if tag:
        label(d, 540, 330, tag, 48, C("fg"), "Black", "c")


# ---------------- Júpiter ----------------
def sc_jupiter_fall(d, t, p, img):
    cx, cy, r = 540, 720, 360
    k = ease(t / 0.6)
    if neon():
        layers = [(1.0, (255, 170, 90)), (0.86, (255, 120, 70)), (0.6, (170, 110, 255)), (0.2, (0, 229, 255))]
    else:
        layers = [(1.0, (196, 150, 100)), (0.86, (150, 105, 70)), (0.6, (90, 80, 110)), (0.2, (120, 120, 125))]
    cut = p.get("cut", True)
    for f, col in layers:
        rr = r * f
        ol = mix(C("bg"), col, k) if neon() else None
        if cut:
            d.pieslice([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=nf(mix(C("bg"), col, k), 55), outline=ol, width=5)
        else:
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=nf(mix(C("bg"), col, k), 55), outline=ol, width=5)
    if cut:
        d.line([(cx - r - 4, cy), (cx + r + 4, cy)], fill=mix(C("bg"), C("comp") if neon() else C("bg"), k), width=4)
    # bandas en la atmósfera
    for i, yy in enumerate(range(int(cy - r + 30), int(cy - r * 0.86), 18)):
        half = math.sqrt(max(0, r ** 2 - (cy - yy) ** 2))
        d.line([(cx - half, yy), (cx + half, yy)], fill=mix(C("bg"), (225, 190, 140), k * 0.6), width=4)
    if p.get("labels") and t > 0.8:
        q = ease(prog(t, 0.8, 1.6))
        col = mix(C("bg"), C("fg"), q)
        fs = [f for _, f in p["labels"]] + [0.0]
        for i, (txt, f) in enumerate(p["labels"]):
            ymid = cy - r * (f + fs[i + 1]) / 2
            fsz = 28 if i == 0 else 32
            ft = font(fsz, "Black")
            x0, y0 = cx + 24, ymid - fsz * 0.6
            for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                d.text((x0 + ox, y0 + oy), txt, font=ft, fill=(0, 0, 0))
            d.text((x0, y0), txt, font=ft, fill=col)
    # caída
    fall = p.get("fall")
    if fall:
        s = ease(prog(t, fall[0], fall[1]))
        y = lerp(cy - r - 160, cy - r * 0.25, s)
        x = cx - 60
        for i in range(8):
            tt = clamp(s - i * 0.02)
            yy = lerp(cy - r - 160, cy - r * 0.25, tt)
            rr = 10 - i
            if rr > 1:
                d.ellipse([x - rr, yy - rr, x + rr, yy + rr], fill=mix(C("bg"), C("fg"), 0.8 - i * 0.09))
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=C("accent"))
        # medidor de presión
        bx = 120
        label(d, bx, 1060, "Presión", 30, C("muted"), "Semi")
        d.rounded_rectangle([bx, 1105, bx + 840, 1135], radius=15, outline=C("muted"), width=3)
        d.rounded_rectangle([bx + 4, 1109, bx + 4 + 832 * s ** 2, 1131], radius=11, fill=(255, 107, 61))


def sc_gravity(d, t, p, img):
    q = ease(prog(t, 0.2, 1.2))
    for x, nm, g, col in ((300, "Tierra", 1.0, (70, 160, 255)), (780, "Júpiter", 2.53, (196, 150, 100))):
        rr = 90 if nm == "Tierra" else 170
        d.ellipse([x - rr, 560 - rr, x + rr, 560 + rr], fill=nf(mix(C("bg"), col, q), 70), outline=mix(C("bg"), col, q), width=6)
        label(d, x, 760, nm, 46, C("fg"), "Black", "c")
        h = 140 * g * q
        arrow(d, x, 830, x, 830 + h, C("accent"), 14, 40)
    if t > 1.2:
        a = ease(prog(t, 1.2, 1.8))
        label(d, 900, 940, "x2,5", 72, mix(C("bg"), C("accent"), a), "Black", "c")


def sc_outro_nls(d, t, p, img):
    k = ease(t / 0.7)
    s = lerp(300, 460, k)
    R.eye_icon(d, 540, 760, s, mix(C("bg"), C("fg"), k), mix(C("bg"), (255, 210, 63), k), (14, 15, 18))
    if t > 0.6:
        q = ease(prog(t, 0.6, 1.2))
        tcenter(d, 1010, p.get("handle", "@ojoaldato.ya"), 52, mix(C("bg"), C("fg"), q), "Black")


def sc_hook_plane(d, t, p, img):
    k = ease(t / 0.4)
    pts = [(lerp(-80, 1160, i / 60), 760 - 260 * math.sin(math.pi * i / 60)) for i in range(61)]
    dashed(d, pts, mix(C("bg"), C("muted"), k), 5)
    s = clamp(t / 2.5)
    end, ang = polyline_partial(d, pts, 0.15 + 0.7 * s, C("accent"), 8)
    plane(d, end[0], end[1], ang, 70, C("fg"))


def sc_hook_sky(d, t, p, img):
    k = ease(t / 0.5)
    for i in range(14):
        y0 = 300 + i * 52
        col = mix((40, 90, 170), (230, 110, 50), i / 13)
        d.rectangle([60, y0, 1020, y0 + 52], fill=mix(C("bg"), col, k))
    tcenter(d, 520, "¿?", 230, mix(C("bg"), C("fg"), k))


# ---------------- nuevas escenas (versión larga) ----------------
def sc_area_compare(d, t, p, img):
    """Dos círculos con área proporcional (p.ej. Groenlandia vs África)."""
    a_nm, a_val, b_nm, b_val = p["a"][0], p["a"][1], p["b"][0], p["b"][1]
    rb = 270
    ra = rb * math.sqrt(a_val / b_val)
    k = ease(prog(t, 0.2, 1.4))
    # primero "como se ve en el mapa": mismo tamaño
    phase = ease(prog(t, 1.8, 3.2))
    ra_now = lerp(rb * 0.82, ra, phase)
    cxa, cxb, cy = 230, 740, 700
    cb, ca = (255, 170, 90), (150, 220, 255)
    d.ellipse([cxb - rb, cy - rb, cxb + rb, cy + rb], fill=nf(mix(C("bg"), cb, k), 60), outline=mix(C("bg"), cb, k), width=6)
    d.ellipse([cxa - ra_now, cy - ra_now, cxa + ra_now, cy + ra_now], fill=nf(mix(C("bg"), ca, k), 60), outline=mix(C("bg"), ca, k), width=6)
    label(d, cxb, cy - 20, b_nm, 46, mix(C("bg"), C("fg") if neon() else C("bg"), k), "Black", "c")
    label(d, cxa, cy + max(ra_now, 40) + 20, a_nm, 40, mix(C("bg"), C("fg"), k), "Black", "c")
    tag = "En el mapa" if phase < 0.5 else "En la realidad"
    tcenter(d, 300, tag, 52, mix(C("bg"), C("accent"), k))
    if phase > 0.95:
        q = ease(prog(t, 3.2, 3.8))
        tcenter(d, 1060, p.get("note", ""), 56, mix(C("bg"), C("fg"), q))


def sc_jet_stream(d, t, p, img):
    k = ease(t / 0.6)
    for row in range(5):
        y0 = 420 + row * 120
        pts = [(x, y0 + 30 * math.sin(x / 120 + t * 3 + row)) for x in range(60, 1021, 20)]
        col = mix(C("bg"), pal("wind"), k * (0.35 + 0.13 * row))
        d.line(pts, fill=col, width=6, joint="curve")
        hx = 60 + ((t * 260 + row * 190) % 960)
        hy = y0 + 30 * math.sin(hx / 120 + t * 3 + row)
        arrow(d, hx - 50, hy, hx, hy, mix(C("bg"), pal("wind"), k), 6, 22)
    px = lerp(140, 900, ease(prog(t, 0.5, 4.5)))
    py = 660 + 30 * math.sin(px / 120 + t * 3 + 2)
    plane(d, px, py, 0.0, 60, C("fg"))
    label(d, 540, 1000, p.get("label", "Corriente en chorro"), 40, mix(C("bg"), C("muted"), k), "Semi", "c")


def sc_great_circle_north(d, t, p, img):
    """Mapa con el arco completo y el punto más al norte señalado."""
    sc_mercator_route(d, t + 6, p, img)
    a, b = p["from"], p["to"]
    pts = great_circle(a, b)
    top = max(pts, key=lambda q: q[0])
    x, y = map_xy(*top)
    q = ease(prog(t, 0.4, 1.2))
    if q > 0:
        r = 22 + 8 * math.sin(t * 6)
        d.ellipse([x - r, y - r, x + r, y + r], outline=mix(C("bg"), C("accent"), q), width=6)
        label(d, x, y - 80, p.get("north_label", ""), 38, mix(C("bg"), C("accent"), q), "Black", "c")


def sc_spectrum_eye(d, t, p, img):
    k = ease(t / 0.6)
    x0, x1, y0, y1 = 120, 960, 600, 700
    for i in range(x1 - x0):
        u = i / (x1 - x0)  # 0 violeta (400 nm) -> 1 rojo (700 nm)
        hue_pts = [(0.0, (140, 80, 255)), (0.17, (70, 120, 255)), (0.33, (60, 200, 255)),
                   (0.5, (80, 220, 110)), (0.67, (240, 230, 70)), (0.83, (255, 150, 50)), (1.0, (240, 50, 50))]
        for (ua, ca), (ub, cb) in zip(hue_pts, hue_pts[1:]):
            if ua <= u <= ub:
                col = mix(ca, cb, (u - ua) / (ub - ua))
                break
        d.line([(x0 + i, y0), (x0 + i, y1)], fill=mix(C("bg"), col, k))
    label(d, x0, y1 + 16, "Violeta", 34, C("muted"), "Semi")
    label(d, x1, y1 + 16, "Rojo", 34, C("muted"), "Semi", "r")
    # sensibilidad del ojo (curva con pico en el verde, ~555 nm)
    q = ease(prog(t, 1.2, 2.6))
    if q > 0:
        pts = []
        for i in range(0, x1 - x0 + 1, 6):
            nm = 400 + 300 * i / (x1 - x0)
            v = math.exp(-((nm - 555) / 55) ** 2)
            pts.append((x0 + i, y0 - 30 - 300 * v))
        polyline_partial(d, pts, q, C("fg"), 7)
        label(d, 540, 200, "Lo que mejor ve tu ojo", 40, mix(C("bg"), C("fg"), q), "Black", "c")


def sc_cloud_white(d, t, p, img):
    k = ease(t / 0.6)
    cx, cy = 540, 640
    for dx, dy, r in ((-150, 30, 120), (-40, -40, 160), (110, 10, 130), (210, 60, 90), (-240, 80, 80)):
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=nf(mix(C("bg"), (240, 240, 245), k), 200))
    rng = random.Random(9)
    q = prog(t, 0.8, 2.6)
    if q > 0:
        for i in range(18):
            ang = rng.uniform(0, 2 * math.pi)
            col = RAINBOW[i % len(RAINBOW)]
            ln = 130 * ease(q)
            sx, sy = cx + math.cos(ang) * 230, cy + math.sin(ang) * 150
            arrow(d, sx, sy, sx + math.cos(ang) * ln, sy + math.sin(ang) * ln, col, 6, 20)


def sc_mars_sky(d, t, p, img):
    k = ease(t / 0.6)
    panels = [("Tierra", (60, 120, 210), (240, 130, 60), 240), ("Marte", (200, 150, 100), (90, 140, 210), 650)]
    for nm, day, dusk, x in panels:
        w = 300
        for i in range(12):
            u = i / 11
            d.rectangle([x, 380 + i * 30, x + w, 410 + i * 30], fill=mix(C("bg"), day, k))
            d.rectangle([x, 760 + i * 30, x + w, 790 + i * 30],
                        fill=mix(C("bg"), mix(day, dusk, 0.3 + 0.7 * u), k))
        r = 34
        d.ellipse([x + w / 2 - r, 1060 - 2 * r, x + w / 2 + r, 1060], fill=mix(C("bg"), (255, 240, 200), k))
        label(d, x + w / 2, 310, nm, 46, mix(C("bg"), C("fg"), k), "Black", "c")
    label(d, 40, 520, "Día", 30, C("muted"), "Semi")
    label(d, 40, 900, "Atardecer", 30, C("muted"), "Semi")


def sc_jupiter_earths(d, t, p, img):
    k = ease(t / 0.6)
    cx, cy, r = 540, 700, 380
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=nf(mix(C("bg"), (196, 150, 100), k), 50), outline=mix(C("bg"), (255, 170, 90), k), width=6)
    n_show = int(p.get("count", 1321) * ease(prog(t, 0.6, 4.0)))
    er = 9
    cnt = 0
    y = cy - r + er
    while y < cy + r and cnt < n_show:
        half = math.sqrt(max(0, r ** 2 - (y - cy) ** 2)) - er
        x = cx - half
        while x <= cx + half and cnt < n_show:
            d.ellipse([x - er + 1, y - er + 1, x + er - 1, y + er - 1], fill=(0, 229, 255) if neon() else (70, 160, 255))
            x += 2 * er
            cnt += 1
        y += 2 * er
    label(d, 540, 1110, f"{n_show:,}".replace(",", ".") + " Tierras", 60, C("accent"), "Black", "c")


def sc_jupiter_spin(d, t, p, img):
    k = ease(t / 0.6)
    cx, cy, r = 540, 650, 300
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=nf(mix(C("bg"), (196, 150, 100), k), 50), outline=mix(C("bg"), (255, 170, 90), k), width=6)
    for i in range(-5, 6):
        yy = cy + i * 52
        half = math.sqrt(max(0, r ** 2 - (yy - cy) ** 2))
        off = (t * 120 + i * 37) % 80
        for xs in range(int(cx - half), int(cx + half), 80):
            x0 = xs + off
            if x0 + 40 < cx + half:
                d.line([(x0, yy), (x0 + 40, yy)], fill=mix(C("bg"), (255, 140, 70) if neon() else (150, 100, 65), k), width=8)
    # reloj
    ccx, ccy, cr = 540, 1080, 70
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=C("fg"), width=6)
    ang = -math.pi / 2 + 2 * math.pi * ease(prog(t, 0.5, 4.5)) * (9.93 / 12)
    d.line([(ccx, ccy), (ccx + cr * 0.75 * math.cos(ang), ccy + cr * 0.75 * math.sin(ang))], fill=C("accent"), width=8)
    label(d, ccx + 110, ccy - 30, "9 h 56 min", 52, C("accent"), "Black")


def sc_red_spot(d, t, p, img):
    k = ease(t / 0.6)
    cx, cy, r = 600, 700, 520
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=nf(mix(C("bg"), (196, 150, 100), k), 45), outline=mix(C("bg"), (255, 170, 90), k), width=6)
    sx, sy, sw, sh = 520, 760, 230, 130
    d.ellipse([sx - sw / 2, sy - sh / 2, sx + sw / 2, sy + sh / 2], fill=nf(mix(C("bg"), (230, 80, 60), k), 140), outline=mix(C("bg"), (255, 90, 70), k), width=5)
    q = ease(prog(t, 1.0, 2.2))
    er = sw / 2 * (12742 / 16500)
    ex = lerp(160, sx, q)
    d.ellipse([ex - er, sy - er, ex + er, sy + er], outline=(70, 160, 255), width=7)
    if q > 0.9:
        label(d, sx, sy + sh / 2 + 24, "La Tierra", 36, C("fg"), "Black", "c")


SCENES = {
    "mercator_route": sc_mercator_route, "globe_route": sc_globe_route,
    "distance_bars": sc_distance_bars, "sun_scatter": sc_sun_scatter,
    "scatter_bars": sc_scatter_bars, "sunset_path": sc_sunset_path,
    "jupiter_fall": sc_jupiter_fall, "gravity": sc_gravity, "outro_nls": sc_outro_nls,
    "hook_plane": sc_hook_plane, "hook_sky": sc_hook_sky,
    "area_compare": sc_area_compare, "jet_stream": sc_jet_stream,
    "great_circle_north": sc_great_circle_north, "spectrum_eye": sc_spectrum_eye,
    "cloud_white": sc_cloud_white, "mars_sky": sc_mars_sky,
    "jupiter_earths": sc_jupiter_earths, "jupiter_spin": sc_jupiter_spin, "red_spot": sc_red_spot,
}
