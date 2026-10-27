"""Escenas para los formatos del vídeo de aviones (Viaje en directo, Top 5, Quiz).
Todo dibujado con código; contornos de costa de geo.py."""
import math
import render as R
from render import W, ease, prog, lerp, mix, clamp, font, arrow
import geo
from scenes_nls import great_circle, plane, dashed, polyline_partial, label, tcenter, C

MAD = (40.4168, -3.7038)
LAX = (34.0522, -118.2437)
JFK = (40.6413, -73.7781)
LHR = (51.4700, -0.4543)
ROUTE = great_circle(MAD, LAX, 160)          # (lat, lon)
ROUTE_KM = 9363

PALETTES = {
    "neon": dict(land_fill=(26, 30, 74), land_line=(92, 128, 230), cyan=(0, 229, 255), orange=(255, 150, 70),
                 red=(255, 80, 90), green=(60, 230, 140), panel=(8, 8, 26), track=(40, 40, 90), grat=(34, 34, 80),
                 globe=(12, 16, 46), g_fill=(20, 60, 90), a_fill=(90, 50, 30), region=(140, 150, 220),
                 dash=(200, 200, 230), bag=(90, 40, 110), bag_line=(230, 120, 255), win2=(140, 150, 220),
                 win3=(90, 100, 170), cabin=(20, 24, 60), lw=3),
    "pop": dict(land_fill=(255, 255, 255), land_line=(22, 20, 35), cyan=(25, 90, 230), orange=(235, 90, 30),
                red=(220, 30, 60), green=(20, 160, 90), panel=(255, 255, 255), track=(235, 190, 90),
                grat=(245, 200, 90), globe=(255, 246, 214), g_fill=(130, 205, 255), a_fill=(255, 140, 90),
                region=(110, 80, 30), dash=(22, 20, 35), bag=(235, 60, 120), bag_line=(22, 20, 35),
                win2=(60, 60, 80), win3=(110, 110, 130), cabin=(255, 255, 255), lw=5),
    "show": dict(land_fill=(64, 26, 120), land_line=(205, 140, 255), cyan=(255, 90, 210), orange=(255, 170, 60),
                 red=(255, 70, 90), green=(70, 240, 150), panel=(28, 8, 56), track=(70, 30, 110), grat=(48, 18, 86),
                 globe=(34, 12, 68), g_fill=(40, 70, 130), a_fill=(110, 50, 40), region=(200, 160, 240),
                 dash=(230, 210, 255), bag=(120, 40, 140), bag_line=(255, 140, 230), win2=(200, 160, 240),
                 win3=(140, 100, 200), cabin=(36, 14, 72), lw=3),
}
P = dict(PALETTES["neon"])


def set_palette(name):
    P.clear()
    P.update(PALETTES.get(name, PALETTES["neon"]))


def mY(lat):
    lat = max(-85, min(85, lat))
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


class Cam:
    def __init__(self, lonc, latc, s, cx=540, cy=700):
        self.lonc, self.latc, self.s, self.cx, self.cy = lonc, latc, s, cx, cy

    def xy(self, lon, lat):
        return (self.cx + (lon - self.lonc) * self.s, self.cy - (mY(lat) - mY(self.latc)) * self.s)


def cam_lerp(c0, c1, k):
    return Cam(lerp(c0[0], c1[0], k), lerp(c0[1], c1[1], k), lerp(c0[2], c1[2], k))


def draw_land(d, cam, k=1.0, polys=None, fill=None, line=None, width=None):
    width = width or P["lw"]
    fill = fill or P["land_fill"]
    line = line or P["land_line"]
    for poly in (polys or geo.LAND):
        pts = [cam.xy(lo, la) for lo, la in poly]
        d.polygon(pts, fill=mix(R.C["bg"], fill, k), outline=mix(R.C["bg"], line, k), width=width)
    if polys is None:
        for poly in geo.SEAS:
            d.polygon([cam.xy(lo, la) for lo, la in poly], fill=R.C["bg"], outline=mix(R.C["bg"], line, k), width=width)


