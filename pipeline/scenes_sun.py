"""Escenas del vídeo «El Sol que ves es el de hace 8 minutos» (estilo premium: líneas limpias + brillo)."""
import math, random
import render as R
from render import ease, prog, lerp, mix, clamp, arrow
import geo
from scenes_nls import dashed, label, tcenter
from scenes_planes import P, ortho

SUN_OUT, SUN_IN = (255, 140, 40), (255, 222, 110)
OCEAN, LAND, NIGHT = (40, 92, 175), (96, 165, 112), (14, 18, 32)


def bgc():
    return R.C["bg"]


def sun(d, cx, cy, r, k=1.0, pulse=0.0):
    r = r * (1 + 0.015 * pulse)
    for i in range(7):
        q = i / 6
        rr = r * (1 - 0.55 * q)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=mix(bgc(), mix(SUN_OUT, SUN_IN, q), k))


def earth(d, cx, cy, r, lon0=0.0, k=1.0, lit=1.0, lat0=20.0):
    ocean = mix(NIGHT, OCEAN, lit)
    land = mix(NIGHT, LAND, lit)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=mix(bgc(), ocean, k), outline=mix(bgc(), P["cyan"], k * (0.4 + 0.6 * lit)),
              width=max(2, int(r / 30)))
    if r < 18:
        return
    for poly in geo.LAND:
        pts, vis = [], False
        for lo, la in poly:
            x, y, z = ortho(la, lo, lat0, lon0)
            if z < 0:
                n = math.hypot(x, y) or 1
                x, y = x / n, y / n
            else:
                vis = True
            pts.append((cx + r * x, cy - r * y))
        if vis:
            d.polygon(pts, fill=mix(bgc(), land, k))


def stars(d, k, seed=3, n=70, ymax=1250):
    rng = random.Random(seed)
    for _ in range(n):
        x, y = rng.uniform(0, 1080), rng.uniform(120, ymax)
        s = rng.choice((1.5, 2, 2.5))
        d.ellipse([x - s, y - s, x + s, y + s], fill=mix(bgc(), (190, 195, 210), k * rng.uniform(0.3, 1)))


def box(d, cx, cy, txt, size, col, k, w_pad=34):
    f = R.font(size, "Black")
    tw = d.textlength(txt, font=f)
    d.rounded_rectangle([cx - tw / 2 - w_pad, cy - size * 0.35, cx + tw / 2 + w_pad, cy + size * 1.2], radius=22,
                        fill=mix(bgc(), P["panel"], k), outline=mix(bgc(), col, k), width=3)
    d.text((cx - tw / 2, cy), txt, font=f, fill=mix(bgc(), col, k))


# 1 · Atardecer: el Sol "congelado" (es luz de hace 8 minutos)
def sc_sunset(d, t, p, img):
    k = ease(t / 0.6)
    stars(d, k * 0.6, n=40, ymax=700)
    hy = 900
    cy = hy + 40 - 50 * ease(prog(t, 0, p["dur"]))
    sun(d, 540, cy, 230, k, math.sin(t * 3))
    d.rectangle([0, hy, 1080, 1300], fill=mix(bgc(), (12, 16, 28), k))
    d.line([(0, hy), (1080, hy)], fill=mix(bgc(), SUN_OUT, k * 0.8), width=3)
    for i in range(9):
        y = hy + 28 + i * 34
        wv = (190 - i * 16) * (0.8 + 0.2 * math.sin(t * 4 + i))
        d.line([(540 - wv, y), (540 + wv, y)], fill=mix(bgc(), SUN_OUT, k * (0.75 - i * 0.07)), width=6)
    f0 = p.get("freeze", 2.2)
    if f0 <= t < f0 + 0.9:
        q = 1 - abs((t - f0) / 0.45 - 1)
        col = mix(bgc(), (255, 255, 255), clamp(q * 1.5))
        d.rounded_rectangle([490, 630, 520, 730], radius=8, fill=col)
        d.rounded_rectangle([560, 630, 590, 730], radius=8, fill=col)
    if t > f0 + 0.9:
        q = ease(prog(t, f0 + 0.9, f0 + 1.5))
        box(d, 540, 1150, "Luz de hace 8 min 20 s", 46, R.C["accent"], q)


