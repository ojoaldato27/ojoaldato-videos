"""N09 · ¿Por qué el móvil carga rápido hasta el 80 % y luego va lento?"""
from neon import *

TITLE = "Por_que_el_movil_carga_lento_despues_del_80"
LINES = [
    "El móvil carga rapidísimo hasta el *80 %*… y luego va a paso de tortuga.",
    "¿Fallo del cargador? No: *es a propósito*.",
    "Dentro de tu batería hay *iones de litio* que viajan de un lado a otro.",
    "Al cargar, la corriente los empuja hacia un lado de la batería.",
    "Al principio hay mucho sitio libre, así que entra *mucha corriente*: es la fase rápida.",
    "Pero cada celda tiene un límite de voltaje: unos *4,2 voltios*.",
    "Si se pasa, la batería se *degrada*… y hasta puede *hincharse*.",
    "Así que, al llegar a ese límite, el móvil cambia de modo.",
    "Mantiene el voltaje fijo… y baja la corriente *poco a poco*.",
    "Es como llenar un vaso: al principio chorro fuerte, y al final despacio para no derramar.",
    "Por eso ese último 20 % puede tardar *casi lo mismo* que todo lo anterior.",
    "Y si la batería se calienta, el móvil *frena la carga*.",
    "Muchos móviles se paran en el 80 % por la noche… y terminan justo antes de que te levantes.",
    "Así que ese frenazo final no es un fallo… es tu móvil *cuidándose*.",
]
SHOTS = [("open", 0, 1, 0.3), ("ions", 2, 4, 0.3), ("limit", 5, 6, 0.3), ("cv", 7, 8, 0.3), ("glass", 9, 9, 0.3),
         ("curve", 10, 11, 0.3), ("night", 12, 12, 0.3), ("final", 13, 13, 1.8)]
FOCUS = {"open": (540, 960, 1.12), "ions": (540, 960, 1.12), "limit": (540, 960, 1.12), "cv": (540, 960, 1.12),
         "glass": (540, 980, 1.12), "curve": (540, 960, 1.12), "night": (540, 960, 1.12), "final": (540, 960, 1.12)}
NOTIF = ("limit", 0.8)
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"
END_CARD = end_card_neon


def battery(d, x, y, pct, col=GR, w=360, h=700, k=1.0):
    rrect(d, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 40, WH, 7, k)
    d.rounded_rectangle([x - 60, y - h / 2 - 50, x + 60, y - h / 2 + 4], radius=12, outline=WH, width=6)
    fill_h = (h - 40) * pct
    if fill_h > 10:
        d.rounded_rectangle([x - w / 2 + 20, y + h / 2 - 20 - fill_h, x + w / 2 - 20, y + h / 2 - 20], radius=24,
                            fill=tuple(int(c * 0.16) for c in col), outline=col, width=5)
    PCT.append((x, y, pct, int(80 * w / 360)))


PCT = []


def pct_labels(img):
    d = ImageDraw.Draw(img)
    for x, y, pct, size in PCT:
        d.text((x, y), f"{pct * 100:.0f} %", font=f(F_POP, size), fill=(255, 255, 255), anchor="mm", stroke_width=6, stroke_fill=(4, 8, 18))
    PCT.clear()


def pct_at(t, rate_fast=0.18, t80=None):
    """Curva realista: rápida hasta 80 %, luego asintótica."""
    t80 = t80 or 0.8 / rate_fast
    if t < t80:
        return rate_fast * t
    return 0.8 + 0.2 * (1 - math.exp(-(t - t80) / 3.0))


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    p = pct_at(t, 0.32)
    col = GR if p < 0.8 else YE
    battery(d, 540, 980, p, col)
    if p < 0.8:
        for j in range(3):
            u = (t * 1.5 + j / 3) % 1.0
            line(d, [(540, 520 - u * 60), (520, 560 - u * 60), (560, 560 - u * 60), (540, 600 - u * 60)], tuple(int(c * (1 - u)) for c in YE), 6)
    finish(img, lay)
    pct_labels(img)
    gtitle2(t, 0.2, "¿POR QUÉ VA LENTO", "DESPUÉS DEL 80 %?", 250, 60, 92, WH, YE, hold=max(1.6, L[1][0] - 0.2))
    if t > L[1][0]:
        chip(t, L[1][0] + 0.3, "ES A PROPÓSITO", 540, 330, GR, 46)
    vignette(img, 150)