def graticule(d, cam, k, step=10):
    col = mix(R.C["bg"], P["grat"], k)
    for lon in range(-180, 181, step):
        x, _ = cam.xy(lon, 0)
        if -10 < x < W + 10:
            d.line([(x, 0), (x, 1920)], fill=col, width=1)
    for lat in range(-80, 81, step):
        _, y = cam.xy(0, lat)
        if -10 < y < 1930:
            d.line([(0, y), (W, y)], fill=col, width=1)


def route_pts(cam, n=None):
    pts = ROUTE if n is None else ROUTE[:n]
    return [cam.xy(lo, la) for la, lo in pts]


def city(d, cam, ll, name, k, below=True):
    x, y = cam.xy(ll[1], ll[0])
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=mix(R.C["bg"], R.C["fg"], k))
    label(d, x, y + (22 if below else -60), name, 34, mix(R.C["bg"], R.C["fg"], k), "Black", "c")


# ---------------- HUD tipo Flightradar ----------------
def hud(d, f, alt, spd, temp, k=1.0):
    x0, y0, x1, y1 = 60, 170, 1020, 330
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=P["panel"], outline=mix(R.C["bg"], P["cyan"], k), width=3)
    label(d, x0 + 24, y0 + 14, "VUELO MAD → LAX", 30, mix(R.C["bg"], P["cyan"], k), "Mono")
    vals = [("ALTITUD", f"{int(alt):,} m".replace(",", ".")), ("VELOCIDAD", f"{int(spd):,} km/h".replace(",", ".")),
            ("EXTERIOR", f"{int(round(temp))} °C"), ("RECORRIDO", f"{int(ROUTE_KM * f):,} km".replace(",", "."))]
    for i, (a, b) in enumerate(vals):
        cx = x0 + 24 + i * 238
        label(d, cx, y0 + 64, a, 24, mix(R.C["bg"], R.C["muted"], k), "Mono")
        label(d, cx, y0 + 98, b, 36, mix(R.C["bg"], R.C["accent"], k), "Mono")
    # barra de progreso del vuelo
    d.line([(x0 + 24, y1 - 16), (x1 - 24, y1 - 16)], fill=P["track"], width=4)
    d.line([(x0 + 24, y1 - 16), (x0 + 24 + (x1 - x0 - 48) * f, y1 - 16)], fill=mix(R.C["bg"], R.C["accent"], k), width=4)


def sc_flight(d, t, p, img):
    """Mapa con costas reales, cámara que sigue al avión y HUD."""
    T = p["dur"]
    q = ease(prog(t, 0, T))
    k = ease(t / 0.5)
    cam = cam_lerp(p["cam0"], p["cam1"], q)
    graticule(d, cam, k)
    draw_land(d, cam, k)
    f = lerp(p["f0"], p["f1"], q)
    n = max(2, int(f * (len(ROUTE) - 1)) + 1)
    pts = route_pts(cam)
    if p.get("straight"):
        a, b = cam.xy(MAD[1], MAD[0]), cam.xy(LAX[1], LAX[0])
        s = ease(prog(t, p["straight"], p["straight"] + 1.5))
        if s > 0:
            dashed(d, [a, (lerp(a[0], b[0], s), lerp(a[1], b[1], s))], P["dash"], 5)
    end, ang = polyline_partial(d, pts, f, R.C["accent"], 8)
    plane(d, end[0], end[1], ang, 36, R.C["fg"])
    city(d, cam, MAD, "Madrid", k)
    city(d, cam, LAX, "Los Ángeles", k)
    for nm, lon, lat in p.get("regions", []):
        x, y = cam.xy(lon, lat)
        label(d, x, y, nm, 28, mix(R.C["bg"], P["region"], k), "Mono", "c")
    alt = lerp(p.get("alt0", 11000), p.get("alt1", 11000), ease(prog(t, 0, p.get("alt_t", T))))
    spd = lerp(p.get("spd0", 900), p.get("spd1", 900), ease(prog(t, 0, p.get("alt_t", T))))
    temp = lerp(p.get("temp0", -56), p.get("temp1", -56), ease(prog(t, 0, p.get("alt_t", T))))
    if p.get("hud", True):
        hud(d, f, alt, spd, temp, k)