# 2 · La distancia y la velocidad de la luz
def sc_distance(d, t, p, img):
    k = ease(t / 0.5)
    stars(d, k * 0.7)
    sun(d, 170, 400, 300, k, math.sin(t * 2))
    ex, ey = 870, 1110
    earth(d, ex, ey, 52, -20 + t * 6, k)
    a, b = (390, 610), (ex - 60, ey - 55)
    dashed(d, [a, b], mix(bgc(), R.C["muted"], k), 3)
    s = ease(prog(t, 0.6, p["dur"] * 0.55))
    hx, hy = lerp(a[0], b[0], s), lerp(a[1], b[1], s)
    for j in range(10):
        q = max(0, s - j * 0.018)
        x, y = lerp(a[0], b[0], q), lerp(a[1], b[1], q)
        r = 12 - j
        d.ellipse([x - r, y - r, x + r, y + r], fill=mix(bgc(), (255, 245, 200), k * (1 - j / 10)))
    if t > 0.9:
        q = ease(prog(t, 0.9, 1.4))
        box(d, 600, 760, "≈ 150 millones de km", 44, R.C["fg"], q)
    t2 = p["dur"] * 0.5
    if t > t2:
        q = ease(prog(t, t2, t2 + 0.5))
        box(d, 330, 1180, "300.000 km/s", 50, R.C["accent"], q)


# 3 · 7,5 vueltas a la Tierra en un segundo
def sc_laps(d, t, p, img):
    k = ease(t / 0.5)
    stars(d, k * 0.5)
    cx, cy, re, ro = 540, 740, 220, 320
    earth(d, cx, cy, re, -10 + t * 8, k)
    laps = 7.5 * ease(prog(t, 0.5, p["dur"] - 0.6))
    for i in range(int(laps)):
        rr = ro + 6 * (i % 3)
        d.ellipse([cx - rr, cy - rr * 0.38, cx + rr, cy + rr * 0.38], outline=mix(bgc(), (255, 230, 150), k * 0.25), width=2)
    a = laps * 2 * math.pi
    for j in range(18):
        aa = a - j * 0.07
        x, y = cx + ro * math.cos(aa), cy + ro * 0.38 * math.sin(aa)
        r = 11 - j * 0.55
        if math.sin(aa) < 0 and abs(math.cos(aa)) < re / ro:
            continue  # detrás de la Tierra
        d.ellipse([x - r, y - r, x + r, y + r], fill=mix(bgc(), (255, 245, 200), k * (1 - j / 18)))
    f = R.font(120, "Black")
    txt = f"{laps:.1f}".replace(".", ",")
    tw = d.textlength(txt, font=f)
    d.text((540 - tw / 2, 1040), txt, font=f, fill=mix(bgc(), R.C["accent"], k))
    tcenter(d, 1180, "vueltas en 1 segundo", 40, mix(bgc(), R.C["muted"], k), "Semi")


# 4 · El cronómetro: 8 min 20 s
def sc_clock(d, t, p, img):
    k = ease(t / 0.5)
    cx, cy, r = 540, 660, 280
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=mix(bgc(), P["track"], k), width=16)
    s = ease(prog(t, 0.4, min(p["dur"] * 0.55, 4.5)))
    if s > 0:
        d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * s, fill=R.C["accent"], width=16)
    secs = int(round(500 * s))
    txt = f"{secs // 60}:{secs % 60:02d}"
    f = R.font(170, "Black")
    tw = d.textlength(txt, font=f)
    d.text((cx - tw / 2, cy - 110), txt, font=f, fill=mix(bgc(), R.C["fg"], k))
    tcenter(d, cy + 90, "min : s", 34, mix(bgc(), R.C["muted"], k), "Semi")
    sun(d, 300, 1100, 44, k)
    earth(d, 780, 1100, 34, 0, k)
    arrow(d, 370, 1100, 720, 1100, mix(bgc(), (255, 245, 200), k), 5, 22)
    if s >= 1:
        q = ease(prog(t, min(p["dur"] * 0.55, 4.5), min(p["dur"] * 0.55, 4.5) + 0.5))
        box(d, 540, 1200, "Estás viendo el pasado", 44, R.C["accent"], q)