def sh_ions(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1, a2 = L[1][0], L[2][0]
    rrect(d, 120, 620, 960, 1300, 30, WH, 6)
    d.line([(540, 640), (540, 1280)], fill=DIM, width=4)
    for x in range(160, 520, 60):
        d.line([(x, 660), (x, 1260)], fill=tuple(int(c * 0.5) for c in CY), width=3)
    for x in range(580, 940, 60):
        d.line([(x, 660), (x, 1260)], fill=tuple(int(c * 0.5) for c in MG), width=3)
    label(d, 330, 1340, "GRAFITO", 30, CY, F_MONO)
    label(d, 750, 1340, "ÓXIDO", 30, MG, F_MONO)
    rr = random.Random(4)
    q = 0.0 if t < a1 else clamp((t - a1) / 3.0)
    speed = 1.0 if t < a2 else 1.6
    for k in range(34):
        x_cat = rr.uniform(600, 920)
        x_an = rr.uniform(160, 500)
        y = rr.uniform(680, 1240)
        done_ = k / 34 < q
        if done_:
            x = x_an
        elif t >= a1 and k / 34 < q + 0.12:
            u = ((t * speed * 0.8) + k * 0.13) % 1.0
            x = lerp(x_cat, x_an, u)
        else:
            x = x_cat + math.sin(t * 2 + k) * 6
        dot(d, x, y, 10, YE)
        label(d, x, y, "+", 16, (20, 20, 20), F_POP)
    if t > a1:
        arrow(d, (860, 560), (220, 560), GR, 8, 1.0, 30)
    finish(img, lay)
    pct_labels(img)
    if t < a1:
        gtitle(t, 0.3, "IONES DE LITIO", 300, 96, YE)
    elif t < a2:
        chip(t, a1 + 0.2, "CARGANDO…", 540, 330, GR, 44)
    else:
        gtitle(t, a2 + 0.2, "FASE RÁPIDA", 300, 100, GR)
    vignette(img, 150)


def sh_limit(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    v = 3.6 + 0.6 * ease(clamp((t - 0.3) / 2.0))
    cx, cy, r = 540, 960, 300
    d.arc([cx - r, cy - r, cx + r, cy + r], 150, 390, fill=DIM, width=10)
    d.arc([cx - r, cy - r, cx + r, cy + r], 360, 390, fill=RD, width=14)
    a = math.radians(150 + 240 * (v - 3.0) / 1.5)
    d.line([(cx, cy), (cx + math.cos(a) * (r - 30), cy + math.sin(a) * (r - 30))], fill=YE, width=10)
    dot(d, cx, cy, 18, YE)
    label(d, cx, cy + 140, f"{v:.2f} V".replace(".", ","), 70, WH, F_MONO)
    if t > a1:
        k = ease(clamp((t - a1) / 0.8))
        x0 = 540
        line(d, [(x0 - 160, 1360), (x0 - 160, 1300 - 40 * k), (x0 - 120, 1250 - 60 * k), (x0 + 120, 1250 - 60 * k), (x0 + 160, 1300 - 40 * k),
                 (x0 + 160, 1360), (x0 - 160, 1360)], RD, 6)
    finish(img, lay)
    pct_labels(img)
    if t < a1:
        gtitle(t, 0.3, "LÍMITE: ~4,2 V", 300, 96, YE)
    else:
        gtitle(t, a1 + 0.2, "SE DEGRADA", 300, 100, RD)
        chip(t, a1 + 0.8, "PUEDE HINCHARSE", 540, 460, WH, 36)
    vignette(img, 150)


def sh_cv(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    ox, oy, gw, gh = 140, 1320, 820, 620
    d.line([(ox, oy), (ox + gw, oy)], fill=DIM, width=4)
    d.line([(ox, oy), (ox, oy - gh)], fill=DIM, width=4)
    label(d, ox + gw, oy + 40, "TIEMPO", 28, DIM, F_MONO, "rm")
    q = ease(clamp((t - 0.2) / 2.4))
    sw = 0.45
    vpts, ipts = [], []
    for i in range(101):
        u = i / 100
        if u > q:
            break
        vv = 0.55 + 0.4 * min(1, u / sw)
        ii = 0.9 if u < sw else 0.9 * math.exp(-(u - sw) * 5)
        vpts.append((ox + gw * u, oy - gh * vv))
        ipts.append((ox + gw * u, oy - gh * ii))
    line(d, vpts, YE, 6)
    line(d, ipts, GR, 6)
    label(d, ox + 20, oy - gh - 30, "VOLTAJE", 30, YE, F_MONO, "lm")
    label(d, ox + 300, oy - gh - 30, "CORRIENTE", 30, GR, F_MONO, "lm")
    if q > sw:
        xs = ox + gw * sw
        dashed(d, (xs, oy), (xs, oy - gh), WH, 3, off=t * 30)
        label(d, xs, oy + 40, "80 %", 34, WH, F_MONO)
    finish(img, lay)
    pct_labels(img)
    if t < a1:
        gtitle(t, 0.3, "CAMBIO DE MODO", 300, 92, WH, pop=False)
    else:
        gtitle(t, a1 + 0.2, "VOLTAJE FIJO", 300, 96, YE, pop=False)
        chip(t, a1 + 0.8, "CORRIENTE ↓", 540, 460, GR, 40)
    vignette(img, 150)


def sh_glass(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    gx, gy0, gy1 = 540, 700, 1300
    line(d, [(gx - 200, gy0), (gx - 160, gy1), (gx + 160, gy1), (gx + 200, gy0)], WH, 7)
    lvl = lerp(gy1, gy0 + 40, ease(clamp(t / (T - 0.4))) * 0.98)
    fast = (gy1 - lvl) / (gy1 - gy0) < 0.8
    d.polygon([(gx - 160 - 40 * (gy1 - lvl) / (gy1 - gy0), lvl), (gx + 160 + 40 * (gy1 - lvl) / (gy1 - gy0), lvl), (gx + 158, gy1 - 4), (gx - 158, gy1 - 4)],
              fill=tuple(int(c * 0.3) for c in BL), outline=BL)
    w = 26 if fast else 6
    d.line([(gx, 460), (gx, lvl)], fill=BL, width=w)
    rrect(d, gx - 50, 420, gx + 50, 470, 10, WH, 5)
    finish(img, lay)
    pct_labels(img)
    gtitle(t, 0.3, "CHORRO FUERTE" if fast else "DESPACITO", 300, 96, BL if fast else YE, pop=False)
    vignette(img, 150)


def sh_curve(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    a1 = L[1][0]
    ox, oy, gw, gh = 140, 1320, 820, 620
    d.line([(ox, oy), (ox + gw, oy)], fill=DIM, width=4)
    d.line([(ox, oy), (ox, oy - gh)], fill=DIM, width=4)
    q = ease(clamp((t - 0.2) / 2.0))
    pts = []
    for i in range(101):
        u = i / 100
        if u > q:
            break
        p = 0.8 * min(1, u / 0.45) + (0.2 * (1 - math.exp(-(u - 0.45) * 5)) if u > 0.45 else 0)
        pts.append((ox + gw * u, oy - gh * p))
    line(d, pts, GR, 7)
    for p in (0.8, 1.0):
        dashed(d, (ox, oy - gh * p), (ox + gw, oy - gh * p), DIM, 2)
        label(d, ox - 20, oy - gh * p, f"{p * 100:.0f}%", 28, DIM, F_MONO, "rm")
    if q > 0.5:
        d.line([(ox, oy + 60), (ox + gw * 0.45, oy + 60)], fill=GR, width=6)
        d.line([(ox + gw * 0.45, oy + 90), (ox + gw, oy + 90)], fill=YE, width=6)
        label(d, ox + gw * 0.22, oy + 30, "0→80 %", 28, GR, F_MONO)
        label(d, ox + gw * 0.72, oy + 130, "80→100 %", 28, YE, F_MONO)
    if t > a1:
        cx, cy = 820, 640
        circle(d, cx, cy, 70, OR, 6)
        rrect(d, cx - 18, cy - 160, cx + 18, cy - 40, 18, OR, 5)
        label(d, cx, cy + 120, "CALOR", 30, OR, F_MONO)
    finish(img, lay)
    pct_labels(img)
    if t < a1:
        gtitle(t, 0.3, "CASI LO MISMO", 300, 96, YE, pop=False)
    else:
        gtitle(t, a1 + 0.2, "CALOR = FRENO", 300, 96, OR, pop=False)
    vignette(img, 150)


def sh_night(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    cx, cy = 300, 640
    d.arc([cx - 80, cy - 80, cx + 80, cy + 80], 70, 290, fill=WH, width=8)
    d.arc([cx - 40, cy - 100, cx + 120, cy + 60], 90, 270, fill=(4, 8, 18), width=30)
    q = clamp(t / (T - 0.3))
    p = 0.8 if q < 0.75 else 0.8 + 0.2 * (q - 0.75) / 0.25
    battery(d, 540, 1040, p, GR if p <= 0.8 else YE, 300, 560)
    clock_t = int(lerp(23, 31, q)) % 24
    label(d, 780, 640, f"{clock_t:02d}:00", 64, CY, F_MONO)
    finish(img, lay)
    pct_labels(img)
    gtitle(t, 0.3, "CARGA OPTIMIZADA", 300, 88, GR, pop=False)
    vignette(img, 150)


def sh_final(img, t, T, L):
    bg(img, t)
    lay, d = layer()
    battery(d, 540, 1000, 0.8 + 0.2 * clamp(t / 3), GR)
    pts = [(540, 1000 - 40)]
    finish(img, lay)
    pct_labels(img)
    gtitle(t, 0.2, "TU MÓVIL SE CUIDA", 300, 92, GR)
    vignette(img, 150)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "creative"), ("ions", "exp"), ("limit", "tension"), ("cv", "creative"), ("night", "space"), ("final", "premium")],
    "gains": {"exp": 0.7},
    "amb": {"hum": ["open", "ions", "limit", "cv", "curve"]},
    "sfx": [("open+0.2", "hum_on", 0.18), ("open+2.5", "blip_down", 0.15), ("open@L1+0.3", "pop", 0.2),
            ("ions+0.3", "draw", 0.15), ("ions@L1", "whoosh_up", 0.12), ("ions@L2+0.2", "riser", 0.1),
            ("limit+0.3", "riser", 0.12), ("limit@L1+0.2", "glitch", 0.15), ("cv+0.2", "draw", 0.18), ("cv@L1+0.2", "blip_down", 0.12),
            ("glass+0.2", "whoosh", 0.12), ("curve+0.2", "draw", 0.15), ("curve@L1+0.2", "zap", 0.1), ("night+0.3", "chime", 0.05),
            ("final+0.2", "ding", 0.08)],
    "bed": [("ions", "curve")],
    "bpm": 104,
}