def ortho(lat, lon, lat0, lon0):
    la, lo, a0, o0 = map(math.radians, (lat, lon, lat0, lon0))
    x = math.cos(la) * math.sin(lo - o0)
    y = math.cos(a0) * math.sin(la) - math.sin(a0) * math.cos(la) * math.cos(lo - o0)
    z = math.sin(a0) * math.sin(la) + math.cos(a0) * math.cos(la) * math.cos(lo - o0)
    return x, y, z


def sc_globe_land(d, t, p, img):
    cx, cy, r = 540, 760, 360
    k = ease(t / 0.6)
    lat0 = p.get("view_lat", 52)
    lon0 = lerp(p.get("view_lon0", -40), p.get("view_lon1", -70), ease(prog(t, 0, p["dur"])))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=mix(R.C["bg"], P["globe"], k), outline=mix(R.C["bg"], P["cyan"], k), width=5)
    for poly in geo.LAND:
        pts = []
        vis = False
        for lo, la in poly:
            x, y, z = ortho(la, lo, lat0, lon0)
            if z < 0:
                n = math.hypot(x, y) or 1
                x, y = x / n, y / n
            else:
                vis = True
            pts.append((cx + r * x, cy - r * y))
        if vis:
            d.polygon(pts, fill=mix(R.C["bg"], P["land_fill"], k), outline=mix(R.C["bg"], P["land_line"], k), width=3)
    s = ease(prog(t, 0.6, 2.6))
    pts = []
    for la, lo in ROUTE:
        x, y, z = ortho(la, lo, lat0, lon0)
        pts.append((cx + r * x, cy - r * y))
    if s > 0:
        end, ang = polyline_partial(d, pts, s, R.C["accent"], 9)
        plane(d, end[0], end[1], ang, 32, R.C["fg"])
    for ll, nm in ((MAD, "Madrid"), (LAX, "Los Ángeles")):
        x, y, z = ortho(ll[0], ll[1], lat0, lon0)
        if z > 0:
            X, Y = cx + r * x, cy - r * y
            d.ellipse([X - 12, Y - 12, X + 12, Y + 12], fill=R.C["fg"])
            label(d, X, Y + 18, nm, 32, R.C["fg"], "Black", "c")
    if p.get("note") and t > 2.8:
        q = ease(prog(t, 2.8, 3.4))
        tcenter(d, 1160, p["note"], 50, mix(R.C["bg"], R.C["accent"], q))


# ---------------- Groenlandia vs África: siluetas reales ----------------
def _merc_targets():
    cam = Cam(-2.0, 25.0, 3.9, 540, 900)
    g = [cam.xy(lo, la) for lo, la in geo.GREENLAND]
    a = [cam.xy(lo, la) for lo, la in geo.AFRICA]
    return cam, g, a


def _ea_targets():
    s = 0.088  # px por km, misma escala para los dos
    gc, ac = geo.centroid(geo.GREENLAND), geo.centroid(geo.AFRICA)
    g = [(250 + x * s, 600 - y * s) for x, y in geo.laea(geo.GREENLAND, *gc)]
    a = [(650 + x * s, 760 - y * s) for x, y in geo.laea(geo.AFRICA, *ac)]
    return g, a