def _walk(n=520, seed=7):
    rng = random.Random(seed)
    x = y = 0.0
    pts = [(0.0, 0.0)]
    for i in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        st = rng.uniform(10, 22)
        rad = math.hypot(x, y)
        bias = 0.9 if rad > 0 else 0
        x += st * math.cos(ang) + bias * (x / (rad or 1))
        y += st * math.sin(ang) + bias * (y / (rad or 1))
        pts.append((x, y))
    return pts


WALK = _walk()


def cross_section(d, cx, cy, r, k):
    for rr, col in ((r, SUN_OUT), (r * 0.72, (245, 120, 40)), (r * 0.27, SUN_IN)):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=mix(bgc(), col, k * 0.9))
    for i in range(26):
        a = i / 26 * 2 * math.pi
        x0, y0 = cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a)
        x1, y1 = cx + r * 0.96 * math.cos(a + 0.05), cy + r * 0.96 * math.sin(a + 0.05)
        d.line([(x0, y0), (x1, y1)], fill=mix(bgc(), (255, 175, 70), k * 0.5), width=3)


# 5 · El núcleo: la luz rebota como en un laberinto
def sc_core(d, t, p, img):
    k = ease(t / 0.5)
    cx, cy, r = 540, 720, 440
    cross_section(d, cx, cy, r, k)
    if t > 0.8:
        q = ease(prog(t, 0.8, 1.3))
        d.line([(cx + 70, cy - 70), (cx + 250, cy - 330)], fill=mix(bgc(), R.C["fg"], q), width=3)
        box(d, cx + 200, cy - 420, "Núcleo · 15 millones °C", 36, R.C["fg"], q)
    t0 = p["dur"] * 0.4
    s = prog(t, t0, p["dur"])
    n = max(2, int(len(WALK) * s))
    sc = (r * 0.68) / max(math.hypot(x, y) for x, y in WALK)
    pts = [(cx + x * sc, cy + y * sc) for x, y in WALK[:n]]
    if s > 0:
        d.line(pts, fill=mix(bgc(), (205, 230, 255), 0.55), width=2)
        hx, hy = pts[-1]
        d.ellipse([hx - 12, hy - 12, hx + 12, hy + 12], fill=(235, 245, 255))


# 6 · La salida: miles de años dentro, 8 minutos fuera
def sc_escape(d, t, p, img):
    k = ease(t / 0.5)
    cx, cy, r = 160, 720, 420
    cross_section(d, cx, cy, r, k)
    stars(d, k * 0.5, seed=9, n=30)
    if t > 0.4:
        q = ease(prog(t, 0.4, 0.9))
        box(d, 260, 1180, "Miles de años", 46, R.C["fg"], q)
    t1 = p["dur"] * 0.45
    s = ease(prog(t, t1, p["dur"] - 0.3))
    x0, x1 = cx + r, 980
    ex = 1010
    earth(d, ex, cy, 26, 0, k)
    if s > 0:
        hx = lerp(x0, x1, s)
        d.line([(x0, cy), (hx, cy)], fill=(255, 245, 200), width=5)
        d.ellipse([hx - 12, cy - 12, hx + 12, cy + 12], fill=(235, 245, 255))
        q = ease(prog(t, t1, t1 + 0.5))
        box(d, 790, 560, "8 min 20 s", 50, R.C["accent"], q)
    else:
        d.ellipse([x0 - 12, cy - 12, x0 + 12, cy + 12], fill=mix(bgc(), (235, 245, 255), k))