def sc_greenland(d, t, p, img):
    k = ease(t / 0.5)
    cam, gm, am = _merc_targets()
    ge, ae = _ea_targets()
    m = ease(prog(t, p.get("morph", 3.0), p.get("morph", 3.0) + 2.0))
    if m < 1:
        for poly in geo.LAND:
            if poly is geo.GREENLAND or poly is geo.AFRICA:
                continue
            d.polygon([cam.xy(lo, la) for lo, la in poly], fill=mix(R.C["bg"], P["land_fill"], k * (1 - m)),
                      outline=mix(R.C["bg"], P["land_line"], k * (1 - m) * 0.7), width=2)
        for poly in geo.SEAS:
            d.polygon([cam.xy(lo, la) for lo, la in poly], fill=R.C["bg"])
    g = [(lerp(a[0], b[0], m), lerp(a[1], b[1], m)) for a, b in zip(gm, ge)]
    a = [(lerp(x[0], y[0], m), lerp(x[1], y[1], m)) for x, y in zip(am, ae)]
    d.polygon(g, fill=mix(R.C["bg"], P["g_fill"], k), outline=mix(R.C["bg"], P["cyan"], k), width=5)
    d.polygon(a, fill=mix(R.C["bg"], P["a_fill"], k), outline=mix(R.C["bg"], P["orange"], k), width=5)
    gx = sum(x for x, _ in g) / len(g)
    gy = max(y for _, y in g)
    ax = sum(x for x, _ in a) / len(a)
    ay = sum(y for _, y in a) / len(a)
    label(d, gx, gy + 14, "Groenlandia", 32, P["cyan"], "Black", "c")
    label(d, ax, ay - 20, "África", 36, P["orange"], "Black", "c")
    head = "En el mapa" if m < 0.5 else "Tamaño real (misma escala)"
    tcenter(d, 250, head, 46, mix(R.C["bg"], R.C["accent"], k))
    if m > 0.98 and p.get("note"):
        q = ease(prog(t, p.get("morph", 3.0) + 2.0, p.get("morph", 3.0) + 2.6))
        tcenter(d, 1180, p["note"], 52, mix(R.C["bg"], R.C["fg"], q))


# ---------------- aire, temperatura, cabina ----------------
def sc_thermo(d, t, p, img):
    k = ease(t / 0.5)
    q = ease(prog(t, 0.4, 3.0))
    x, y0, y1 = 300, 380, 1080
    d.rounded_rectangle([x - 34, y0, x + 34, y1], radius=34, outline=mix(R.C["bg"], R.C["fg"], k), width=5)
    d.ellipse([x - 62, y1 - 30, x + 62, y1 + 94], outline=mix(R.C["bg"], R.C["fg"], k), width=5,
              fill=mix(R.C["bg"], P["cyan"], k))
    lo_t, hi_t = -60, 20

    def ty(v):
        return y1 - (v - lo_t) / (hi_t - lo_t) * (y1 - y0 - 40)
    temp = lerp(15, -56, q)
    col = mix(P["orange"], P["cyan"], q)
    d.rounded_rectangle([x - 18, ty(temp), x + 18, y1 + 10], radius=18, fill=col)
    for v in (20, 0, -20, -40, -60):
        yy = ty(v)
        d.line([(x + 40, yy), (x + 64, yy)], fill=R.C["muted"], width=3)
        label(d, x + 76, yy - 16, f"{v} °C", 28, R.C["muted"], "Mono")
    label(d, 600, 420, "Suelo", 34, R.C["fg"], "Mono")
    label(d, 600, 466, "+15 °C", 54, P["orange"], "Black")
    label(d, 600, 760, "A 11.000 m", 34, R.C["fg"], "Mono")
    label(d, 600, 806, f"{int(round(temp))} °C", 72, mix(R.C["bg"], P["cyan"], q), "Black")


def sc_density(d, t, p, img):
    k = ease(t / 0.5)
    q = ease(prog(t, 0.3, 1.8))
    base = 1060
    for x, v, nm, col in ((320, 1.225, "Nivel del mar", R.C["muted"]), (760, 0.364, "A 11.000 m", P["cyan"])):
        h = 620 * v / 1.225 * q
        d.rounded_rectangle([x - 120, base - h, x + 120, base], radius=18, fill=tuple(col) + (70,),
                            outline=col, width=5)
        label(d, x, base + 20, nm, 32, R.C["fg"], "Mono", "c")
        label(d, x, base - h - 60, f"{v:.2f} kg/m³".replace(".", ","), 32, col, "Mono", "c")
    if t > 2.0:
        a = ease(prog(t, 2.0, 2.6))
        label(d, 760, 520, "≈ 30 %", 84, mix(R.C["bg"], R.C["accent"], a), "Black", "c")
    tcenter(d, 300, "Densidad del aire", 44, mix(R.C["bg"], R.C["fg"], k))


def sc_cabin(d, t, p, img):
    k = ease(t / 0.5)
    cx, cy, r = 540, 720, 330
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=mix(R.C["bg"], P["cabin"], k), outline=mix(R.C["bg"], R.C["fg"], k), width=8)
    d.line([(cx - r + 40, cy + 120), (cx + r - 40, cy + 120)], fill=mix(R.C["bg"], R.C["muted"], k), width=6)
    for i in range(-3, 4):
        sx = cx + i * 72
        d.rounded_rectangle([sx - 22, cy + 40, sx + 22, cy + 116], radius=8, outline=mix(R.C["bg"], R.C["muted"], k), width=4)
    q = ease(prog(t, 0.6, 2.0))
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x0, y0 = cx + math.cos(a) * (r - 90), cy + math.sin(a) * (r - 90)
        arrow(d, x0, y0, x0 + math.cos(a) * 70 * q, y0 + math.sin(a) * 70 * q, mix(R.C["bg"], R.C["accent"], q), 6, 20)
    label(d, cx, cy - 120, "Dentro", 34, R.C["fg"], "Mono", "c")
    label(d, cx, cy - 76, "≤ 2.400 m", 54, R.C["accent"], "Black", "c")
    label(d, cx, cy + r + 30, "Fuera: 11.000 m", 34, P["cyan"], "Mono", "c")


def sc_chips(d, t, p, img):
    k = ease(t / 0.5)
    q = ease(prog(t, 0.6, 3.0))
    for x, puff, nm in ((300, 0.0, "En el suelo"), (780, q, "En vuelo")):
        w, h = 260, 340
        bulge = 70 * puff
        top, bot = 470, 470 + h
        pts = []
        for i in range(21):
            u = i / 20
            pts.append((x - w / 2 - bulge * math.sin(math.pi * u), top + h * u))
        for i in range(21):
            u = 1 - i / 20
            pts.append((x + w / 2 + bulge * math.sin(math.pi * u), top + h * u))
        d.polygon(pts, fill=mix(R.C["bg"], P["bag"], k), outline=mix(R.C["bg"], P["bag_line"], k), width=5)
        d.line([(x - w / 2 - 6, top), (x + w / 2 + 6, top)], fill=R.C["fg"], width=10)
        d.line([(x - w / 2 - 6, bot), (x + w / 2 + 6, bot)], fill=R.C["fg"], width=10)
        label(d, x, (top + bot) / 2 - 20, "CHIPS", 40, mix(R.C["bg"], R.C["accent"], k), "Black", "c")
        label(d, x, bot + 30, nm, 32, R.C["fg"], "Mono", "c")