ORB = (540, 560, 400, 160)


def orbit_xy(a):
    cx, cy, rx, ry = ORB
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


# 7 · El Sol desaparece: la luz y la gravedad tardan 8 minutos en enterarse
def sc_vanish(d, t, p, img):
    k = ease(t / 0.5)
    cx, cy, rx, ry = ORB
    stars(d, k * 0.6)
    dashed(d, [orbit_xy(i / 80 * 2 * math.pi) for i in range(81)], mix(bgc(), R.C["muted"], k * 0.6), 2)
    toff = p.get("off", 3.0)
    a = -0.4 + 0.08 * t
    ex, ey = orbit_xy(a)
    if t < toff:
        sun(d, cx, cy, 130, k, math.sin(t * 3))
    else:
        q = 1 - ease(prog(t, toff, toff + 0.25))
        if q > 0:
            sun(d, cx, cy, 130, q)
        dashed(d, [(cx + 130 * math.cos(i / 40 * 2 * math.pi), cy + 130 * math.sin(i / 40 * 2 * math.pi)) for i in range(41)],
               mix(bgc(), R.C["muted"], 1 - q), 2)
        dist = math.hypot(ex - cx, (ey - cy) * rx / ry)
        speed = (dist - 130) / max(1.0, p["dur"] - toff - 0.8)
        R_ = 130 + (t - toff) * speed
        if R_ < dist:
            d.ellipse([cx - R_, cy - R_ * ry / rx, cx + R_, cy + R_ * ry / rx], outline=(255, 235, 170), width=6)
        frac = clamp((R_ - 130) / max(1, dist - 130))
        secs = int(500 * frac)
        box(d, 540, 1150, f"{secs // 60}:{secs % 60:02d}", 64, R.C["accent"], ease(prog(t, toff, toff + 0.4)))
    earth(d, ex, ey, 46, t * 10, k, 1.0)


# 8 · Oscuridad: la Tierra sale en línea recta
def sc_dark(d, t, p, img):
    k = ease(t / 0.4)
    cx, cy, rx, ry = ORB
    stars(d, 0.5)
    dashed(d, [orbit_xy(i / 80 * 2 * math.pi) for i in range(81)], mix(bgc(), R.C["muted"], 0.35), 2)
    dashed(d, [(cx + 130 * math.cos(i / 40 * 2 * math.pi), cy + 130 * math.sin(i / 40 * 2 * math.pi)) for i in range(41)],
           mix(bgc(), R.C["muted"], 0.5), 2)
    a0 = p.get("a0", 0.64)
    x0, y0 = orbit_xy(a0)
    tx, ty = -rx * math.sin(a0), ry * math.cos(a0)
    n = math.hypot(tx, ty)
    tx, ty = tx / n, ty / n
    s = ease(prog(t, 0.8, p["dur"]))
    L = 900
    ex, ey = x0 + tx * L * s, y0 + ty * L * s
    lit = 1 - ease(prog(t, 0, 0.8))
    dashed(d, [(x0, y0), (x0 + tx * L, y0 + ty * L)], mix(bgc(), R.C["accent"], 0.7 * k), 3)
    earth(d, ex, ey, 46, t * 10, 1.0, 0.15 + 0.85 * lit)
    if t > p["dur"] * 0.45:
        q = ease(prog(t, p["dur"] * 0.45, p["dur"] * 0.45 + 0.5))
        box(d, 540, 1150, "En línea recta", 50, R.C["fg"], q)


SCENES = {"sunset": sc_sunset, "distance": sc_distance, "laps": sc_laps, "clock": sc_clock, "core": sc_core,
          "escape": sc_escape, "vanish": sc_vanish, "dark": sc_dark}