def sc_window(d, t, p, img):
    k = ease(t / 0.5)
    phase = p.get("phase", "round")
    if phase == "square":
        cx, cy, w, h = 540, 700, 420, 520
        d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], outline=mix(R.C["bg"], R.C["fg"], k), width=10)
        q = prog(t, 0.6, 3.0)
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            px, py = cx + sx * w / 2, cy + sy * h / 2
            rr = 30 + 40 * ease(q) + 8 * math.sin(t * 8)
            d.ellipse([px - rr, py - rr, px + rr, py + rr], outline=mix(R.C["bg"], P["red"], ease(q)), width=6)
        c = ease(prog(t, 1.8, 3.6))
        if c > 0:
            px, py = cx + w / 2, cy - h / 2
            pts = [(px, py), (px + 50, py - 40), (px + 80, py - 30), (px + 130, py - 90), (px + 170, py - 80)]
            polyline_partial(d, pts, c, P["red"], 6)
        label(d, cx, cy + h / 2 + 90, "Comet · 1953-1954", 36, mix(R.C["bg"], P["red"], k), "Mono", "c")
    else:
        cx, cy, w, h = 540, 700, 380, 540
        for i, col in enumerate((R.C["fg"], P["win2"], P["win3"])):
            off = i * 26
            d.rounded_rectangle([cx - w / 2 + off, cy - h / 2 + off, cx + w / 2 - off, cy + h / 2 - off],
                                radius=170 - off, outline=mix(R.C["bg"], col, k), width=8)
        q = ease(prog(t, 1.0, 1.8))
        hx, hy = cx, cy + h / 2 - 120
        if q > 0:
            rr = 10 + 26 * (0.5 + 0.5 * math.sin(t * 6))
            d.ellipse([hx - rr, hy - rr, hx + rr, hy + rr], outline=mix(R.C["bg"], R.C["accent"], q), width=5)
            d.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=R.C["accent"])
            label(d, hx + 60, hy - 18, "agujero", 30, mix(R.C["bg"], R.C["accent"], q), "Mono")
        label(d, cx, cy + h / 2 + 40, "3 capas · esquinas redondas", 32, mix(R.C["bg"], R.C["fg"], k), "Mono", "c")


def sc_record(d, t, p, img):
    """Atlántico con la ruta Nueva York → Londres y la corriente en chorro."""
    k = ease(t / 0.5)
    cam = Cam(-37, 49, 7.0, 540, 760)
    graticule(d, cam, k)
    draw_land(d, cam, k)
    for row in range(4):
        y0 = 560 + row * 90
        pts = [(x, y0 + 26 * math.sin(x / 110 + t * 3 + row)) for x in range(40, 1041, 20)]
        d.line(pts, fill=mix(R.C["bg"], P["cyan"], k * 0.5), width=5, joint="curve")
        hx = 40 + ((t * 300 + row * 230) % 1000)
        hy = y0 + 26 * math.sin(hx / 110 + t * 3 + row)
        arrow(d, hx - 46, hy, hx, hy, mix(R.C["bg"], P["cyan"], k), 5, 20)
    rt = great_circle(JFK, LHR, 80)
    pts = [cam.xy(lo, la) for la, lo in rt]
    s = ease(prog(t, 0.6, 3.0))
    end, ang = polyline_partial(d, pts, s, R.C["accent"], 8)
    plane(d, end[0], end[1], ang, 34, R.C["fg"])
    city(d, cam, JFK, "Nueva York", k)
    city(d, cam, LHR, "Londres", k, below=False)
    if t > 2.6:
        q = ease(prog(t, 2.6, 3.2))
        d.rounded_rectangle([140, 1060, 940, 1240], radius=20, fill=P["panel"], outline=mix(R.C["bg"], R.C["accent"], q), width=3)
        label(d, 540, 1078, "Récord · febrero 2020 · Boeing 747", 28, mix(R.C["bg"], R.C["muted"], q), "Mono", "c")
        label(d, 540, 1120, "4 h 56 min · ~1.290 km/h", 52, mix(R.C["bg"], R.C["accent"], q), "Black", "c")


# ---------------- formato Top 5 ----------------
def sc_top_card(d, t, p, img):
    k = ease(t / 0.35)
    n = p["n"]
    s = lerp(1.6, 1.0, k)
    f = font(int(420 * s), "Black")
    txt = f"#{n}"
    tw = d.textlength(txt, font=f)
    d.text((540 - tw / 2, 520 - 210 * s), txt, font=f, fill=mix(R.C["bg"], R.C["accent"], k))
    tcenter(d, 1000, p["title"], 56, mix(R.C["bg"], R.C["fg"], ease(prog(t, 0.2, 0.6))))


def sc_title(d, t, p, img):
    k = ease(t / 0.4)
    for i, line in enumerate(p["lines"]):
        q = ease(prog(t, i * 0.25, i * 0.25 + 0.4))
        col = R.C["accent"] if i == p.get("hl", 1) else R.C["fg"]
        tcenter(d, 470 + i * 150, line, 110, mix(R.C["bg"], col, q))
    plane(d, lerp(-100, 1180, prog(t, 0, p.get("dur", 3))), 1150, 0.0, 50, mix(R.C["bg"], R.C["fg"], k))


# ---------------- formato Quiz ----------------
def sc_quiz(d, t, p, img):
    k = ease(t / 0.35)
    tcenter(d, 330, f"PREGUNTA {p['i']}/{p['n']}", 40, mix(R.C["bg"], P["cyan"], k))
    stmt = p.get("text", "¿Verdadero o falso?").replace("*", "")
    f = font(66, "Black")
    words, lines, cur = stmt.split(), [], ""
    for w in words:
        if d.textlength((cur + " " + w).strip(), font=f) > 900:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    for j, ln in enumerate(lines):
        kk = ease((t - 0.08 * j) / 0.35)
        tcenter(d, 400 + j * 80, "“" + ln + "”" if len(lines) == 1 else ln, 66, mix(R.C["bg"], R.C["fg"], kk))
    T0, T1 = p.get("count_at", 1.2), p.get("count_at", 1.2) + 3.0
    cx, cy, r = 540, 860, 150
    if t < T1:
        q = prog(t, T0, T1)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=P["track"], width=14)
        if q > 0:
            d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * (1 - q), fill=R.C["accent"], width=14)
            num = str(3 - min(2, int(q * 3)))
            f = font(200, "Black")
            tw = d.textlength(num, font=f)
            d.text((cx - tw / 2, cy - 120), num, font=f, fill=R.C["fg"])
        for x, txt, col in ((300, "V", P["green"]), (780, "F", P["red"])):
            d.rounded_rectangle([x - 90, 1090, x + 90, 1250], radius=24, outline=col, width=6)
            f = font(110, "Black")
            tw = d.textlength(txt, font=f)
            d.text((x - tw / 2, 1102), txt, font=f, fill=col)
    else:
        a = ease(prog(t, T1, T1 + 0.25))
        ok = p["answer"]
        col = P["green"] if ok else P["red"]
        word = "VERDADERO" if ok else "FALSO"
        s = lerp(1.5, 1.0, a)
        f = font(int(150 * s), "Black")
        tw = d.textlength(word, font=f)
        x0, y0 = 540 - tw / 2, 860 - 90 * s
        d.rounded_rectangle([x0 - 30, y0 - 10, x0 + tw + 30, y0 + 190 * s], radius=26, outline=mix(R.C["bg"], col, a), width=10)
        d.text((x0, y0), word, font=f, fill=mix(R.C["bg"], col, a))


def sc_quiz_end(d, t, p, img):
    k = ease(t / 0.4)
    tcenter(d, 520, "¿Cuántas", 120, mix(R.C["bg"], R.C["fg"], k))
    tcenter(d, 670, "acertaste?", 120, mix(R.C["bg"], R.C["accent"], k))
    q = ease(prog(t, 0.6, 1.2))
    tcenter(d, 900, "Dímelo en comentarios", 48, mix(R.C["bg"], P["cyan"], q))
    for i in range(5):
        x = 540 + (i - 2) * 130
        d.ellipse([x - 44, 1050, x + 44, 1138], outline=mix(R.C["bg"], R.C["fg"], q), width=5)
        tcenter_x(d, x, 1062, str(i + 1), 52, mix(R.C["bg"], R.C["fg"], q))


def tcenter_x(d, x, y, txt, size, col):
    f = font(size, "Mono")
    d.text((x - d.textlength(txt, font=f) / 2, y), txt, font=f, fill=col)


SCENES = {"flight": sc_flight, "globe_land": sc_globe_land, "greenland": sc_greenland, "thermo": sc_thermo,
          "density": sc_density, "cabin": sc_cabin, "chips": sc_chips, "window": sc_window, "record": sc_record,
          "top_card": sc_top_card, "title": sc_title, "quiz": sc_quiz, "quiz_end": sc_quiz_end}
